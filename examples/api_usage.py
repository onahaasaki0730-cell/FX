"""
Market Analysis System - 使用例

このスクリプトは、APIの基本的な使用方法を示します。
"""

import requests
import json
from datetime import datetime

# APIのベースURL
BASE_URL = "http://localhost:8000/api/v1"


def print_json(data, title=""):
    """JSONデータを整形して表示"""
    if title:
        print(f"\n{'=' * 60}")
        print(f" {title}")
        print('=' * 60)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def example_get_quote(symbol="AAPL"):
    """例1: リアルタイム価格を取得"""
    print(f"\n📊 {symbol}の現在価格を取得中...")
    
    response = requests.get(f"{BASE_URL}/market/quote/{symbol}")
    
    if response.status_code == 200:
        data = response.json()
        print_json(data, f"{symbol} リアルタイム価格")
        
        print(f"\n価格: ${data['price']:.2f}")
        print(f"変動: {data['change']:.2f} ({data['change_percent']:.2f}%)")
        print(f"高値: ${data['high']:.2f}")
        print(f"安値: ${data['low']:.2f}")
        return data
    else:
        print(f"❌ エラー: {response.status_code}")
        return None


def example_get_indicators(symbol="AAPL", timeframe="1h"):
    """例2: テクニカル指標を取得"""
    print(f"\n📈 {symbol}のテクニカル指標を取得中 ({timeframe})...")
    
    response = requests.get(
        f"{BASE_URL}/market/indicators/{symbol}",
        params={"timeframe": timeframe}
    )
    
    if response.status_code == 200:
        data = response.json()
        print_json(data, f"{symbol} テクニカル指標 ({timeframe})")
        
        print(f"\nRSI: {data['rsi']:.2f}" if data['rsi'] else "\nRSI: N/A")
        print(f"MACD: {data['macd']:.4f}" if data['macd'] else "MACD: N/A")
        print(f"SMA(20): ${data['sma_20']:.2f}" if data['sma_20'] else "SMA(20): N/A")
        print(f"SMA(50): ${data['sma_50']:.2f}" if data['sma_50'] else "SMA(50): N/A")
        return data
    else:
        print(f"❌ エラー: {response.status_code}")
        return None


def example_get_trend(symbol="AAPL", timeframe="1h"):
    """例3: トレンド分析を取得"""
    print(f"\n📊 {symbol}のトレンド分析中 ({timeframe})...")
    
    response = requests.get(
        f"{BASE_URL}/market/trend/{symbol}",
        params={"timeframe": timeframe}
    )
    
    if response.status_code == 200:
        data = response.json()
        print_json(data, f"{symbol} トレンド分析 ({timeframe})")
        
        print(f"\nトレンド方向: {data['direction']}")
        print(f"トレンド強度: {data['strength']:.1f}%")
        print(f"サポートレベル: {data['support_levels']}")
        print(f"レジスタンスレベル: {data['resistance_levels']}")
        print(f"説明: {data['description']}")
        return data
    else:
        print(f"❌ エラー: {response.status_code}")
        return None


def example_get_multi_timeframe(symbol="AAPL"):
    """例4: マルチタイムフレーム分析"""
    print(f"\n🔍 {symbol}のマルチタイムフレーム分析中...")
    
    timeframes = ["15m", "1h", "4h", "1d"]
    
    response = requests.get(
        f"{BASE_URL}/market/multi-timeframe/{symbol}",
        params={"timeframes": timeframes}
    )
    
    if response.status_code == 200:
        data = response.json()
        print_json(data, f"{symbol} マルチタイムフレーム分析")
        
        print(f"\n現在価格: ${data['current_price']:.2f}")
        print(f"全体的なトレンド: {data['overall_trend']}")
        print(f"コンセンサスシグナル: {data['consensus_signal']}")
        print(f"\n各時間足の分析:")
        for tf, analysis in data['analyses'].items():
            print(f"  {tf}: {analysis['direction']} (強度: {analysis['strength']:.0f}%)")
        return data
    else:
        print(f"❌ エラー: {response.status_code}")
        return None


def example_get_trading_signal(symbol="AAPL", timeframe="1h"):
    """例5: トレーディングシグナルを取得"""
    print(f"\n💡 {symbol}のトレーディングシグナルを生成中 ({timeframe})...")
    
    response = requests.get(
        f"{BASE_URL}/signals/{symbol}",
        params={"timeframe": timeframe}
    )
    
    if response.status_code == 200:
        data = response.json()
        print_json(data, f"{symbol} トレーディングシグナル ({timeframe})")
        
        print(f"\nシグナル: {data['signal']}")
        print(f"信頼度: {data['confidence']:.1f}%")
        print(f"エントリー価格: ${data['entry_price']:.2f}" if data.get('entry_price') else "")
        print(f"ストップロス: ${data['stop_loss']:.2f}" if data.get('stop_loss') else "")
        print(f"テイクプロフィット: ${data['take_profit']:.2f}" if data.get('take_profit') else "")
        print("\nシグナルの理由:")
        for reason in data['reasons']:
            print(f"  • {reason}")
        return data
    else:
        print(f"❌ エラー: {response.status_code}")
        return None


def example_get_news(limit=5):
    """例6: 最新ニュースを取得"""
    print(f"\n📰 最新ニュースを取得中...")
    
    response = requests.get(
        f"{BASE_URL}/news/latest",
        params={"limit": limit}
    )
    
    if response.status_code == 200:
        data = response.json()
        print_json(data, "最新ニュース")
        
        print(f"\n取得したニュース数: {len(data)}")
        for i, item in enumerate(data[:3], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   ソース: {item['source']}")
            print(f"   影響度: {item['impact']}")
            print(f"   センチメント: {item['sentiment']:.2f}")
            print(f"   公開日時: {item['published_at']}")
        return data
    else:
        print(f"❌ エラー: {response.status_code}")
        return None


def example_get_economic_calendar():
    """例7: 経済カレンダーを取得"""
    print(f"\n📅 経済カレンダーを取得中...")
    
    response = requests.get(f"{BASE_URL}/news/calendar")
    
    if response.status_code == 200:
        data = response.json()
        print_json(data, "経済カレンダー")
        
        print(f"\n予定されているイベント数: {len(data)}")
        for event in data:
            print(f"\n• {event['title']}")
            print(f"  国: {event['country']} | 通貨: {event['currency']}")
            print(f"  影響度: {event['impact']}")
            print(f"  予定時刻: {event['event_time']}")
            if event.get('forecast'):
                print(f"  予測値: {event['forecast']} | 前回値: {event['previous']}")
        return data
    else:
        print(f"❌ エラー: {response.status_code}")
        return None


def main():
    """メイン実行関数"""
    print("=" * 60)
    print(" Market Analysis System - API使用例")
    print("=" * 60)
    
    # 分析する銘柄
    symbol = "AAPL"  # Apple株
    # symbol = "USDJPY=X"  # USD/JPY為替
    # symbol = "BTC-USD"  # Bitcoin
    
    try:
        # 各APIの使用例を実行
        print(f"\n🎯 銘柄: {symbol}")
        
        # 1. リアルタイム価格
        example_get_quote(symbol)
        
        # 2. テクニカル指標
        example_get_indicators(symbol, "1h")
        
        # 3. トレンド分析
        example_get_trend(symbol, "1h")
        
        # 4. マルチタイムフレーム分析
        example_get_multi_timeframe(symbol)
        
        # 5. トレーディングシグナル
        example_get_trading_signal(symbol, "1h")
        
        # 6. 最新ニュース
        example_get_news(5)
        
        # 7. 経済カレンダー
        example_get_economic_calendar()
        
        print("\n" + "=" * 60)
        print(" ✅ すべての例が正常に実行されました！")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ エラー: APIサーバーに接続できません")
        print("バックエンドサーバーが起動しているか確認してください")
        print("起動方法: python -m app.main")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
