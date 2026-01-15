from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from ..models.market import (
    MarketQuote, OHLCV, TimeFrame, TechnicalIndicators,
    TrendAnalysis, MultiTimeframeAnalysis
)
from ..services.market_data import MarketDataService

router = APIRouter(prefix="/market", tags=["market"])
market_service = MarketDataService()


@router.get("/quote/{symbol}", response_model=MarketQuote)
async def get_quote(symbol: str):
    """
    リアルタイム価格を取得
    
    - **symbol**: 通貨ペアまたは銘柄シンボル (例: USDJPY, AAPL)
    """
    try:
        quote = await market_service.get_quote(symbol)
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{symbol}", response_model=List[OHLCV])
async def get_historical_data(
    symbol: str,
    timeframe: TimeFrame = Query(TimeFrame.H1),
    start: Optional[datetime] = None,
    end: Optional[datetime] = None
):
    """
    履歴データを取得
    
    - **symbol**: 通貨ペアまたは銘柄シンボル
    - **timeframe**: 時間足 (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M)
    - **start**: 開始日時（オプション）
    - **end**: 終了日時（オプション）
    """
    try:
        data = await market_service.get_historical_data(
            symbol, timeframe, start, end
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/indicators/{symbol}", response_model=TechnicalIndicators)
async def get_technical_indicators(
    symbol: str,
    timeframe: TimeFrame = Query(TimeFrame.H1)
):
    """
    テクニカル指標を計算
    
    - **symbol**: 通貨ペアまたは銘柄シンボル
    - **timeframe**: 時間足
    
    計算される指標:
    - 移動平均線 (SMA 20, 50, 200, EMA 12, 26)
    - MACD
    - RSI
    - Stochastic
    - ボリンジャーバンド
    - ATR
    - OBV
    - VWAP
    """
    try:
        indicators = await market_service.calculate_indicators(symbol, timeframe)
        return indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trend/{symbol}", response_model=TrendAnalysis)
async def get_trend_analysis(
    symbol: str,
    timeframe: TimeFrame = Query(TimeFrame.H1)
):
    """
    トレンド分析を実行
    
    - **symbol**: 通貨ペアまたは銘柄シンボル
    - **timeframe**: 時間足
    
    返される情報:
    - トレンド方向 (bullish, bearish, sideways)
    - トレンド強度 (0-100)
    - サポートレベル
    - レジスタンスレベル
    - 分析の説明
    """
    try:
        analysis = await market_service.analyze_trend(symbol, timeframe)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/multi-timeframe/{symbol}", response_model=MultiTimeframeAnalysis)
async def get_multi_timeframe_analysis(
    symbol: str,
    timeframes: List[TimeFrame] = Query(
        default=[TimeFrame.M15, TimeFrame.H1, TimeFrame.H4, TimeFrame.D1]
    )
):
    """
    マルチタイムフレーム分析を実行
    
    - **symbol**: 通貨ペアまたは銘柄シンボル
    - **timeframes**: 分析する時間足のリスト
    
    複数の時間足を同時に分析し、全体的なトレンドと
    コンセンサスシグナルを提供します。
    """
    try:
        from ..services.signal_service import SignalService
        signal_service = SignalService(market_service)
        analysis = await signal_service.get_multi_timeframe_analysis(
            symbol, timeframes
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
