const axios = require('axios');

async function testYahooAlternative() {
  console.log('🚀 Testing Alternative Yahoo Finance Endpoints...');
  console.log('==================================================');
  
  // Try multiple Yahoo Finance endpoints
  const endpoints = [
    // Chart endpoint (often more lenient)
    {
      name: 'Chart API',
      url: 'https://query1.finance.yahoo.com/v8/finance/chart/TCS.NS',
      params: {
        interval: '1d',
        range: '1d'
      }
    },
    // Different quotes endpoint
    {
      name: 'Quotes V6',
      url: 'https://query1.finance.yahoo.com/v6/finance/quote',
      params: {
        symbols: 'TCS.NS,RELIANCE.NS'
      }
    },
    // Summary endpoint
    {
      name: 'Summary',
      url: 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/TCS.NS',
      params: {
        modules: 'price,summaryDetail'
      }
    }
  ];

  for (const endpoint of endpoints) {
    console.log(`\n📡 Testing ${endpoint.name}...`);
    console.log(`URL: ${endpoint.url}`);
    
    try {
      const response = await axios.get(endpoint.url, {
        params: endpoint.params,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
          'Accept': 'application/json',
          'Accept-Language': 'en-US,en;q=0.9',
          'Referer': 'https://finance.yahoo.com/'
        },
        timeout: 15000
      });

      console.log(`✅ ${endpoint.name} - SUCCESS!`);
      console.log(`Status: ${response.status}`);
      
      if (response.data) {
        console.log('Response keys:', Object.keys(response.data));
        
        // Try to extract price data
        let priceData = null;
        
        if (response.data.chart?.result?.[0]?.meta) {
          const meta = response.data.chart.result[0].meta;
          priceData = {
            symbol: meta.symbol?.replace('.NS', ''),
            price: meta.regularMarketPrice,
            change: meta.regularMarketPrice - meta.previousClose,
            changePercent: ((meta.regularMarketPrice - meta.previousClose) / meta.previousClose) * 100,
            volume: meta.regularMarketVolume
          };
        } else if (response.data.quoteSummary?.result?.[0]) {
          const data = response.data.quoteSummary.result[0];
          const price = data.price;
          priceData = {
            symbol: price.symbol?.replace('.NS', ''),
            price: price.regularMarketPrice?.raw,
            change: price.regularMarketChange?.raw,
            changePercent: price.regularMarketChangePercent?.raw,
            volume: price.regularMarketVolume?.raw
          };
        } else if (response.data.quoteResponse?.result?.[0]) {
          const quote = response.data.quoteResponse.result[0];
          priceData = {
            symbol: quote.symbol?.replace('.NS', ''),
            price: quote.regularMarketPrice,
            change: quote.regularMarketChange,
            changePercent: quote.regularMarketChangePercent,
            volume: quote.regularMarketVolume
          };
        }
        
        if (priceData) {
          console.log('📊 Extracted price data:');
          console.log(`   ${priceData.symbol}: ₹${priceData.price?.toFixed(2) || 'N/A'}`);
          console.log(`   Change: ${priceData.change?.toFixed(2) || 'N/A'} (${priceData.changePercent?.toFixed(2) || 'N/A'}%)`);
          console.log(`   Volume: ${priceData.volume?.toLocaleString() || 'N/A'}`);
          
          if (priceData.price > 0) {
            console.log(`🎉 WORKING ENDPOINT FOUND: ${endpoint.name}!`);
            break;
          }
        } else {
          console.log('Sample data:', JSON.stringify(response.data).substring(0, 200) + '...');
        }
      }
      
    } catch (error) {
      console.log(`❌ ${endpoint.name} failed`);
      console.log(`Error: ${error.message}`);
      
      if (error.response) {
        console.log(`Status: ${error.response.status}`);
        if (error.response.data) {
          const errorMsg = JSON.stringify(error.response.data).substring(0, 200);
          console.log(`Response: ${errorMsg}...`);
        }
      }
    }
  }
  
  console.log('\n📋 Alternative Options:');
  console.log('1. Alpha Vantage (free tier: 5 API calls/min, 500/day)');
  console.log('2. Finnhub (free tier: 60 calls/min)');
  console.log('3. Polygon.io (free tier: 5 calls/min)');
  console.log('4. NSE unofficial endpoints (rate limited, no auth)');
  console.log('\n💡 If all Yahoo endpoints are blocked, we can switch to Alpha Vantage');
}

testYahooAlternative().then(() => {
  console.log('\n🏁 Alternative endpoint test completed!');
}).catch(console.error);
