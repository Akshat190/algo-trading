#!/usr/bin/env python3
"""
Debug script to test the exact scenario used in token_manager
"""

from near_future_fetcher import NearFutureFetcher
from config import API_KEY
import json

def test_token_manager_scenario():
    """Test exactly what token_manager does"""
    
    # Get the access token from saved token data
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
    
    print(f"🔑 Using access token: {access_token[:30]}...")
    
    # Initialize Near Future fetcher (exactly like token_manager does)
    try:
        print("🔄 Initializing NearFutureFetcher...")
        near_future_fetcher = NearFutureFetcher(API_KEY, access_token)
        
        # Get near future contracts (exactly like token_manager does)
        print("🔍 Calling get_near_expiry_futures(days_to_expiry=30)...")
        contracts = near_future_fetcher.get_near_expiry_futures(days_to_expiry=30)
        
        print(f"📊 Result: Found {len(contracts)} contracts")
        
        if contracts:
            print("✅ SUCCESS! Found contracts:")
            for i, contract in enumerate(contracts[:5]):
                print(f"   {i+1}. {contract['symbol']} - Expires: {contract['expiry']} ({contract['days_to_expiry']} days)")
        else:
            print("❌ No contracts found - debugging...")
            
            # Let's debug step by step
            print("\n🔬 Debugging step by step:")
            
            # Test master data fetch
            try:
                master_data = near_future_fetcher.sk_connect.master("NF")
                if master_data and 'data' in master_data:
                    print(f"   ✅ Master data OK: {len(master_data['data'])} instruments")
                    
                    # Count FS instruments
                    fs_count = 0
                    fs_with_expiry = 0
                    fs_with_sep30 = 0
                    
                    for instrument in master_data['data']:
                        inst_type = instrument.get('instType', '').upper()
                        expiry = instrument.get('expiry', '')
                        
                        if inst_type == 'FS':
                            fs_count += 1
                            if expiry and str(expiry) != '0':
                                fs_with_expiry += 1
                                if expiry == '30/09/2025':
                                    fs_with_sep30 += 1
                    
                    print(f"   📊 FS instruments: {fs_count}")
                    print(f"   📊 FS with expiry: {fs_with_expiry}")
                    print(f"   📊 FS expiring 30/09/2025: {fs_with_sep30}")
                    
                else:
                    print("   ❌ Master data problem")
            except Exception as e:
                print(f"   ❌ Master data error: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Testing Token Manager Scenario")
    print("=" * 60)
    test_token_manager_scenario()
