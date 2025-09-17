#!/usr/bin/env python3
"""
Debug script to find ALL FS instruments and check expiry dates
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from config import API_KEY
from datetime import datetime
import json

def debug_all_fs_instruments(access_token):
    """Find ALL FS instruments and categorize by expiry"""
    
    try:
        sk_connect = SharekhanConnect(api_key=API_KEY, access_token=access_token)
        
        print("🔍 Fetching NF exchange data...")
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
            
        print(f"📊 Total instruments: {len(master_data['data'])}")
        
        current_date = datetime.now()
        print(f"📅 Current date: {current_date.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Find all FS instruments
        fs_instruments = []
        expiry_counts = {}
        
        for i, instrument in enumerate(master_data['data']):
            inst_type = instrument.get('instType', '').upper()
            
            if inst_type == 'FS':
                fs_instruments.append(instrument)
                
                expiry = instrument.get('expiry', '')
                if expiry:
                    expiry_counts[expiry] = expiry_counts.get(expiry, 0) + 1
        
        print(f"\n📊 Total FS instruments found: {len(fs_instruments)}")
        
        # Show expiry date distribution
        print(f"\n📅 Expiry date distribution:")
        for expiry, count in sorted(expiry_counts.items()):
            # Calculate days to expiry
            try:
                expiry_dt = datetime.strptime(expiry, '%d/%m/%Y')
                days_diff = (expiry_dt - current_date).days
                within_30 = "✅" if 0 <= days_diff <= 30 else "❌"
                print(f"   {expiry}: {count} contracts ({days_diff} days) {within_30}")
            except:
                print(f"   {expiry}: {count} contracts (invalid date format)")
        
        # Show sample FS instruments that expire on 30/09/2025
        print(f"\n🎯 Sample FS instruments expiring on 30/09/2025:")
        
        sep30_instruments = [inst for inst in fs_instruments if inst.get('expiry') == '30/09/2025']
        print(f"   Found {len(sep30_instruments)} instruments expiring on 30/09/2025")
        
        for i, inst in enumerate(sep30_instruments[:10]):  # Show first 10
            print(f"   {i+1}. {inst.get('tradingSymbol', 'N/A')} - Code: {inst.get('scripCode', 'N/A')} - Lot: {inst.get('lotSize', 'N/A')}")
        
        return fs_instruments
        
    except Exception as e:
        print(f"❌ Error: {e}")
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
    
    debug_all_fs_instruments(access_token)

if __name__ == "__main__":
    main()
