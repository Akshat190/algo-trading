## Sharekhan Python – Quick Start

This repo helps you authenticate with Sharekhan, obtain an access token, and call market data APIs. It also includes a WebSocket example.

### 1) Setup

- Windows PowerShell:
```powershell
cd C:\Users\Admin\Desktop\shareconnectpython-main
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

- Verify your credentials in `config.py`:
```python
API_KEY = "6N2P70M5viQq2GfGGgfGonnCgaB1CdTz"
SECRET_KEY = "gYTcB24y68fL8VNTWKnj6fXsyPwXs7ia"
USERNAME = "4031914"
PASSWORD = "<your password>"
TOTP_SECRET = "<your Base32 TOTP secret (optional)>"
```
Note: TOTP_SECRET is a Base32 seed (like JBSWY3DPEHPK3PXP), not a 6‑digit OTP. If you don’t have it, you can still enter the 6‑digit code interactively.

### 2) Get an access token (browser-assisted flow)
Each session, do this to log in and generate a fresh token:
```powershell
python .\SharekhanApi\automated_auth.py
```
- The script opens a login URL in your browser. Log in with username, password, and your 6‑digit TOTP.
- After redirect, copy the `request_token` from the browser URL and paste it back into the script when asked.
- The script will print your `access_token` and confirm “Ready for API operations”.

Troubleshooting:
- If the page says “The requested URL was rejected…”, retry in a new browser/Incognito, disable VPN/proxy/ad-block, or change network. If it persists, contact Sharekhan support with the Support ID.

### 3) Call market data (REST)
Use the token immediately after login. Example quick test in Python REPL:
```python
from SharekhanApi.sharekhanConnect import SharekhanConnect

api_key = "6N2P70M5viQq2GfGGgfGonnCgaB1CdTz"
access_token = "<PASTE_ACCESS_TOKEN_FROM_STEP_2>"

sk = SharekhanConnect(api_key=api_key, access_token=access_token)
print(sk.requestHeaders())

# Examples (replace params with real ones)
print(sk.master("MX"))
print(sk.historicaldata("BC", 500410, "daily"))
```

Token expiry:
- If you see `{ "status": 403, "message": "Token is Expired" }`, repeat Step 2 to get a new access token.

### 4) WebSocket (live streaming)
Run the example and follow any prompts to supply your token if required:
```powershell
python .\example\sharekhanwebsocketexample.py
```
Note: Streaming requires market hours and valid subscriptions.

### 5) Sample script safety
`example\sample.py` includes live order methods:
- `placeOrder`, `modifyOrder`, `cancelOrder` will send real orders if you set a valid token and realistic parameters.
- For market data only, comment those lines and use read-only calls such as `master` and `historicaldata`.

### 6) Tests
A basic test harness is available:
```powershell
python .\test\complete_test.py
```
- It validates headers and demonstrates API calls. Update it to use your fresh access token if you modify it for live calls.

### 7) Notes on TOTP
- The 6‑digit TOTP changes every ~30 seconds; it’s generated from your Base32 TOTP secret.
- If you know your Base32 secret, set it in `automated_auth.py` to auto-generate the code; otherwise, enter the 6‑digit code interactively when prompted.

### 8) Common issues
- 404 on OTP verify: Programmatic OTP endpoints are not publicly available. Use the browser-assisted flow and paste `request_token`.
- URL rejected by WAF: Try a different network/browser/incognito, clear cookies, or contact Sharekhan support with the Support ID.
- Token expired: Get a new token via Step 2.

### 9) What to run (summary)
- Authenticate and get token: `python .\SharekhanApi\automated_auth.py`
- Fetch REST data (your script or REPL) using the printed access token
- WebSocket streaming: `python .\example\sharekhanwebsocketexample.py`
- Optional tests: `python .\test\complete_test.py`

---
Optionally, we can add prompts to `example\sample.py` to paste `request_token` and run only read‑only data calls by default.


