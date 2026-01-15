@echo off
echo =========================================
echo Market Analysis System - Startup Script
echo =========================================
echo.

cd backend

:: 仮想環境の確認
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: 仮想環境の有効化
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: 依存関係のインストール
echo Installing Python dependencies...
pip install -q -r requirements.txt

:: .envファイルの確認
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo Please edit backend\.env file to add your API keys if needed
)

:: データディレクトリの作成
if not exist "..\data" mkdir ..\data

:: バックエンドを起動
echo Starting backend on http://localhost:8000
start "Backend Server" cmd /c "python -m app.main > ..\data\backend.log 2>&1"

:: バックエンドが起動するまで待機
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

:: フロントエンドのセットアップと起動
cd ..\frontend

echo.
echo Starting frontend server...

:: node_modulesの確認
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

:: フロントエンドを起動
echo Starting frontend on http://localhost:5173
call npm run dev

pause
