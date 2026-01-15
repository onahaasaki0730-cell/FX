import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pandas_ta as ta

from ..models.market import (
    OHLCV, MarketQuote, TimeFrame, TrendDirection, 
    TrendAnalysis, TechnicalIndicators
)


class MarketDataService:
    """市場データ取得サービス"""
    
    # Yahoo Financeの時間足マッピング
    TIMEFRAME_MAPPING = {
        TimeFrame.M1: "1m",
        TimeFrame.M5: "5m",
        TimeFrame.M15: "15m",
        TimeFrame.M30: "30m",
        TimeFrame.M45: "1h",  # 45mは直接サポートされていないため1hで代用
        TimeFrame.H1: "1h",
        TimeFrame.H4: "4h",
        TimeFrame.D1: "1d",
        TimeFrame.W1: "1wk",
        TimeFrame.MN1: "1mo",
    }
    
    # 期間マッピング
    PERIOD_MAPPING = {
        TimeFrame.M1: "1d",
        TimeFrame.M5: "5d",
        TimeFrame.M15: "5d",
        TimeFrame.M30: "1mo",
        TimeFrame.M45: "1mo",  # 45mは1hデータを使用するため
        TimeFrame.H1: "1mo",
        TimeFrame.H4: "3mo",
        TimeFrame.D1: "1y",
        TimeFrame.W1: "2y",
        TimeFrame.MN1: "5y",
    }
    
    def __init__(self):
        self.cache: Dict[str, Any] = {}
    
    async def get_quote(self, symbol: str) -> MarketQuote:
        """リアルタイム価格を取得"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            history = ticker.history(period="1d", interval="1m")
            
            if history.empty:
                raise ValueError(f"No data available for {symbol}")
            
            latest = history.iloc[-1]
            previous_close = info.get('previousClose', latest['Close'])
            
            quote = MarketQuote(
                symbol=symbol,
                price=float(latest['Close']),
                high=float(latest['High']),
                low=float(latest['Low']),
                volume=float(latest['Volume']),
                change=float(latest['Close'] - previous_close),
                change_percent=float((latest['Close'] - previous_close) / previous_close * 100),
                timestamp=history.index[-1].to_pydatetime()
            )
            
            return quote
        except Exception as e:
            raise Exception(f"Failed to get quote for {symbol}: {str(e)}")
    
    async def get_historical_data(
        self, 
        symbol: str, 
        timeframe: TimeFrame,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
    ) -> List[OHLCV]:
        """履歴データを取得"""
        try:
            ticker = yf.Ticker(symbol)
            
            interval = self.TIMEFRAME_MAPPING[timeframe]
            period = self.PERIOD_MAPPING[timeframe]
            
            if start and end:
                df = ticker.history(start=start, end=end, interval=interval)
            else:
                df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                return []
            
            ohlcv_list = []
            for idx, row in df.iterrows():
                ohlcv = OHLCV(
                    timestamp=idx.to_pydatetime(),
                    open=float(row['Open']),
                    high=float(row['High']),
                    low=float(row['Low']),
                    close=float(row['Close']),
                    volume=float(row['Volume'])
                )
                ohlcv_list.append(ohlcv)
            
            return ohlcv_list
        except Exception as e:
            raise Exception(f"Failed to get historical data for {symbol}: {str(e)}")
    
    async def calculate_indicators(
        self, 
        symbol: str, 
        timeframe: TimeFrame
    ) -> TechnicalIndicators:
        """テクニカル指標を計算"""
        try:
            # 履歴データを取得
            ohlcv_list = await self.get_historical_data(symbol, timeframe)
            
            if not ohlcv_list:
                raise ValueError(f"No data available for {symbol}")
            
            # DataFrameに変換
            df = pd.DataFrame([{
                'Open': o.open,
                'High': o.high,
                'Low': o.low,
                'Close': o.close,
                'Volume': o.volume
            } for o in ohlcv_list])
            
            # 移動平均線
            df['SMA_20'] = ta.sma(df['Close'], length=20)
            df['SMA_50'] = ta.sma(df['Close'], length=50)
            df['SMA_200'] = ta.sma(df['Close'], length=200)
            df['EMA_12'] = ta.ema(df['Close'], length=12)
            df['EMA_26'] = ta.ema(df['Close'], length=26)
            
            # MACD
            macd = ta.macd(df['Close'])
            if macd is not None:
                df = pd.concat([df, macd], axis=1)
            
            # RSI
            df['RSI'] = ta.rsi(df['Close'], length=14)
            
            # Stochastic
            stoch = ta.stoch(df['High'], df['Low'], df['Close'])
            if stoch is not None:
                df = pd.concat([df, stoch], axis=1)
            
            # ボリンジャーバンド
            bbands = ta.bbands(df['Close'], length=20, std=2)
            if bbands is not None:
                df = pd.concat([df, bbands], axis=1)
            
            # ATR
            df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
            
            # OBV
            df['OBV'] = ta.obv(df['Close'], df['Volume'])
            
            # VWAP
            df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'])
            
            # 最新の値を取得
            latest = df.iloc[-1]
            
            indicators = TechnicalIndicators(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=ohlcv_list[-1].timestamp,
                sma_20=float(latest['SMA_20']) if pd.notna(latest.get('SMA_20')) else None,
                sma_50=float(latest['SMA_50']) if pd.notna(latest.get('SMA_50')) else None,
                sma_200=float(latest['SMA_200']) if pd.notna(latest.get('SMA_200')) else None,
                ema_12=float(latest['EMA_12']) if pd.notna(latest.get('EMA_12')) else None,
                ema_26=float(latest['EMA_26']) if pd.notna(latest.get('EMA_26')) else None,
                macd=float(latest['MACD_12_26_9']) if pd.notna(latest.get('MACD_12_26_9')) else None,
                macd_signal=float(latest['MACDs_12_26_9']) if pd.notna(latest.get('MACDs_12_26_9')) else None,
                macd_histogram=float(latest['MACDh_12_26_9']) if pd.notna(latest.get('MACDh_12_26_9')) else None,
                rsi=float(latest['RSI']) if pd.notna(latest.get('RSI')) else None,
                stoch_k=float(latest['STOCHk_14_3_3']) if pd.notna(latest.get('STOCHk_14_3_3')) else None,
                stoch_d=float(latest['STOCHd_14_3_3']) if pd.notna(latest.get('STOCHd_14_3_3')) else None,
                bb_upper=float(latest['BBU_20_2.0']) if pd.notna(latest.get('BBU_20_2.0')) else None,
                bb_middle=float(latest['BBM_20_2.0']) if pd.notna(latest.get('BBM_20_2.0')) else None,
                bb_lower=float(latest['BBL_20_2.0']) if pd.notna(latest.get('BBL_20_2.0')) else None,
                atr=float(latest['ATR']) if pd.notna(latest.get('ATR')) else None,
                obv=float(latest['OBV']) if pd.notna(latest.get('OBV')) else None,
                vwap=float(latest['VWAP']) if pd.notna(latest.get('VWAP')) else None,
            )
            
            return indicators
        except Exception as e:
            raise Exception(f"Failed to calculate indicators for {symbol}: {str(e)}")
    
    async def analyze_trend(
        self, 
        symbol: str, 
        timeframe: TimeFrame
    ) -> TrendAnalysis:
        """トレンドを分析"""
        try:
            indicators = await self.calculate_indicators(symbol, timeframe)
            ohlcv_list = await self.get_historical_data(symbol, timeframe)
            
            if not ohlcv_list:
                return TrendAnalysis(
                    timeframe=timeframe,
                    direction=TrendDirection.UNKNOWN,
                    strength=0,
                    description="データ不足"
                )
            
            current_price = ohlcv_list[-1].close
            
            # トレンド判定
            direction = TrendDirection.SIDEWAYS
            strength = 50.0
            reasons = []
            
            # 移動平均線によるトレンド判定
            if indicators.sma_20 and indicators.sma_50:
                if current_price > indicators.sma_20 > indicators.sma_50:
                    direction = TrendDirection.BULLISH
                    strength += 20
                    reasons.append("価格が移動平均線の上にある")
                elif current_price < indicators.sma_20 < indicators.sma_50:
                    direction = TrendDirection.BEARISH
                    strength += 20
                    reasons.append("価格が移動平均線の下にある")
            
            # RSIによる判定
            if indicators.rsi:
                if indicators.rsi > 70:
                    reasons.append(f"RSI買われすぎ ({indicators.rsi:.1f})")
                    if direction == TrendDirection.BEARISH:
                        strength += 10
                elif indicators.rsi < 30:
                    reasons.append(f"RSI売られすぎ ({indicators.rsi:.1f})")
                    if direction == TrendDirection.BULLISH:
                        strength += 10
                elif 40 <= indicators.rsi <= 60:
                    reasons.append(f"RSI中立 ({indicators.rsi:.1f})")
            
            # MACDによる判定
            if indicators.macd and indicators.macd_signal:
                if indicators.macd > indicators.macd_signal:
                    if direction == TrendDirection.BULLISH:
                        strength += 15
                    reasons.append("MACD上昇シグナル")
                else:
                    if direction == TrendDirection.BEARISH:
                        strength += 15
                    reasons.append("MACD下降シグナル")
            
            strength = min(strength, 100)
            
            # サポート・レジスタンスレベルを計算
            closes = [o.close for o in ohlcv_list[-50:]]
            support_levels = self._find_support_levels(closes, current_price)
            resistance_levels = self._find_resistance_levels(closes, current_price)
            
            description = f"{timeframe.value}: {direction.value} (強度: {strength:.0f}%). " + "; ".join(reasons)
            
            return TrendAnalysis(
                timeframe=timeframe,
                direction=direction,
                strength=strength,
                support_levels=support_levels,
                resistance_levels=resistance_levels,
                description=description
            )
        except Exception as e:
            raise Exception(f"Failed to analyze trend for {symbol}: {str(e)}")
    
    def _find_support_levels(self, prices: List[float], current_price: float) -> List[float]:
        """サポートレベルを検出"""
        prices_array = np.array(prices)
        support_levels = []
        
        # 直近の安値を検出
        for i in range(2, len(prices_array) - 2):
            if (prices_array[i] < prices_array[i-1] and 
                prices_array[i] < prices_array[i-2] and
                prices_array[i] < prices_array[i+1] and 
                prices_array[i] < prices_array[i+2] and
                prices_array[i] < current_price):
                support_levels.append(float(prices_array[i]))
        
        # 重複を削除し、現在価格に近い順にソート
        support_levels = sorted(list(set([round(s, 2) for s in support_levels])), reverse=True)
        return support_levels[:3]
    
    def _find_resistance_levels(self, prices: List[float], current_price: float) -> List[float]:
        """レジスタンスレベルを検出"""
        prices_array = np.array(prices)
        resistance_levels = []
        
        # 直近の高値を検出
        for i in range(2, len(prices_array) - 2):
            if (prices_array[i] > prices_array[i-1] and 
                prices_array[i] > prices_array[i-2] and
                prices_array[i] > prices_array[i+1] and 
                prices_array[i] > prices_array[i+2] and
                prices_array[i] > current_price):
                resistance_levels.append(float(prices_array[i]))
        
        # 重複を削除し、現在価格に近い順にソート
        resistance_levels = sorted(list(set([round(r, 2) for r in resistance_levels])))
        return resistance_levels[:3]
