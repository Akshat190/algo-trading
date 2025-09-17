import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { requestToken } = await req.json();

    if (!requestToken) {
      return NextResponse.json(
        { error: "Request token is required" },
        { status: 400 }
      );
    }

    // Note: The actual API might need different field names or structure
    // This is based on the error message suggesting missing credentials fields
    const res = await fetch("https://api.sharekhan.com/skapi/auth/token", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "X-API-KEY": process.env.SHAREKHAN_API_KEY || ""
      },
      body: JSON.stringify({
        apiKey: process.env.SHAREKHAN_API_KEY,
        secretKey: process.env.SHAREKHAN_SECRET_KEY, 
        requestToken: requestToken,
        // Additional fields that might be required
        clientId: process.env.SHAREKHAN_API_KEY,
        clientSecret: process.env.SHAREKHAN_SECRET_KEY
      })
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error("Sharekhan token API error:", res.status, errorText);
      return NextResponse.json(
        { 
          error: "Failed to exchange token", 
          details: errorText,
          status: res.status 
        },
        { status: res.status }
      );
    }

    const data = await res.json();
    
    // Validate the response contains expected tokens
    if (!data.accessToken) {
      console.error("Invalid response from Sharekhan:", data);
      return NextResponse.json(
        { error: "Invalid response from Sharekhan API" },
        { status: 500 }
      );
    }

    // Log successful authentication (without exposing tokens)
    console.log("Sharekhan token exchange successful");

    // Return the tokens - accessToken & refreshToken
    return NextResponse.json(data);

  } catch (error: any) {
    console.error("Sharekhan token route error:", error);
    return NextResponse.json(
      { 
        error: "Internal server error", 
        details: error.message 
      },
      { status: 500 }
    );
  }
}

// Optional: Add GET method to check if API keys are configured
export async function GET() {
  const hasApiKey = !!process.env.SHAREKHAN_API_KEY;
  const hasSecretKey = !!process.env.SHAREKHAN_SECRET_KEY;
  
  return NextResponse.json({
    configured: hasApiKey && hasSecretKey,
    apiKey: hasApiKey ? "configured" : "missing",
    secretKey: hasSecretKey ? "configured" : "missing"
  });
}
