#!/usr/bin/env python3
"""
Real-time Options Chain (OI Chain) Data Fetcher
Streams live options data including Open Interest, LTP, Volume, etc.
"""

from SharekhanApi.sharekhanWebsocket import SharekhanWebSocket
from SharekhanApi.sharekhanConnect import SharekhanConnect
import json
import csv
import os
from datetime import datetime
import time

class RealTimeOIChain:
    def __init__(self, access_token, api_key=None):
        self.access_token = access_token
        self.api_key = api_key
        self.sws = SharekhanWebSocket(access_token)
        if api_key:
            self.sk_connect = SharekhanConnect(api_key=api_key, access_token=access_token)
        
        # CSV setup for logging OI data
        self.csv_filename = os.path.join(os.getcwd(), f"oi_chain_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
        self._csv_file = None
        self._csv_writer = None
        
        # Options data storage
        self.options_data = {}
        self.strike_prices = []
        
    def setup_csv_logger(self):
        """Initialize CSV logging for OI chain data"""
        if self._csv_file is None:
            exists = os.path.exists(self.csv_filename)
            self._csv_file = open(self.csv_filename, mode="a", newline="", encoding="utf-8")
            self._csv_writer = csv.writer(self._csv_file)
            if not exists:
                # CSV headers for options chain data
                self._csv_writer.writerow([
                    "timestamp", "symbol", "strike_price", "option_type", 
                    "ltp", "bid", "ask", "volume", "open_interest", 
                    "change", "change_percent"
                ])
    
    def get_nifty_options_contracts(self, exchange="NF"):
        """Fetch available Nifty options contracts"""
        try:
            if not hasattr(self, 'sk_connect'):
                print("⚠️  REST API client not initialized. Need API key for contract fetching.")
                return []
                
            print(f"🔍 Fetching options contracts for exchange: {exchange}")
            master_data = self.sk_connect.master(exchange)
            
            if not master_data or 'data' not in master_data:
                print("❌ No master data available")
                return []
            
            contracts = []
            for instrument in master_data['data']:
                symbol = instrument.get('tradingSymbol', '').upper()
                name = instrument.get('name', '').upper()
                instrument_type = instrument.get('instrumentType', '').upper()
                
                # Filter for Nifty options
                if ('NIFTY' in symbol and 
                    instrument_type in ['CE', 'PE', 'OPTIDX'] and
                    'scripCode' in instrument):
                    contracts.append({
                        'symbol': symbol,
                        'scripCode': instrument['scripCode'],
                        'strike': instrument.get('strikePrice', 0),
                        'expiry': instrument.get('expiryDate', ''),
                        'optionType': instrument_type,
                        'name': name
                    })
            
            print(f"✅ Found {len(contracts)} Nifty options contracts")
            return contracts
            
        except Exception as e:
            print(f"❌ Error fetching options contracts: {e}")
            return []
    
    def subscribe_to_options_feed(self, contracts, max_contracts=50):
        """Subscribe to real-time feed for options contracts"""
        if not contracts:
            print("❌ No contracts to subscribe to")
            return
            
        # Limit the number of contracts to avoid overwhelming the feed
        selected_contracts = contracts[:max_contracts]
        contract_codes = [str(contract['scripCode']) for contract in selected_contracts]
        
        print(f"📡 Subscribing to {len(contract_codes)} options contracts...")
        
        # Subscribe to feed
        subscribe_msg = {
            "action": "subscribe",
            "key": ["feed"],
            "value": [""]
        }
        
        # Fetch real-time data for options
        feed_msg = {
            "action": "feed",
            "key": ["ltp", "volume", "oi", "bid", "ask", "change"],
            "value": [",".join(contract_codes)]
        }
        
        self.sws.subscribe(subscribe_msg)
        time.sleep(1)  # Brief pause between subscribe and feed
        self.sws.fetchData(feed_msg)
        
        print("✅ Subscription requests sent!")
    
    def on_open(self, wsapp):
        """WebSocket connection opened"""
        print("🚀 WebSocket connection established!")
        
        # Get available options contracts
        contracts = self.get_nifty_options_contracts()
        
        if contracts:
            # Filter for near-the-money options for current month
            current_month_contracts = self.filter_current_month_contracts(contracts)
            self.subscribe_to_options_feed(current_month_contracts)
        else:
            print("⚠️  No options contracts found. Subscribing to basic feed...")
            # Fallback: subscribe to basic Nifty feed
            basic_feed = {
                "action": "feed",
                "key": ["ltp"],
                "value": ["NC22"]  # Nifty 50 index
            }
            self.sws.fetchData(basic_feed)
    
    def filter_current_month_contracts(self, contracts):
        """Filter contracts for current month expiry and ATM strikes"""
        if not contracts:
            return []
        
        # Sort by expiry date to get nearest expiry
        contracts.sort(key=lambda x: x['expiry'])
        
        # Get contracts for the nearest expiry
        nearest_expiry = contracts[0]['expiry']
        current_month_contracts = [c for c in contracts if c['expiry'] == nearest_expiry]
        
        # Get unique strikes and sort them
        strikes = sorted(set(c['strike'] for c in current_month_contracts if c['strike'] > 0))
        
        if not strikes:
            return current_month_contracts[:20]  # Return first 20 if no strikes found
        
        # Find ATM and nearby strikes (assume Nifty around middle of strike range)
        mid_index = len(strikes) // 2
        start_idx = max(0, mid_index - 10)
        end_idx = min(len(strikes), mid_index + 10)
        selected_strikes = strikes[start_idx:end_idx]
        
        # Filter contracts for selected strikes
        filtered_contracts = [
            c for c in current_month_contracts 
            if c['strike'] in selected_strikes
        ]
        
        print(f"📊 Filtered to {len(filtered_contracts)} contracts around ATM strikes: {selected_strikes[:5]}...{selected_strikes[-5:]}")
        return filtered_contracts
    
    def on_data(self, wsapp, data):
        """Handle incoming real-time data"""
        try:
            self.setup_csv_logger()
            
            timestamp = datetime.now().isoformat(timespec="seconds")
            print(f"📈 [{timestamp}] Options Data: {data}")
            
            # Log to CSV (simplified format)
            self._csv_writer.writerow([timestamp, "OPTIONS_DATA", str(data)])
            self._csv_file.flush()
            
            # Parse and process the options data here
            self.process_options_data(data, timestamp)
            
        except Exception as e:
            print(f"❌ Error processing data: {e}")
    
    def process_options_data(self, data, timestamp):
        """Process and analyze the incoming options data"""
        try:
            # This is where you'd parse the specific options data format
            # The exact format depends on Sharekhan's WebSocket response structure
            
            if isinstance(data, dict):
                # Extract relevant options information
                symbol = data.get('symbol', 'UNKNOWN')
                ltp = data.get('ltp', 0)
                volume = data.get('volume', 0)
                oi = data.get('oi', 0)
                
                print(f"  💰 {symbol}: LTP={ltp}, Vol={volume}, OI={oi}")
                
            elif isinstance(data, str):
                # If data is a string, try to parse it
                print(f"  📝 Raw data: {data}")
                
        except Exception as e:
            print(f"❌ Error processing options data: {e}")
    
    def on_error(self, wsapp, error):
        """Handle WebSocket errors"""
        print(f"❌ WebSocket Error: {error}")
    
    def on_close(self, wsapp):
        """Handle WebSocket close"""
        print("🔌 WebSocket connection closed")
        if self._csv_file:
            self._csv_file.close()
            print(f"💾 Data saved to: {self.csv_filename}")
    
    def start_streaming(self):
        """Start the real-time options chain data streaming"""
        print("=== Real-Time Options Chain (OI Chain) Data Streamer ===")
        print(f"🕐 Started at: {datetime.now()}")
        print()
        
        # Set up WebSocket callbacks
        self.sws.on_open = self.on_open
        self.sws.on_data = self.on_data
        self.sws.on_error = self.on_error
        self.sws.on_close = self.on_close
        
        try:
            print("🔄 Starting WebSocket connection...")
            self.sws.connect()
        except KeyboardInterrupt:
            print("\n⏹️  Stopping data stream...")
            self.sws.close_connection()
        except Exception as e:
            print(f"❌ Error starting stream: {e}")

def main():
    """Main function to start OI chain streaming"""
    # Get credentials from config or user input
    try:
        from config import API_KEY
        api_key = API_KEY
    except ImportError:
        api_key = input("Enter your Sharekhan API Key: ").strip()
    
    access_token = input("Enter your Sharekhan Access Token: ").strip()
    
    if not access_token:
        print("❌ Access token is required!")
        return
    
    # Initialize and start the OI chain streamer
    oi_streamer = RealTimeOIChain(access_token, api_key)
    oi_streamer.start_streaming()

if __name__ == "__main__":
    main()
