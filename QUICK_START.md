# 🎯 クイックスタートガイド - 今すぐ試す！

## 🌐 最も簡単な方法: ブラウザで試す

### 1. APIドキュメントを開く
以下のURLをブラウザで開いてください：

**👉 https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/docs**

### 2. 試してみよう！

#### ステップ1: Apple株の価格を取得
1. 「market」セクションを展開
2. `GET /api/v1/market/quote/{symbol}` をクリック
3. 「Try it out」をクリック
4. `symbol` に `AAPL` と入力
5. 「Execute」をクリック
6. 結果を確認！

#### ステップ2: トレーディングシグナルを取得
1. 「signals」セクションを展開
2. `GET /api/v1/signals/{symbol}` をクリック
3. 「Try it out」をクリック
4. `symbol` に `AAPL` と入力
5. `timeframe` は `1h` のまま
6. 「Execute」をクリック
7. 買い/売りシグナルと理由を確認！

---

## 💻 コマンドラインで試す

### Apple株の現在価格
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/quote/AAPL"
```

### Bitcoinの価格
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/quote/BTC-USD"
```

### ドル円の為替レート
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/quote/USDJPY=X"
```

### トレーディングシグナル（買い/売りの推奨）
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/AAPL?timeframe=1h"
```

### テクニカル指標（RSI、MACDなど）
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/indicators/AAPL?timeframe=1h"
```

### トレンド分析
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/trend/AAPL?timeframe=1h"
```

### 最新ニュース
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/news/latest?limit=5"
```

### 経済カレンダー
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/news/calendar"
```

---

## 🐍 Pythonで試す

サンドボックス内で実行:

```bash
cd /home/user/webapp/examples
python api_usage.py
```

または、以下のコードを試してください:

```python
import requests
import json

# ベースURL
BASE_URL = "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1"

# Apple株の価格を取得
response = requests.get(f"{BASE_URL}/market/quote/AAPL")
data = response.json()

print(f"銘柄: {data['symbol']}")
print(f"価格: ${data['price']:.2f}")
print(f"変動: {data['change_percent']:.2f}%")
print(f"高値: ${data['high']:.2f}")
print(f"安値: ${data['low']:.2f}")

# トレーディングシグナルを取得
response = requests.get(f"{BASE_URL}/signals/AAPL", params={"timeframe": "1h"})
signal = response.json()

print(f"\nシグナル: {signal['signal']}")
print(f"信頼度: {signal['confidence']:.0f}%")
print(f"理由:")
for reason in signal['reasons']:
    print(f"  • {reason}")
```

---

## 📊 試せる銘柄リスト

### 米国株
- `AAPL` - Apple
- `MSFT` - Microsoft
- `GOOGL` - Google
- `AMZN` - Amazon
- `TSLA` - Tesla
- `META` - Meta (Facebook)
- `NVDA` - NVIDIA

### 為替
- `USDJPY=X` - ドル/円
- `EURUSD=X` - ユーロ/ドル
- `GBPUSD=X` - ポンド/ドル
- `AUDUSD=X` - 豪ドル/米ドル

### 暗号通貨
- `BTC-USD` - Bitcoin
- `ETH-USD` - Ethereum
- `BNB-USD` - Binance Coin

---

## 🎯 おすすめの使い方

### 1. まず価格をチェック
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/quote/AAPL"
```

### 2. テクニカル指標を確認
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/indicators/AAPL?timeframe=1h"
```
RSIが70以上なら買われすぎ、30以下なら売られすぎ！

### 3. トレーディングシグナルをチェック
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/AAPL?timeframe=1h"
```
買い/売りの推奨が表示されます！

### 4. マルチタイムフレームで総合判断
```bash
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/multi-timeframe/AAPL?timeframes=15m&timeframes=1h&timeframes=4h&timeframes=1d"
```

---

## 🔍 各エンドポイントの説明

### 📈 市場データ
- **/market/quote/{symbol}** - リアルタイム価格、高値、安値、出来高
- **/market/indicators/{symbol}** - RSI、MACD、ボリンジャーバンドなど13種類
- **/market/trend/{symbol}** - トレンド方向、強度、サポート/レジスタンス
- **/market/multi-timeframe/{symbol}** - 複数時間足の同時分析

### 💡 シグナル
- **/signals/{symbol}** - 買い/売りシグナルと信頼度、エントリー価格

### 📰 ニュース
- **/news/latest** - 最新市場ニュース
- **/news/sentiment/{symbol}** - ニュースセンチメント分析
- **/news/calendar** - 経済カレンダー（重要イベント）

---

## 🎮 インタラクティブに試す

### Swagger UI（最もおすすめ）
https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/docs

**できること:**
- ✅ ブラウザから直接APIを実行
- ✅ パラメータを簡単に変更
- ✅ レスポンスをリアルタイムで確認
- ✅ コード例を自動生成

### ReDoc（見やすいドキュメント）
https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/redoc

**できること:**
- ✅ 全APIの詳細仕様を閲覧
- ✅ データモデルの確認
- ✅ エラーコードの説明

---

## 📱 簡単な使用例

### 例1: Appleが買い時かチェック
```bash
# ステップ1: 現在価格を確認
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/quote/AAPL"

# ステップ2: シグナルを確認
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/AAPL?timeframe=1h"
```

### 例2: ビットコインのトレンドを分析
```bash
# トレンド分析
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/market/trend/BTC-USD?timeframe=1h"
```

### 例3: 複数銘柄を比較
```bash
# Apple
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/AAPL?timeframe=1h"

# Microsoft
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/MSFT?timeframe=1h"

# Tesla
curl "https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/api/v1/signals/TSLA?timeframe=1h"
```

---

## 🧪 総合テストを実行

サンドボックス内で全機能をテスト:

```bash
cd /home/user/webapp
python test_api.py
```

これで8つの主要機能すべてをテストできます！

---

## 💡 ヒント

1. **Swagger UIが一番簡単**: ブラウザで `/docs` を開くだけ
2. **JSON を見やすく**: コマンドの最後に `| python3 -m json.tool` を追加
3. **複数試す**: 異なる銘柄、時間足で試してみてください
4. **ニュースも確認**: `/news/latest` で市場の雰囲気をチェック

---

## 🎉 今すぐ試してみよう！

**👉 https://8000-ipiyu6278hxw01fehjgee-5185f4aa.sandbox.novita.ai/docs**

ブラウザでこのURLを開いて、すぐに始められます！
