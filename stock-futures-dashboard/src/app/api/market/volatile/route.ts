import { NextResponse } from 'next/server';
import { MarketData } from '../route';

// Volatile market data with higher returns to test threshold filtering and toasts - 40+ stocks
const volatileMarketData: MarketData[] = [
  // Top performing volatile stocks
  { symbol: "TCS", lotSize: 300, returns: { current: 2.85, near: 6.25, far: 9.85 } },
  { symbol: "RELIANCE", lotSize: 250, returns: { current: 2.45, near: 5.95, far: 8.75 } },
  { symbol: "INFY", lotSize: 600, returns: { current: 3.15, near: 7.35, far: 11.15 } },
  { symbol: "BAJFINANCE", lotSize: 125, returns: { current: 4.25, near: 9.45, far: 14.65 } },
  { symbol: "TATAMOTORS", lotSize: 1800, returns: { current: 3.85, near: 8.15, far: 12.85 } },
  
  // Banking volatile
  { symbol: "HDFCBANK", lotSize: 550, returns: { current: 2.95, near: 6.85, far: 10.45 } },
  { symbol: "KOTAKBANK", lotSize: 400, returns: { current: 2.55, near: 6.25, far: 9.75 } },
  { symbol: "ICICIBANK", lotSize: 375, returns: { current: 2.15, near: 5.45, far: 8.45 } },
  { symbol: "AXISBANK", lotSize: 500, returns: { current: 2.25, near: 5.65, far: 8.85 } },
  { symbol: "SBIN", lotSize: 1500, returns: { current: 1.95, near: 4.85, far: 7.35 } },
  
  // IT volatile
  { symbol: "WIPRO", lotSize: 800, returns: { current: 1.95, near: 4.85, far: 7.65 } },
  { symbol: "HCLTECH", lotSize: 700, returns: { current: 2.65, near: 6.35, far: 9.85 } },
  { symbol: "TECHM", lotSize: 600, returns: { current: 2.25, near: 5.75, far: 8.85 } },
  { symbol: "LTIM", lotSize: 350, returns: { current: 3.05, near: 7.45, far: 11.45 } },
  { symbol: "MINDTREE", lotSize: 400, returns: { current: 2.75, near: 6.65, far: 10.05 } },
  
  // Auto volatile
  { symbol: "MARUTI", lotSize: 100, returns: { current: 3.45, near: 7.95, far: 12.15 } },
  { symbol: "BAJAJFINSERV", lotSize: 125, returns: { current: 3.20, near: 7.70, far: 11.70 } },
  { symbol: "M&M", lotSize: 300, returns: { current: 2.70, near: 6.40, far: 9.90 } },
  { symbol: "EICHERMOT", lotSize: 100, returns: { current: 3.00, near: 7.30, far: 11.30 } },
  
  // FMCG volatile
  { symbol: "HINDUUNILVR", lotSize: 300, returns: { current: 2.05, near: 5.25, far: 8.25 } },
  { symbol: "ITC", lotSize: 1600, returns: { current: 1.80, near: 4.70, far: 7.20 } },
  { symbol: "NESTLEIND", lotSize: 50, returns: { current: 2.35, near: 5.85, far: 9.05 } },
  { symbol: "BRITANNIA", lotSize: 125, returns: { current: 2.50, near: 6.00, far: 9.20 } },
  { symbol: "DABUR", lotSize: 1000, returns: { current: 2.20, near: 5.60, far: 8.60 } },
  
  // Pharma volatile
  { symbol: "SUNPHARMA", lotSize: 700, returns: { current: 2.60, near: 6.30, far: 9.80 } },
  { symbol: "DRREDDY", lotSize: 125, returns: { current: 2.90, near: 6.90, far: 10.40 } },
  { symbol: "CIPLA", lotSize: 700, returns: { current: 2.30, near: 5.80, far: 8.90 } },
  { symbol: "DIVISLAB", lotSize: 150, returns: { current: 2.85, near: 6.85, far: 10.35 } },
  
  // Energy volatile
  { symbol: "ONGC", lotSize: 4200, returns: { current: 1.75, near: 4.65, far: 7.15 } },
  { symbol: "IOC", lotSize: 4000, returns: { current: 1.85, near: 4.80, far: 7.30 } },
  { symbol: "BPCL", lotSize: 1500, returns: { current: 2.00, near: 5.00, far: 7.60 } },
  { symbol: "HINDPETRO", lotSize: 2000, returns: { current: 1.90, near: 4.90, far: 7.40 } },
  
  // Industrial volatile
  { symbol: "LT", lotSize: 500, returns: { current: 2.35, near: 5.85, far: 9.05 } },
  { symbol: "ULTRACEMCO", lotSize: 300, returns: { current: 2.75, near: 6.75, far: 10.25 } },
  { symbol: "GRASIM", lotSize: 400, returns: { current: 2.65, near: 6.45, far: 9.95 } },
  { symbol: "ADANIPORTS", lotSize: 900, returns: { current: 3.05, near: 7.55, far: 11.55 } },
  
  // Metals volatile
  { symbol: "TATASTEEL", lotSize: 2000, returns: { current: 3.10, near: 7.60, far: 11.60 } },
  { symbol: "HINDALCO", lotSize: 1500, returns: { current: 2.85, near: 6.85, far: 10.35 } },
  { symbol: "JSWSTEEL", lotSize: 1200, returns: { current: 2.95, near: 7.15, far: 10.85 } },
  { symbol: "VEDL", lotSize: 2500, returns: { current: 2.80, near: 6.80, far: 10.40 } },
  
  // Others volatile
  { symbol: "ASIANPAINT", lotSize: 300, returns: { current: 2.18, near: 5.48, far: 8.28 } },
  { symbol: "TITAN", lotSize: 300, returns: { current: 2.95, near: 7.25, far: 10.95 } },
  { symbol: "APOLLOHOSP", lotSize: 300, returns: { current: 3.15, near: 7.75, far: 11.75 } },
  { symbol: "BHARTIARTL", lotSize: 1800, returns: { current: 1.85, near: 4.75, far: 7.25 } },
  { symbol: "POWERGRID", lotSize: 3200, returns: { current: 1.45, near: 4.25, far: 6.75 } },
  { symbol: "NTPC", lotSize: 2000, returns: { current: 1.75, near: 4.60, far: 7.10 } },
  { symbol: "COALINDIA", lotSize: 3000, returns: { current: 1.65, near: 4.45, far: 6.95 } },
  { symbol: "INDUSINDBK", lotSize: 900, returns: { current: 2.05, near: 5.15, far: 8.15 } }
];

// Add some randomization to simulate live market data
function addRandomVariation(value: number): number {
  const variation = (Math.random() - 0.5) * 0.2; // ±0.1% variation for volatility
  return Math.max(0, value + variation);
}

export async function GET() {
  // Add slight random variations to simulate live volatile data
  const liveData = volatileMarketData.map(stock => ({
    ...stock,
    returns: {
      current: addRandomVariation(stock.returns.current),
      near: addRandomVariation(stock.returns.near), 
      far: addRandomVariation(stock.returns.far)
    }
  }));

  return NextResponse.json(liveData);
}
