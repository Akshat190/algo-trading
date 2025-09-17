#!/usr/bin/env python3
"""
Search specifically for 30/09/2025 FS contracts
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from datetime import datetime

def find_sept30_fs():
    """Find FS contracts with 30/09/2025 expiry"""
    
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
    
    print("🔍 Searching for FS contracts with 30/09/2025 expiry...")
    try:
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
            
        instruments = master_data['data']
        print(f"📊 Processing {len(instruments)} instruments...")
        
        sept30_fs_contracts = []
        current_date = datetime.now()
        
        for instrument in instruments:
            inst_type = instrument.get('instType', '').upper()
            expiry_date = instrument.get('expiry', '')
            
            if inst_type == 'FS' and expiry_date == '30/09/2025':
                symbol = instrument.get('tradingSymbol', '')
                scripCode = instrument.get('scripCode', '')
                lotSize = instrument.get('lotSize', 1)
                companyName = instrument.get('companyName', '')
                
                # Calculate days to expiry
                expiry_dt = datetime.strptime(expiry_date, '%d/%m/%Y')
                days_diff = (expiry_dt - current_date).days
                
                sept30_fs_contracts.append({
                    'symbol': symbol,
                    'scripCode': scripCode,
                    'expiry': expiry_date,
                    'days_to_expiry': days_diff,
                    'lotSize': lotSize,
                    'companyName': companyName
                })
        
        print(f"🎯 Found {len(sept30_fs_contracts)} FS contracts expiring on 30/09/2025")
        
        if sept30_fs_contracts:
            print(f"\n📋 FS Contracts expiring on 30/09/2025 ({sept30_fs_contracts[0]['days_to_expiry']} days):")
            for i, contract in enumerate(sept30_fs_contracts[:10]):  # Show first 10
                company_name = contract['companyName'] or 'N/A'
                print(f"   {i+1:>2}. {contract['symbol']:<15} | ScripCode: {contract['scripCode']:<10} | Lot: {contract['lotSize']:<6} | Company: {company_name[:30]}")
            
            if len(sept30_fs_contracts) > 10:
                print(f"   ... and {len(sept30_fs_contracts) - 10} more contracts")
            
            print("\n✅ SUCCESS! These are the contracts that should appear in Near Future!")
            print(f"📊 Days to expiry: {sept30_fs_contracts[0]['days_to_expiry']} days")
            
            # Test the date range condition
            days_diff = sept30_fs_contracts[0]['days_to_expiry']
            print(f"\n🧪 Testing date range condition:")
            print(f"   0 <= {days_diff} <= 30 = {0 <= days_diff <= 30}")
            
        else:
            print("❌ No FS contracts found with 30/09/2025 expiry")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    find_sept30_fs()
