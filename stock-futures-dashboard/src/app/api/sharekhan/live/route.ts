import { NextRequest, NextResponse } from "next/server";
import SharekhanTradingAPI from "../../../../lib/sharekhan-trading-api";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const symbols = searchParams.get('symbols')?.split(',');
    
    const sharekhan = new SharekhanTradingAPI();
    
    // Test connection first
    const connectionTest = await sharekhan.testConnection();
    
    if (connectionTest.status === 'error') {
      return NextResponse.json({
        error: "Failed to connect to Sharekhan API",
        details: connectionTest.message,
        debug: connectionTest
      }, { status: 503 });
    }

    // Get market data
    const marketData = await sharekhan.getMarketData(symbols);
    
    // Get futures data (optional)
    let futuresData = [];
    try {
      futuresData = await sharekhan.getFuturesData(symbols);
    } catch (error) {
      console.log("Futures data not available:", error.message);
    }

    // Convert to dashboard format
    const convertedData = sharekhan.convertToMarketData(marketData, futuresData);

    return NextResponse.json({
      success: true,
      data: convertedData,
      timestamp: new Date().toISOString(),
      source: "Sharekhan API",
      connectionStatus: connectionTest.status
    });

  } catch (error: any) {
    console.error("Live data API error:", error);
    
    return NextResponse.json({
      error: "Failed to fetch live data",
      details: error.message,
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { symbols, accessToken } = body;
    
    if (!accessToken) {
      return NextResponse.json(
        { error: "Access token is required for live data" },
        { status: 401 }
      );
    }

    // Use the provided access token to fetch live data from Sharekhan SKAPI
    const response = await fetch("https://api.sharekhan.com/skapi/services/live", {
      method: "GET", // Try GET first, POST might need different format
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`,
        "X-API-KEY": process.env.SHAREKHAN_API_KEY || ""
      },
      // For GET request, use query parameters instead of body
      ...(symbols && {
        // Add query parameters for GET request
        // Note: This might need to be adjusted based on actual API documentation
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Sharekhan live API error:", response.status, errorText);
      
      return NextResponse.json({
        error: "Failed to fetch live data from Sharekhan",
        status: response.status,
        details: errorText
      }, { status: response.status });
    }

    const data = await response.json();
    
    return NextResponse.json({
      success: true,
      data: data,
      timestamp: new Date().toISOString(),
      source: "Sharekhan Live API"
    });

  } catch (error: any) {
    console.error("Live data POST API error:", error);
    
    return NextResponse.json({
      error: "Failed to fetch live data",
      details: error.message,
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}
