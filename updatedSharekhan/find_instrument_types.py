#!/usr/bin/env python3
"""
Script to find all instrument types and understand the data structure
"""

from SharekhanApi.sharekhanConnect import SharekhanConnect

def find_instrument_types():
    """Find all possible instrument types"""
    
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
    
    exchanges_to_check = ["NF", "NC", "MX", "BC"]
    
    for exchange in exchanges_to_check:
        print(f"\n🔍 Checking {exchange} exchange...")
        try:
            master_data = sk_connect.master(exchange)
            
            if not master_data or 'data' not in master_data:
                print(f"❌ No master data for {exchange}")
                continue
                
            instruments = master_data['data']
            print(f"📊 Total instruments in {exchange}: {len(instruments)}")
            
            # Collect all unique instrument types
            inst_types = {}
            expiry_samples = {}
            
            for instrument in instruments:
                inst_type = instrument.get('instType', '').upper()
                expiry = str(instrument.get('expiry', '')).strip()
                symbol = instrument.get('tradingSymbol', '')
                
                # Count instrument types
                if inst_type not in inst_types:
                    inst_types[inst_type] = []
                inst_types[inst_type].append(symbol)
                
                # Collect expiry samples
                if expiry and expiry != '0' and expiry.lower() != 'none':
                    if expiry not in expiry_samples:
                        expiry_samples[expiry] = []
                    expiry_samples[expiry].append(f"{symbol}({inst_type})")
            
            print(f"\n📈 Instrument types found in {exchange}:")
            for inst_type, symbols in inst_types.items():
                sample_symbols = symbols[:3]  # Show first 3 symbols
                print(f"   {inst_type or 'BLANK':<10} : {len(symbols):>6} contracts | Examples: {', '.join(sample_symbols)}")
            
            print(f"\n📅 Expiry dates found in {exchange} (first 10):")
            count = 0
            for expiry, symbols in list(expiry_samples.items())[:10]:
                sample_symbols = symbols[:2]  # Show first 2 symbols
                print(f"   {expiry:<15} : {len(symbols):>4} contracts | Examples: {', '.join(sample_symbols)}")
                count += 1
                if count >= 10:
                    break
            
            if len(expiry_samples) > 10:
                print(f"   ... and {len(expiry_samples) - 10} more expiry dates")
                
        except Exception as e:
            print(f"❌ Error checking {exchange}: {e}")

if __name__ == "__main__":
    find_instrument_types()
