from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # アプリケーション設定
    APP_NAME: str = "Market Analysis System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API設定
    API_V1_PREFIX: str = "/api/v1"
    
    # データベース設定
    DATABASE_URL: str = "sqlite:///./data/market_analysis.db"
    
    # Redis設定
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_EXPIRE: int = 300  # 5分
    
    # 外部API設定
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None
    FINNHUB_API_KEY: Optional[str] = None
    
    # WebSocket設定
    WS_MESSAGE_QUEUE_SIZE: int = 100
    WS_HEARTBEAT_INTERVAL: int = 30
    
    # 市場データ更新間隔（秒）
    MARKET_DATA_UPDATE_INTERVAL: int = 60
    NEWS_UPDATE_INTERVAL: int = 300
    
    # CORS設定
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
