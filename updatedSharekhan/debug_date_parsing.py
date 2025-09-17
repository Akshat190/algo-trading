#!/usr/bin/env python3
"""
Debug date parsing issue
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from datetime import datetime

def debug_date_parsing():
    """Debug why date parsing is failing"""
    
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
    
    print("🔍 Debugging date parsing for FS contracts...")
    try:
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
            
        instruments = master_data['data']
        print(f"📊 Processing {len(instruments)} instruments...")
        
        current_date = datetime.now()
        print(f"📅 Current date: {current_date}")
        
        processed_count = 0
        found_count = 0
        
        for instrument in instruments:
            inst_type = instrument.get('instType', '').upper()
            
            if inst_type == 'FS':
                processed_count += 1
                symbol = instrument.get('tradingSymbol', '')
                expiry_date = instrument.get('expiry', '')
                
                print(f"\n🔍 Processing FS #{processed_count}: {symbol}")
                print(f"   Expiry string: '{expiry_date}'")
                print(f"   Type check: {type(expiry_date)}")
                print(f"   Bool check: {bool(expiry_date)}")
                print(f"   Not 0 check: {str(expiry_date) != '0'}")
                print(f"   Not none check: {str(expiry_date).lower() != 'none'}")
                
                # Test our filtering logic
                if (expiry_date and str(expiry_date) != '0' and str(expiry_date).lower() != 'none'):
                    print(f"   ✅ Passed filter checks")
                    
                    # Test date parsing
                    expiry_dt = None
                    date_formats = ['%d/%m/%Y']  # Only test the main format
                    
                    for date_format in date_formats:
                        try:
                            expiry_dt = datetime.strptime(expiry_date, date_format)
                            print(f"   ✅ Date parsed successfully: {expiry_dt}")
                            break
                        except ValueError as e:
                            print(f"   ❌ Date parsing failed with {date_format}: {e}")
                    
                    if expiry_dt:
                        days_diff = (expiry_dt - current_date).days
                        print(f"   📅 Days difference: {days_diff}")
                        
                        if 0 <= days_diff <= 30:
                            found_count += 1
                            print(f"   🎯 FOUND NEAR EXPIRY CONTRACT! #{found_count}")
                        else:
                            print(f"   ⏰ Not in range (0 <= {days_diff} <= 30)")
                    else:
                        print(f"   ❌ Failed to parse date")
                else:
                    print(f"   ❌ Failed filter checks")
                
                # Only process first 5 FS contracts to avoid spam
                if processed_count >= 5:
                    print(f"\n... processed {processed_count} FS contracts, found {found_count} near expiry")
                    break
        
        print(f"\n📊 Final result: Found {found_count} near expiry contracts out of {processed_count} FS contracts checked")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_date_parsing()
