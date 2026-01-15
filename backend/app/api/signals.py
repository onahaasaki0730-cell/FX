from fastapi import APIRouter, HTTPException, Query
from typing import List

from ..models.market import (
    TradingSignal, TimeFrame
)
from ..services.market_data import MarketDataService
from ..services.signal_service import SignalService

router = APIRouter(prefix="/signals", tags=["signals"])
market_service = MarketDataService()
signal_service = SignalService(market_service)


@router.get("/{symbol}", response_model=TradingSignal)
async def get_trading_signal(
    symbol: str,
    timeframe: TimeFrame = Query(TimeFrame.H1)
):
    """
    トレーディングシグナルを生成
    
    - **symbol**: 通貨ペアまたは銘柄シンボル
    - **timeframe**: 時間足
    
    返される情報:
    - シグナル (strong_buy, buy, neutral, sell, strong_sell)
    - 信頼度 (0-100)
    - シグナルの理由
    - エントリー価格
    - ストップロス
    - テイクプロフィット
    """
    try:
        signal = await signal_service.generate_signal(symbol, timeframe)
        return signal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/multi/{symbol}", response_model=List[TradingSignal])
async def get_multi_timeframe_signals(
    symbol: str,
    timeframes: List[TimeFrame] = Query(
        default=[TimeFrame.M15, TimeFrame.H1, TimeFrame.H4, TimeFrame.D1]
    )
):
    """
    複数時間足のトレーディングシグナルを生成
    
    - **symbol**: 通貨ペアまたは銘柄シンボル
    - **timeframes**: 分析する時間足のリスト
    
    各時間足のシグナルを個別に返します。
    """
    try:
        signals = []
        for tf in timeframes:
            signal = await signal_service.generate_signal(symbol, tf)
            signals.append(signal)
        return signals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
