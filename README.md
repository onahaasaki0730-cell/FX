# リアルタイム市場分析システム

## 概要
市場のリアルタイム分析ができる包括的なトレーディングプラットフォーム。ファンダメンタル分析とテクニカル分析の両方に対応。

## 主要機能

### 1. マルチタイムフレーム分析
- 1分足、5分足、15分足、1時間足、4時間足、日足の同時分析
- 各時間足でのトレンド状況の可視化
- タイムフレーム間の相関分析

### 2. テクニカル指標分析
- **トレンド指標**: 移動平均線（SMA、EMA）、MACD
- **モメンタム指標**: RSI、Stochastic
- **ボラティリティ指標**: ボリンジャーバンド、ATR
- **出来高指標**: OBV、VWAP
- カスタマイズ可能なインジケータ設定

### 3. ニュース・経済指標分析
- 経済カレンダーとの連携
- ニュースセンチメント分析
- 重要イベントの市場影響予測
- リアルタイムニュースフィード

### 4. ファンダメンタル分析
- 経済指標の追跡
- 中央銀行政策の分析
- 地政学的イベントの影響評価

### 5. リアルタイムダッシュボード
- WebSocketによるリアルタイム更新
- インタラクティブなチャート
- カスタマイズ可能なレイアウト

## 技術スタック

### バックエンド
- **フレームワーク**: FastAPI
- **データ処理**: Pandas, NumPy
- **テクニカル分析**: TA-Lib, pandas-ta
- **データベース**: SQLite (開発), PostgreSQL (本番)
- **WebSocket**: FastAPI WebSocket
- **キャッシュ**: Redis

### フロントエンド
- **フレームワーク**: React + TypeScript
- **UI**: Material-UI
- **チャート**: TradingView Lightweight Charts, Recharts
- **状態管理**: Redux Toolkit
- **WebSocket**: Socket.io-client

### データソース
- **市場データ**: Alpha Vantage, Yahoo Finance
- **ニュース**: NewsAPI, RSS Feeds
- **経済カレンダー**: Trading Economics API

## セットアップ

### バックエンド
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

### フロントエンド
```bash
cd frontend
npm install
npm run dev
```

## 環境変数
`.env`ファイルを作成して以下を設定:
```
ALPHA_VANTAGE_API_KEY=your_api_key
NEWS_API_KEY=your_news_api_key
DATABASE_URL=sqlite:///./data/market_analysis.db
REDIS_URL=redis://localhost:6379
```

## API エンドポイント

### 市場データ
- `GET /api/v1/market/quote/{symbol}` - リアルタイム価格取得
- `GET /api/v1/market/history/{symbol}` - 履歴データ取得
- `GET /api/v1/market/multi-timeframe/{symbol}` - マルチタイムフレーム分析

### テクニカル分析
- `POST /api/v1/technical/indicators` - インジケータ計算
- `GET /api/v1/technical/signals/{symbol}` - トレーディングシグナル

### ニュース・イベント
- `GET /api/v1/news/latest` - 最新ニュース
- `GET /api/v1/news/sentiment/{symbol}` - センチメント分析
- `GET /api/v1/events/calendar` - 経済カレンダー
- `GET /api/v1/events/impact/{event_id}` - イベント影響予測

### WebSocket
- `ws://localhost:8000/ws/market/{symbol}` - リアルタイム市場データ
- `ws://localhost:8000/ws/news` - リアルタイムニュースフィード

## 使用例

### Python APIクライアント
```python
import requests

# マルチタイムフレーム分析
response = requests.get(
    "http://localhost:8000/api/v1/market/multi-timeframe/USDJPY",
    params={"timeframes": ["1m", "5m", "1h", "1d"]}
)
analysis = response.json()

# テクニカル指標
indicators_request = {
    "symbol": "USDJPY",
    "indicators": ["rsi", "macd", "bollinger_bands"],
    "timeframe": "1h"
}
response = requests.post(
    "http://localhost:8000/api/v1/technical/indicators",
    json=indicators_request
)
```

### WebSocket接続
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market/USDJPY');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Market update:', data);
};
```

## プロジェクト構造
```
.
├── backend/
│   ├── app/
│   │   ├── api/          # APIエンドポイント
│   │   ├── core/         # 設定・認証
│   │   ├── models/       # データモデル
│   │   ├── services/     # ビジネスロジック
│   │   └── utils/        # ユーティリティ
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/   # Reactコンポーネント
│   │   ├── services/     # API通信
│   │   ├── hooks/        # カスタムフック
│   │   └── utils/        # ユーティリティ
│   └── public/
├── data/                 # データベース・キャッシュ
└── config/              # 設定ファイル
```

## ライセンス
MIT License
