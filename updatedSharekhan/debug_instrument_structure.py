#!/usr/bin/env python3
"""
Debug script to examine the actual structure of instruments in master data
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from config import API_KEY
import json

def debug_instrument_structure(access_token):
    """Examine the structure of the first few instruments"""
    
    try:
        sk_connect = SharekhanConnect(api_key=API_KEY, access_token=access_token)
        
        print("🔍 Fetching NF exchange data...")
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
            
        print(f"📊 Total instruments: {len(master_data['data'])}")
        
        # Look at the first 10 instruments to understand structure
        print(f"\n🔬 Examining first 10 instruments structure:")
        
        for i in range(min(10, len(master_data['data']))):
            instrument = master_data['data'][i]
            print(f"\n   Instrument #{i+1}:")
            print(f"   Keys: {list(instrument.keys())}")
            print(f"   Sample values:")
            for key, value in instrument.items():
                print(f"     {key}: '{value}'")
                
        # Now look specifically for any FS instruments and show their structure
        print(f"\n🎯 Looking for FS instruments specifically:")
        
        fs_found = 0
        for i, instrument in enumerate(master_data['data']):
            # Check all possible field names for instrument type
            inst_type_fields = ['instType', 'instrumentType', 'type', 'segment', 'product']
            inst_types = []
            
            for field in inst_type_fields:
                if field in instrument:
                    inst_types.append(f"{field}='{instrument[field]}'")
            
            # Check if any field contains 'FS'
            has_fs = False
            for field in inst_type_fields:
                if field in instrument and str(instrument[field]).upper() == 'FS':
                    has_fs = True
                    break
                    
            if has_fs:
                fs_found += 1
                if fs_found <= 3:  # Show first 3 FS instruments
                    print(f"\n   FS Instrument #{fs_found}:")
                    print(f"   All type fields: {', '.join(inst_types)}")
                    print(f"   Symbol: {instrument.get('tradingSymbol', 'N/A')}")
                    print(f"   Expiry: {instrument.get('expiry', 'N/A')}")
                    print(f"   ScripCode: {instrument.get('scripCode', 'N/A')}")
                    print(f"   Full structure: {instrument}")
                    
            if fs_found >= 3:  # Only show first 3
                break
                
        print(f"\n📊 Total FS instruments found: {fs_found}")
        
        # Also try to find instruments with other field names that might contain FS
        print(f"\n🔍 Checking for any instruments with 'FS' in any field:")
        
        fs_in_any_field = 0
        for i, instrument in enumerate(master_data['data']):
            for key, value in instrument.items():
                if 'FS' in str(value).upper():
                    fs_in_any_field += 1
                    if fs_in_any_field <= 5:
                        print(f"   Found 'FS' in {key}: '{value}' (instrument: {instrument.get('tradingSymbol', 'N/A')})")
                    break
                    
        print(f"\n📊 Instruments with 'FS' in any field: {fs_in_any_field}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    # Get the access token
    try:
        with open('token_config.json', 'r') as f:
            token_data = json.load(f)
            access_token = token_data.get('access_token')
    except Exception as e:
        print(f"❌ Error loading token: {e}")
        return
    
    if not access_token:
        print("❌ No access token found")
        return
    
    debug_instrument_structure(access_token)

if __name__ == "__main__":
    main()
