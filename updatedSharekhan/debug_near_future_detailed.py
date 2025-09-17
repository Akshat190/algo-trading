#!/usr/bin/env python3
"""
Debug version of the near_future_fetcher with detailed logging to find the issue
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from datetime import datetime, timedelta
from config import API_KEY
import json

def debug_get_near_expiry_futures(api_key, access_token, exchange="NF", days_to_expiry=30):
    """Debug version with extensive logging"""
    
    try:
        print(f"🔍 Fetching futures contracts from exchange: {exchange}")
        sk_connect = SharekhanConnect(api_key=api_key, access_token=access_token)
        master_data = sk_connect.master(exchange)
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return []
        
        print(f"📊 Processing {len(master_data['data'])} instruments...")
        
        current_date = datetime.now()
        print(f"📅 Current date: {current_date.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"🎯 Looking for contracts expiring within {days_to_expiry} days")
        
        futures_contracts = []
        
        debug_counters = {
            'total_processed': 0,
            'fs_instruments': 0,
            'fs_with_scripcode': 0,
            'fs_with_expiry': 0,
            'expiry_parsing_success': 0,
            'expiry_parsing_failed': 0,
            'within_date_range': 0,
            'final_added': 0
        }
        
        for i, instrument in enumerate(master_data['data']):
            debug_counters['total_processed'] += 1
            
            # Show progress every 10k instruments
            if i % 10000 == 0:
                print(f"   Processing instrument {i+1}/{len(master_data['data'])}...")
            
            try:
                symbol = instrument.get('tradingSymbol', '').upper()
                name = instrument.get('companyName', '').upper()
                instrument_type = instrument.get('instType', '').upper()
                expiry_date = instrument.get('expiry', '')
                
                # Check if it's FS instrument
                if instrument_type == 'FS':
                    debug_counters['fs_instruments'] += 1
                    
                    # Check if has scripCode
                    if 'scripCode' in instrument:
                        debug_counters['fs_with_scripcode'] += 1
                        
                        # Check expiry date conditions
                        if expiry_date and str(expiry_date) != '0' and str(expiry_date).lower() != 'none':
                            debug_counters['fs_with_expiry'] += 1
                            
                            # Log first few FS contracts for inspection
                            if debug_counters['fs_with_expiry'] <= 5:
                                print(f"   📋 Sample FS contract #{debug_counters['fs_with_expiry']}: {symbol} - Expiry: '{expiry_date}' - Code: {instrument['scripCode']}")
                            
                            # Parse expiry date and check if it's near expiry
                            try:
                                if expiry_date and str(expiry_date) != '0':
                                    expiry_dt = datetime.strptime(expiry_date, '%d/%m/%Y')
                                    days_diff = (expiry_dt - current_date).days
                                    
                                    debug_counters['expiry_parsing_success'] += 1
                                    
                                    # Log the first few date calculations
                                    if debug_counters['expiry_parsing_success'] <= 5:
                                        print(f"   🧮 Date calc #{debug_counters['expiry_parsing_success']}: {expiry_date} -> {days_diff} days diff")
                                    
                                    # Include contracts expiring within the target days
                                    if 0 <= days_diff <= days_to_expiry:
                                        debug_counters['within_date_range'] += 1
                                        
                                        # Log the first few contracts that meet criteria
                                        if debug_counters['within_date_range'] <= 5:
                                            print(f"   ✅ Match #{debug_counters['within_date_range']}: {symbol} expires in {days_diff} days")
                                        
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
                                debug_counters['expiry_parsing_failed'] += 1
                                if debug_counters['expiry_parsing_failed'] <= 3:
                                    print(f"   ❌ Date parsing error: {expiry_date} -> {date_error}")
                                continue
                            
            except Exception as e:
                continue
        
        print(f"\n📊 Debug Summary:")
        for key, value in debug_counters.items():
            print(f"   {key}: {value}")
        
        print(f"\n✅ Found {len(futures_contracts)} near expiry futures contracts")
        return futures_contracts
        
    except Exception as e:
        print(f"❌ Error fetching near expiry futures: {e}")
        import traceback
        traceback.print_exc()
        return []

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
    
    print(f"🔑 Using API Key: {API_KEY[:20]}...")
    print(f"🎫 Using Access Token: {access_token[:30]}...")
    
    contracts = debug_get_near_expiry_futures(API_KEY, access_token)
    
    if contracts:
        print(f"\n🎉 SUCCESS! Found {len(contracts)} contracts")
        print("Top 10 contracts:")
        for i, contract in enumerate(contracts[:10]):
            print(f"   {i+1}. {contract['symbol']} - {contract['expiry']} ({contract['days_to_expiry']} days)")
    else:
        print("\n❌ No contracts found")

if __name__ == "__main__":
    main()
