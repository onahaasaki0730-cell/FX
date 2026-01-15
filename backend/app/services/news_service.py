import aiohttp
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import asyncio
from ..models.market import (
    NewsItem, NewsImpact, EconomicEvent, MarketSentiment
)
from ..core.config import settings


class NewsService:
    """ニュース分析サービス"""
    
    NEWS_API_URL = "https://newsapi.org/v2/everything"
    
    # キーワードによる影響度判定
    IMPACT_KEYWORDS = {
        NewsImpact.CRITICAL: [
            "central bank", "interest rate", "fed", "ecb", "boj",
            "crisis", "war", "emergency", "default"
        ],
        NewsImpact.HIGH: [
            "gdp", "inflation", "employment", "unemployment",
            "policy", "regulation", "sanctions"
        ],
        NewsImpact.MEDIUM: [
            "earnings", "forecast", "outlook", "data",
            "report", "announcement"
        ]
    }
    
    # センチメント分析用キーワード
    POSITIVE_KEYWORDS = [
        "surge", "rally", "gain", "rise", "up", "positive",
        "growth", "strong", "bullish", "recovery", "upgrade"
    ]
    
    NEGATIVE_KEYWORDS = [
        "fall", "drop", "decline", "down", "negative",
        "weak", "bearish", "crisis", "concern", "downgrade"
    ]
    
    def __init__(self):
        self.cache: Dict[str, List[NewsItem]] = {}
    
    async def get_latest_news(
        self, 
        symbols: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[NewsItem]:
        """最新ニュースを取得"""
        try:
            # キャッシュチェック
            cache_key = f"news_{','.join(symbols or [])}"
            if cache_key in self.cache:
                return self.cache[cache_key][:limit]
            
            news_items = []
            
            # デモデータを返す（実際のAPIキーがない場合）
            if not settings.NEWS_API_KEY:
                news_items = self._get_demo_news(symbols)
            else:
                # NewsAPIから取得
                news_items = await self._fetch_from_newsapi(symbols, limit)
            
            # キャッシュに保存
            self.cache[cache_key] = news_items
            
            return news_items[:limit]
        except Exception as e:
            print(f"Failed to get news: {str(e)}")
            return self._get_demo_news(symbols)
    
    async def _fetch_from_newsapi(
        self, 
        symbols: Optional[List[str]], 
        limit: int
    ) -> List[NewsItem]:
        """NewsAPIからニュースを取得"""
        news_items = []
        
        query = "forex OR stock market OR economy"
        if symbols:
            query += " AND (" + " OR ".join(symbols) + ")"
        
        params = {
            "q": query,
            "apiKey": settings.NEWS_API_KEY,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": limit
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.NEWS_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for article in data.get("articles", []):
                        news_item = NewsItem(
                            id=str(hash(article["url"])),
                            title=article["title"],
                            description=article.get("description"),
                            source=article["source"]["name"],
                            url=article["url"],
                            published_at=datetime.fromisoformat(
                                article["publishedAt"].replace("Z", "+00:00")
                            ),
                            impact=self._assess_impact(article["title"], article.get("description", "")),
                            sentiment=self._analyze_sentiment(article["title"], article.get("description", "")),
                            related_symbols=symbols or [],
                            tags=self._extract_tags(article["title"], article.get("description", ""))
                        )
                        news_items.append(news_item)
        
        return news_items
    
    def _get_demo_news(self, symbols: Optional[List[str]] = None) -> List[NewsItem]:
        """デモニュースデータを生成"""
        now = datetime.now()
        
        demo_news = [
            NewsItem(
                id="demo_1",
                title="FRB、金利を維持すると発表",
                description="連邦準備制度理事会は、現在の金利を維持することを決定しました。",
                source="Bloomberg",
                url="https://example.com/news/1",
                published_at=now - timedelta(hours=2),
                impact=NewsImpact.CRITICAL,
                sentiment=0.3,
                related_symbols=symbols or ["USDJPY", "EURUSD"],
                tags=["central_bank", "interest_rate", "monetary_policy"]
            ),
            NewsItem(
                id="demo_2",
                title="米雇用統計、予想を上回る",
                description="最新の雇用統計が発表され、市場予想を上回る結果となりました。",
                source="Reuters",
                url="https://example.com/news/2",
                published_at=now - timedelta(hours=5),
                impact=NewsImpact.HIGH,
                sentiment=0.6,
                related_symbols=symbols or ["USDJPY", "GBPUSD"],
                tags=["employment", "economic_data"]
            ),
            NewsItem(
                id="demo_3",
                title="中国GDP成長率が減速",
                description="中国の第4四半期GDP成長率は予想を下回りました。",
                source="Financial Times",
                url="https://example.com/news/3",
                published_at=now - timedelta(hours=8),
                impact=NewsImpact.HIGH,
                sentiment=-0.4,
                related_symbols=symbols or ["USDJPY", "AUDUSD"],
                tags=["gdp", "china", "economic_growth"]
            ),
        ]
        
        return demo_news
    
    def _assess_impact(self, title: str, description: str) -> NewsImpact:
        """ニュースの影響度を評価"""
        text = (title + " " + description).lower()
        
        for impact, keywords in self.IMPACT_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return impact
        
        return NewsImpact.LOW
    
    def _analyze_sentiment(self, title: str, description: str) -> float:
        """センチメントを分析 (-1 to 1)"""
        text = (title + " " + description).lower()
        
        positive_count = sum(1 for keyword in self.POSITIVE_KEYWORDS if keyword in text)
        negative_count = sum(1 for keyword in self.NEGATIVE_KEYWORDS if keyword in text)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / total
        return max(-1.0, min(1.0, sentiment))
    
    def _extract_tags(self, title: str, description: str) -> List[str]:
        """タグを抽出"""
        text = (title + " " + description).lower()
        tags = []
        
        tag_keywords = {
            "central_bank": ["fed", "ecb", "boj", "central bank"],
            "interest_rate": ["interest rate", "rate hike", "rate cut"],
            "gdp": ["gdp", "economic growth"],
            "inflation": ["inflation", "cpi", "pce"],
            "employment": ["employment", "jobs", "unemployment"],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    async def get_economic_calendar(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[EconomicEvent]:
        """経済カレンダーを取得"""
        # デモデータを返す
        now = datetime.now()
        
        events = [
            EconomicEvent(
                id="event_1",
                title="米国 雇用統計（NFP）",
                country="US",
                currency="USD",
                event_time=now + timedelta(days=3, hours=8),
                impact=NewsImpact.CRITICAL,
                forecast="200K",
                previous="180K",
                description="非農業部門雇用者数の発表"
            ),
            EconomicEvent(
                id="event_2",
                title="日本 GDP速報値",
                country="JP",
                currency="JPY",
                event_time=now + timedelta(days=5, hours=23),
                impact=NewsImpact.HIGH,
                forecast="0.5%",
                previous="0.3%",
                description="四半期GDP成長率の発表"
            ),
            EconomicEvent(
                id="event_3",
                title="ECB 政策金利発表",
                country="EU",
                currency="EUR",
                event_time=now + timedelta(days=7, hours=12),
                impact=NewsImpact.CRITICAL,
                forecast="4.50%",
                previous="4.50%",
                description="欧州中央銀行の金融政策決定"
            ),
        ]
        
        return events
    
    async def calculate_market_sentiment(
        self, 
        symbol: str,
        news_items: Optional[List[NewsItem]] = None
    ) -> MarketSentiment:
        """市場センチメントを計算"""
        if not news_items:
            news_items = await self.get_latest_news([symbol])
        
        # ニュースセンチメント
        related_news = [n for n in news_items if symbol in n.related_symbols]
        
        if related_news:
            news_sentiment = sum(n.sentiment for n in related_news) / len(related_news)
        else:
            news_sentiment = 0.0
        
        # センチメントのカウント
        bullish = sum(1 for n in related_news if n.sentiment > 0.2)
        bearish = sum(1 for n in related_news if n.sentiment < -0.2)
        neutral = len(related_news) - bullish - bearish
        
        # テクニカルセンチメントは別サービスで計算される想定
        technical_sentiment = 0.0
        
        # 総合センチメント
        overall_sentiment = news_sentiment * 0.6 + technical_sentiment * 0.4
        
        return MarketSentiment(
            symbol=symbol,
            timestamp=datetime.now(),
            overall_sentiment=overall_sentiment,
            news_sentiment=news_sentiment,
            technical_sentiment=technical_sentiment,
            bullish_count=bullish,
            bearish_count=bearish,
            neutral_count=neutral
        )
