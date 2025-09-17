#!/usr/bin/env python3
"""
Enhanced Real-time WebSocket Streaming for Sharekhan API
Automatically subscribes to market feeds and logs real-time data
"""

from SharekhanApi.sharekhanWebsocket import SharekhanWebSocket
import csv
import os
import json
from datetime import datetime
import time

class EnhancedWebSocketStreamer:
    def __init__(self, access_token):
        self.access_token = access_token
        self.sws = SharekhanWebSocket(access_token)
        
        # CSV setup for logging tick data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.csv_filename = os.path.join(os.getcwd(), f"realtime_ticks_{timestamp}.csv")
        self._csv_file = None
        self._csv_writer = None
        
        # Data tracking
        self.data_count = 0
        self.start_time = datetime.now()
        
    def setup_csv_logger(self):
        """Initialize CSV logging"""
        if self._csv_file is None:
            exists = os.path.exists(self.csv_filename)
            self._csv_file = open(self.csv_filename, mode="a", newline="", encoding="utf-8")
            self._csv_writer = csv.writer(self._csv_file)
            if not exists:
                self._csv_writer.writerow([
                    "timestamp", "data_type", "symbol", "ltp", "volume", 
                    "change", "raw_message"
                ])
                
    def parse_market_data(self, message):
        """Parse and extract market data from WebSocket message"""
        try:
            # Default values
            data_info = {
                "data_type": "tick",
                "symbol": "UNKNOWN",
                "ltp": None,
                "volume": None,
                "change": None
            }
            
            # Try to parse if it's JSON
            if isinstance(message, str):
                try:
                    parsed = json.loads(message)
                    if isinstance(parsed, dict):
                        data_info.update({
                            "symbol": parsed.get("symbol", "UNKNOWN"),
                            "ltp": parsed.get("ltp", parsed.get("last_price")),
                            "volume": parsed.get("volume"),
                            "change": parsed.get("change", parsed.get("net_change"))
                        })
                except json.JSONDecodeError:
                    # If not JSON, treat as raw string data
                    if "," in message:
                        # Might be CSV-like data
                        parts = message.split(",")
                        if len(parts) >= 2:
                            data_info["symbol"] = parts[0] if parts[0] else "UNKNOWN"
                            try:
                                data_info["ltp"] = float(parts[1]) if parts[1] else None
                            except (ValueError, IndexError):
                                pass
            
            return data_info
            
        except Exception as e:
            print(f"❌ Error parsing market data: {e}")
            return {
                "data_type": "raw",
                "symbol": "ERROR",
                "ltp": None,
                "volume": None,
                "change": None
            }

    def on_data(self, wsapp, message):
        """Handle incoming real-time data"""
        try:
            self.setup_csv_logger()
            self.data_count += 1
            
            timestamp = datetime.now().isoformat(timespec="seconds")
            
            # Parse the market data
            data_info = self.parse_market_data(message)
            
            # Display real-time info
            if self.data_count % 10 == 1:  # Show every 10th message to avoid spam
                print(f"📈 [{timestamp}] Data #{self.data_count}")
                print(f"   Symbol: {data_info['symbol']}")
                print(f"   LTP: {data_info['ltp']}")
                print(f"   Volume: {data_info['volume']}")
                print(f"   Change: {data_info['change']}")
                print(f"   Raw: {str(message)[:100]}{'...' if len(str(message)) > 100 else ''}")
                print()
            elif self.data_count % 10 == 0:
                # Show count update every 10 messages
                elapsed = (datetime.now() - self.start_time).total_seconds()
                rate = self.data_count / elapsed if elapsed > 0 else 0
                print(f"📊 Received {self.data_count} messages (Rate: {rate:.1f}/sec)")
            
            # Log to CSV
            self._csv_writer.writerow([
                timestamp,
                data_info['data_type'],
                data_info['symbol'],
                data_info['ltp'],
                data_info['volume'],
                data_info['change'],
                str(message)
            ])
            self._csv_file.flush()
            
        except Exception as e:
            print(f"❌ Error processing data: {e}")

    def on_open(self, wsapp):
        """WebSocket connection opened - set up subscriptions"""
        print("🚀 WebSocket connection established!")
        print("📡 Setting up market data subscriptions...")
        
        try:
            # Subscribe to feed
            print("   📋 Subscribing to general feed...")
            subscribe_msg = {
                "action": "subscribe", 
                "key": ["feed"], 
                "value": [""]
            }
            self.sws.subscribe(subscribe_msg)
            time.sleep(1)
            
            # Subscribe to Nifty and popular stocks
            print("   📈 Requesting Nifty and stock data...")
            
            # Common Nifty and stock codes (you may need to adjust these based on actual scrip codes)
            instruments = [
                "NC22",      # Nifty 50
                "NF37833",   # Common futures/options
                "NF37834",   # Common futures/options  
                "MX253461",  # Sample stock
                "RN7719"     # Sample stock
            ]
            
            feed_msg = {
                "action": "feed",
                "key": ["ltp", "volume", "change", "bid", "ask"],
                "value": [",".join(instruments)]
            }
            self.sws.fetchData(feed_msg)
            
            print("✅ Subscription requests sent!")
            print("🎯 Now streaming real-time market data...")
            print("   Press Ctrl+C to stop streaming")
            print()
            
        except Exception as e:
            print(f"❌ Error setting up subscriptions: {e}")

    def on_error(self, wsapp, error):
        """Handle WebSocket errors"""
        print(f"❌ WebSocket Error: {error}")

    def on_close(self, wsapp):
        """Handle WebSocket close"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"\n🔌 WebSocket connection closed")
        print(f"📊 Session Summary:")
        print(f"   Duration: {elapsed:.1f} seconds")
        print(f"   Messages received: {self.data_count}")
        print(f"   Average rate: {self.data_count/elapsed:.1f} messages/sec" if elapsed > 0 else "   Average rate: N/A")
        
        if self._csv_file:
            self._csv_file.close()
            print(f"💾 Data saved to: {self.csv_filename}")

    def start_streaming(self):
        """Start the real-time streaming"""
        print("=== Enhanced Real-Time Market Data Streamer ===")
        print(f"🕐 Started at: {datetime.now()}")
        print(f"🔑 Using access token: {self.access_token[:20]}...")
        print()
        
        # Set up WebSocket callbacks
        self.sws.on_open = self.on_open
        self.sws.on_data = self.on_data
        self.sws.on_error = self.on_error
        self.sws.on_close = self.on_close
        
        try:
            print("🔄 Connecting to WebSocket...")
            self.sws.connect()
        except KeyboardInterrupt:
            print("\n⏹️  Stopping data stream...")
            self.sws.close_connection()
        except Exception as e:
            print(f"❌ Error starting stream: {e}")

def main():
    """Main function"""
    # Use the access token from your config
    access_token = "eyJ0eXAiOiJzZWMiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ4NnpvMmJMdUhJZk5VRmV5MjhpblgvWEdiNG5uNmI3SkhhRnBxQWQzVnI4em9rdFlQaVB4dFI4MllBS3dhK2VYR0V5MHNyWnFZZ21qdTJ0elBGbFFONHlGK0JUZFJmSUtKd3M4VVJobWxKWTFYNENNM1RmWGd2M1NSTnZEam5MWUpMS01rdDc4L3BrdnlLSE56YTZoTmdqekNyK1VQRUhIYStrZmFYZ3I2eXM5Rzgzb0Iwd290cWdlTlIzSFFKSmkiLCJpYXQiOjE3NTgwODc3NTQsImV4cCI6MTc1ODEzMzc5OX0.jI5sZNf4plLZ2BtAPN9alB-DsrshIKz3xs7IOkFEvJw"
    
    print("🔍 Checking access token validity...")
    if not access_token:
        print("❌ No access token found!")
        print("💡 Please update the access_token variable in this script")
        return
    
    # Check if token might be expired (basic check)
    try:
        import jwt
        decoded = jwt.decode(access_token, options={"verify_signature": False})
        exp_time = decoded.get('exp', 0)
        current_time = time.time()
        
        if current_time > exp_time:
            print(f"⚠️  Access token appears to be expired!")
            print(f"   Token expired at: {datetime.fromtimestamp(exp_time)}")
            print(f"   Current time: {datetime.fromtimestamp(current_time)}")
            print("💡 You may need to get a fresh access token")
            
            response = input("Do you want to continue anyway? (y/N): ").strip().lower()
            if response != 'y':
                return
        else:
            print(f"✅ Access token is valid until: {datetime.fromtimestamp(exp_time)}")
            
    except ImportError:
        print("ℹ️  Cannot verify token expiry (PyJWT not installed)")
    except Exception as e:
        print(f"⚠️  Could not verify token: {e}")
    
    print()
    
    # Initialize and start the streamer
    streamer = EnhancedWebSocketStreamer(access_token)
    streamer.start_streaming()

if __name__ == "__main__":
    main()
