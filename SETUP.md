# リアルタイム市場分析システム - セットアップガイド

## システム概要

このシステムは、市場のリアルタイム分析を提供する包括的なトレーディングプラットフォームです。

### 主要機能

1. **マルチタイムフレーム分析**
   - 複数の時間足（1分～月足）で同時分析
   - トレンド方向と強度の可視化
   - サポート・レジスタンスレベルの自動検出

2. **テクニカル分析**
   - 移動平均線（SMA、EMA）
   - MACD（Moving Average Convergence Divergence）
   - RSI（Relative Strength Index）
   - ストキャスティクス
   - ボリンジャーバンド
   - ATR（Average True Range）
   - OBV（On-Balance Volume）
   - VWAP（Volume Weighted Average Price）

3. **ファンダメンタル分析**
   - 経済ニュースの自動収集
   - ニュースセンチメント分析
   - 経済カレンダー
   - 重要イベントの影響予測

4. **トレーディングシグナル**
   - 買い/売りシグナルの自動生成
   - 信頼度スコアリング
   - エントリー価格、ストップロス、テイクプロフィットの提案

5. **リアルタイムダッシュボード**
   - レスポンシブなWebUI
   - 自動更新機能
   - カスタマイズ可能なレイアウト

## クイックスタート

### 1. バックエンドのセットアップ

```bash
# ディレクトリに移動
cd backend

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# Linux/Mac:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定（.env.exampleをコピー）
cp .env.example .env

# サーバーを起動
python -m app.main
```

バックエンドは `http://localhost:8000` で起動します。

### 2. フロントエンドのセットアップ

```bash
# 別のターミナルを開く
cd frontend

# 依存関係をインストール
npm install

# 開発サーバーを起動
npm run dev
```

フロントエンドは `http://localhost:5173` で起動します。

## 使用方法

### 1. 基本的な使い方

1. ブラウザで `http://localhost:5173` にアクセス
2. 銘柄シンボルを入力（例: AAPL, USDJPY, BTCUSD）
3. 「分析開始」ボタンをクリック
4. 各タブで異なる分析結果を確認

### 2. 対応している銘柄

- **株式**: AAPL, MSFT, GOOGL, TSLA, AMZN など
- **為替**: USDJPY=X, EURUSD=X, GBPUSD=X など
- **暗号通貨**: BTC-USD, ETH-USD など

※ Yahoo Financeのシンボル形式に準拠

### 3. API エンドポイント

#### 市場データ
- `GET /api/v1/market/quote/{symbol}` - リアルタイム価格
- `GET /api/v1/market/history/{symbol}` - 履歴データ
- `GET /api/v1/market/indicators/{symbol}` - テクニカル指標
- `GET /api/v1/market/trend/{symbol}` - トレンド分析
- `GET /api/v1/market/multi-timeframe/{symbol}` - マルチタイムフレーム分析

#### シグナル
- `GET /api/v1/signals/{symbol}` - トレーディングシグナル

#### ニュース
- `GET /api/v1/news/latest` - 最新ニュース
- `GET /api/v1/news/sentiment/{symbol}` - センチメント分析
- `GET /api/v1/news/calendar` - 経済カレンダー

#### WebSocket
- `ws://localhost:8000/ws/market/{symbol}` - リアルタイム市場データ配信
- `ws://localhost:8000/ws/news` - リアルタイムニュース配信

### 4. APIドキュメント

バックエンド起動後、以下のURLでインタラクティブなAPIドキュメントにアクセスできます:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 高度な設定

### 外部APIの設定

より正確なデータを取得するため、以下のAPIキーを`.env`ファイルに設定できます:

1. **Alpha Vantage** (株式・為替データ)
   - https://www.alphavantage.co/support/#api-key
   - `.env`に `ALPHA_VANTAGE_API_KEY=your_key` を追加

2. **NewsAPI** (ニュースデータ)
   - https://newsapi.org/register
   - `.env`に `NEWS_API_KEY=your_key` を追加

3. **Finnhub** (追加の市場データ)
   - https://finnhub.io/register
   - `.env`に `FINNHUB_API_KEY=your_key` を追加

### データベース設定

デフォルトはSQLiteですが、本番環境ではPostgreSQLを推奨:

```bash
# .envファイルで設定
DATABASE_URL=postgresql://user:password@localhost/market_analysis
```

### Redisキャッシュ

パフォーマンス向上のためRedisを使用できます:

```bash
# Redisをインストール
# Ubuntu/Debian:
sudo apt-get install redis-server

# Mac (Homebrew):
brew install redis

# Redisを起動
redis-server

# .envファイルで設定
REDIS_URL=redis://localhost:6379/0
```

## トラブルシューティング

### バックエンドが起動しない

1. Python 3.8以上がインストールされているか確認
2. 仮想環境が有効化されているか確認
3. すべての依存関係がインストールされているか確認

```bash
pip install -r requirements.txt --upgrade
```

### フロントエンドが起動しない

1. Node.js 16以上がインストールされているか確認
2. node_modulesを再インストール

```bash
rm -rf node_modules package-lock.json
npm install
```

### データが取得できない

1. インターネット接続を確認
2. 銘柄シンボルが正しいか確認（Yahoo Finance形式）
3. APIキーが正しく設定されているか確認（外部APIを使用している場合）

### CORS エラーが発生する

バックエンドの`app/core/config.py`で、フロントエンドのURLがCORS_ORIGINSに含まれているか確認してください。

## 開発ガイド

### カスタムインジケータの追加

`backend/app/services/market_data.py`の`calculate_indicators`メソッドを編集:

```python
# 新しいインジケータを追加
df['MY_INDICATOR'] = ta.my_indicator(df['Close'], ...)

# モデルに追加
indicators = TechnicalIndicators(
    ...
    my_indicator=float(latest['MY_INDICATOR']) if pd.notna(latest.get('MY_INDICATOR')) else None,
)
```

### 新しいデータソースの追加

`backend/app/services/`に新しいサービスファイルを作成し、APIエンドポイントを`backend/app/api/`に追加します。

## パフォーマンス最適化

### キャッシュの活用

```python
# Redisキャッシュを使用してAPIコール数を削減
from redis import Redis
redis_client = Redis.from_url(settings.REDIS_URL)
```

### バッチ処理

複数の銘柄を一度に分析する場合は、非同期処理を活用:

```python
import asyncio

symbols = ['AAPL', 'MSFT', 'GOOGL']
results = await asyncio.gather(*[
    market_service.get_quote(symbol) for symbol in symbols
])
```

## セキュリティ

### 本番環境へのデプロイ時の注意事項

1. **環境変数の保護**: APIキーなどの機密情報を環境変数で管理
2. **HTTPS の使用**: 本番環境では必ずHTTPSを使用
3. **レート制限**: API呼び出しにレート制限を実装
4. **認証**: ユーザー認証システムを追加（必要に応じて）

## ライセンス

MIT License

## サポート

問題が発生した場合は、GitHubのIssueセクションで報告してください。
