#!/usr/bin/env python3
"""
Near Future Data Fetcher - Similar to TradeTiger's Near Future Screen
Shows ~240 companies with near expiry futures contracts

Data includes: Current Price, % Change, Bid Price, Offer Price, Lot Size
Updates in real-time (every few milliseconds via WebSocket)
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from SharekhanApi.sharekhanWebsocket import SharekhanWebSocket
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import os

class NearFutureFetcher:
    def __init__(self, api_key, access_token):
        self.api_key = api_key
        self.access_token = access_token
        self.sk_connect = SharekhanConnect(api_key=api_key, access_token=access_token)
        self.sws = SharekhanWebSocket(access_token)
        
        # Data storage
        self.futures_data = {}
        self.near_expiry_contracts = []
        self.live_data = {}
        
        # Display settings
        self.update_count = 0
        self.last_display_time = time.time()
        
    def get_all_futures_by_category(self, exchange="NF"):
        """
        Get all futures contracts categorized by expiry periods:
        - Current: 30/09/2025 (12 days)
        - Near Future: 28/10/2025 (40 days) 
        - Far Future: 25/11/2025 (68 days)
        """
        try:
            print(f"🔍 Fetching futures contracts from exchange: {exchange}")
            master_data = self.sk_connect.master(exchange)
            
            if not master_data or 'data' not in master_data:
                print("❌ No master data available")
                return {"current": [], "near": [], "far": []}
            
            print(f"📊 Processing {len(master_data['data'])} instruments...")
            
            current_date = datetime.now()
            
            # Define the three expiry categories
            target_expiries = {
                "current": "30/09/2025",    # Current month expiry
                "near": "28/10/2025",      # Near future expiry  
                "far": "25/11/2025"       # Far future expiry
            }
            
            categorized_contracts = {
                "current": [],
                "near": [], 
                "far": []
            }
            
            for instrument in master_data['data']:
                try:
                    symbol = instrument.get('tradingSymbol', '').upper()
                    name = (instrument.get('companyName', '') or '').upper()  # Handle None values
                    instrument_type = instrument.get('instType', '').upper()
                    expiry_date = instrument.get('expiry', '')
                    
                    # Filter for stock futures contracts 
                    if (instrument_type == 'FS' and  # Stock Futures
                        'scripCode' in instrument and
                        expiry_date and str(expiry_date) != '0' and str(expiry_date).lower() != 'none'):
                        
                        # Check which category this contract belongs to
                        for category, target_expiry in target_expiries.items():
                            if expiry_date == target_expiry:
                                # Calculate days to expiry
                                try:
                                    expiry_dt = datetime.strptime(expiry_date, '%d/%m/%Y')
                                    days_diff = (expiry_dt - current_date).days
                                    
                                    categorized_contracts[category].append({
                                        'symbol': symbol,
                                        'name': name,
                                        'scripCode': instrument['scripCode'],
                                        'expiry': expiry_date,
                                        'days_to_expiry': days_diff,
                                        'lotSize': instrument.get('lotSize', 1),
                                        'instrumentType': instrument_type,
                                        'tickSize': instrument.get('tickSize', 0.05),
                                        'category': category
                                    })
                                    break  # Found the category, no need to check others
                                    
                                except Exception as date_error:
                                    continue
                                
                except Exception as e:
                    continue
            
            # Sort each category by symbol name
            for category in categorized_contracts:
                categorized_contracts[category].sort(key=lambda x: x['symbol'])
            
            # Print summary
            total_contracts = sum(len(contracts) for contracts in categorized_contracts.values())
            print(f"✅ Found {total_contracts} futures contracts across all categories")
            
            print("\n📅 Contract Summary by Category:")
            for category, contracts in categorized_contracts.items():
                if contracts:
                    expiry = contracts[0]['expiry']
                    days = contracts[0]['days_to_expiry']
                    category_name = category.upper().replace("_", " ")
                    print(f"   {category_name}: {expiry} ({days} days) - {len(contracts)} contracts")
                else:
                    print(f"   {category.upper()}: No contracts found")
            
            return categorized_contracts
            
        except Exception as e:
            print(f"❌ Error fetching futures contracts: {e}")
            return {"current": [], "near": [], "far": []}
    
    def start_categorized_futures_stream(self):
        """
        Main function to start categorized futures data streaming
        Fetches Current, Near, and Far future contracts
        """
        print("🚀 Starting Categorized Futures Data Fetcher")
        print("📅 Fetching Current, Near, and Far future contracts")
        print("="*70)
        
        # Step 1: Get all categorized futures contracts
        categorized_contracts = self.get_all_futures_by_category()
        
        total_contracts = sum(len(contracts) for contracts in categorized_contracts.values())
        
        if total_contracts == 0:
            print("❌ No futures contracts found!")
            return
        
        print(f"\n🎯 Choose which category to stream:")
        print(f"   1. Current Month: {len(categorized_contracts['current'])} contracts (30/09/2025)")
        print(f"   2. Near Future: {len(categorized_contracts['near'])} contracts (28/10/2025)")
        print(f"   3. Far Future: {len(categorized_contracts['far'])} contracts (25/11/2025)")
        print(f"   4. All Categories: {total_contracts} contracts combined")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            selected_contracts = categorized_contracts['current']
            category_name = "Current Month"
        elif choice == "2":
            selected_contracts = categorized_contracts['near']
            category_name = "Near Future"
        elif choice == "3":
            selected_contracts = categorized_contracts['far']
            category_name = "Far Future"
        elif choice == "4":
            # Combine all categories
            selected_contracts = []
            for contracts in categorized_contracts.values():
                selected_contracts.extend(contracts)
            category_name = "All Categories"
        else:
            print("❌ Invalid choice. Using Current Month by default.")
            selected_contracts = categorized_contracts['current']
            category_name = "Current Month"
        
        print(f"\n📡 Starting real-time streaming for {category_name}: {len(selected_contracts)} contracts")
        
        # Step 2: Start real-time streaming
        self.get_realtime_prices(selected_contracts)
    
    def get_realtime_prices(self, contracts, max_contracts=240):
        """
        Subscribe to real-time prices for near expiry futures contracts
        """
        if not contracts:
            print("❌ No contracts to subscribe to")
            return
        
        # Limit to ~240 contracts as mentioned
        selected_contracts = contracts[:max_contracts]
        self.near_expiry_contracts = selected_contracts
        
        print(f"📡 Subscribing to real-time data for {len(selected_contracts)} contracts...")
        
        # Prepare scrip codes for WebSocket subscription
        scrip_codes = [str(contract['scripCode']) for contract in selected_contracts]
        
        # Set up WebSocket callbacks
        self.sws.on_open = self.on_websocket_open
        self.sws.on_data = self.on_websocket_data
        self.sws.on_error = self.on_websocket_error
        self.sws.on_close = self.on_websocket_close
        
        # Store scrip codes for subscription
        self.scrip_codes_to_subscribe = scrip_codes
        
        # Start WebSocket connection
        print("🔄 Starting WebSocket connection...")
        try:
            self.sws.connect()
        except KeyboardInterrupt:
            print("\n⏹️  Stopping Near Future data stream...")
            self.sws.close_connection()
    
    def on_websocket_open(self, wsapp):
        """WebSocket connection opened - subscribe to futures data"""
        print("🚀 WebSocket connected! Subscribing to near expiry futures...")
        
        try:
            # Subscribe to feed
            subscribe_msg = {
                "action": "subscribe",
                "key": ["feed"],
                "value": [""]
            }
            self.sws.subscribe(subscribe_msg)
            time.sleep(1)
            
            # Request real-time data for futures contracts
            feed_msg = {
                "action": "feed",
                "key": ["ltp", "bid", "ask", "volume", "change", "change_percent"],
                "value": [",".join(self.scrip_codes_to_subscribe)]
            }
            self.sws.fetchData(feed_msg)
            
            print("✅ Subscription successful! Streaming near future data...")
            print("📊 Press Ctrl+C to stop")
            print("\n" + "="*100)
            self.display_header()
            
        except Exception as e:
            print(f"❌ Error setting up subscriptions: {e}")
    
    def on_websocket_data(self, wsapp, data):
        """Process incoming real-time futures data"""
        try:
            self.update_count += 1
            
            # Parse the incoming data (format depends on Sharekhan's WebSocket response)
            self.process_futures_data(data)
            
            # Display data every few updates (to avoid spam)
            current_time = time.time()
            if current_time - self.last_display_time >= 2:  # Update display every 2 seconds
                self.display_near_future_data()
                self.last_display_time = current_time
                
        except Exception as e:
            print(f"❌ Error processing real-time data: {e}")
    
    def process_futures_data(self, data):
        """Parse and store the real-time futures data"""
        try:
            # This depends on the exact format of Sharekhan's WebSocket data
            # You may need to adjust this based on actual response format
            
            if isinstance(data, dict):
                scrip_code = data.get('scripCode') or data.get('token')
                if scrip_code:
                    self.live_data[str(scrip_code)] = {
                        'ltp': data.get('ltp', 0),
                        'bid': data.get('bid', 0),
                        'ask': data.get('ask', 0),
                        'volume': data.get('volume', 0),
                        'change': data.get('change', 0),
                        'change_percent': data.get('change_percent', 0),
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    }
            
            elif isinstance(data, str):
                # If data is CSV-like string, try to parse it
                if ',' in data:
                    parts = data.split(',')
                    if len(parts) >= 3:
                        try:
                            scrip_code = parts[0]
                            ltp = float(parts[1]) if parts[1] else 0
                            volume = int(parts[2]) if parts[2] else 0
                            
                            self.live_data[scrip_code] = {
                                'ltp': ltp,
                                'bid': ltp - 0.05,  # Approximate bid
                                'ask': ltp + 0.05,  # Approximate ask
                                'volume': volume,
                                'change': 0,
                                'change_percent': 0,
                                'timestamp': datetime.now().strftime('%H:%M:%S')
                            }
                        except (ValueError, IndexError):
                            pass
                            
        except Exception as e:
            print(f"❌ Error parsing futures data: {e}")
    
    def display_header(self):
        """Display the header for Near Future data"""
        print(f"🔥 NEAR FUTURE - {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"📊 Showing {len(self.near_expiry_contracts)} contracts near expiry")
        print("-" * 100)
        print(f"{'Symbol':<15} {'Price':<10} {'Change%':<10} {'Bid':<10} {'Ask':<10} {'Lot':<8} {'Expiry':<12} {'Days':<5}")
        print("-" * 100)
    
    def display_near_future_data(self):
        """Display the Near Future data in table format"""
        # Clear screen for better display (Windows)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        self.display_header()
        
        displayed_count = 0
        for contract in self.near_expiry_contracts:
            scrip_code = str(contract['scripCode'])
            live = self.live_data.get(scrip_code, {})
            
            symbol = contract['symbol'][:15]  # Truncate long symbols
            price = live.get('ltp', 0)
            change_pct = live.get('change_percent', 0)
            bid = live.get('bid', 0)
            ask = live.get('ask', 0)
            lot_size = contract['lotSize']
            expiry = contract['expiry']
            days = contract['days_to_expiry']
            
            # Color coding for change percentage
            if change_pct > 0:
                change_color = f"+{change_pct:.2f}%" 
            elif change_pct < 0:
                change_color = f"{change_pct:.2f}%"
            else:
                change_color = "0.00%"
            
            print(f"{symbol:<15} {price:<10.2f} {change_color:<10} {bid:<10.2f} {ask:<10.2f} {lot_size:<8} {expiry:<12} {days:<5}")
            
            displayed_count += 1
            if displayed_count >= 240:  # Limit display to ~240 as requested
                break
        
        print("-" * 100)
        print(f"💫 Updates: {self.update_count} | Last Update: {datetime.now().strftime('%H:%M:%S')}")
        print("⏹️  Press Ctrl+C to stop streaming")
    
    def on_websocket_error(self, wsapp, error):
        """Handle WebSocket errors"""
        print(f"❌ WebSocket Error: {error}")
    
    def on_websocket_close(self, wsapp):
        """Handle WebSocket close"""
        print(f"\n🔌 WebSocket connection closed")
        print(f"📊 Total updates received: {self.update_count}")
    
    def start_near_future_stream(self, days_to_expiry=30):
        """
        Main function to start Near Future data streaming
        
        Args:
            days_to_expiry: Number of days to expiry to consider as "near future"
        """
        print("🚀 Starting Near Future Data Fetcher")
        print(f"📅 Looking for contracts expiring within {days_to_expiry} days")
        print("="*60)
        
        # Step 1: Get near expiry futures contracts
        contracts = self.get_near_expiry_futures(days_to_expiry=days_to_expiry)
        
        if not contracts:
            print("❌ No near expiry contracts found!")
            return
        
        # Step 2: Start real-time streaming
        self.get_realtime_prices(contracts)

def main():
    """Main function"""
    print("🔍 Near Future Data Fetcher - TradeTiger Style")
    print("=" * 60)
    
    # Try to load from config first
    try:
        from config import API_KEY, SECRET_KEY
        api_key = API_KEY
        print(f"✅ Loaded API key from config.py")
    except ImportError:
        print("⚠️  config.py not found")
        api_key = input("Enter your Sharekhan API Key: ").strip()
    
    # Get access token from user (after running automated_auth.py)
    print("\n💡 Run 'python SharekhanApi\\automated_auth.py' first to get your access token")
    access_token = input("Enter your Sharekhan Access Token: ").strip()
    
    # Validate credentials
    if not api_key or not access_token:
        print("❌ Both API Key and Access Token are required!")
        return
    
    if access_token in ["YOUR_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE"]:
        print("❌ Please provide a valid access token!")
        print("💡 Run automated_auth.py first to get a real access token")
        return
    
    print(f"🔑 Using API Key: {api_key[:20]}...")
    print(f"🎫 Using Access Token: {access_token[:30]}...")
    
    # Initialize and start
    near_future = NearFutureFetcher(api_key, access_token)
    
    # Start categorized futures streaming (Current, Near, Far future)
    near_future.start_categorized_futures_stream()

if __name__ == "__main__":
    main()
