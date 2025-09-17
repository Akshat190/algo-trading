#!/usr/bin/env python3
"""
Script to find and fetch actual Nifty 50 index data using ShareKhan API
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
import json
from datetime import datetime

# Your authentication details
api_key = "6N2P70M5viQq2GfGGgfGonnCgaB1CdTz"
access_token = "eyJ0eXAiOiJzZWMiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJ4NnpvMmJMdUhJZk5VRmV5MjhpblgvWEdiNG5uNmI3SkhhRnBxQWQzVnI4em9rdFlQaVB4dFI4MllBS3dhK2VYR0V5MHNyWnFZZ21qdTJ0elBGbFFONHlGK0JUZFJmSUtKd3M4VVJobWxKWTFYNENNM1RmWGd2M1NSTnZEam5MWUpMS01rdDc4L3BrdnlLSE56YTZoTmdqekNyK1VQRUhIYStrZmFYZ3I2eXM5Rzgzb0Iwd290cWdlTlIzSFFKSmkiLCJpYXQiOjE3NTgwODc3NTQsImV4cCI6MTc1ODEzMzc5OX0.jI5sZNf4plLZ2BtAPN9alB-DsrshIKz3xs7IOkFEvJw"

# Initialize ShareKhan client
sk = SharekhanConnect(api_key=api_key, access_token=access_token)

print("=== Finding Nifty 50 Index Data ===")
print(f"Time: {datetime.now()}")
print()

def search_instruments_in_exchange(exchange, search_terms):
    """Search for specific instruments in an exchange"""
    try:
        print(f"🔍 Searching in exchange: {exchange}")
        data = sk.master(exchange)
        
        if not data or 'data' not in data:
            print(f"❌ No data found for exchange: {exchange}")
            return []
        
        instruments = data.get('data', [])
        print(f"📊 Total instruments in {exchange}: {len(instruments)}")
        
        matching_instruments = []
        
        for instrument in instruments:
            if isinstance(instrument, dict):
                symbol = str(instrument.get('tradingSymbol', '')).upper()
                name = str(instrument.get('companyName', '')).upper()
                
                # Look for exact matches to Nifty 50 index
                for term in search_terms:
                    if term in symbol or term in name:
                        # Avoid options and futures - look for the actual index
                        inst_type = instrument.get('instType', '').upper()
                        if inst_type in ['EQ', 'INDEX', 'IN', ''] or inst_type is None:
                            if 'CE' not in symbol and 'PE' not in symbol:  # Avoid options
                                matching_instruments.append(instrument)
                                print(f"🎯 Found: {instrument}")
                                break
        
        print(f"✅ Found {len(matching_instruments)} matching instruments in {exchange}")
        return matching_instruments
        
    except Exception as e:
        print(f"❌ Error searching in {exchange}: {e}")
        return []

def test_historical_data(exchange, scripcode, symbol):
    """Test different intervals for historical data"""
    print(f"\n📈 Testing historical data for {symbol} (ScripCode: {scripcode})")
    
    # Try different intervals
    intervals = ['daily', 'weekly', 'monthly', '1D', '1W', '1M']
    
    for interval in intervals:
        try:
            print(f"   Trying interval: {interval}")
            data = sk.historicaldata(exchange, scripcode, interval)
            
            if data and 'status' in data:
                if data['status'] == 200:
                    print(f"   ✅ Success with {interval}! Data keys: {list(data.keys())}")
                    
                    # Save successful data
                    filename = f"nifty_{symbol}_{interval}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f"   💾 Data saved to: {filename}")
                    
                    # Show sample of the data
                    if 'data' in data and len(data['data']) > 0:
                        sample = data['data'][:3] if isinstance(data['data'], list) else data['data']
                        print(f"   📊 Sample data: {sample}")
                    
                    return True
                else:
                    print(f"   ❌ Failed with {interval}: {data.get('message', 'Unknown error')}")
            else:
                print(f"   ❌ No data returned for {interval}")
                
        except Exception as e:
            print(f"   ❌ Error with {interval}: {e}")
    
    print(f"   ⚠️ No successful intervals found for {symbol}")
    return False

# Search terms for Nifty index
nifty_search_terms = ['NIFTY 50', 'NIFTY', 'CNXNIFTY', 'NSE NIFTY']

# Exchanges to try
exchanges_to_try = ['NC', 'BC', 'MX', 'NF', 'BF']  # Different order, focusing on cash segments first

all_found_instruments = []

for exchange in exchanges_to_try:
    print(f"\n{'='*50}")
    matching_instruments = search_instruments_in_exchange(exchange, nifty_search_terms)
    
    if matching_instruments:
        all_found_instruments.extend(matching_instruments)
        
        # Test historical data for the first few instruments
        for i, instrument in enumerate(matching_instruments[:3]):  # Test first 3
            scripcode = instrument.get('scripCode')
            symbol = instrument.get('tradingSymbol', f'instrument_{i}')
            
            if scripcode:
                success = test_historical_data(exchange, scripcode, symbol)
                if success:
                    break  # Stop if we found working historical data

print(f"\n{'='*60}")
print(f"🎉 Search Complete!")
print(f"📊 Total Nifty instruments found: {len(all_found_instruments)}")

if all_found_instruments:
    print(f"\n📋 Summary of found instruments:")
    for i, instrument in enumerate(all_found_instruments[:10], 1):  # Show first 10
        print(f"   {i}. {instrument.get('tradingSymbol', 'N/A')} "
              f"(ScripCode: {instrument.get('scripCode', 'N/A')}, "
              f"Exchange: {instrument.get('exchange', 'N/A')}, "
              f"Type: {instrument.get('instType', 'N/A')})")

print(f"\n💡 Check the generated JSON files for historical data.")
print(f"📁 Files created in current directory.")
