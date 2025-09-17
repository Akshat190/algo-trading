#!/usr/bin/env python3
"""
Quick debug to check FS (Stock Futures) contract expiry dates
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect
from datetime import datetime

def debug_fs_contracts():
    """Check FS contract expiry dates"""
    
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
    
    print("🔍 Fetching FS contracts from NF exchange...")
    try:
        master_data = sk_connect.master("NF")
        
        if not master_data or 'data' not in master_data:
            print("❌ No master data available")
            return
            
        instruments = master_data['data']
        print(f"📊 Processing {len(instruments)} instruments...")
        
        fs_contracts = []
        expiry_dates = {}
        current_date = datetime.now()
        
        for instrument in instruments:
            inst_type = instrument.get('instType', '').upper()
            if inst_type == 'FS':
                symbol = instrument.get('tradingSymbol', '')
                expiry = instrument.get('expiry', '')
                
                fs_contracts.append({
                    'symbol': symbol,
                    'expiry': expiry,
                    'scripCode': instrument.get('scripCode', ''),
                    'lotSize': instrument.get('lotSize', '')
                })
                
                if expiry not in expiry_dates:
                    expiry_dates[expiry] = []
                expiry_dates[expiry].append(symbol)
        
        print(f"✅ Found {len(fs_contracts)} FS (Stock Futures) contracts")
        
        # Show first 10 FS contracts
        print("\n📋 Sample FS contracts:")
        for i, contract in enumerate(fs_contracts[:10]):
            print(f"   {i+1:>2}. {contract['symbol']:<15} | Expiry: {contract['expiry']:<12} | Lot: {contract['lotSize']}")
        
        # Show expiry dates with counts
        print(f"\n📅 FS Contract Expiry Dates:")
        sorted_expiries = sorted(expiry_dates.keys(), key=lambda x: x if x else "0")
        
        for expiry in sorted_expiries:
            contracts = expiry_dates[expiry]
            print(f"   {expiry:<15} : {len(contracts):>3} contracts | Examples: {', '.join(contracts[:3])}")
            
            # Calculate days to expiry for 30/09/2025
            if expiry == '30/09/2025':
                try:
                    expiry_dt = datetime.strptime(expiry, '%d/%m/%Y')
                    days_diff = (expiry_dt - current_date).days
                    print(f"      *** {expiry} is {days_diff} days away from today! ***")
                except:
                    pass
                    
        # Check if any contracts expire within 30 days
        near_expiry_count = 0
        for expiry, contracts in expiry_dates.items():
            if expiry and expiry != '0':
                try:
                    expiry_dt = datetime.strptime(expiry, '%d/%m/%Y')
                    days_diff = (expiry_dt - current_date).days
                    if 0 <= days_diff <= 30:
                        near_expiry_count += len(contracts)
                        print(f"\n🎯 NEAR EXPIRY: {expiry} ({days_diff} days) - {len(contracts)} contracts")
                        print(f"   Examples: {', '.join(contracts[:5])}")
                except:
                    continue
        
        print(f"\n📊 Total FS contracts expiring within 30 days: {near_expiry_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_fs_contracts()
