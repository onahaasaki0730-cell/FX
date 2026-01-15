#!/usr/bin/env python3
"""
クイックテストスクリプト - 主要機能の動作確認
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    print("=" * 70)
    print(" 🧪 Market Analysis System - API動作確認")
    print("=" * 70)
    
    tests = [
        {
            "name": "📊 株式（AAPL）の価格取得",
            "url": f"{BASE_URL}/market/quote/AAPL",
            "check": lambda r: r['price'] > 0
        },
        {
            "name": "💱 為替（USDJPY）の価格取得",
            "url": f"{BASE_URL}/market/quote/USDJPY=X",
            "check": lambda r: r['price'] > 0
        },
        {
            "name": "₿ 暗号通貨（BTC）の価格取得",
            "url": f"{BASE_URL}/market/quote/BTC-USD",
            "check": lambda r: r['price'] > 0
        },
        {
            "name": "📈 テクニカル指標計算",
            "url": f"{BASE_URL}/market/indicators/AAPL?timeframe=1h",
            "check": lambda r: r['rsi'] is not None
        },
        {
            "name": "📊 トレンド分析",
            "url": f"{BASE_URL}/market/trend/AAPL?timeframe=1h",
            "check": lambda r: r['direction'] in ['bullish', 'bearish', 'sideways', 'unknown']
        },
        {
            "name": "💡 トレーディングシグナル",
            "url": f"{BASE_URL}/signals/AAPL?timeframe=1h",
            "check": lambda r: r['confidence'] >= 0 and r['confidence'] <= 100
        },
        {
            "name": "📰 最新ニュース取得",
            "url": f"{BASE_URL}/news/latest?limit=3",
            "check": lambda r: len(r) > 0
        },
        {
            "name": "📅 経済カレンダー",
            "url": f"{BASE_URL}/news/calendar",
            "check": lambda r: len(r) > 0
        },
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            print(f"\n{'─' * 70}")
            print(f"テスト: {test['name']}")
            print(f"URL: {test['url']}")
            
            response = requests.get(test['url'], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if test['check'](data):
                    print("✅ 成功")
                    passed += 1
                else:
                    print("❌ 失敗: チェック条件を満たしていません")
                    failed += 1
            else:
                print(f"❌ 失敗: HTTPステータス {response.status_code}")
                failed += 1
                
        except Exception as e:
            print(f"❌ 失敗: {str(e)}")
            failed += 1
    
    print(f"\n{'=' * 70}")
    print(f" 📊 テスト結果")
    print(f"{'=' * 70}")
    print(f"✅ 成功: {passed}")
    print(f"❌ 失敗: {failed}")
    print(f"📈 成功率: {passed / (passed + failed) * 100:.1f}%")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 すべてのテストが正常に完了しました！")
    else:
        print(f"\n⚠️  {failed}個のテストが失敗しました。")
    
    return failed == 0


if __name__ == "__main__":
    import sys
    success = test_api()
    sys.exit(0 if success else 1)
