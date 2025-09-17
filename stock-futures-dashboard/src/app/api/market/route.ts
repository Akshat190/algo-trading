import { NextResponse } from 'next/server';

export interface MarketData {
  symbol: string;
  lotSize: number;
  returns: {
    current: number;
    near: number;
    far: number;
  };
  lastUpdated: string;
}

// Mock data with 40+ Indian stocks - futures returns are always higher than current for positive profits
const mockMarketData: MarketData[] = [
  // Top Tier Stocks
  { symbol: "TCS", lotSize: 300, returns: { current: 1.20, near: 2.85, far: 4.15 } },
  { symbol: "RELIANCE", lotSize: 250, returns: { current: 0.95, near: 2.45, far: 3.78 } },
  { symbol: "HDFC", lotSize: 550, returns: { current: 1.15, near: 2.95, far: 4.25 } },
  { symbol: "INFY", lotSize: 600, returns: { current: 1.35, near: 3.10, far: 4.55 } },
  { symbol: "ICICIBANK", lotSize: 375, returns: { current: 0.85, near: 2.15, far: 3.45 } },
  
  // Banking Sector
  { symbol: "HDFCBANK", lotSize: 550, returns: { current: 1.10, near: 2.80, far: 4.00 } },
  { symbol: "KOTAKBANK", lotSize: 400, returns: { current: 1.05, near: 2.55, far: 3.75 } },
  { symbol: "SBIN", lotSize: 1500, returns: { current: 0.75, near: 1.95, far: 2.85 } },
  { symbol: "AXISBANK", lotSize: 500, returns: { current: 0.90, near: 2.25, far: 3.35 } },
  { symbol: "INDUSINDBK", lotSize: 900, returns: { current: 0.80, near: 2.05, far: 3.15 } },
  
  // IT Sector
  { symbol: "WIPRO", lotSize: 800, returns: { current: 0.75, near: 1.95, far: 2.98 } },
  { symbol: "HCLTECH", lotSize: 700, returns: { current: 1.05, near: 2.65, far: 3.85 } },
  { symbol: "TECHM", lotSize: 600, returns: { current: 0.95, near: 2.25, far: 3.35 } },
  { symbol: "LTIM", lotSize: 350, returns: { current: 1.25, near: 3.05, far: 4.45 } },
  { symbol: "MINDTREE", lotSize: 400, returns: { current: 1.15, near: 2.75, far: 4.05 } },
  
  // Telecom & Utilities
  { symbol: "BHARTIARTL", lotSize: 1800, returns: { current: 0.65, near: 1.85, far: 2.75 } },
  { symbol: "POWERGRID", lotSize: 3200, returns: { current: 0.55, near: 1.45, far: 2.25 } },
  { symbol: "NTPC", lotSize: 2000, returns: { current: 0.70, near: 1.75, far: 2.60 } },
  { symbol: "COALINDIA", lotSize: 3000, returns: { current: 0.60, near: 1.65, far: 2.45 } },
  
  // Auto Sector
  { symbol: "MARUTI", lotSize: 100, returns: { current: 1.25, near: 2.95, far: 4.15 } },
  { symbol: "TATAMOTORS", lotSize: 1800, returns: { current: 1.35, near: 3.15, far: 4.65 } },
  { symbol: "BAJAJFINSERV", lotSize: 125, returns: { current: 1.40, near: 3.20, far: 4.70 } },
  { symbol: "M&M", lotSize: 300, returns: { current: 1.10, near: 2.70, far: 3.90 } },
  { symbol: "EICHERMOT", lotSize: 100, returns: { current: 1.30, near: 3.00, far: 4.30 } },
  
  // FMCG & Consumer
  { symbol: "HINDUUNILVR", lotSize: 300, returns: { current: 0.85, near: 2.05, far: 3.25 } },
  { symbol: "ITC", lotSize: 1600, returns: { current: 0.70, near: 1.80, far: 2.70 } },
  { symbol: "NESTLEIND", lotSize: 50, returns: { current: 0.95, near: 2.35, far: 3.55 } },
  { symbol: "BRITANNIA", lotSize: 125, returns: { current: 1.00, near: 2.50, far: 3.70 } },
  { symbol: "DABUR", lotSize: 1000, returns: { current: 0.90, near: 2.20, far: 3.40 } },
  
  // Pharma Sector
  { symbol: "SUNPHARMA", lotSize: 700, returns: { current: 1.05, near: 2.60, far: 3.80 } },
  { symbol: "DRREDDY", lotSize: 125, returns: { current: 1.20, near: 2.90, far: 4.20 } },
  { symbol: "CIPLA", lotSize: 700, returns: { current: 0.95, near: 2.30, far: 3.50 } },
  { symbol: "DIVISLAB", lotSize: 150, returns: { current: 1.15, near: 2.85, far: 4.15 } },
  
  // Energy & Oil
  { symbol: "ONGC", lotSize: 4200, returns: { current: 0.65, near: 1.75, far: 2.65 } },
  { symbol: "IOC", lotSize: 4000, returns: { current: 0.70, near: 1.85, far: 2.80 } },
  { symbol: "BPCL", lotSize: 1500, returns: { current: 0.80, near: 2.00, far: 3.00 } },
  { symbol: "HINDPETRO", lotSize: 2000, returns: { current: 0.75, near: 1.90, far: 2.90 } },
  
  // Industrial & Infra
  { symbol: "LT", lotSize: 500, returns: { current: 0.95, near: 2.35, far: 3.55 } },
  { symbol: "ULTRACEMCO", lotSize: 300, returns: { current: 1.10, near: 2.75, far: 4.05 } },
  { symbol: "GRASIM", lotSize: 400, returns: { current: 1.05, near: 2.65, far: 3.95 } },
  { symbol: "ADANIPORTS", lotSize: 900, returns: { current: 1.25, near: 3.05, far: 4.55 } },
  
  // Metals & Mining
  { symbol: "TATASTEEL", lotSize: 2000, returns: { current: 1.30, near: 3.10, far: 4.60 } },
  { symbol: "HINDALCO", lotSize: 1500, returns: { current: 1.15, near: 2.85, far: 4.25 } },
  { symbol: "JSWSTEEL", lotSize: 1200, returns: { current: 1.20, near: 2.95, far: 4.35 } },
  { symbol: "VEDL", lotSize: 2500, returns: { current: 1.10, near: 2.80, far: 4.20 } },
  
  // Other Sectors
  { symbol: "ASIANPAINT", lotSize: 300, returns: { current: 0.88, near: 2.18, far: 3.28 } },
  { symbol: "BAJFINANCE", lotSize: 125, returns: { current: 1.45, near: 3.25, far: 4.85 } },
  { symbol: "TITAN", lotSize: 300, returns: { current: 1.25, near: 2.95, far: 4.25 } },
  { symbol: "APOLLOHOSP", lotSize: 300, returns: { current: 1.35, near: 3.15, far: 4.75 } }
];

// Add some randomization to simulate live market data
function addRandomVariation(value: number): number {
  const variation = (Math.random() - 0.5) * 0.1; // ±0.05% variation
  return Math.max(0, value + variation);
}

export async function GET() {
  const currentTimestamp = new Date().toISOString();
  
  // Add slight random variations to simulate live data
  const liveData = mockMarketData.map(stock => ({
    ...stock,
    returns: {
      current: addRandomVariation(stock.returns.current),
      near: addRandomVariation(stock.returns.near), 
      far: addRandomVariation(stock.returns.far)
    },
    lastUpdated: currentTimestamp
  }));

  return NextResponse.json(liveData);
}
