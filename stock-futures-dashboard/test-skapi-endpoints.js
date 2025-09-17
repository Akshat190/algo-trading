const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

async function testSKAPIEndpoints() {
  console.log('🔍 Testing Sharekhan SKAPI Endpoints...');
  console.log('=====================================');
  
  const apiKey = process.env.SHAREKHAN_API_KEY;
  const secretKey = process.env.SHAREKHAN_SECRET_KEY;
  const baseURL = 'https://api.sharekhan.com/skapi';
  
  console.log(`API Key: ${apiKey ? apiKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Secret Key: ${secretKey ? secretKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Base URL: ${baseURL}`);
  console.log('');

  if (!apiKey || !secretKey) {
    console.log('❌ API credentials not found');
    return;
  }

  // Test different authentication methods for SKAPI
  const testCases = [
    // Test 1: Check error endpoint (we know this exists)
    {
      name: 'Error Endpoint (Known Working)',
      method: 'GET',
      url: `${baseURL}/services/error`,
      headers: {
        'Content-Type': 'application/json'
      }
    },
    
    // Test 2: Try auth/token endpoint with different formats
    {
      name: 'Auth Token - Format 1 (apiKey/secureKey)',
      method: 'POST',
      url: `${baseURL}/auth/token`,
      data: {
        apiKey: apiKey,
        secureKey: secretKey,
        requestToken: 'test_request_token'
      },
      headers: {
        'Content-Type': 'application/json'
      }
    },

    // Test 3: Try with different field names
    {
      name: 'Auth Token - Format 2 (api_key/secret_key)',
      method: 'POST',
      url: `${baseURL}/auth/token`,
      data: {
        api_key: apiKey,
        secret_key: secretKey,
        request_token: 'test_request_token'
      },
      headers: {
        'Content-Type': 'application/json'
      }
    },

    // Test 4: Try with different field names
    {
      name: 'Auth Token - Format 3 (client_id/client_secret)',
      method: 'POST',
      url: `${baseURL}/auth/token`,
      data: {
        client_id: apiKey,
        client_secret: secretKey,
        request_token: 'test_request_token'
      },
      headers: {
        'Content-Type': 'application/json'
      }
    },

    // Test 5: Try login endpoint
    {
      name: 'Auth Login Endpoint',
      method: 'POST',
      url: `${baseURL}/auth/login`,
      data: {
        apiKey: apiKey,
        secretKey: secretKey
      },
      headers: {
        'Content-Type': 'application/json'
      }
    },

    // Test 6: Try with auth headers
    {
      name: 'With Auth Headers',
      method: 'GET',
      url: `${baseURL}/services/live`,
      headers: {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey,
        'Authorization': `Bearer ${secretKey}`
      }
    },

    // Test 7: Try market data endpoints
    {
      name: 'Market Data Endpoint',
      method: 'GET',
      url: `${baseURL}/services/market`,
      headers: {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey
      },
      params: {
        symbols: 'TCS,RELIANCE'
      }
    },

    // Test 8: Check if there's a user/profile endpoint
    {
      name: 'User Profile Endpoint',
      method: 'GET',
      url: `${baseURL}/user/profile`,
      headers: {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey,
        'Authorization': `Bearer ${secretKey}`
      }
    }
  ];

  for (let i = 0; i < testCases.length; i++) {
    const test = testCases[i];
    console.log(`${i + 1}️⃣ Testing: ${test.name}`);
    console.log(`URL: ${test.url}`);
    
    try {
      const config = {
        method: test.method,
        url: test.url,
        headers: test.headers,
        timeout: 10000
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
      console.log('Response Type:', typeof response.data);
      
      if (typeof response.data === 'object') {
        console.log('Response:', JSON.stringify(response.data, null, 2));
        
        // Check for token fields
        if (response.data.accessToken || response.data.access_token || response.data.token) {
          console.log('🎉 AUTHENTICATION TOKEN FOUND!');
        }
        
        // Check for market data
        if (Array.isArray(response.data) || (response.data.data && Array.isArray(response.data.data))) {
          console.log('📊 MARKET DATA FOUND!');
        }
      } else {
        console.log('Response Preview:', String(response.data).substring(0, 300));
      }

    } catch (error) {
      console.log('❌ Failed');
      console.log('Error:', error.message);
      
      if (error.response) {
        console.log('Status:', error.response.status);
        console.log('Status Text:', error.response.statusText);
        
        if (error.response.data && typeof error.response.data === 'object') {
          console.log('Error Response:', JSON.stringify(error.response.data, null, 2));
        } else if (error.response.data) {
          console.log('Error Response Preview:', String(error.response.data).substring(0, 200));
        }
        
        // Analyze status codes
        if (error.response.status === 401) {
          console.log('🔐 Authentication required - endpoint exists but needs valid credentials');
        } else if (error.response.status === 400) {
          console.log('❓ Bad request - endpoint exists but request format might be wrong');
        } else if (error.response.status === 403) {
          console.log('🛑 Forbidden - endpoint exists but access denied');
        } else if (error.response.status === 404) {
          console.log('🚫 Endpoint not found');
        }
      }
    }
    
    console.log('');
  }

  console.log('📋 Summary and Next Steps:');
  console.log('1. Look for ✅ SUCCESS responses above');
  console.log('2. 🎉 indicates authentication token found');
  console.log('3. 📊 indicates market data found');
  console.log('4. 🔐/🛑/❓ status codes indicate the endpoint exists but needs proper format');
  console.log('');
  console.log('💡 If you found working endpoints:');
  console.log('- Update your API routes to use the correct URL structure');
  console.log('- Use the correct field names for authentication');
  console.log('- Check Sharekhan documentation for the exact request format');
}

// Run the test
testSKAPIEndpoints().then(() => {
  console.log('🏁 SKAPI endpoint test completed!');
}).catch(console.error);
