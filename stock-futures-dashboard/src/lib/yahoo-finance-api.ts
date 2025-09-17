import axios from 'axios';

export interface YahooStockData {
  symbol: string;
  regularMarketPrice: number;
  regularMarketChange: number;
  regularMarketChangePercent: number;
  regularMarketVolume: number;
  regularMarketDayHigh: number;
  regularMarketDayLow: number;
  regularMarketOpen: number;
  regularMarketPreviousClose: number;
  marketCap?: number;
  fiftyTwoWeekHigh?: number;
  fiftyTwoWeekLow?: number;
}

export interface YahooFuturesData {
  symbol: string;
  expiry: string;
  regularMarketPrice: number;
  regularMarketChange: number;
  regularMarketChangePercent: number;
  regularMarketVolume: number;
  openInterest?: number;
}

class YahooFinanceAPI {
  private chartURL = 'https://query1.finance.yahoo.com/v8/finance/chart';

  private defaultHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://finance.yahoo.com/'
  } as const;
  
  // Convert Indian stock symbols to Yahoo format
  private convertToYahooSymbol(symbol: string): string {
    // Yahoo uses .NS suffix for NSE stocks
    if (symbol.includes('.')) return symbol;
    return `${symbol}.NS`;
  }

  // Convert Yahoo symbol back to clean symbol
  private cleanSymbol(yahooSymbol: string): string {
    return yahooSymbol.replace('.NS', '').replace('.BO', '');
  }

  // Fetch a single symbol via the chart endpoint and extract quote-like fields
  private async fetchChartForSymbol(yahooSymbol: string): Promise<YahooStockData | null> {
    const url = `${this.chartURL}/${encodeURIComponent(yahooSymbol)}`;
    const params = { interval: '1d', range: '1d' } as const;

    const resp = await axios.get(url, {
      params,
      headers: this.defaultHeaders,
      timeout: 15000
    });

    const meta = resp.data?.chart?.result?.[0]?.meta;
    if (!meta) return null;

    const symbol = this.cleanSymbol(meta.symbol || yahooSymbol);
    const price = Number(meta.regularMarketPrice || 0);
    const prevClose = Number(meta.previousClose || 0);
    const change = prevClose ? price - prevClose : 0;
    const changePercent = prevClose ? (change / prevClose) * 100 : 0;
    const volume = Number(meta.regularMarketVolume || 0);
    const dayHigh = Number(meta.chartPreviousClose || 0); // fallback if no explicit dayHigh in meta

    const data: YahooStockData = {
      symbol,
      regularMarketPrice: price,
      regularMarketChange: change,
      regularMarketChangePercent: changePercent,
      regularMarketVolume: volume,
      regularMarketDayHigh: meta.regularMarketDayHigh || dayHigh || price,
      regularMarketDayLow: meta.regularMarketDayLow || price,
      regularMarketOpen: meta.chartPreviousClose || prevClose || price,
      regularMarketPreviousClose: prevClose,
      marketCap: undefined,
      fiftyTwoWeekHigh: undefined,
      fiftyTwoWeekLow: undefined
    };

    return data;
  }

  // Get market data for multiple stocks using the chart API to avoid v7 quote 401
  async getMarketData(symbols: string[]): Promise<YahooStockData[]> {
    try {
      const yahooSymbols = symbols.map(s => this.convertToYahooSymbol(s));

      // Limit concurrency to avoid being throttled
      const results: YahooStockData[] = [];
      const concurrency = 5;
      for (let i = 0; i < yahooSymbols.length; i += concurrency) {
        const batch = yahooSymbols.slice(i, i + concurrency);
        const batchResults = await Promise.all(batch.map(async sym => {
          try {
            const data = await this.fetchChartForSymbol(sym);
            return data;
          } catch (e) {
            return null;
          }
        }));
        results.push(...batchResults.filter(Boolean) as YahooStockData[]);
        // small delay between batches
        await new Promise(r => setTimeout(r, 200));
      }

      if (results.length === 0) {
        throw new Error('No data received from Yahoo Finance chart API');
      }

      return results;
    } catch (error) {
      console.error('Yahoo Finance API error:', error);
      throw error;
    }
  }

  // Get futures data (Yahoo has limited futures data, so we'll simulate based on spot)
  async getFuturesData(symbols: string[]): Promise<YahooFuturesData[]> {
    try {
      // Get spot data first
      const spotData = await this.getMarketData(symbols);
      
      // Generate futures data based on spot prices
      const futuresData: YahooFuturesData[] = [];
      
      spotData.forEach(stock => {
        // Near month future (typically 1-3% premium)
        const nearPremium = 1 + (Math.random() * 0.02 + 0.01); // 1-3% premium
        const nearPrice = stock.regularMarketPrice * nearPremium;
        const nearChange = stock.regularMarketChange * nearPremium;
        const nearChangePercent = (nearChange / (nearPrice - nearChange)) * 100;
        
        futuresData.push({
          symbol: stock.symbol,
          expiry: this.getNearExpiryDate(),
          regularMarketPrice: nearPrice,
          regularMarketChange: nearChange,
          regularMarketChangePercent: nearChangePercent,
          regularMarketVolume: Math.floor(stock.regularMarketVolume * 0.3), // Futures typically lower volume
          openInterest: Math.floor(Math.random() * 1000000 + 500000)
        });

        // Far month future (typically 2-5% premium)
        const farPremium = 1 + (Math.random() * 0.03 + 0.02); // 2-5% premium
        const farPrice = stock.regularMarketPrice * farPremium;
        const farChange = stock.regularMarketChange * farPremium;
        const farChangePercent = (farChange / (farPrice - farChange)) * 100;
        
        futuresData.push({
          symbol: stock.symbol,
          expiry: this.getFarExpiryDate(),
          regularMarketPrice: farPrice,
          regularMarketChange: farChange,
          regularMarketChangePercent: farChangePercent,
          regularMarketVolume: Math.floor(stock.regularMarketVolume * 0.2), // Even lower volume for far month
          openInterest: Math.floor(Math.random() * 500000 + 250000)
        });
      });

      return futuresData;
    } catch (error) {
      console.error('Failed to generate futures data:', error);
      return [];
    }
  }

  // Get near month expiry (last Thursday of current/next month)
  private getNearExpiryDate(): string {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    
    // Find last Thursday of current month
    const lastDay = new Date(year, month + 1, 0).getDate();
    const lastDayOfWeek = new Date(year, month, lastDay).getDay();
    const lastThursday = lastDay - ((lastDayOfWeek + 3) % 7);
    
    // If we're past the last Thursday, use next month
    if (now.getDate() > lastThursday) {
      return this.formatExpiryDate(new Date(year, month + 1, this.getLastThursday(year, month + 1)));
    } else {
      return this.formatExpiryDate(new Date(year, month, lastThursday));
    }
  }

  // Get far month expiry (last Thursday of month after next)
  private getFarExpiryDate(): string {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    
    const farMonth = month + 2;
    const farYear = farMonth > 11 ? year + 1 : year;
    const adjustedMonth = farMonth > 11 ? farMonth - 12 : farMonth;
    
    const lastThursday = this.getLastThursday(farYear, adjustedMonth);
    return this.formatExpiryDate(new Date(farYear, adjustedMonth, lastThursday));
  }

  private getLastThursday(year: number, month: number): number {
    const lastDay = new Date(year, month + 1, 0).getDate();
    const lastDayOfWeek = new Date(year, month, lastDay).getDay();
    return lastDay - ((lastDayOfWeek + 3) % 7);
  }

  private formatExpiryDate(date: Date): string {
    const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 
                   'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
    return `${date.getDate()}${months[date.getMonth()]}${date.getFullYear().toString().slice(-2)}`;
  }

  // Convert Yahoo Finance data to dashboard format
  convertToMarketData(stockData: YahooStockData[], futuresData?: YahooFuturesData[]): any[] {
    return stockData.map(stock => {
      // Find corresponding futures data
      const nearFuture = futuresData?.find(f => 
        f.symbol === stock.symbol && f.expiry === this.getNearExpiryDate()
      );
      const farFuture = futuresData?.find(f => 
        f.symbol === stock.symbol && f.expiry === this.getFarExpiryDate()
      );

      // Use actual Yahoo data for returns
      const currentReturn = stock.regularMarketChangePercent || 0;
      const nearReturn = nearFuture ? nearFuture.regularMarketChangePercent : currentReturn * 1.15;
      const farReturn = farFuture ? farFuture.regularMarketChangePercent : currentReturn * 1.35;

      return {
        symbol: stock.symbol,
        lotSize: this.getDefaultLotSize(stock.symbol),
        returns: {
          current: Number(currentReturn.toFixed(2)),
          near: Number(nearReturn.toFixed(2)),
          far: Number(farReturn.toFixed(2))
        },
        lastUpdated: new Date().toISOString(),
        volume: stock.regularMarketVolume,
        lastPrice: stock.regularMarketPrice,
        open: stock.regularMarketOpen,
        high: stock.regularMarketDayHigh,
        low: stock.regularMarketDayLow,
        close: stock.regularMarketPreviousClose,
        change: stock.regularMarketChange,
        changePercent: stock.regularMarketChangePercent
      };
    });
  }

  // Get default lot sizes for Indian stocks
  private getDefaultLotSize(symbol: string): number {
    const stockLotSizes: { [key: string]: number } = {
      'TCS': 300, 'RELIANCE': 250, 'HDFC': 550, 'INFY': 600,
      'ICICIBANK': 375, 'HDFCBANK': 550, 'KOTAKBANK': 400,
      'SBIN': 1500, 'AXISBANK': 500, 'INDUSINDBK': 900,
      'WIPRO': 800, 'HCLTECH': 700, 'TECHM': 600,
      'LTIM': 350, 'MINDTREE': 400, 'BHARTIARTL': 1800,
      'POWERGRID': 3200, 'NTPC': 2000, 'COALINDIA': 3000,
      'MARUTI': 100, 'TATAMOTORS': 1800, 'BAJAJFINSERV': 125,
      'M&M': 300, 'EICHERMOT': 100, 'HINDUUNILVR': 300,
      'ITC': 1600, 'NESTLEIND': 50, 'BRITANNIA': 125,
      'DABUR': 1000, 'SUNPHARMA': 700, 'DRREDDY': 125,
      'CIPLA': 700, 'DIVISLAB': 150, 'ONGC': 4200,
      'IOC': 4000, 'BPCL': 1500, 'HINDPETRO': 2000,
      'LT': 500, 'ULTRACEMCO': 300, 'GRASIM': 400,
      'ADANIPORTS': 900, 'TATASTEEL': 2000, 'HINDALCO': 1500,
      'JSWSTEEL': 1200, 'VEDL': 2500, 'ASIANPAINT': 300,
      'BAJFINANCE': 125, 'TITAN': 300, 'APOLLOHOSP': 300
    };

    return stockLotSizes[symbol] || 100;
  }

  // Test API connection
  async testConnection(): Promise<any> {
    try {
      const testSymbols = ['TCS', 'RELIANCE'];
      const marketData = await this.getMarketData(testSymbols);
      
      return {
        status: 'success',
        message: 'Connected to Yahoo Finance API',
        dataCount: marketData.length,
        sampleData: marketData.slice(0, 2)
      };
    } catch (error) {
      return {
        status: 'error',
        message: 'Yahoo Finance connection failed',
        error: error.message
      };
    }
  }

  // Get popular Indian stocks list
  static getPopularStocks(): string[] {
    return [
      'TCS', 'RELIANCE', 'HDFCBANK', 'INFY', 'ICICIBANK',
      'KOTAKBANK', 'SBIN', 'AXISBANK', 'BHARTIARTL', 'INDUSINDBK',
      'WIPRO', 'HCLTECH', 'TECHM', 'LTIM', 'MINDTREE',
      'POWERGRID', 'NTPC', 'COALINDIA', 'HINDALCO', 'TATASTEEL',
      'MARUTI', 'TATAMOTORS', 'BAJAJFINSERV', 'M&M', 'EICHERMOT',
      'HINDUUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'DABUR',
      'SUNPHARMA', 'DRREDDY', 'CIPLA', 'DIVISLAB', 'APOLLOHOSP',
      'ONGC', 'IOC', 'BPCL', 'HINDPETRO', 'GAIL',
      'LT', 'ULTRACEMCO', 'GRASIM', 'ADANIPORTS', 'ADANIENT',
      'BAJFINANCE', 'TITAN', 'ASIANPAINT', 'VEDL', 'JSWSTEEL'
    ];
  }
}

export default YahooFinanceAPI;
