from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api import market, news, signals, websocket

# FastAPIアプリケーションを作成
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="市場のリアルタイム分析システム - ファンダメンタル・テクニカル分析プラットフォーム"
)

# CORSミドルウェアを設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルーターを登録
app.include_router(market.router, prefix=settings.API_V1_PREFIX)
app.include_router(news.router, prefix=settings.API_V1_PREFIX)
app.include_router(signals.router, prefix=settings.API_V1_PREFIX)
app.include_router(websocket.router)


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "market_data": f"{settings.API_V1_PREFIX}/market",
            "news": f"{settings.API_V1_PREFIX}/news",
            "signals": f"{settings.API_V1_PREFIX}/signals",
            "websocket_market": "/ws/market/{symbol}",
            "websocket_news": "/ws/news"
        }
    }


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
