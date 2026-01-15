"""
Market Analysis System - WebSocket使用例

リアルタイムデータ配信のWebSocket接続例
"""

import asyncio
import websockets
import json
from datetime import datetime


async def test_market_websocket(symbol="AAPL"):
    """市場データのWebSocket接続テスト"""
    uri = f"ws://localhost:8000/ws/market/{symbol}"
    
    print(f"🔌 {symbol}の市場データWebSocketに接続中...")
    print(f"URI: {uri}\n")
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"✅ 接続成功！{symbol}のリアルタイムデータを受信中...\n")
            
            # ハートビートを送信するタスク
            async def send_heartbeat():
                while True:
                    await asyncio.sleep(30)
                    await websocket.send("ping")
                    print("💓 Heartbeat送信")
            
            # ハートビートタスクを開始
            heartbeat_task = asyncio.create_task(send_heartbeat())
            
            # メッセージを受信
            message_count = 0
            try:
                async for message in websocket:
                    message_count += 1
                    
                    if message == "pong":
                        print("✅ Heartbeat応答受信\n")
                        continue
                    
                    # JSONデータをパース
                    data = json.loads(message)
                    
                    print("=" * 70)
                    print(f"📊 市場データ更新 #{message_count}")
                    print(f"受信時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print("=" * 70)
                    
                    if data['type'] == 'market_update':
                        symbol = data['symbol']
                        quote = data['data']['quote']
                        indicators = data['data']['indicators']
                        trend = data['data']['trend']
                        
                        print(f"\n💰 価格情報:")
                        print(f"  銘柄: {symbol}")
                        print(f"  現在価格: ${quote['price']:.2f}")
                        print(f"  変動: {quote['change']:.2f} ({quote['change_percent']:.2f}%)")
                        print(f"  高値: ${quote['high']:.2f}")
                        print(f"  安値: ${quote['low']:.2f}")
                        
                        print(f"\n📈 テクニカル指標:")
                        if indicators['rsi']:
                            print(f"  RSI: {indicators['rsi']:.2f}")
                        if indicators['macd']:
                            print(f"  MACD: {indicators['macd']:.4f}")
                        if indicators['sma_20']:
                            print(f"  SMA(20): ${indicators['sma_20']:.2f}")
                        
                        print(f"\n📊 トレンド分析:")
                        print(f"  方向: {trend['direction']}")
                        print(f"  強度: {trend['strength']:.1f}%")
                        print(f"  時間足: {trend['timeframe']}")
                        
                    print("\n")
                    
                    # テストのため3回受信したら終了
                    if message_count >= 3:
                        print("✅ テスト完了（3回のデータ受信）")
                        break
                        
            except KeyboardInterrupt:
                print("\n⏸️  ユーザーによる中断")
            finally:
                heartbeat_task.cancel()
                
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket エラー: {e}")
    except Exception as e:
        print(f"❌ エラー: {e}")


async def test_news_websocket():
    """ニュースのWebSocket接続テスト"""
    uri = "ws://localhost:8000/ws/news"
    
    print(f"🔌 ニュースWebSocketに接続中...")
    print(f"URI: {uri}\n")
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"✅ 接続成功！リアルタイムニュースを受信中...\n")
            
            # ハートビートを送信するタスク
            async def send_heartbeat():
                while True:
                    await asyncio.sleep(30)
                    await websocket.send("ping")
                    print("💓 Heartbeat送信")
            
            heartbeat_task = asyncio.create_task(send_heartbeat())
            
            message_count = 0
            try:
                async for message in websocket:
                    message_count += 1
                    
                    if message == "pong":
                        print("✅ Heartbeat応答受信\n")
                        continue
                    
                    data = json.loads(message)
                    
                    print("=" * 70)
                    print(f"📰 ニュース更新 #{message_count}")
                    print(f"受信時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    print("=" * 70)
                    
                    if data['type'] == 'news_update':
                        count = data['count']
                        items = data['items']
                        
                        print(f"\n新しいニュース: {count}件")
                        
                        for i, item in enumerate(items[:3], 1):  # 最初の3件のみ表示
                            print(f"\n{i}. {item['title']}")
                            print(f"   ソース: {item['source']}")
                            print(f"   影響度: {item['impact']}")
                            print(f"   センチメント: {item['sentiment']:.2f}")
                            if item.get('description'):
                                print(f"   説明: {item['description'][:100]}...")
                        
                    print("\n")
                    
                    # テストのため2回受信したら終了
                    if message_count >= 2:
                        print("✅ テスト完了（2回のデータ受信）")
                        break
                        
            except KeyboardInterrupt:
                print("\n⏸️  ユーザーによる中断")
            finally:
                heartbeat_task.cancel()
                
    except websockets.exceptions.WebSocketException as e:
        print(f"❌ WebSocket エラー: {e}")
    except Exception as e:
        print(f"❌ エラー: {e}")


async def main():
    """メイン実行関数"""
    print("=" * 70)
    print(" Market Analysis System - WebSocket使用例")
    print("=" * 70)
    print()
    
    symbol = "AAPL"
    
    try:
        # 市場データのWebSocketテスト
        print("🧪 テスト1: 市場データWebSocket")
        print("-" * 70)
        await test_market_websocket(symbol)
        
        print("\n\n")
        
        # ニュースのWebSocketテスト
        print("🧪 テスト2: ニュースWebSocket")
        print("-" * 70)
        await test_news_websocket()
        
        print("\n" + "=" * 70)
        print(" ✅ すべてのWebSocketテストが完了しました！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")


if __name__ == "__main__":
    print("⚠️  このスクリプトを実行する前に、バックエンドサーバーが起動していることを確認してください")
    print("起動方法: python -m app.main\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏸️  プログラムを終了しました")
