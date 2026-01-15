from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

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


@app.get("/charts")
async def charts_page():
    """チャートページを表示"""
    charts_path = os.path.join(os.path.dirname(__file__), "..", "charts.html")
    if os.path.exists(charts_path):
        return FileResponse(charts_path)
    return {"error": "Charts page not found"}


@app.get("/mt5")
async def mt5_charts_page():
    """MT5スタイルのFXチャートページを表示"""
    mt5_path = os.path.join(os.path.dirname(__file__), "..", "mt5_charts.html")
    if os.path.exists(mt5_path):
        return FileResponse(mt5_path)
    return {"error": "MT5 charts page not found"}


@app.get("/")
async def root():
    """ルートエンドポイント - デモページを表示"""
    demo_path = os.path.join(os.path.dirname(__file__), "..", "demo.html")
    if os.path.exists(demo_path):
        return FileResponse(demo_path)
    
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "demo": "/",
            "charts": "/charts",
            "mt5_charts": "/mt5",
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
