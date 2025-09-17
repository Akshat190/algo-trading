const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

async function testCorrectIIFLAPI() {
  console.log('🎯 Testing IIFL API with Correct Format...');
  console.log('==========================================');
  
  const apiKey = process.env.SHERKHAN_API_KEY;
  const secretKey = process.env.SHERKHAN_SECRET_KEY;
  const authURL = process.env.SHERKHAN_AUTH_URL;
  
  console.log(`API Key: ${apiKey ? apiKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Secret Key: ${secretKey ? secretKey.substring(0, 8) + '...' : 'NOT SET'}`);
  console.log(`Auth URL: ${authURL}`);
  console.log('');
  
  if (!apiKey || !secretKey) {
    console.log('❌ API credentials not found in .env.local');
    return;
  }
  
  // Test with the correct field names based on the error message
  const testCases = [
    {
      name: 'IIFL Login (with secretKey field)',
      method: 'POST',
      url: authURL,
      data: {
        UserId: apiKey,
        secretKey: secretKey,
        LocalIP: '192.168.1.1',
        PublicIP: '49.36.71.206'
      }
    },
    {
      name: 'IIFL Login (alternative format)',
      method: 'POST', 
      url: authURL,
      data: {
        apiKey: apiKey,
        secretKey: secretKey,
        source: 'API'
      }
    },
    {
      name: 'IIFL Login (minimal format)',
      method: 'POST',
      url: authURL,
      data: {
        secretKey: secretKey,
        userId: apiKey
      }
    }
  ];
  
  for (let i = 0; i < testCases.length; i++) {
    const test = testCases[i];
    console.log(`${i + 1}️⃣ Testing: ${test.name}`);
    console.log(`Data:`, JSON.stringify(test.data, null, 2));
    
    try {
      const response = await axios({
        method: test.method,
        url: test.url,
        data: test.data,
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });
      
      console.log('✅ SUCCESS!');
      console.log('Status:', response.status);
      console.log('Response:', JSON.stringify(response.data, null, 2));
      
      // If we got a successful login, try to get market data
      if (response.data && (response.data.token || response.data.access_token || response.data.sessionToken)) {
        console.log('');
        console.log('🎉 Login successful! Trying to fetch market data...');
        
        const token = response.data.token || response.data.access_token || response.data.sessionToken;
        
        try {
          const marketResponse = await axios.get('https://ttblaze.iifl.com/apimarketdata/instruments/master', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            timeout: 15000
          });
          
          console.log('✅ Market data fetch successful!');
          console.log('Market data sample:', JSON.stringify(marketResponse.data, null, 2).substring(0, 1000));
          
        } catch (marketError) {
          console.log('❌ Market data fetch failed:', marketError.message);
          if (marketError.response) {
            console.log('Market error details:', JSON.stringify(marketError.response.data, null, 2));
          }
        }
      }
      
    } catch (error) {
      console.log('❌ Failed');
      console.log('Error:', error.message);
      
      if (error.response) {
        console.log('Status:', error.response.status);
        console.log('Response:', JSON.stringify(error.response.data, null, 2));
        
        // Analyze the error for helpful information
        if (error.response.data && error.response.data.result && error.response.data.result.errors) {
          console.log('');
          console.log('🔍 Error Analysis:');
          error.response.data.result.errors.forEach(err => {
            console.log(`Field: ${err.field.join(', ')}`);
            console.log(`Messages: ${err.messages.join(', ')}`);
          });
        }
      }
    }
    
    console.log('');
  }
}

// Test the API
testCorrectIIFLAPI().then(() => {
  console.log('🏁 Test completed!');
  console.log('');
  console.log('📝 What we learned:');
  console.log('- The IIFL API server is responding');
  console.log('- It expects specific field names');
  console.log('- Your credentials might need a different format');
  console.log('');
  console.log('💡 If still not working, check:');
  console.log('- Your IIFL developer portal for exact API documentation');
  console.log('- Whether your API access needs to be activated');
  console.log('- If you need additional authentication parameters');
}).catch(console.error);
