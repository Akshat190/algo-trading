#!/usr/bin/env python3
"""
Script to fetch the actual NIFTY 50 INDEX data using ShareKhan API
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
import json
from datetime import datetime

# Your authentication details
api_key = "6N2P70M5viQq2GfGGgfGonnCgaB1CdTz"
access_token = "eyJ0eXAiOiJzZWMiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ4NnpvMmJMdUhJZk5VRmV5MjhpblgvWEdiNG5uNmI3SkhhRnBxQWQzVnI4em9rdFlQaVB4dFI4MllBS3dhK2VYR0V5MHNyWnFZZ21qdTJ0elBGbFFONHlGK0JUZFJmSUtKd3M4VVJobWxKWTFYNENNM1RmWGd2M1NSTnZEam5MWUpMS01rdDc4L3BrdnlLSE56YTZoTmdqekNyK1VQRUhIYStrZmFYZ3I2eXM5Rzgzb0Iwd290cWdlTlIzSFFKSmkiLCJpYXQiOjE3NTgwODc3NTQsImV4cCI6MTc1ODEzMzc5OX0.jI5sZNf4plLZ2BtAPN9alB-DsrshIKz3xs7IOkFEvJw"

# Initialize ShareKhan client
sk = SharekhanConnect(api_key=api_key, access_token=access_token)

print("=== NIFTY 50 INDEX Data Fetcher ===")
print(f"Time: {datetime.now()}")
print()

# NIFTY 50 INDEX Information from our search
nifty_instruments = [
    {"exchange": "NC", "scripcode": 20000, "symbol": "NIFTY", "name": "NIFTY 50 INDEX"},
    {"exchange": "NC", "scripcode": 20004, "symbol": "NiftyNxt50", "name": "Nifty Next 50"},
    {"exchange": "NC", "scripcode": 26000, "symbol": "NIFTY", "name": "NIFTY 50"},
    {"exchange": "NC", "scripcode": 26009, "symbol": "NiftyBank", "name": "Nifty Bank"},
    {"exchange": "NC", "scripcode": 26008, "symbol": "NiftyIT", "name": "Nifty IT"},
    {"exchange": "NC", "scripcode": 26012, "symbol": "Nifty100", "name": "Nifty 100"},
]

def get_historical_data(exchange, scripcode, symbol, intervals):
    """Get historical data for different intervals"""
    print(f"\n🔍 Fetching data for {symbol} (ScripCode: {scripcode})")
    
    successful_data = []
    
    for interval in intervals:
        try:
            print(f"   📈 Trying {interval} interval...")
            data = sk.historicaldata(exchange, scripcode, interval)
            
            if data and isinstance(data, dict):
                if data.get('status') == 200 and 'data' in data:
                    print(f"   ✅ SUCCESS with {interval}!")
                    
                    # Save the data
                    filename = f"nifty_{symbol}_{interval}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    # Show sample data
                    historical_data = data['data']
                    if isinstance(historical_data, list) and len(historical_data) > 0:
                        print(f"   📊 Records: {len(historical_data)}")
                        print(f"   📅 Latest: {historical_data[-1]}")
                        print(f"   📅 Oldest: {historical_data[0]}")
                        
                        successful_data.append({
                            'interval': interval,
                            'filename': filename,
                            'records': len(historical_data),
                            'latest_price': historical_data[-1].get('close'),
                            'latest_date': historical_data[-1].get('tradeDate')
                        })
                    else:
                        print(f"   📊 Data format: {type(historical_data)}")
                        
                    print(f"   💾 Saved to: {filename}")
                    
                else:
                    status = data.get('status', 'Unknown')
                    message = data.get('message', 'No message')
                    print(f"   ❌ Failed: Status {status}, {message}")
                    
            else:
                print(f"   ❌ No data returned")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return successful_data

# Intervals to try
intervals_to_try = ['daily', 'weekly', 'monthly', '1D', '1W', '1M', 'hourly', '60min', '30min', '15min', '5min', '1min']

print("🚀 Starting NIFTY data fetch...")

all_results = {}

for instrument in nifty_instruments:
    exchange = instrument['exchange']
    scripcode = instrument['scripcode']
    symbol = instrument['symbol']
    name = instrument['name']
    
    print(f"\n{'='*60}")
    print(f"📋 {name}")
    print(f"🔗 Exchange: {exchange}, ScripCode: {scripcode}, Symbol: {symbol}")
    
    results = get_historical_data(exchange, scripcode, symbol, intervals_to_try)
    all_results[symbol] = results
    
    # Stop if we get good data for the main NIFTY
    if symbol == "NIFTY" and len(results) > 0:
        print(f"\n🎯 Found working data for main NIFTY index!")
        break

print(f"\n{'='*60}")
print(f"🎉 SUMMARY")
print(f"{'='*60}")

for symbol, results in all_results.items():
    if results:
        print(f"\n📊 {symbol}:")
        for result in results:
            print(f"   ✅ {result['interval']}: {result['records']} records, Latest: ₹{result['latest_price']} on {result['latest_date']}")
            print(f"      📁 File: {result['filename']}")
    else:
        print(f"\n❌ {symbol}: No successful data retrieved")

print(f"\n🎯 You now have NIFTY data!")
print(f"💡 Use the JSON files to analyze NSE NIFTY trends, create charts, etc.")
print(f"📈 The 'close' prices give you the NIFTY index values for each trading day.")
