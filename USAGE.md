# リアルタイム市場分析システム - 使用方法

## 🎯 システム概要

市場のリアルタイム分析ができる包括的なトレーディングプラットフォームです。ファンダメンタル分析とテクニカル分析の両方に対応しています。

## 🚀 クイックスタート

### バックエンドサーバーが起動中！

✅ **バックエンドAPI**: https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai

### 主要エンドポイント

#### 📊 市場データ
```bash
# リアルタイム価格取得（Apple株の例）
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/quote/AAPL"

# テクニカル指標の取得
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/indicators/AAPL?timeframe=1h"

# トレンド分析
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/trend/AAPL?timeframe=1h"

# マルチタイムフレーム分析
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/multi-timeframe/AAPL?timeframes=15m&timeframes=1h&timeframes=4h&timeframes=1d"
```

#### 💡 トレーディングシグナル
```bash
# シグナル生成
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/AAPL?timeframe=1h"
```

#### 📰 ニュース・イベント
```bash
# 最新ニュース取得
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/news/latest?limit=10"

# センチメント分析
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/news/sentiment/AAPL"

# 経済カレンダー
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/news/calendar"
```

## 📚 APIドキュメント

インタラクティブなAPIドキュメントにアクセス:
- **Swagger UI**: https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/docs
- **ReDoc**: https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/redoc

## 🎨 主要機能

### 1. マルチタイムフレーム分析
- **対応時間足**: 1分、5分、15分、30分、1時間、4時間、日足、週足、月足
- **トレンド判定**: 上昇、下降、レンジ相場の自動判定
- **強度スコア**: 0-100のトレンド強度評価
- **サポート・レジスタンス**: 重要な価格レベルの自動検出

### 2. テクニカル指標（自動計算）
#### トレンド指標
- 単純移動平均線（SMA 20, 50, 200）
- 指数移動平均線（EMA 12, 26）

#### モメンタム指標
- RSI（Relative Strength Index）- 買われすぎ/売られすぎ判定
- MACD（Moving Average Convergence Divergence）
- ストキャスティクス

#### ボラティリティ指標
- ボリンジャーバンド
- ATR（Average True Range）

#### 出来高指標
- OBV（On-Balance Volume）
- VWAP（Volume Weighted Average Price）

### 3. トレーディングシグナル
- **シグナルタイプ**: 強い買い、買い、中立、売り、強い売り
- **信頼度スコア**: 0-100の信頼度評価
- **エントリー/エグジット**: 推奨エントリー価格、ストップロス、テイクプロフィット
- **根拠表示**: シグナル生成の理由を詳細に説明

### 4. ニュース・ファンダメンタル分析
- **最新ニュース**: 市場に影響を与えるニュースの自動収集
- **センチメント分析**: ニュースの感情分析（-1 to 1）
- **影響度評価**: Critical, High, Medium, Lowの4段階
- **経済カレンダー**: 重要な経済イベントのスケジュール

### 5. WebSocketリアルタイム配信
```javascript
// 市場データのリアルタイム配信
const ws = new WebSocket('wss://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/ws/market/AAPL');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Market update:', data);
};

// ニュース配信
const newsWs = new WebSocket('wss://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/ws/news');
```

## 💻 対応銘柄

### 株式
- **米国株**: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA など
- **日本株**: 7203.T (トヨタ), 9984.T (ソフトバンク) など

### 為替（Forex）
- USDJPY=X (ドル円)
- EURUSD=X (ユーロドル)
- GBPUSD=X (ポンドドル)
- AUDUSD=X (豪ドル米ドル)

### 暗号通貨
- BTC-USD (Bitcoin)
- ETH-USD (Ethereum)
- BNB-USD (Binance Coin)

## 📊 使用例

### Python
```python
import requests

# リアルタイム価格取得
response = requests.get(
    "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/quote/AAPL"
)
quote = response.json()
print(f"Price: ${quote['price']:.2f}")
print(f"Change: {quote['change_percent']:.2f}%")

# トレーディングシグナル取得
response = requests.get(
    "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/AAPL",
    params={"timeframe": "1h"}
)
signal = response.json()
print(f"Signal: {signal['signal']}")
print(f"Confidence: {signal['confidence']:.0f}%")
```

### JavaScript
```javascript
// リアルタイム価格取得
fetch('https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/quote/AAPL')
  .then(response => response.json())
  .then(data => {
    console.log(`Price: $${data.price.toFixed(2)}`);
    console.log(`Change: ${data.change_percent.toFixed(2)}%`);
  });

// マルチタイムフレーム分析
const timeframes = ['15m', '1h', '4h', '1d'];
const params = new URLSearchParams();
timeframes.forEach(tf => params.append('timeframes', tf));

fetch(`https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/multi-timeframe/AAPL?${params}`)
  .then(response => response.json())
  .then(data => {
    console.log(`Overall Trend: ${data.overall_trend}`);
    console.log(`Consensus Signal: ${data.consensus_signal}`);
  });
```

### cURL
```bash
# マルチタイムフレーム分析
curl -X GET \
  "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/multi-timeframe/AAPL?timeframes=15m&timeframes=1h&timeframes=4h&timeframes=1d" \
  | python3 -m json.tool

# トレーディングシグナル
curl -X GET \
  "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/AAPL?timeframe=1h" \
  | python3 -m json.tool
```

## 🔧 ローカル開発

### バックエンドのセットアップ
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

### フロントエンドのセットアップ
```bash
cd frontend
npm install
npm run dev
```

## 📝 技術スタック

### バックエンド
- **フレームワーク**: FastAPI 0.104
- **データ処理**: Pandas 2.3, NumPy 2.2
- **テクニカル分析**: pandas-ta 0.4.71
- **市場データ**: yfinance 0.2.59
- **WebSocket**: websockets 13.0+

### フロントエンド（準備中）
- React + TypeScript
- Material-UI
- Recharts / TradingView Charts
- WebSocket クライアント

## 🎓 学習リソース

### テクニカル分析の基礎
1. **RSI**: 14日間の価格変動から買われすぎ/売られすぎを判定
   - 70以上: 買われすぎ
   - 30以下: 売られすぎ

2. **MACD**: トレンドの転換点を検出
   - MACDラインがシグナルラインを上抜け: 買いシグナル
   - 下抜け: 売りシグナル

3. **ボリンジャーバンド**: 価格のボラティリティを可視化
   - 上限突破: 買われすぎの可能性
   - 下限突破: 売られすぎの可能性

### トレーディング戦略
- **トレンドフォロー**: トレンド方向に沿ってエントリー
- **逆張り**: RSIの極端な値でエントリー
- **ブレイクアウト**: サポート/レジスタンスの突破時にエントリー

## ⚠️ 免責事項

このシステムは教育・研究目的で提供されています。
- 実際の投資判断は自己責任で行ってください
- 過去のデータは将来の結果を保証するものではありません
- リスク管理を徹底してください

## 📞 サポート

問題が発生した場合:
1. APIドキュメント（/docs）を確認
2. GitHubのIssueで報告
3. ログファイル（data/backend.log）を確認

## 🔐 セキュリティ

本番環境で使用する場合:
- 環境変数でAPIキーを管理
- HTTPS を使用
- レート制限を実装
- 認証システムを追加

---

**Happy Trading! 📈**
