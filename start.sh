#!/bin/bash

echo "========================================="
echo "Market Analysis System - Startup Script"
echo "========================================="
echo ""

# エラーが発生したら終了
set -e

# バックエンドのセットアップと起動
echo "🚀 Starting backend server..."
cd backend

# 仮想環境の確認
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# 仮想環境の有効化
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# 依存関係のインストール
echo "📥 Installing Python dependencies..."
pip install -q -r requirements.txt

# .envファイルの確認
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env file to add your API keys if needed"
fi

# データディレクトリの作成
mkdir -p ../data

# バックエンドをバックグラウンドで起動
echo "✅ Starting backend on http://localhost:8000"
python -m app.main > ../data/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# バックエンドが起動するまで待機
echo "⏳ Waiting for backend to start..."
sleep 5

# バックエンドのヘルスチェック
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running!"
else
    echo "❌ Backend failed to start. Check logs in data/backend.log"
    exit 1
fi

# フロントエンドのセットアップと起動
cd ../frontend

echo ""
echo "🎨 Starting frontend server..."

# node_modulesの確認
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# フロントエンドを起動
echo "✅ Starting frontend on http://localhost:5173"
npm run dev

# スクリプト終了時にバックエンドも停止
trap "echo '🛑 Stopping backend...'; kill $BACKEND_PID 2>/dev/null" EXIT
