const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

async function testNSEScannerAPI() {
  console.log('🔍 Testing NSE Arbitrage Scanner API...');
  console.log('====================================');
  
  const apiKey = process.env.SHERKHAN_API_KEY;
  const secretKey = process.env.SHERKHAN_SECRET_KEY;
  const baseURL = 'http://127.0.0.1:5000';
  
  console.log(`API Key: ${apiKey ? apiKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Secret Key: ${secretKey ? secretKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Base URL: ${baseURL}`);
  console.log('');
  
  if (!apiKey || !secretKey) {
    console.log('❌ API credentials not found in .env.local');
    return;
  }
  
  // Test different endpoints that might exist in NSE Scanner
  const testEndpoints = [
    {
      name: 'Health Check',
      method: 'GET',
      url: `${baseURL}/health`
    },
    {
      name: 'API Status',
      method: 'GET',
      url: `${baseURL}/api/status`
    },
    {
      name: 'Auth Callback (mentioned in your info)',
      method: 'GET',
      url: `${baseURL}/auth/callback`
    },
    {
      name: 'Login/Authentication',
      method: 'POST',
      url: `${baseURL}/auth/login`,
      data: {
        api_key: apiKey,
        secret_key: secretKey
      }
    },
    {
      name: 'Alternative Login Format',
      method: 'POST',
      url: `${baseURL}/api/login`,
      data: {
        apiKey: apiKey,
        secretKey: secretKey
      }
    },
    {
      name: 'Market Data',
      method: 'GET',
      url: `${baseURL}/api/market`
    },
    {
      name: 'NSE Data',
      method: 'GET',
      url: `${baseURL}/api/nse`
    },
    {
      name: 'Arbitrage Data',
      method: 'GET',
      url: `${baseURL}/api/arbitrage`
    },
    {
      name: 'Scanner Data',
      method: 'GET',
      url: `${baseURL}/api/scanner`
    },
    {
      name: 'Stocks List',
      method: 'GET',
      url: `${baseURL}/api/stocks`
    }
  ];
  
  console.log('🧪 Testing local NSE Scanner endpoints...');
  console.log('');
  
  for (let i = 0; i < testEndpoints.length; i++) {
    const test = testEndpoints[i];
    console.log(`${i + 1}️⃣ Testing: ${test.name}`);
    console.log(`URL: ${test.url}`);
    
    try {
      const config = {
        method: test.method,
        url: test.url,
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 5000 // Shorter timeout for local API
      };
      
      if (test.data) {
        config.data = test.data;
        console.log(`Data:`, JSON.stringify(test.data, null, 2));
      }
      
      const response = await axios(config);
      
      console.log('✅ SUCCESS!');
      console.log('Status:', response.status);
      console.log('Response type:', typeof response.data);
      
      if (typeof response.data === 'object') {
        console.log('Response:', JSON.stringify(response.data, null, 2));
      } else {
        console.log('Response preview:', String(response.data).substring(0, 500));
      }
      
      // If this looks like market data, let's analyze it
      if (Array.isArray(response.data) && response.data.length > 0) {
        console.log('📊 This looks like market data!');
        console.log('Number of records:', response.data.length);
        console.log('Sample record:', JSON.stringify(response.data[0], null, 2));
      }
      
    } catch (error) {
      console.log('❌ Failed');
      console.log('Error:', error.message);
      
      if (error.code === 'ECONNREFUSED') {
        console.log('🔴 Connection refused - NSE Scanner app is not running on localhost:5000');
      } else if (error.response) {
        console.log('Status:', error.response.status);
        console.log('Response:', JSON.stringify(error.response.data, null, 2));
      }
    }
    
    console.log('');
  }
}

// First, let's check if the NSE Scanner is running
async function checkNSEScannerStatus() {
  console.log('🔍 Checking if NSE Arbitrage Scanner is running...');
  
  try {
    const response = await axios.get('http://127.0.0.1:5000', { timeout: 2000 });
    console.log('✅ NSE Scanner is running!');
    return true;
  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      console.log('❌ NSE Scanner is NOT running on localhost:5000');
      console.log('');
      console.log('💡 To fix this:');
      console.log('1. Start your NSE Arbitrage Scanner application');
      console.log('2. Make sure it\'s running on port 5000');
      console.log('3. Then run this test again');
      return false;
    } else {
      console.log('⚠️ Unexpected error:', error.message);
      return false;
    }
  }
}

// Test the API
checkNSEScannerStatus().then(isRunning => {
  if (isRunning) {
    console.log('');
    return testNSEScannerAPI();
  }
}).then(() => {
  console.log('🏁 Test completed!');
}).catch(console.error);
