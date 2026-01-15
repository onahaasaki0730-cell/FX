import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface MarketQuote {
  symbol: string;
  price: number;
  bid?: number;
  ask?: number;
  high?: number;
  low?: number;
  volume?: number;
  change?: number;
  change_percent?: number;
  timestamp: string;
}

export interface TechnicalIndicators {
  symbol: string;
  timeframe: string;
  timestamp: string;
  sma_20?: number;
  sma_50?: number;
  sma_200?: number;
  ema_12?: number;
  ema_26?: number;
  macd?: number;
  macd_signal?: number;
  macd_histogram?: number;
  rsi?: number;
  stoch_k?: number;
  stoch_d?: number;
  bb_upper?: number;
  bb_middle?: number;
  bb_lower?: number;
  atr?: number;
  obv?: number;
  vwap?: number;
}

export interface TrendAnalysis {
  timeframe: string;
  direction: 'bullish' | 'bearish' | 'sideways' | 'unknown';
  strength: number;
  support_levels: number[];
  resistance_levels: number[];
  description: string;
}

export interface TradingSignal {
  symbol: string;
  timeframe: string;
  signal: 'strong_buy' | 'buy' | 'neutral' | 'sell' | 'strong_sell';
  confidence: number;
  reasons: string[];
  entry_price?: number;
  stop_loss?: number;
  take_profit?: number;
  timestamp: string;
}

export interface NewsItem {
  id: string;
  title: string;
  description?: string;
  source: string;
  url?: string;
  published_at: string;
  impact: 'critical' | 'high' | 'medium' | 'low';
  sentiment: number;
  related_symbols: string[];
  tags: string[];
}

export interface EconomicEvent {
  id: string;
  title: string;
  country: string;
  currency: string;
  event_time: string;
  impact: 'critical' | 'high' | 'medium' | 'low';
  forecast?: string;
  previous?: string;
  actual?: string;
  description?: string;
}

export interface MultiTimeframeAnalysis {
  symbol: string;
  timestamp: string;
  current_price: number;
  analyses: Record<string, TrendAnalysis>;
  overall_trend: 'bullish' | 'bearish' | 'sideways' | 'unknown';
  consensus_signal: 'strong_buy' | 'buy' | 'neutral' | 'sell' | 'strong_sell';
  summary: string;
}

class MarketAPI {
  async getQuote(symbol: string): Promise<MarketQuote> {
    const response = await axios.get(`${API_BASE_URL}/market/quote/${symbol}`);
    return response.data;
  }

  async getIndicators(symbol: string, timeframe: string = '1h'): Promise<TechnicalIndicators> {
    const response = await axios.get(`${API_BASE_URL}/market/indicators/${symbol}`, {
      params: { timeframe }
    });
    return response.data;
  }

  async getTrend(symbol: string, timeframe: string = '1h'): Promise<TrendAnalysis> {
    const response = await axios.get(`${API_BASE_URL}/market/trend/${symbol}`, {
      params: { timeframe }
    });
    return response.data;
  }

  async getMultiTimeframeAnalysis(
    symbol: string,
    timeframes: string[] = ['15m', '1h', '4h', '1d']
  ): Promise<MultiTimeframeAnalysis> {
    const response = await axios.get(`${API_BASE_URL}/market/multi-timeframe/${symbol}`, {
      params: { timeframes }
    });
    return response.data;
  }

  async getTradingSignal(symbol: string, timeframe: string = '1h'): Promise<TradingSignal> {
    const response = await axios.get(`${API_BASE_URL}/signals/${symbol}`, {
      params: { timeframe }
    });
    return response.data;
  }

  async getNews(symbols?: string[], limit: number = 20): Promise<NewsItem[]> {
    const response = await axios.get(`${API_BASE_URL}/news/latest`, {
      params: { symbols, limit }
    });
    return response.data;
  }

  async getEconomicCalendar(): Promise<EconomicEvent[]> {
    const response = await axios.get(`${API_BASE_URL}/news/calendar`);
    return response.data;
  }
}

export const marketAPI = new MarketAPI();
