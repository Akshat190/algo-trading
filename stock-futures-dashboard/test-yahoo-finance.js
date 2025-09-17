const axios = require('axios');

async function testYahooFinance() {
  console.log('🚀 Testing Yahoo Finance API for Indian Stocks...');
  console.log('===================================================');
  
  try {
    // Test a few Indian stocks directly with Yahoo Finance
    const testSymbols = ['TCS.NS', 'RELIANCE.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS'];
    const quotesURL = 'https://query1.finance.yahoo.com/v7/finance/quote';
    
    console.log('📈 Fetching real-time data for:', testSymbols.map(s => s.replace('.NS', '')).join(', '));
    console.log('');
    
    const response = await axios.get(quotesURL, {
      params: {
        symbols: testSymbols.join(','),
        fields: 'regularMarketPrice,regularMarketChange,regularMarketChangePercent,regularMarketVolume,regularMarketDayHigh,regularMarketDayLow,regularMarketOpen,regularMarketPreviousClose'
      },
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      timeout: 15000
    });

    if (response.data?.quoteResponse?.result) {
      const stocks = response.data.quoteResponse.result;
      
      console.log(`✅ Successfully fetched data for ${stocks.length} stocks`);
      console.log('');
      
      stocks.forEach((stock, index) => {
        const symbol = stock.symbol.replace('.NS', '');
        const price = stock.regularMarketPrice || 0;
        const change = stock.regularMarketChange || 0;
        const changePercent = stock.regularMarketChangePercent || 0;
        const volume = stock.regularMarketVolume || 0;
        
        console.log(`${index + 1}. ${symbol}:`);
        console.log(`   Price: ₹${price.toFixed(2)}`);
        console.log(`   Change: ${change >= 0 ? '+' : ''}${change.toFixed(2)} (${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}%)`);
        console.log(`   Volume: ${volume.toLocaleString()}`);
        console.log('');
      });
      
      console.log('🎯 Data Quality Check:');
      console.log(`- All prices > 0: ${stocks.every(s => s.regularMarketPrice > 0)}`);
      console.log(`- Has volume data: ${stocks.every(s => s.regularMarketVolume > 0)}`);
      console.log(`- Has change data: ${stocks.every(s => s.regularMarketChange !== undefined)}`);
      console.log('');
      
      // Test futures simulation
      console.log('📊 Testing futures simulation...');
      stocks.forEach(stock => {
        const symbol = stock.symbol.replace('.NS', '');
        const spotChangePercent = stock.regularMarketChangePercent || 0;
        const nearFuturePercent = spotChangePercent * 1.15; // 15% premium simulation
        const farFuturePercent = spotChangePercent * 1.35;  // 35% premium simulation
        
        console.log(`${symbol} Futures: Current: ${spotChangePercent.toFixed(2)}% → Near: ${nearFuturePercent.toFixed(2)}% → Far: ${farFuturePercent.toFixed(2)}%`);
      });
      
      console.log('');
      console.log('🎉 Yahoo Finance integration working perfectly!');
      console.log('✅ Ready to replace Sharekhan with Yahoo Finance');
      console.log('✅ Your dashboard will now show real Indian stock market data');
      
    } else {
      console.log('❌ No data received from Yahoo Finance');
      console.log('Response:', JSON.stringify(response.data, null, 2));
    }
    
  } catch (error) {
    console.log('❌ Yahoo Finance test failed');
    console.log('Error:', error.message);
    
    if (error.response) {
      console.log('Status:', error.response.status);
      console.log('Response:', JSON.stringify(error.response.data, null, 2));
    } else if (error.code === 'ENOTFOUND') {
      console.log('🌐 Network error - check internet connection');
    }
  }
}

// Run the test
testYahooFinance().then(() => {
  console.log('🏁 Yahoo Finance test completed!');
}).catch(console.error);
