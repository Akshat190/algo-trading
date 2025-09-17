#!/usr/bin/env python3
"""
Test the specific line that's causing the exception
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from config import API_KEY
import json

def test_exception_line(access_token):
    """Test what line is causing the exception"""
    
    try:
        sk_connect = SharekhanConnect(api_key=API_KEY, access_token=access_token)
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
        
        print(f"📊 Testing first 10 instruments...")
        
        for i in range(min(10, len(master_data['data']))):
            instrument = master_data['data'][i]
            
            print(f"\nInstrument #{i+1}: {instrument.get('tradingSymbol', 'N/A')}")
            
            try:
                print("  Step 1: symbol = instrument.get('tradingSymbol', '').upper()")
                symbol = instrument.get('tradingSymbol', '').upper()
                print(f"    ✅ symbol = '{symbol}'")
            except Exception as e:
                print(f"    ❌ Error: {e}")
                continue
            
            try:
                print("  Step 2: name = instrument.get('companyName', '').upper()")
                name = instrument.get('companyName', '').upper()
                print(f"    ✅ name = '{name}'")
            except Exception as e:
                print(f"    ❌ Error: {e}")
                print(f"    companyName value: {instrument.get('companyName', 'MISSING')}")
                print(f"    companyName type: {type(instrument.get('companyName', 'MISSING'))}")
                continue
            
            try:
                print("  Step 3: instrument_type = instrument.get('instType', '').upper()")
                instrument_type = instrument.get('instType', '').upper()
                print(f"    ✅ instrument_type = '{instrument_type}'")
            except Exception as e:
                print(f"    ❌ Error: {e}")
                continue
            
            try:
                print("  Step 4: expiry_date = instrument.get('expiry', '')")
                expiry_date = instrument.get('expiry', '')
                print(f"    ✅ expiry_date = '{expiry_date}'")
            except Exception as e:
                print(f"    ❌ Error: {e}")
                continue
                
            print(f"    All steps passed!")
            
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
    
    test_exception_line(access_token)

if __name__ == "__main__":
    main()
