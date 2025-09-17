# Sherkhan API Integration Setup

## What is Sherkhan API?

Sherkhan API provides real-time Indian stock market data including:
- **Live Stock Prices** (NSE/BSE)
- **Futures Data** with expiry dates
- **Open Interest** information
- **Volume** and **Price Changes**
- **Account Information** and **Positions**

Perfect for your Indian stock futures dashboard!

## Your API Credentials

You provided these credentials:
- **API Key**: `6N2P70M5viQq2GfGGgfGonnCgaB1CdTz`
- **Secret Key**: `gYTcB24y68fL8VNTWKnj6fXsyPwXs7ia`

## Quick Setup

### 1. Run the Setup Script
```bash
npm run setup
```

### 2. Enter Your Credentials
When prompted, paste your credentials:
- API Key: `6N2P70M5viQq2GfGGgfGonnCgaB1CdTz`
- Secret Key: `gYTcB24y68fL8VNTWKnj6fXsyPwXs7ia`

### 3. Start Development Server
```bash
npm run dev
```

### 4. Test the Integration
- Visit: http://localhost:3000/api/market/live
- This will show real Indian stock market data!

## Available Endpoints

### Live Market Data
- **GET** `/api/market/live` - Real Sherkhan data
- **GET** `/api/market` - Fallback mock data
- **GET** `/api/market/volatile` - Mock volatile data

### API Testing
- **POST** `/api/market/live` with `{"action": "test-connection"}`
- **POST** `/api/market/live` with `{"action": "get-positions"}`

## Features You'll Get

✅ **Real-time Indian Stock Data**
- TCS, RELIANCE, HDFC, INFY, ICICIBANK, etc.
- Live price updates
- Percentage changes

✅ **Futures Information**
- Near month and far month contracts
- Open interest data
- Futures vs spot pricing

✅ **Account Integration**
- Your account balance
- Current positions
- P&L information

✅ **Automatic Fallback**
- Falls back to mock data if API is down
- No interruption to your dashboard

## Security Notes

🔒 **Your credentials are stored securely in `.env.local`**
🔒 **`.env.local` is automatically added to `.gitignore`**
🔒 **Never commit API credentials to version control**

## What Data You'll See

The dashboard will show:
```json
{
  "symbol": "TCS",
  "lotSize": 300,
  "returns": {
    "current": 2.45,
    "near": 3.15,
    "far": 4.25
  },
  "lastUpdated": "2025-01-10T06:12:00.000Z",
  "volume": 1250000,
  "lastPrice": 3850.50
}
```

## Need Help?

1. **API Not Working?** Check your Sherkhan developer dashboard
2. **Wrong Data Format?** The API automatically converts to your dashboard format
3. **Connection Issues?** The system falls back to mock data
4. **Want More Stocks?** Edit the `SherkhanAPI.getPopularStocks()` method

Your dashboard is now ready to display real Indian stock market data! 🎉
