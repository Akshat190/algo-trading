const axios = require('axios');
const crypto = require('crypto');
require('dotenv').config({ path: '.env.local' });

async function testSharekhanAPI() {
  console.log('🔍 Testing Direct Sharekhan API Connection...');
  console.log('===============================================');
  
  const apiKey = process.env.SHAREKHAN_API_KEY;
  const secretKey = process.env.SHAREKHAN_SECRET_KEY;
  const baseURL = process.env.SHAREKHAN_API_BASE;
  
  console.log(`API Key: ${apiKey ? apiKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Secret Key: ${secretKey ? secretKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Base URL: ${baseURL}`);
  console.log('');

  if (!apiKey || !secretKey) {
    console.log('❌ API credentials not found');
    return;
  }

  // Test different possible Sharekhan API endpoints and authentication methods
  const testEndpoints = [
    // Test 1: Check if API base URL exists
    {
      name: 'API Health Check',
      method: 'GET',
      url: `${baseURL}/health`,
      headers: {
        'User-Agent': 'SharekhanAPI/1.0'
      }
    },
    // Test 2: Try login with API key/secret
    {
      name: 'Direct API Key Login',
      method: 'POST',
      url: `${baseURL}/api/v1/login`,
      data: {
        apiKey: apiKey,
        secretKey: secretKey
      },
      headers: {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey
      }
    },
    // Test 3: Try alternative login endpoint
    {
      name: 'Alternative Login Endpoint',
      method: 'POST',
      url: `${baseURL}/login`,
      data: {
        api_key: apiKey,
        api_secret: secretKey
      },
      headers: {
        'Content-Type': 'application/json'
      }
    },
    // Test 4: Try with authentication header
    {
      name: 'Auth Header Method',
      method: 'GET',
      url: `${baseURL}/api/v1/user/profile`,
      headers: {
        'Authorization': `Bearer ${apiKey}:${secretKey}`,
        'X-API-KEY': apiKey,
        'Content-Type': 'application/json'
      }
    },
    // Test 5: Try market data directly
    {
      name: 'Direct Market Data',
      method: 'GET',
      url: `${baseURL}/api/v1/market/quotes`,
      params: {
        symbols: 'TCS,RELIANCE'
      },
      headers: {
        'X-API-KEY': apiKey,
        'Authorization': `Bearer ${secretKey}`,
        'Content-Type': 'application/json'
      }
    }
  ];

  for (let i = 0; i < testEndpoints.length; i++) {
    const test = testEndpoints[i];
    console.log(`${i + 1}️⃣ Testing: ${test.name}`);
    console.log(`URL: ${test.url}`);
    
    try {
      const config = {
        method: test.method,
        url: test.url,
        headers: test.headers,
        timeout: 15000
      };

      if (test.data) {
        config.data = test.data;
        console.log(`Data:`, JSON.stringify(test.data, null, 2));
      }

      if (test.params) {
        config.params = test.params;
        console.log(`Params:`, JSON.stringify(test.params, null, 2));
      }

      const response = await axios(config);
      
      console.log('✅ SUCCESS!');
      console.log('Status:', response.status);
      console.log('Response Headers:', Object.keys(response.headers));
      console.log('Response Type:', typeof response.data);
      
      if (typeof response.data === 'object') {
        console.log('Response:', JSON.stringify(response.data, null, 2));
      } else {
        console.log('Response Preview:', String(response.data).substring(0, 500));
      }

      // If this looks like authentication success
      if (response.data && (response.data.token || response.data.access_token || response.data.jwtToken)) {
        console.log('🎉 Found authentication token!');
        console.log('Token type:', response.data.token ? 'token' : response.data.access_token ? 'access_token' : 'jwtToken');
      }

      // If this looks like market data
      if (Array.isArray(response.data) || (response.data && response.data.data && Array.isArray(response.data.data))) {
        console.log('📊 Found market data!');
      }

    } catch (error) {
      console.log('❌ Failed');
      console.log('Error:', error.message);
      
      if (error.response) {
        console.log('Status:', error.response.status);
        console.log('Status Text:', error.response.statusText);
        console.log('Response Headers:', Object.keys(error.response.headers || {}));
        console.log('Error Response:', JSON.stringify(error.response.data, null, 2));
        
        // Analyze common error patterns
        if (error.response.status === 401) {
          console.log('🔐 Authentication required - credentials might be invalid or endpoint needs different auth method');
        } else if (error.response.status === 404) {
          console.log('🚫 Endpoint not found - URL might be incorrect');
        } else if (error.response.status === 403) {
          console.log('🛑 Forbidden - might need different permissions or API approval');
        }
      } else if (error.code === 'ENOTFOUND') {
        console.log('🌐 DNS resolution failed - API base URL might be incorrect');
      }
    }
    
    console.log('');
  }

  console.log('📋 Summary and Next Steps:');
  console.log('1. Check if any endpoint returned success');
  console.log('2. If no success, the API base URL or authentication method might be different');
  console.log('3. Check Sharekhan API documentation for correct endpoints');
  console.log('4. Your credentials might need to be activated in Sharekhan dashboard');
  console.log('');
  console.log('💡 Common Sharekhan API endpoints to check:');
  console.log('- Login: POST /api/v1/auth/login or POST /login');
  console.log('- Market Data: GET /api/v1/market/quotes or GET /quotes');
  console.log('- User Profile: GET /api/v1/user/profile');
}

// Run the test
testSharekhanAPI().then(() => {
  console.log('🏁 Direct API test completed!');
}).catch(console.error);
