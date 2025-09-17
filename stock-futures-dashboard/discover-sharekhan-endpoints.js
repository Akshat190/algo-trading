const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

async function discoverSharekhanEndpoints() {
  console.log('🔍 Discovering Sharekhan API Endpoints...');
  console.log('==========================================');
  
  const apiKey = process.env.SHAREKHAN_API_KEY;
  const secretKey = process.env.SHAREKHAN_SECRET_KEY;
  
  console.log(`API Key: ${apiKey ? apiKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Secret Key: ${secretKey ? secretKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log('');

  if (!apiKey || !secretKey) {
    console.log('❌ API credentials not found');
    return;
  }

  // Common broker API base URLs to test
  const possibleBaseUrls = [
    'https://api.sharekhan.com',
    'https://apiconnect.sharekhan.com',
    'https://connect.sharekhan.com',
    'https://tradeapi.sharekhan.com',
    'https://developer.sharekhan.com',
    'https://openapi.sharekhan.com',
    'https://api-connect.sharekhan.com',
    'https://trading-api.sharekhan.com',
    'https://sandbox.sharekhan.com',
    'https://test-api.sharekhan.com',
    'https://beta.api.sharekhan.com',
    'https://gateway.sharekhan.com'
  ];

  // Test each base URL
  for (const baseUrl of possibleBaseUrls) {
    console.log(`🌐 Testing Base URL: ${baseUrl}`);
    
    // Test common endpoints for this base URL
    const testEndpoints = [
      // Health/Status checks
      { path: '/health', method: 'GET' },
      { path: '/status', method: 'GET' },
      { path: '/api/health', method: 'GET' },
      
      // Authentication endpoints
      { path: '/auth/login', method: 'POST' },
      { path: '/api/auth/login', method: 'POST' },
      { path: '/api/v1/login', method: 'POST' },
      { path: '/login', method: 'POST' },
      { path: '/oauth/token', method: 'POST' },
      
      // Market data endpoints (GET only for discovery)
      { path: '/api/market/quotes', method: 'GET' },
      { path: '/api/v1/market/quotes', method: 'GET' },
      { path: '/market/quotes', method: 'GET' },
      { path: '/quotes', method: 'GET' },
      { path: '/api/marketdata', method: 'GET' },
      
      // User profile endpoints
      { path: '/api/user/profile', method: 'GET' },
      { path: '/api/v1/user/profile', method: 'GET' },
      { path: '/profile', method: 'GET' }
    ];

    let foundWorking = false;

    for (const endpoint of testEndpoints) {
      try {
        const config = {
          method: endpoint.method,
          url: `${baseUrl}${endpoint.path}`,
          headers: {
            'Content-Type': 'application/json',
            'X-API-KEY': apiKey,
            'User-Agent': 'NSE-Arbitrage-Scanner/1.0'
          },
          timeout: 8000
        };

        // Add auth data for POST requests
        if (endpoint.method === 'POST') {
          config.data = {
            api_key: apiKey,
            api_secret: secretKey
          };
        }

        // Add common query params for market data
        if (endpoint.path.includes('quotes') || endpoint.path.includes('market')) {
          config.params = {
            symbols: 'TCS,RELIANCE'
          };
        }

        const response = await axios(config);
        
        console.log(`  ✅ ${endpoint.method} ${endpoint.path} - Status: ${response.status}`);
        console.log(`     Response type: ${typeof response.data}`);
        
        if (response.data) {
          if (typeof response.data === 'object') {
            console.log(`     Keys: [${Object.keys(response.data).join(', ')}]`);
            
            // Check for authentication success indicators
            if (response.data.access_token || response.data.token || response.data.jwtToken) {
              console.log(`     🎉 AUTHENTICATION TOKEN FOUND!`);
              foundWorking = true;
            }
            
            // Check for market data indicators
            if (Array.isArray(response.data) || 
                (response.data.data && Array.isArray(response.data.data))) {
              console.log(`     📊 MARKET DATA FOUND!`);
              foundWorking = true;
            }
          } else {
            const preview = String(response.data).substring(0, 100);
            console.log(`     Preview: ${preview}...`);
          }
        }

      } catch (error) {
        const status = error.response?.status;
        
        // Only log interesting errors (not 404s)
        if (status && status !== 404) {
          console.log(`  ⚠️  ${endpoint.method} ${endpoint.path} - Status: ${status}`);
          
          if (status === 401) {
            console.log(`     🔐 Authentication required - this endpoint exists!`);
            foundWorking = true;
          } else if (status === 403) {
            console.log(`     🛑 Forbidden - endpoint exists but needs different auth`);
            foundWorking = true;
          } else if (status === 400) {
            console.log(`     ❓ Bad request - endpoint exists but wrong params`);
            foundWorking = true;
          }
          
          if (error.response?.data) {
            console.log(`     Error: ${JSON.stringify(error.response.data).substring(0, 100)}`);
          }
        }
      }
    }

    if (foundWorking) {
      console.log(`🎯 FOUND WORKING BASE URL: ${baseUrl}`);
      console.log('');
    }

    // Small delay between base URLs
    await new Promise(resolve => setTimeout(resolve, 500));
  }

  console.log('');
  console.log('📋 Discovery Summary:');
  console.log('1. Look for ✅ or ⚠️ marks above - those are working endpoints');
  console.log('2. 🎉 means authentication endpoint found');
  console.log('3. 📊 means market data endpoint found');
  console.log('4. 🔐/🛑 means endpoint exists but needs proper auth');
  console.log('');
  console.log('💡 Next Steps:');
  console.log('- If you found working endpoints, update your .env.local with the correct base URL');
  console.log('- If no endpoints work, check your Sharekhan developer dashboard for the actual API documentation');
  console.log('- The API might be sandbox-only or require OAuth flow first');
}

// Run discovery
discoverSharekhanEndpoints().then(() => {
  console.log('🏁 Endpoint discovery completed!');
}).catch(console.error);
