from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class TimeFrame(str, Enum):
    """時間足の定義"""
    M1 = "1m"   # 1分足
    M5 = "5m"   # 5分足
    M15 = "15m" # 15分足
    M30 = "30m" # 30分足
    M45 = "45m" # 45分足
    H1 = "1h"   # 1時間足
    H4 = "4h"   # 4時間足
    D1 = "1d"   # 日足
    W1 = "1w"   # 週足
    MN1 = "1M"  # 月足


class TrendDirection(str, Enum):
    """トレンド方向"""
    BULLISH = "bullish"        # 上昇トレンド
    BEARISH = "bearish"        # 下降トレンド
    SIDEWAYS = "sideways"      # レンジ
    UNKNOWN = "unknown"        # 不明


class SignalStrength(str, Enum):
    """シグナル強度"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    NEUTRAL = "neutral"
    SELL = "sell"
    STRONG_SELL = "strong_sell"


class OHLCV(BaseModel):
    """ローソク足データ"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    

class MarketQuote(BaseModel):
    """市場価格情報"""
    symbol: str
    price: float
    bid: Optional[float] = None
    ask: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class TrendAnalysis(BaseModel):
    """トレンド分析結果"""
    timeframe: TimeFrame
    direction: TrendDirection
    strength: float = Field(ge=0, le=100)  # 0-100
    support_levels: List[float] = []
    resistance_levels: List[float] = []
    description: str = ""


class TechnicalIndicators(BaseModel):
    """テクニカル指標"""
    symbol: str
    timeframe: TimeFrame
    timestamp: datetime
    
    # トレンド指標
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    
    # MACD
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    
    # RSI
    rsi: Optional[float] = None
    
    # Stochastic
    stoch_k: Optional[float] = None
    stoch_d: Optional[float] = None
    
    # ボリンジャーバンド
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    
    # ATR
    atr: Optional[float] = None
    
    # 出来高指標
    obv: Optional[float] = None
    vwap: Optional[float] = None


class TradingSignal(BaseModel):
    """トレーディングシグナル"""
    symbol: str
    timeframe: TimeFrame
    signal: SignalStrength
    confidence: float = Field(ge=0, le=100)
    reasons: List[str] = []
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class MultiTimeframeAnalysis(BaseModel):
    """マルチタイムフレーム分析"""
    symbol: str
    timestamp: datetime
    current_price: float
    analyses: Dict[TimeFrame, TrendAnalysis]
    overall_trend: TrendDirection
    consensus_signal: SignalStrength
    summary: str


class NewsImpact(str, Enum):
    """ニュースの影響度"""
    CRITICAL = "critical"  # 重大
    HIGH = "high"          # 高い
    MEDIUM = "medium"      # 中程度
    LOW = "low"            # 低い


class NewsItem(BaseModel):
    """ニュース項目"""
    id: str
    title: str
    description: Optional[str] = None
    source: str
    url: Optional[str] = None
    published_at: datetime
    impact: NewsImpact
    sentiment: float = Field(ge=-1, le=1)  # -1 (negative) to 1 (positive)
    related_symbols: List[str] = []
    tags: List[str] = []


class EconomicEvent(BaseModel):
    """経済イベント"""
    id: str
    title: str
    country: str
    currency: str
    event_time: datetime
    impact: NewsImpact
    forecast: Optional[str] = None
    previous: Optional[str] = None
    actual: Optional[str] = None
    description: Optional[str] = None
    
    
class MarketSentiment(BaseModel):
    """市場センチメント"""
    symbol: str
    timestamp: datetime
    overall_sentiment: float = Field(ge=-1, le=1)
    news_sentiment: float = Field(ge=-1, le=1)
    social_sentiment: Optional[float] = Field(default=None, ge=-1, le=1)
    technical_sentiment: float = Field(ge=-1, le=1)
    bullish_count: int = 0
    bearish_count: int = 0
    neutral_count: int = 0
