#!/usr/bin/env python3
"""
Test the exact filtering logic used in near_future_fetcher with known FS instruments
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from config import API_KEY
from datetime import datetime, timedelta
import json

def test_filtering_logic(access_token):
    """Test the exact filtering logic with known FS data"""
    
    try:
        sk_connect = SharekhanConnect(api_key=API_KEY, access_token=access_token)
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
        
        print(f"📊 Processing {len(master_data['data'])} instruments...")
        
        current_date = datetime.now()
        days_to_expiry = 30
        futures_contracts = []
        
        # Counters for debugging
        debug_counters = {
            'total_processed': 0,
            'fs_instruments': 0,
            'has_scripcode': 0,
            'has_valid_expiry': 0,
            'date_parsing_success': 0,
            'within_30_days': 0,
            'final_added': 0
        }
        
        for instrument in master_data['data']:
            debug_counters['total_processed'] += 1
            
            try:
                symbol = instrument.get('tradingSymbol', '').upper()
                name = instrument.get('companyName', '').upper() 
                instrument_type = instrument.get('instType', '').upper()  # Use 'instType' not 'instrumentType'
                expiry_date = instrument.get('expiry', '')  # Use 'expiry' not 'expiryDate'
                
                # TEST: Check if it's FS
                if instrument_type == 'FS':
                    debug_counters['fs_instruments'] += 1
                    
                    # First few FS instruments for debugging
                    if debug_counters['fs_instruments'] <= 3:
                        print(f"   FS #{debug_counters['fs_instruments']}: {symbol} - type: '{instrument_type}' - expiry: '{expiry_date}' - scripCode: {'scripCode' in instrument}")
                    
                    # TEST: Check if has scripCode
                    if 'scripCode' in instrument:
                        debug_counters['has_scripcode'] += 1
                        
                        # TEST: Check expiry conditions
                        if expiry_date and str(expiry_date) != '0' and str(expiry_date).lower() != 'none':
                            debug_counters['has_valid_expiry'] += 1
                            
                            # First few valid expiry for debugging
                            if debug_counters['has_valid_expiry'] <= 3:
                                print(f"   Valid expiry #{debug_counters['has_valid_expiry']}: {symbol} - '{expiry_date}'")
                            
                            # TEST: Parse expiry date and check if it's near expiry
                            try:
                                if expiry_date and str(expiry_date) != '0':
                                    expiry_dt = datetime.strptime(expiry_date, '%d/%m/%Y')
                                    days_diff = (expiry_dt - current_date).days
                                    
                                    debug_counters['date_parsing_success'] += 1
                                    
                                    # First few date parsing for debugging
                                    if debug_counters['date_parsing_success'] <= 3:
                                        print(f"   Date parsing #{debug_counters['date_parsing_success']}: {symbol} - {days_diff} days")
                                    
                                    # TEST: Include contracts expiring within the target days
                                    if 0 <= days_diff <= days_to_expiry:
                                        debug_counters['within_30_days'] += 1
                                        
                                        # First few matches for debugging  
                                        if debug_counters['within_30_days'] <= 5:
                                            print(f"   ✅ MATCH #{debug_counters['within_30_days']}: {symbol} expires in {days_diff} days")
                                        
                                        futures_contracts.append({
                                            'symbol': symbol,
                                            'name': name,
                                            'scripCode': instrument['scripCode'],
                                            'expiry': expiry_date,
                                            'days_to_expiry': days_diff,
                                            'lotSize': instrument.get('lotSize', 1),
                                            'instrumentType': instrument_type,
                                            'tickSize': instrument.get('tickSize', 0.05)
                                        })
                                        
                                        debug_counters['final_added'] += 1
                                        
                            except Exception as date_error:
                                if debug_counters['date_parsing_success'] == 0:  # Show first error
                                    print(f"   ❌ Date parsing error: '{expiry_date}' -> {date_error}")
                                continue
                                
            except Exception as e:
                continue
        
        print(f"\n📊 Debug Counters:")
        for key, value in debug_counters.items():
            print(f"   {key}: {value}")
            
        print(f"\n✅ Found {len(futures_contracts)} near expiry futures contracts")
        
        if futures_contracts:
            print(f"\n🎯 First 10 contracts found:")
            for i, contract in enumerate(futures_contracts[:10]):
                print(f"   {i+1}. {contract['symbol']} - {contract['expiry']} ({contract['days_to_expiry']} days)")
        
        return len(futures_contracts)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 0

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
    
    print("🚀 Testing Exact Near Future Filtering Logic")
    print("=" * 60)
    
    result_count = test_filtering_logic(access_token)
    
    if result_count > 0:
        print(f"\n🎉 SUCCESS! Filtering logic works - found {result_count} contracts")
    else:
        print(f"\n❌ FAILURE! Filtering logic didn't find any contracts")

if __name__ == "__main__":
    main()
