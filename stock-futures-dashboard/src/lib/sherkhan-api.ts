import crypto from 'crypto';
import axios from 'axios';

export interface SherkhanStockData {
  symbol: string;
  ltp: number; // Last Traded Price
  change: number;
  changePercent: number;
  volume: number;
  lotSize: number;
  open: number;
  high: number;
  low: number;
  close: number;
}

export interface SherkhanFuturesData {
  symbol: string;
  expiry: string;
  ltp: number;
  change: number;
  changePercent: number;
  oi: number; // Open Interest
  volume: number;
  lotSize: number;
}

export interface SherkhanLoginResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

class SherkhanAPI {
  private apiKey: string;
  private secretKey: string;
  private baseURL: string;
  private accessToken: string | null = null;

  constructor() {
    this.apiKey = process.env.SHERKHAN_API_KEY || '';
    this.secretKey = process.env.SHERKHAN_SECRET_KEY || '';
    this.baseURL = process.env.SHERKHAN_API_BASE || 'https://api.sherkhan.com';
  }

  // Generate authentication headers
  private getHeaders(includeAuth = true) {
    const headers: any = {
      'Content-Type': 'application/json',
      'X-API-Key': this.apiKey,
    };

    if (includeAuth && this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    return headers;
  }

  // Login to get access token
  async login() {
    try {
      const response = await axios.post(
        `${this.baseURL}/auth/login`,
        {
          api_key: this.apiKey,
          api_secret: this.secretKey,
        },
        {
          headers: this.getHeaders(false)
        }
      );

      this.accessToken = response.data.access_token;
      return response.data;
    } catch (error) {
      console.error('Sherkhan login error:', error);
      throw error;
    }
  }

  // Get market data for stocks
  async getStockData(symbols?: string[]) {
    try {
      if (!this.accessToken) {
        await this.login();
      }

      const url = `${this.baseURL}/api/v1/market/stocks`;
      const params = symbols ? { symbols: symbols.join(',') } : {};

      const response = await axios.get(url, {
        headers: this.getHeaders(),
        params
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching stock data:', error);
      throw error;
    }
  }

  // Get futures data
  async getFuturesData(symbols?: string[]) {
    try {
      if (!this.accessToken) {
        await this.login();
      }

      const url = `${this.baseURL}/api/v1/market/futures`;
      const params = symbols ? { symbols: symbols.join(',') } : {};

      const response = await axios.get(url, {
        headers: this.getHeaders(),
        params
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching futures data:', error);
      throw error;
    }
  }

  // Get account information
  async getAccountInfo() {
    try {
      if (!this.accessToken) {
        await this.login();
      }

      const response = await axios.get(`${this.baseURL}/api/v1/account`, {
        headers: this.getHeaders()
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching account info:', error);
      throw error;
    }
  }

  // Get positions
  async getPositions() {
    try {
      if (!this.accessToken) {
        await this.login();
      }

      const response = await axios.get(`${this.baseURL}/api/v1/positions`, {
        headers: this.getHeaders()
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching positions:', error);
      throw error;
    }
  }

  // Convert Sherkhan data to your dashboard format
  convertToMarketData(stockData: SherkhanStockData[], futuresData?: SherkhanFuturesData[]) {
    return stockData.map(stock => {
      // Find corresponding futures data
      const nearFuture = futuresData?.find(f => 
        f.symbol === stock.symbol && f.expiry.includes('near')
      );
      const farFuture = futuresData?.find(f => 
        f.symbol === stock.symbol && f.expiry.includes('far')
      );

      // Calculate returns
      const currentReturn = stock.changePercent;
      const nearReturn = nearFuture ? nearFuture.changePercent : currentReturn * 1.2;
      const farReturn = farFuture ? farFuture.changePercent : currentReturn * 1.5;

      return {
        symbol: stock.symbol,
        lotSize: stock.lotSize || this.getDefaultLotSize(stock.symbol),
        returns: {
          current: currentReturn,
          near: nearReturn,
          far: farReturn
        },
        lastUpdated: new Date().toISOString(),
        volume: stock.volume,
        lastPrice: stock.ltp,
        open: stock.open,
        high: stock.high,
        low: stock.low,
        close: stock.close
      };
    });
  }

  // Get default lot sizes for Indian stocks
  private getDefaultLotSize(symbol: string): number {
    const stockLotSizes: { [key: string]: number } = {
      'TCS': 300,
      'RELIANCE': 250,
      'HDFC': 550,
      'INFY': 600,
      'ICICIBANK': 375,
      'HDFCBANK': 550,
      'KOTAKBANK': 400,
      'SBIN': 1500,
      'AXISBANK': 500,
      'INDUSINDBK': 900,
      'WIPRO': 800,
      'HCLTECH': 700,
      'TECHM': 600,
      'LTIM': 350,
      'MINDTREE': 400,
      'BHARTIARTL': 1800,
      'POWERGRID': 3200,
      'NTPC': 2000,
      'COALINDIA': 3000,
      'MARUTI': 100,
      'TATAMOTORS': 1800,
      'BAJAJFINSERV': 125,
      'M&M': 300,
      'EICHERMOT': 100,
      'HINDUUNILVR': 300,
      'ITC': 1600,
      'NESTLEIND': 50,
      'BRITANNIA': 125,
      'DABUR': 1000,
      'SUNPHARMA': 700,
      'DRREDDY': 125,
      'CIPLA': 700,
      'DIVISLAB': 150,
      'ONGC': 4200,
      'IOC': 4000,
      'BPCL': 1500,
      'HINDPETRO': 2000,
      'LT': 500,
      'ULTRACEMCO': 300,
      'GRASIM': 400,
      'ADANIPORTS': 900,
      'TATASTEEL': 2000,
      'HINDALCO': 1500,
      'JSWSTEEL': 1200,
      'VEDL': 2500,
      'ASIANPAINT': 300,
      'BAJFINANCE': 125,
      'TITAN': 300,
      'APOLLOHOSP': 300
    };

    return stockLotSizes[symbol] || 100;
  }

  // Get popular Indian stocks symbols
  static getPopularStocks(): string[] {
    return [
      'TCS', 'RELIANCE', 'HDFC', 'INFY', 'ICICIBANK',
      'HDFCBANK', 'KOTAKBANK', 'SBIN', 'AXISBANK', 'INDUSINDBK',
      'WIPRO', 'HCLTECH', 'TECHM', 'LTIM', 'MINDTREE',
      'BHARTIARTL', 'POWERGRID', 'NTPC', 'COALINDIA',
      'MARUTI', 'TATAMOTORS', 'BAJAJFINSERV', 'M&M', 'EICHERMOT',
      'HINDUUNILVR', 'ITC', 'NESTLEIND', 'BRITANNIA', 'DABUR',
      'SUNPHARMA', 'DRREDDY', 'CIPLA', 'DIVISLAB',
      'ONGC', 'IOC', 'BPCL', 'HINDPETRO',
      'LT', 'ULTRACEMCO', 'GRASIM', 'ADANIPORTS',
      'TATASTEEL', 'HINDALCO', 'JSWSTEEL', 'VEDL',
      'ASIANPAINT', 'BAJFINANCE', 'TITAN', 'APOLLOHOSP'
    ];
  }
}

export default SherkhanAPI;
