const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

async function testSherkhanAPI() {
  console.log('🧪 Testing Sherkhan API Connection...');
  console.log('=====================================');
  
  const apiKey = process.env.SHERKHAN_API_KEY;
  const secretKey = process.env.SHERKHAN_SECRET_KEY;
  const baseURL = process.env.SHERKHAN_API_BASE || 'https://api.sherkhan.com';
  
  console.log(`API Key: ${apiKey ? apiKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Secret Key: ${secretKey ? secretKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Base URL: ${baseURL}`);
  console.log('');
  
  if (!apiKey || !secretKey) {
    console.log('❌ API credentials not found in .env.local');
    return;
  }
  
  try {
    // Test 1: Try to login/authenticate
    console.log('1️⃣ Testing authentication...');
    const authResponse = await axios.post(`${baseURL}/auth/login`, {
      api_key: apiKey,
      api_secret: secretKey
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey
      },
      timeout: 10000
    });
    
    console.log('✅ Authentication successful!');
    console.log('Response:', JSON.stringify(authResponse.data, null, 2));
    
    // Test 2: Try to get market data with different auth methods
    console.log('');
    console.log('2️⃣ Testing market data fetch (with API key only)...');
    
    try {
      const marketResponse = await axios.get(`${baseURL}/api/v1/market/stocks`, {
        headers: {
          'X-API-Key': apiKey,
          'Content-Type': 'application/json'
        },
        params: {
          symbols: 'TCS,RELIANCE,HDFC,INFY'
        },
        timeout: 10000
      });
      
      console.log('✅ Market data fetch successful (API key only)!');
      console.log('Number of stocks received:', marketResponse.data.length || 'Unknown');
      console.log('Sample data:', JSON.stringify(marketResponse.data[0] || {}, null, 2));
    } catch (marketError) {
      console.log('❌ Market data fetch failed (API key only)');
      console.log('Market Error:', marketError.message);
      if (marketError.response) {
        console.log('Market Status:', marketError.response.status);
        console.log('Market Response:', JSON.stringify(marketError.response.data, null, 2));
      }
    }
    
    // Test 3: Try with access token if available
    if (authResponse.data.access_token) {
      console.log('');
      console.log('2️⃣ Testing market data fetch...');
      
      const marketResponse = await axios.get(`${baseURL}/api/v1/market/stocks`, {
        headers: {
          'Authorization': `Bearer ${authResponse.data.access_token}`,
          'X-API-Key': apiKey
        },
        params: {
          symbols: 'TCS,RELIANCE,HDFC,INFY'
        },
        timeout: 10000
      });
      
      console.log('✅ Market data fetch successful!');
      console.log('Number of stocks received:', marketResponse.data.length || 'Unknown');
      console.log('Sample data:', JSON.stringify(marketResponse.data[0] || {}, null, 2));
    }
    
  } catch (error) {
    console.log('❌ API Test Failed');
    console.log('Error:', error.message);
    
    if (error.response) {
      console.log('Status:', error.response.status);
      console.log('Response:', JSON.stringify(error.response.data, null, 2));
    } else if (error.code === 'ENOTFOUND') {
      console.log('🌐 Network Error: Cannot reach Sherkhan API servers');
      console.log('This could mean:');
      console.log('- The API base URL is incorrect');
      console.log('- Your internet connection has issues');
      console.log('- Sherkhan API servers are down');
    } else if (error.code === 'ECONNREFUSED') {
      console.log('🚫 Connection Refused: API server rejected the connection');
    }
  }
}

// Test the API
testSherkhanAPI().then(() => {
  console.log('\n🏁 Test completed!');
}).catch(console.error);
