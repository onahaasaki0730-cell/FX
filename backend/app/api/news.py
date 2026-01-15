from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from ..models.market import (
    NewsItem, EconomicEvent, MarketSentiment
)
from ..services.news_service import NewsService

router = APIRouter(prefix="/news", tags=["news"])
news_service = NewsService()


@router.get("/latest", response_model=List[NewsItem])
async def get_latest_news(
    symbols: Optional[List[str]] = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100)
):
    """
    最新ニュースを取得
    
    - **symbols**: フィルタリングする銘柄シンボルのリスト（オプション）
    - **limit**: 取得するニュースの数 (1-100)
    
    返される情報:
    - ニュースタイトル
    - 説明
    - ソース
    - 公開日時
    - 影響度 (critical, high, medium, low)
    - センチメント (-1 to 1)
    - 関連シンボル
    - タグ
    """
    try:
        news = await news_service.get_latest_news(symbols, limit)
        return news
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sentiment/{symbol}", response_model=MarketSentiment)
async def get_market_sentiment(symbol: str):
    """
    市場センチメントを分析
    
    - **symbol**: 通貨ペアまたは銘柄シンボル
    
    返される情報:
    - 総合センチメント
    - ニュースセンチメント
    - テクニカルセンチメント
    - 強気・弱気・中立のカウント
    """
    try:
        sentiment = await news_service.calculate_market_sentiment(symbol)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar", response_model=List[EconomicEvent])
async def get_economic_calendar(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    経済カレンダーを取得
    
    - **start_date**: 開始日時（オプション）
    - **end_date**: 終了日時（オプション）
    
    返される情報:
    - イベント名
    - 国・通貨
    - 予定時刻
    - 影響度
    - 予測値・前回値・実際値
    - 説明
    """
    try:
        events = await news_service.get_economic_calendar(start_date, end_date)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
