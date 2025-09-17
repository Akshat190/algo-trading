const axios = require('axios');
require('dotenv').config({ path: '.env.local' });

async function testSharekhanIntegration() {
  console.log('🚀 Testing Sharekhan API Integration...\n');

  // Test 1: Check environment variables
  console.log('1. Checking environment variables:');
  const hasApiKey = !!process.env.SHAREKHAN_API_KEY;
  const hasSecretKey = !!process.env.SHAREKHAN_SECRET_KEY;
  
  console.log(`   API Key: ${hasApiKey ? '✅ Configured' : '❌ Missing'}`);
  console.log(`   Secret Key: ${hasSecretKey ? '✅ Configured' : '❌ Missing'}`);
  
  if (!hasApiKey || !hasSecretKey) {
    console.log('\n❌ Please configure your API keys in .env.local file');
    return;
  }

  // Test 2: Test token route configuration
  console.log('\n2. Testing token route configuration:');
  try {
    const response = await axios.get('http://localhost:3000/api/sharekhan/token');
    console.log(`   Token Route: ${response.data.configured ? '✅ Configured' : '❌ Not properly configured'}`);
    console.log(`   Details:`, response.data);
  } catch (error) {
    console.log('   ⚠️  Token route test failed - make sure Next.js dev server is running');
    console.log(`   Error: ${error.message}`);
  }

  // Test 3: Test direct API call to error endpoint (your example)
  console.log('\n3. Testing direct API call to Sharekhan:');
  try {
    const response = await axios.post('https://api.sharekhan.com/skapi/auth/token', {
      apiKey: process.env.SHAREKHAN_API_KEY,
      secureKey: process.env.SHAREKHAN_SECRET_KEY,
      requestToken: 'test_token' // This will likely fail but shows API structure
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 10000
    });
    console.log('   ✅ API call successful:', response.data);
  } catch (error) {
    if (error.response) {
      console.log(`   ⚠️  API responded with error ${error.response.status}: ${error.response.statusText}`);
      console.log(`   Response:`, error.response.data);
    } else if (error.code === 'ECONNABORTED') {
      console.log('   ⏱️  Request timeout - API might be slow or unreachable');
    } else {
      console.log(`   ❌ Network error: ${error.message}`);
    }
  }

  // Test 4: Test error endpoint you mentioned
  console.log('\n4. Testing error endpoint:');
  try {
    const response = await axios.get('https://api.sharekhan.com/skapi/services/error', {
      timeout: 10000
    });
    console.log('   ✅ Error endpoint response:', response.data);
  } catch (error) {
    if (error.response?.status === 403) {
      console.log('   🔒 Error endpoint requires authentication (403 Forbidden)');
      console.log('   This is expected - you need proper authentication to access live data');
    } else {
      console.log(`   ❌ Error endpoint failed: ${error.message}`);
    }
  }

  console.log('\n📋 Integration Test Summary:');
  console.log('1. Configure your API keys in .env.local');
  console.log('2. Start Next.js dev server: npm run dev');
  console.log('3. Test your authentication flow');
  console.log('4. Use the /api/sharekhan/token route to exchange tokens');
  console.log('5. Use the /api/sharekhan/live route to fetch live data');
}

// Run the test
testSharekhanIntegration().catch(error => {
  console.error('Test failed:', error.message);
});
