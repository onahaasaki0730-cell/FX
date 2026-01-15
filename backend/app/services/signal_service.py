from typing import List, Dict
from datetime import datetime

from ..models.market import (
    TradingSignal, SignalStrength, TimeFrame, TrendDirection,
    TechnicalIndicators, MultiTimeframeAnalysis
)
from .market_data import MarketDataService


class SignalService:
    """トレーディングシグナル生成サービス"""
    
    def __init__(self, market_service: MarketDataService):
        self.market_service = market_service
    
    async def generate_signal(
        self, 
        symbol: str, 
        timeframe: TimeFrame
    ) -> TradingSignal:
        """トレーディングシグナルを生成"""
        try:
            # テクニカル指標とトレンド分析を取得
            indicators = await self.market_service.calculate_indicators(symbol, timeframe)
            trend = await self.market_service.analyze_trend(symbol, timeframe)
            quote = await self.market_service.get_quote(symbol)
            
            # シグナル強度を計算
            signal_strength = SignalStrength.NEUTRAL
            confidence = 50.0
            reasons = []
            
            # トレンドベースの判定
            if trend.direction == TrendDirection.BULLISH and trend.strength > 60:
                signal_strength = SignalStrength.BUY
                confidence += 20
                reasons.append(f"強い上昇トレンド (強度: {trend.strength:.0f}%)")
            elif trend.direction == TrendDirection.BEARISH and trend.strength > 60:
                signal_strength = SignalStrength.SELL
                confidence += 20
                reasons.append(f"強い下降トレンド (強度: {trend.strength:.0f}%)")
            
            # RSIベースの判定
            if indicators.rsi:
                if indicators.rsi > 70:
                    if signal_strength == SignalStrength.SELL:
                        signal_strength = SignalStrength.STRONG_SELL
                        confidence += 15
                    reasons.append(f"RSI買われすぎ ({indicators.rsi:.1f})")
                elif indicators.rsi < 30:
                    if signal_strength == SignalStrength.BUY:
                        signal_strength = SignalStrength.STRONG_BUY
                        confidence += 15
                    reasons.append(f"RSI売られすぎ ({indicators.rsi:.1f})")
            
            # MACDベースの判定
            if indicators.macd and indicators.macd_signal:
                macd_diff = indicators.macd - indicators.macd_signal
                if macd_diff > 0 and indicators.macd_histogram and indicators.macd_histogram > 0:
                    if signal_strength in [SignalStrength.BUY, SignalStrength.NEUTRAL]:
                        confidence += 10
                    reasons.append("MACD買いシグナル")
                elif macd_diff < 0 and indicators.macd_histogram and indicators.macd_histogram < 0:
                    if signal_strength in [SignalStrength.SELL, SignalStrength.NEUTRAL]:
                        confidence += 10
                    reasons.append("MACD売りシグナル")
            
            # ボリンジャーバンドベースの判定
            if indicators.bb_upper and indicators.bb_lower and indicators.bb_middle:
                current_price = quote.price
                if current_price > indicators.bb_upper:
                    reasons.append("価格がボリンジャーバンド上限を超えている")
                    if signal_strength == SignalStrength.SELL:
                        confidence += 10
                elif current_price < indicators.bb_lower:
                    reasons.append("価格がボリンジャーバンド下限を下回っている")
                    if signal_strength == SignalStrength.BUY:
                        confidence += 10
            
            # 移動平均線クロス
            if indicators.sma_20 and indicators.sma_50:
                if quote.price > indicators.sma_20 > indicators.sma_50:
                    if signal_strength in [SignalStrength.BUY, SignalStrength.NEUTRAL]:
                        confidence += 10
                    reasons.append("価格が移動平均線の上にある")
                elif quote.price < indicators.sma_20 < indicators.sma_50:
                    if signal_strength in [SignalStrength.SELL, SignalStrength.NEUTRAL]:
                        confidence += 10
                    reasons.append("価格が移動平均線の下にある")
            
            confidence = min(confidence, 100)
            
            # エントリー、ストップロス、テイクプロフィットを計算
            entry_price = quote.price
            atr = indicators.atr or (quote.price * 0.02)  # ATRがない場合は2%を使用
            
            if signal_strength in [SignalStrength.BUY, SignalStrength.STRONG_BUY]:
                stop_loss = entry_price - (2 * atr)
                take_profit = entry_price + (3 * atr)
            elif signal_strength in [SignalStrength.SELL, SignalStrength.STRONG_SELL]:
                stop_loss = entry_price + (2 * atr)
                take_profit = entry_price - (3 * atr)
            else:
                stop_loss = None
                take_profit = None
            
            return TradingSignal(
                symbol=symbol,
                timeframe=timeframe,
                signal=signal_strength,
                confidence=confidence,
                reasons=reasons,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                timestamp=datetime.now()
            )
        except Exception as e:
            raise Exception(f"Failed to generate signal for {symbol}: {str(e)}")
    
    async def get_multi_timeframe_analysis(
        self, 
        symbol: str,
        timeframes: List[TimeFrame] = None
    ) -> MultiTimeframeAnalysis:
        """マルチタイムフレーム分析を実行"""
        if not timeframes:
            timeframes = [
                TimeFrame.M15,
                TimeFrame.H1,
                TimeFrame.H4,
                TimeFrame.D1
            ]
        
        try:
            quote = await self.market_service.get_quote(symbol)
            
            # 各時間足の分析を取得
            analyses = {}
            for tf in timeframes:
                trend = await self.market_service.analyze_trend(symbol, tf)
                analyses[tf] = trend
            
            # 全体的なトレンドを判定
            bullish_count = sum(1 for a in analyses.values() if a.direction == TrendDirection.BULLISH)
            bearish_count = sum(1 for a in analyses.values() if a.direction == TrendDirection.BEARISH)
            
            if bullish_count > bearish_count:
                overall_trend = TrendDirection.BULLISH
                consensus_signal = SignalStrength.BUY if bullish_count > len(timeframes) / 2 else SignalStrength.NEUTRAL
            elif bearish_count > bullish_count:
                overall_trend = TrendDirection.BEARISH
                consensus_signal = SignalStrength.SELL if bearish_count > len(timeframes) / 2 else SignalStrength.NEUTRAL
            else:
                overall_trend = TrendDirection.SIDEWAYS
                consensus_signal = SignalStrength.NEUTRAL
            
            # サマリーを作成
            summary_parts = []
            for tf, analysis in analyses.items():
                summary_parts.append(
                    f"{tf.value}: {analysis.direction.value} ({analysis.strength:.0f}%)"
                )
            
            summary = f"全体的なトレンド: {overall_trend.value}. " + ", ".join(summary_parts)
            
            return MultiTimeframeAnalysis(
                symbol=symbol,
                timestamp=datetime.now(),
                current_price=quote.price,
                analyses=analyses,
                overall_trend=overall_trend,
                consensus_signal=consensus_signal,
                summary=summary
            )
        except Exception as e:
            raise Exception(f"Failed to perform multi-timeframe analysis: {str(e)}")
