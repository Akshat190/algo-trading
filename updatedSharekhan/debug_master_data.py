#!/usr/bin/env python3
"""
Debug script to inspect Sharekhan master data and understand the format
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
import json

def debug_master_data():
    """Debug the master data to understand the structure"""
    
    # Get credentials
    try:
        from config import API_KEY
        api_key = API_KEY
        print(f"✅ Loaded API key from config.py")
    except ImportError:
        api_key = input("Enter your Sharekhan API Key: ").strip()
    
    access_token = input("Enter your Sharekhan Access Token: ").strip()
    
    if not api_key or not access_token:
        print("❌ Both API Key and Access Token are required!")
        return
    
    # Initialize connection
    sk_connect = SharekhanConnect(api_key=api_key, access_token=access_token)
    
    # Try different exchanges to find stock futures
    exchanges_to_try = ["NF", "NC", "MX", "BC"]
    
    for exchange in exchanges_to_try:
        print(f"\n🔍 Fetching master data from {exchange} exchange...")
        try:
            master_data = sk_connect.master(exchange)
            
            if not master_data:
                print(f"❌ No master data received from {exchange}!")
                continue
                
            print(f"📊 Master data structure: {type(master_data)}")
            
            if isinstance(master_data, dict):
                print(f"🔑 Keys in master data: {list(master_data.keys())}")
                
                if 'data' in master_data:
                    instruments = master_data['data']
                    print(f"📈 Found {len(instruments)} instruments in {exchange}")
                    
                    # Look for futures contracts - use correct field names
                    futures_found = 0
                    sample_futures = []
                    
                    for i, instrument in enumerate(instruments[:10]):  # Check first 10
                        # Use correct field names based on the API response
                        instrument_type = instrument.get('instType', '').upper()
                        expiry_date = instrument.get('expiry', '')
                        symbol = instrument.get('tradingSymbol', '')
                        
                        print(f"\n🔍 Sample {exchange} instrument {i+1}:")
                        print(f"   Symbol: {symbol}")
                        print(f"   instType: {instrument_type}")
                        print(f"   expiry: {expiry_date}")
                        print(f"   Keys: {list(instrument.keys())}")
                        
                        # Look for futures - check various possible type values
                        if any(fut_type in instrument_type for fut_type in ['FUT', 'FUTURE']):
                            futures_found += 1
                            sample_futures.append(instrument)
                            print(f"   *** FOUND FUTURE CONTRACT! ***")
                            
                        if len(sample_futures) >= 3:  # Get 3 samples per exchange
                            break
                    
                    print(f"\n✅ Found {futures_found} futures in {exchange} exchange")
                    
                    if sample_futures:
                        print(f"\n🎯 Sample futures contracts from {exchange}:")
                        for i, future in enumerate(sample_futures):
                            print(f"\n   Future {i+1}:")
                            print(f"     Symbol: {future.get('tradingSymbol', 'N/A')}")
                            print(f"     instType: {future.get('instType', 'N/A')}")
                            print(f"     expiry: {future.get('expiry', 'N/A')}")
                            print(f"     ScripCode: {future.get('scripCode', 'N/A')}")
                            print(f"     LotSize: {future.get('lotSize', 'N/A')}")
                            
                            # Show all fields
                            print(f"     All fields: {json.dumps(future, indent=8, default=str)}")
                    
                    # Look specifically for Sept 30 expiry using correct field name
                    print(f"\n🎯 Looking for September 30, 2025 expiry contracts in {exchange}...")
                    sept_contracts = []
                    
                    for instrument in instruments:
                        expiry_date = str(instrument.get('expiry', '')).lower()  # Use 'expiry' not 'expiryDate'
                        if any(date_part in expiry_date for date_part in ['30', '09', '2025', 'sep', 'september']):
                            sept_contracts.append(instrument)
                            if len(sept_contracts) <= 5:  # Show first 5
                                print(f"   Found: {instrument.get('tradingSymbol', 'N/A')} - Expiry: {expiry_date} - Type: {instrument.get('instType', 'N/A')}")
                    
                    print(f"\n📅 Total contracts with Sept 30 indicators in {exchange}: {len(sept_contracts)}")
                    
                else:
                    print(f"❌ No 'data' key found in master_data for {exchange}")
                    print(f"Raw response: {json.dumps(master_data, indent=2, default=str)[:500]}...")
            else:
                print(f"❌ Unexpected master data type for {exchange}: {type(master_data)}")
                print(f"Raw response: {str(master_data)[:500]}...")
                
        except Exception as e:
            print(f"❌ Error fetching master data from {exchange}: {e}")

if __name__ == "__main__":
    debug_master_data()
