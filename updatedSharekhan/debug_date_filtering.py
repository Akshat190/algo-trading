#!/usr/bin/env python3
"""
Debug script to test the date filtering logic specifically
"""

from datetime import datetime, timedelta

def test_date_filtering():
    """Test the exact date filtering logic used in near_future_fetcher"""
    
    # Current date (as used in the script)
    current_date = datetime.now()
    print(f"📅 Current date: {current_date.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Test expiry date
    expiry_date_str = '30/09/2025'
    print(f"🎯 Test expiry date: {expiry_date_str}")
    
    # Parse expiry date (as done in the script)
    try:
        expiry_dt = datetime.strptime(expiry_date_str, '%d/%m/%Y')
        print(f"✅ Parsed expiry datetime: {expiry_dt.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Calculate days difference (as done in the script)
        days_diff = (expiry_dt - current_date).days
        print(f"📊 Days difference: {days_diff}")
        
        # Test the filtering condition
        days_to_expiry = 30
        print(f"🔍 Threshold: {days_to_expiry} days")
        print(f"🧪 Condition: 0 <= {days_diff} <= {days_to_expiry}")
        
        if 0 <= days_diff <= days_to_expiry:
            print("✅ PASS: Contract would be included")
        else:
            print("❌ FAIL: Contract would be excluded")
            
        # Let's also test some edge cases
        print(f"\n🔬 Edge case testing:")
        print(f"   Is days_diff >= 0? {days_diff >= 0}")
        print(f"   Is days_diff <= 30? {days_diff <= 30}")
        print(f"   Both conditions: {days_diff >= 0 and days_diff <= 30}")
        
    except Exception as e:
        print(f"❌ Error parsing date: {e}")

def test_other_expiry_dates():
    """Test filtering for other expiry dates found"""
    
    current_date = datetime.now()
    test_dates = ['30/09/2025', '28/10/2025', '25/11/2025']
    
    print(f"\n📋 Testing all found expiry dates:")
    
    for expiry_str in test_dates:
        try:
            expiry_dt = datetime.strptime(expiry_str, '%d/%m/%Y')
            days_diff = (expiry_dt - current_date).days
            
            within_30_days = 0 <= days_diff <= 30
            status = "✅ INCLUDED" if within_30_days else "❌ EXCLUDED"
            
            print(f"   {expiry_str}: {days_diff} days -> {status}")
            
        except Exception as e:
            print(f"   {expiry_str}: ERROR - {e}")

if __name__ == "__main__":
    print("🚀 Testing Date Filtering Logic")
    print("=" * 50)
    
    test_date_filtering()
    test_other_expiry_dates()
