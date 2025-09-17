#!/usr/bin/env python3
"""
Side-by-side comparison of working vs non-working FS detection
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from config import API_KEY
import json

def debug_side_by_side(access_token):
    """Compare working vs non-working FS detection logic"""
    
    try:
        sk_connect = SharekhanConnect(api_key=API_KEY, access_token=access_token)
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
        
        print(f"📊 Processing {len(master_data['data'])} instruments...")
        
        # Method 1: Working method (from debug_all_fs_instruments.py)
        print(f"\n🟢 Method 1 (WORKING):")
        fs_count_1 = 0
        for instrument in master_data['data']:
            inst_type = instrument.get('instType', '').upper()
            if inst_type == 'FS':
                fs_count_1 += 1
                if fs_count_1 <= 3:
                    print(f"   Found FS #{fs_count_1}: {instrument.get('tradingSymbol')} - instType: '{instrument.get('instType')}'")
        print(f"   Total FS found: {fs_count_1}")
        
        # Method 2: Non-working method (from near_future_fetcher.py logic)
        print(f"\n🔴 Method 2 (NON-WORKING):")
        fs_count_2 = 0
        for instrument in master_data['data']:
            try:
                symbol = instrument.get('tradingSymbol', '').upper()
                name = instrument.get('companyName', '').upper() 
                instrument_type = instrument.get('instType', '').upper()  # Use 'instType' not 'instrumentType'
                expiry_date = instrument.get('expiry', '')  # Use 'expiry' not 'expiryDate'
                
                if instrument_type == 'FS':
                    fs_count_2 += 1
                    if fs_count_2 <= 3:
                        print(f"   Found FS #{fs_count_2}: {symbol} - instType: '{instrument_type}'")
                        
            except Exception as e:
                continue
                
        print(f"   Total FS found: {fs_count_2}")
        
        # Let's check what exactly is different
        print(f"\n🔍 Detailed comparison:")
        
        # Check first few instruments with both methods
        for i in range(min(10, len(master_data['data']))):
            instrument = master_data['data'][i]
            
            # Method 1 check
            inst_type_1 = instrument.get('instType', '').upper()
            
            # Method 2 check  
            try:
                symbol = instrument.get('tradingSymbol', '').upper()
                name = instrument.get('companyName', '').upper() 
                instrument_type_2 = instrument.get('instType', '').upper()
                expiry_date = instrument.get('expiry', '')
                
                method_2_success = True
            except Exception as e:
                method_2_success = False
                instrument_type_2 = "ERROR"
            
            print(f"   Instrument #{i+1}: {instrument.get('tradingSymbol', 'N/A')}")
            print(f"     Method 1: instType = '{inst_type_1}' -> FS? {inst_type_1 == 'FS'}")
            print(f"     Method 2: instType = '{instrument_type_2}' -> FS? {instrument_type_2 == 'FS'} (Success: {method_2_success})")
            
            if inst_type_1 != instrument_type_2 or (inst_type_1 == 'FS'):
                print(f"     ⚠️  DIFFERENCE FOUND!")
                break
                
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
    
    print("🚀 Side-by-Side Comparison of FS Detection")
    print("=" * 60)
    
    debug_side_by_side(access_token)

if __name__ == "__main__":
    main()
