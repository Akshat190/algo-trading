#!/usr/bin/env python3
"""
Token Manager for Website - Automatically handles token refresh
"""

import json
import time
try:
    import jwt
except ImportError:
    # Fallback if PyJWT not installed
    jwt = None
from datetime import datetime, timedelta
from SharekhanApi.automated_auth import automated_sharekhan_login
import os

class TokenManager:
    def __init__(self, config_file="token_config.json"):
        self.config_file = config_file
        self.token_data = self.load_token_data()
        
    def load_token_data(self):
        """Load token data from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading token data: {e}")
        
        return {
            "access_token": None,
            "refresh_token": None,
            "expires_at": None,
            "last_refreshed": None
        }
    
    def save_token_data(self):
        """Save token data to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.token_data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving token data: {e}")
    
    def is_token_valid(self, buffer_minutes=5):
        """Check if current token is valid (with buffer time)"""
        if not self.token_data.get("access_token"):
            return False
        
        try:
            # Decode JWT token to check expiry
            token = self.token_data["access_token"]
            # Handle different PyJWT versions
            try:
                # For PyJWT >= 2.0
                decoded = jwt.decode(token, options={"verify_signature": False})
            except AttributeError:
                # For PyJWT < 2.0
                decoded = jwt.decode(token, verify=False)
            except Exception:
                # Alternative method using base64 decoding
                import base64
                import json
                # JWT tokens have 3 parts separated by dots
                parts = token.split('.')
                if len(parts) >= 2:
                    # Decode the payload (second part)
                    payload = parts[1]
                    # Add padding if necessary
                    payload += '=' * (4 - len(payload) % 4)
                    decoded_bytes = base64.urlsafe_b64decode(payload)
                    decoded = json.loads(decoded_bytes.decode('utf-8'))
                else:
                    return False
            exp_time = decoded.get('exp', 0)
            
            # Add buffer time (5 minutes before actual expiry)
            current_time = time.time()
            buffer_time = buffer_minutes * 60
            
            return current_time < (exp_time - buffer_time)
            
        except Exception as e:
            print(f"⚠️  Error checking token validity: {e}")
            return False
    
    def refresh_token_automatically(self):
        """Automatically refresh token using saved credentials"""
        try:
            # Load credentials from config
            from config import API_KEY, SECRET_KEY, USERNAME, PASSWORD, TOTP_SECRET, VENDOR_KEY, VERSION_ID
            
            print("🔄 Auto-refreshing access token...")
            
            access_token = automated_sharekhan_login(
                api_key=API_KEY,
                secret_key=SECRET_KEY,
                username=USERNAME,
                password=PASSWORD,
                totp_secret=TOTP_SECRET,
                vendor_key=VENDOR_KEY,
                version_id=VERSION_ID
            )
            
            if access_token:
                # Decode token to get expiry
                try:
                    # Handle different PyJWT versions
                    try:
                        decoded = jwt.decode(access_token, options={"verify_signature": False})
                    except AttributeError:
                        decoded = jwt.decode(access_token, verify=False)
                    except Exception:
                        # Fallback to base64 decoding
                        import base64
                        parts = access_token.split('.')
                        payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
                        decoded_bytes = base64.urlsafe_b64decode(payload)
                        decoded = json.loads(decoded_bytes.decode('utf-8'))
                    exp_time = decoded.get('exp', 0)
                except Exception:
                    exp_time = int(time.time()) + 7200  # Default to 2 hours from now
                
                self.token_data.update({
                    "access_token": access_token,
                    "expires_at": exp_time,
                    "last_refreshed": time.time()
                })
                
                self.save_token_data()
                print("✅ Token refreshed successfully!")
                return True
            else:
                print("❌ Failed to refresh token")
                return False
                
        except Exception as e:
            print(f"❌ Auto-refresh failed: {e}")
            return False
    
    def get_valid_token(self):
        """Get a valid access token, refreshing if necessary"""
        if self.is_token_valid():
            print("✅ Using existing valid token")
            return self.token_data["access_token"]
        
        print("⏰ Token expired or invalid, refreshing...")
        if self.refresh_token_automatically():
            return self.token_data["access_token"]
        
        return None
    
    def get_token_info(self):
        """Get information about current token"""
        if not self.token_data.get("access_token"):
            return {"status": "no_token"}
        
        try:
            token = self.token_data["access_token"]
            # Handle different PyJWT versions
            try:
                decoded = jwt.decode(token, options={"verify_signature": False})
            except AttributeError:
                decoded = jwt.decode(token, verify=False)
            except Exception:
                # Fallback to base64 decoding
                import base64
                parts = token.split('.')
                payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
                decoded_bytes = base64.urlsafe_b64decode(payload)
                decoded = json.loads(decoded_bytes.decode('utf-8'))
            exp_time = decoded.get('exp', 0)
            
            return {
                "status": "valid" if self.is_token_valid() else "expired",
                "expires_at": datetime.fromtimestamp(exp_time).strftime("%Y-%m-%d %H:%M:%S"),
                "last_refreshed": datetime.fromtimestamp(self.token_data.get("last_refreshed", 0)).strftime("%Y-%m-%d %H:%M:%S") if self.token_data.get("last_refreshed") else "Never",
                "time_remaining": max(0, exp_time - time.time()) // 60  # Minutes remaining
            }
        except:
            return {"status": "invalid"}

# Usage example for your website
class WebsiteNearFuture:
    def __init__(self):
        self.token_manager = TokenManager()
        self.near_future_fetcher = None
    
    def initialize_connection(self):
        """Initialize connection with valid token"""
        try:
            from config import API_KEY
            
            # Get valid token (auto-refreshes if needed)
            access_token = self.token_manager.get_valid_token()
            
            if not access_token:
                return {"success": False, "error": "Failed to get valid access token"}
            
            # Initialize Near Future fetcher
            from near_future_fetcher import NearFutureFetcher
            self.near_future_fetcher = NearFutureFetcher(API_KEY, access_token)
            
            return {"success": True, "message": "Connection initialized successfully"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_near_future_data(self):
        """Get near future data for website"""
        try:
            # Ensure we have a valid connection
            if not self.near_future_fetcher:
                init_result = self.initialize_connection()
                if not init_result["success"]:
                    return init_result
            
            # Get categorized futures contracts
            categorized_contracts = self.near_future_fetcher.get_all_futures_by_category()
            
            # Check if any contracts found
            total_contracts = sum(len(contracts) for contracts in categorized_contracts.values())
            
            if total_contracts == 0:
                return {"success": False, "error": "No futures contracts found"}
            
            # Format data for website by category
            formatted_data = {
                "current": [],
                "near": [], 
                "far": []
            }
            
            for category, contracts in categorized_contracts.items():
                for contract in contracts[:240]:  # Limit each category to 240
                    formatted_data[category].append({
                        "symbol": contract["symbol"],
                        "expiry": contract["expiry"],
                        "days_to_expiry": contract["days_to_expiry"],
                        "lot_size": contract["lotSize"],
                        "scrip_code": contract["scripCode"],
                        "category": contract["category"]
                    })
            
            return {
                "success": True,
                "data": formatted_data,
                "summary": {
                    "current": len(formatted_data["current"]),
                    "near": len(formatted_data["near"]),
                    "far": len(formatted_data["far"]),
                    "total": sum(len(contracts) for contracts in formatted_data.values())
                },
                "token_info": self.token_manager.get_token_info()
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_token_status(self):
        """Get current token status for website dashboard"""
        return self.token_manager.get_token_info()

# Example usage
def main():
    """Example of how to use in your website"""
    
    # Initialize website near future
    website = WebsiteNearFuture()
    
    # Get token status
    token_info = website.get_token_status()
    print(f"🔑 Token Status: {token_info}")
    
    # Get near future data
    result = website.get_near_future_data()
    
    if result["success"]:
        summary = result['summary']
        print(f"✅ Retrieved {summary['total']} futures contracts across all categories")
        print("📊 Contract Summary:")
        print(f"   Current Month (30/09/2025): {summary['current']} contracts")
        print(f"   Near Future (28/10/2025): {summary['near']} contracts")
        print(f"   Far Future (25/11/2025): {summary['far']} contracts")
        
        print("\n📋 Sample contracts from Current Month:")
        for i, contract in enumerate(result["data"]["current"][:5]):
            print(f"   {i+1}. {contract['symbol']} - Expires: {contract['expiry']} ({contract['days_to_expiry']} days)")
    else:
        print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    main()
