#!/usr/bin/env python3
"""
Script to fetch NSE Nifty data using ShareKhan API
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
import json
from datetime import datetime

# Your authentication details (from the successful login)
api_key = "6N2P70M5viQq2GfGGgfGonnCgaB1CdTz"
access_token = "eyJ0eXAiOiJzZWMiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ4NnpvMmJMdUhJZk5VRmV5MjhpblgvWEdiNG5uNmI3SkhhRnBxQWQzVnI4em9rdFlQaVB4dFI4MllBS3dhK2VYR0V5MHNyWnFZZ21qdTJ0elBGbFFONHlGK0JUZFJmSUtKd3M4VVJobWxKWTFYNENNM1RmWGd2M1NSTnZEam5MWUpMS01rdDc4L3BrdnlLSE56YTZoTmdqekNyK1VQRUhIYStrZmFYZ3I2eXM5Rzgzb0Iwd290cWdlTlIzSFFKSmkiLCJpYXQiOjE3NTgwODc3NTQsImV4cCI6MTc1ODEzMzc5OX0.jI5sZNf4plLZ2BtAPN9alB-DsrshIKz3xs7IOkFEvJw"

# Initialize ShareKhan client
sk = SharekhanConnect(api_key=api_key, access_token=access_token)

print("=== ShareKhan NSE Nifty Data Fetcher ===")
print(f"Authenticated as: KANDARP GIRISHCHANDRA BAROT")
print(f"Time: {datetime.now()}")
print()

def fetch_master_data(exchange):
    """Fetch master data for an exchange"""
    try:
        print(f"🔍 Fetching master data for exchange: {exchange}")
        data = sk.master(exchange)
        print(f"✅ Master data fetched successfully!")
        
        if isinstance(data, dict):
            print(f"📊 Data keys: {list(data.keys())}")
        else:
            print(f"📊 Data type: {type(data)}")
            print(f"📊 Data length: {len(data) if hasattr(data, '__len__') else 'N/A'}")
        
        return data
    except Exception as e:
        print(f"❌ Error fetching master data: {e}")
        return None

def fetch_historical_data(exchange, scripcode, interval):
    """Fetch historical data for a specific scrip"""
    try:
        print(f"🔍 Fetching historical data:")
        print(f"   Exchange: {exchange}")
        print(f"   Scrip Code: {scripcode}")
        print(f"   Interval: {interval}")
        
        data = sk.historicaldata(exchange, scripcode, interval)
        print(f"✅ Historical data fetched successfully!")
        
        if isinstance(data, dict):
            print(f"📊 Data keys: {list(data.keys())}")
        else:
            print(f"📊 Data type: {type(data)}")
            print(f"📊 Data length: {len(data) if hasattr(data, '__len__') else 'N/A'}")
        
        return data
    except Exception as e:
        print(f"❌ Error fetching historical data: {e}")
        return None

def save_data_to_file(data, filename):
    """Save data to a JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, dict):
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump({"data": str(data)}, f, indent=2, ensure_ascii=False)
        print(f"💾 Data saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

# Test connection
print("🧪 Testing API connection...")
try:
    headers = sk.requestHeaders()
    print("✅ API connection successful!")
    print(f"🔑 Headers: {headers}")
    print()
except Exception as e:
    print(f"❌ API connection failed: {e}")
    exit(1)

# Try different exchanges to find NSE data
exchanges_to_try = ["NF", "NC", "BF", "BC", "MX"]

print("🔍 Exploring available exchanges...")
for exchange in exchanges_to_try:
    print(f"\n📋 Trying exchange: {exchange}")
    master_data = fetch_master_data(exchange)
    
    if master_data:
        # Save the master data
        save_data_to_file(master_data, f"master_data_{exchange}.json")
        
        # If we got data, try to find Nifty-related instruments
        if isinstance(master_data, dict) and 'data' in master_data:
            instruments = master_data.get('data', [])
            print(f"📊 Found {len(instruments)} instruments in {exchange}")
            
            # Look for Nifty instruments
            nifty_instruments = []
            if isinstance(instruments, list):
                for instrument in instruments[:10]:  # Show first 10 for brevity
                    if isinstance(instrument, dict):
                        symbol = instrument.get('tradingSymbol', '').upper()
                        name = instrument.get('name', '').upper()
                        if 'NIFTY' in symbol or 'NIFTY' in name:
                            nifty_instruments.append(instrument)
                            print(f"🎯 Found Nifty instrument: {instrument}")
            
            if nifty_instruments:
                print(f"🎯 Found {len(nifty_instruments)} Nifty-related instruments!")
                
                # Try to fetch historical data for the first Nifty instrument
                first_nifty = nifty_instruments[0]
                scripcode = first_nifty.get('scripCode')
                if scripcode:
                    print(f"\n📈 Fetching historical data for Nifty (ScripCode: {scripcode})")
                    for interval in ['daily', '1min', '5min', '15min', '30min', '60min']:
                        historical_data = fetch_historical_data(exchange, scripcode, interval)
                        if historical_data:
                            save_data_to_file(historical_data, f"nifty_historical_{interval}.json")
                            break  # Success! Stop trying other intervals
        
        break  # Success! Stop trying other exchanges

print(f"\n🎉 Data fetching complete!")
print(f"📁 Check the generated JSON files for the data.")
print(f"💡 You can now analyze the Nifty data from the saved files.")
