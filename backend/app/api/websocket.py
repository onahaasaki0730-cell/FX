from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import Dict, Set
import asyncio
import json
from datetime import datetime

from ..services.market_data import MarketDataService
from ..services.news_service import NewsService
from ..models.market import TimeFrame

router = APIRouter()

market_service = MarketDataService()
news_service = NewsService()


class ConnectionManager:
    """WebSocket接続を管理"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.market_tasks: Dict[str, asyncio.Task] = {}
    
    async def connect(self, websocket: WebSocket, channel: str):
        """接続を追加"""
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)
    
    def disconnect(self, websocket: WebSocket, channel: str):
        """接続を削除"""
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
            if not self.active_connections[channel]:
                del self.active_connections[channel]
                # タスクをキャンセル
                if channel in self.market_tasks:
                    self.market_tasks[channel].cancel()
                    del self.market_tasks[channel]
    
    async def broadcast(self, channel: str, message: dict):
        """チャンネルの全接続にメッセージを送信"""
        if channel not in self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections[channel]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)
        
        # 切断された接続を削除
        for connection in disconnected:
            self.disconnect(connection, channel)


manager = ConnectionManager()


@router.websocket("/ws/market/{symbol}")
async def websocket_market_endpoint(websocket: WebSocket, symbol: str):
    """
    市場データのリアルタイム配信
    
    接続後、指定されたシンボルの市場データを定期的に配信します。
    
    送信されるデータ:
    - 現在価格
    - テクニカル指標
    - トレンド分析
    """
    channel = f"market:{symbol}"
    await manager.connect(websocket, channel)
    
    try:
        # バックグラウンドタスクを開始（まだ実行されていない場合）
        if channel not in manager.market_tasks:
            manager.market_tasks[channel] = asyncio.create_task(
                broadcast_market_data(symbol, channel)
            )
        
        # 接続を維持
        while True:
            # クライアントからのメッセージを待つ（ハートビート用）
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket, channel)


@router.websocket("/ws/news")
async def websocket_news_endpoint(websocket: WebSocket):
    """
    ニュースのリアルタイム配信
    
    接続後、最新のニュースを定期的に配信します。
    """
    channel = "news"
    await manager.connect(websocket, channel)
    
    try:
        # バックグラウンドタスクを開始（まだ実行されていない場合）
        if channel not in manager.market_tasks:
            manager.market_tasks[channel] = asyncio.create_task(
                broadcast_news(channel)
            )
        
        # 接続を維持
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket, channel)


async def broadcast_market_data(symbol: str, channel: str):
    """市場データを定期的にブロードキャスト"""
    while True:
        try:
            # 市場データを取得
            quote = await market_service.get_quote(symbol)
            indicators = await market_service.calculate_indicators(
                symbol, TimeFrame.H1
            )
            trend = await market_service.analyze_trend(symbol, TimeFrame.H1)
            
            # データをJSON形式で送信
            message = {
                "type": "market_update",
                "symbol": symbol,
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "quote": quote.model_dump(),
                    "indicators": indicators.model_dump(),
                    "trend": trend.model_dump()
                }
            }
            
            await manager.broadcast(channel, message)
            
            # 60秒待機
            await asyncio.sleep(60)
        
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error broadcasting market data: {str(e)}")
            await asyncio.sleep(60)


async def broadcast_news(channel: str):
    """ニュースを定期的にブロードキャスト"""
    last_update = datetime.now()
    
    while True:
        try:
            # 最新ニュースを取得
            news_items = await news_service.get_latest_news(limit=10)
            
            # 新しいニュースのみをフィルタ
            new_items = [
                item for item in news_items
                if item.published_at > last_update
            ]
            
            if new_items:
                message = {
                    "type": "news_update",
                    "timestamp": datetime.now().isoformat(),
                    "count": len(new_items),
                    "items": [item.model_dump() for item in new_items]
                }
                
                await manager.broadcast(channel, message)
                last_update = datetime.now()
            
            # 300秒（5分）待機
            await asyncio.sleep(300)
        
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error broadcasting news: {str(e)}")
            await asyncio.sleep(300)
