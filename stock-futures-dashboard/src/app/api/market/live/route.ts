import { NextResponse } from 'next/server';
import YahooFinanceAPI from '../../../../lib/yahoo-finance-api';
import { MarketData } from '../route';

export async function GET() {
  try {
    const yf = new YahooFinanceAPI();

    // Get popular Indian stocks
    const popularStocks = YahooFinanceAPI.getPopularStocks();

    // Fetch market and simulated futures data from Yahoo Finance
    const [stockData, futuresData] = await Promise.all([
      yf.getMarketData(popularStocks),
      yf.getFuturesData(popularStocks)
    ]);

    // Convert to your dashboard format
    const marketData: MarketData[] = yf.convertToMarketData(stockData, futuresData);

    console.log(`Successfully fetched ${marketData.length} stocks from Yahoo Finance`);
    return NextResponse.json(marketData);

  } catch (error) {
    console.error('Error fetching Yahoo Finance data:', error);

    // Fallback to mock data if API fails
    console.log('Yahoo Finance fetch failed, falling back to mock data');
    const { GET: getMockData } = await import('../route');
    return getMockData();
  }
}

// Test endpoint for Yahoo Finance connection
export async function POST(request: Request) {
  try {
    const yf = new YahooFinanceAPI();
    const body = await request.json();

    if (body.action === 'test-connection') {
      const testResult = await yf.testConnection();
      return NextResponse.json(testResult);
    }

    if (body.action === 'get-futures') {
      try {
        const popularStocks = YahooFinanceAPI.getPopularStocks().slice(0, 10);
        const futuresData = await yf.getFuturesData(popularStocks);
        return NextResponse.json({
          status: 'success',
          data: futuresData
        });
      } catch (error: any) {
        return NextResponse.json({
          status: 'error',
          error: 'Failed to fetch futures data',
          details: error.message
        });
      }
    }

    return NextResponse.json({ error: 'Invalid action' }, { status: 400 });

  } catch (error: any) {
    console.error('Yahoo Finance API error:', error);
    return NextResponse.json({
      error: 'API connection failed',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}
