#!/usr/bin/env python3
"""
Debug script to examine the actual expiry date format used by Sharekhan API
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from config import API_KEY
from datetime import datetime

def debug_expiry_formats(access_token):
    """Check what date formats are actually used in NF exchange FS contracts"""
    
    try:
        sk_connect = SharekhanConnect(api_key=API_KEY, access_token=access_token)
        
        print("🔍 Fetching NF exchange data to check FS contract expiry formats...")
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
            
        print(f"📊 Processing {len(master_data['data'])} instruments...")
        
        fs_contracts = []
        unique_expiry_formats = set()
        
        for i, instrument in enumerate(master_data['data']):
            try:
                instrument_type = instrument.get('instType', '').upper()
                expiry_date = instrument.get('expiry', '')
                
                if instrument_type == 'FS' and expiry_date:
                    fs_contracts.append({
                        'symbol': instrument.get('tradingSymbol', ''),
                        'expiry': expiry_date,
                        'scripCode': instrument.get('scripCode', ''),
                        'lotSize': instrument.get('lotSize', 1)
                    })
                    unique_expiry_formats.add(str(expiry_date))
                    
            except Exception as e:
                continue
        
        print(f"\n✅ Found {len(fs_contracts)} FS (Stock Futures) contracts")
        print(f"📅 Found {len(unique_expiry_formats)} unique expiry date formats")
        
        print("\n🗓️ Sample expiry date formats found:")
        sample_formats = sorted(list(unique_expiry_formats))[:20]  # Show first 20
        for fmt in sample_formats:
            print(f"   '{fmt}'")
            
        print(f"\n📋 Sample FS contracts:")
        for i, contract in enumerate(fs_contracts[:10]):  # Show first 10
            print(f"   {i+1}. {contract['symbol']} - Expiry: '{contract['expiry']}' - Code: {contract['scripCode']}")
            
        # Try to find contracts with expiry '30/09/2025' specifically
        print(f"\n🎯 Looking for contracts expiring on '30/09/2025'...")
        sep_30_contracts = [c for c in fs_contracts if c['expiry'] == '30/09/2025']
        print(f"Found {len(sep_30_contracts)} contracts expiring on 30/09/2025")
        
        if sep_30_contracts:
            print("Sample contracts expiring 30/09/2025:")
            for contract in sep_30_contracts[:5]:
                print(f"   - {contract['symbol']} (Code: {contract['scripCode']})")
                
        # Try different date formats that might be used
        print(f"\n🔍 Checking for other common date formats around Sep 30, 2025:")
        
        test_formats = [
            '30/09/2025', '30-09-2025', '2025-09-30', '30092025', '20250930',
            '30/9/2025', '30-9-2025', '30 Sep 2025', '30-Sep-2025'
        ]
        
        for test_fmt in test_formats:
            matching = [c for c in fs_contracts if c['expiry'] == test_fmt]
            if matching:
                print(f"   '{test_fmt}': {len(matching)} contracts")
        
        return fs_contracts
        
    except Exception as e:
        print(f"❌ Error debugging expiry formats: {e}")
        return []

if __name__ == "__main__":
    # Get access token from a recent token file or user input
    try:
        import json
        with open('token_config.json', 'r') as f:
            token_data = json.load(f)
            access_token = token_data.get('access_token')
    except:
        access_token = None
    
    if not access_token:
        access_token = input("Enter your access token: ").strip()
    
    if access_token:
        debug_expiry_formats(access_token)
    else:
        print("❌ Access token required")
