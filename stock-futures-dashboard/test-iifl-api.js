const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

async function testIIFLAPI() {
  console.log('🧪 Testing IIFL/Sherkhan API Connection...');
  console.log('=========================================');
  
  const apiKey = process.env.SHERKHAN_API_KEY;
  const secretKey = process.env.SHERKHAN_SECRET_KEY;
  const baseURL = process.env.SHERKHAN_API_BASE;
  const authURL = process.env.SHERKHAN_AUTH_URL;
  
  console.log(`API Key: ${apiKey ? apiKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Secret Key: ${secretKey ? secretKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Base URL: ${baseURL}`);
  console.log(`Auth URL: ${authURL}`);
  console.log('');
  
  if (!apiKey || !secretKey) {
    console.log('❌ API credentials not found in .env.local');
    return;
  }
  
  // Test different possible API formats for Indian brokers
  const testEndpoints = [
    {
      name: 'IIFL TTBlaze Login',
      method: 'POST',
      url: `${authURL}`,
      data: {
        UserId: apiKey,
        Password: secretKey,
        LocalIP: '192.168.1.1',
        PublicIP: '49.36.71.206'
      },
      headers: {
        'Content-Type': 'application/json'
      }
    },
    {
      name: 'IIFL Market Data (Direct)',
      method: 'GET',
      url: `${baseURL}/marketfeed`,
      headers: {
        'Authorization': `Bearer ${apiKey}:${secretKey}`,
        'Content-Type': 'application/json'
      }
    },
    {
      name: 'Alternative: REST API with API Key',
      method: 'POST',
      url: `${baseURL}/api/login`,
      data: {
        apikey: apiKey,
        apisecret: secretKey
      },
      headers: {
        'Content-Type': 'application/json'
      }
    },
    {
      name: 'Check API Health',
      method: 'GET',
      url: `${baseURL}/health`,
      headers: {
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
        timeout: 10000
      };
      
      if (test.data) {
        config.data = test.data;
      }
      
      const response = await axios(config);
      
      console.log('✅ Success!');
      console.log('Status:', response.status);
      console.log('Response type:', typeof response.data);
      console.log('Response preview:', JSON.stringify(response.data, null, 2).substring(0, 500) + '...');
      console.log('');
      
    } catch (error) {
      console.log('❌ Failed');
      console.log('Error:', error.message);
      
      if (error.response) {
        console.log('Status:', error.response.status);
        console.log('Status Text:', error.response.statusText);
        console.log('Response preview:', JSON.stringify(error.response.data, null, 2).substring(0, 300));
      } else if (error.code === 'ENOTFOUND') {
        console.log('🌐 Domain not found - this endpoint doesn\'t exist');
      } else if (error.code === 'ECONNREFUSED') {
        console.log('🚫 Connection refused');
      }
      console.log('');
    }
  }
  
  console.log('📋 Summary:');
  console.log('If none of the endpoints worked, it could mean:');
  console.log('1. Your credentials are for a different API system');
  console.log('2. The API requires additional authentication steps');
  console.log('3. The credentials need to be activated/approved first');
  console.log('4. Different base URLs are needed');
  console.log('');
  console.log('💡 Next steps:');
  console.log('- Check your Sherkhan/IIFL developer portal for correct API URLs');
  console.log('- Verify your API access is activated');
  console.log('- Look for API documentation with example requests');
}

// Test the API
testIIFLAPI().then(() => {
  console.log('\n🏁 Test completed!');
}).catch(console.error);
