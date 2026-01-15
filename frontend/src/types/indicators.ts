// インジケーター設定の型定義

export interface IndicatorSettings {
  // 移動平均線
  sma: {
    enabled: boolean;
    periods: number[];
    colors: string[];
  };
  ema: {
    enabled: boolean;
    periods: number[];
    colors: string[];
  };
  
  // オシレーター
  rsi: {
    enabled: boolean;
    period: number;
    overbought: number;
    oversold: number;
  };
  
  macd: {
    enabled: boolean;
    fastPeriod: number;
    slowPeriod: number;
    signalPeriod: number;
  };
  
  stochastic: {
    enabled: boolean;
    kPeriod: number;
    dPeriod: number;
    overbought: number;
    oversold: number;
  };
  
  // ボラティリティ
  bollingerBands: {
    enabled: boolean;
    period: number;
    stdDev: number;
  };
  
  atr: {
    enabled: boolean;
    period: number;
  };
  
  // 出来高
  volume: {
    enabled: boolean;
  };
  
  obv: {
    enabled: boolean;
  };
}

// デフォルト設定
export const defaultIndicatorSettings: IndicatorSettings = {
  sma: {
    enabled: true,
    periods: [20, 50, 200],
    colors: ['#2196F3', '#FF9800', '#9C27B0'],
  },
  ema: {
    enabled: false,
    periods: [12, 26],
    colors: ['#4CAF50', '#F44336'],
  },
  rsi: {
    enabled: true,
    period: 14,
    overbought: 70,
    oversold: 30,
  },
  macd: {
    enabled: true,
    fastPeriod: 12,
    slowPeriod: 26,
    signalPeriod: 9,
  },
  stochastic: {
    enabled: false,
    kPeriod: 14,
    dPeriod: 3,
    overbought: 80,
    oversold: 20,
  },
  bollingerBands: {
    enabled: true,
    period: 20,
    stdDev: 2,
  },
  atr: {
    enabled: false,
    period: 14,
  },
  volume: {
    enabled: true,
  },
  obv: {
    enabled: false,
  },
};

// ローカルストレージのキー
export const INDICATOR_SETTINGS_KEY = 'market_analysis_indicator_settings';

// 設定の保存
export const saveIndicatorSettings = (settings: IndicatorSettings): void => {
  try {
    localStorage.setItem(INDICATOR_SETTINGS_KEY, JSON.stringify(settings));
  } catch (error) {
    console.error('Failed to save indicator settings:', error);
  }
};

// 設定の読み込み
export const loadIndicatorSettings = (): IndicatorSettings => {
  try {
    const saved = localStorage.getItem(INDICATOR_SETTINGS_KEY);
    if (saved) {
      return { ...defaultIndicatorSettings, ...JSON.parse(saved) };
    }
  } catch (error) {
    console.error('Failed to load indicator settings:', error);
  }
  return defaultIndicatorSettings;
};
