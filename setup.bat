@echo off
REM Job Search Automation System - Setup Script for Windows

echo 🚀 Setting up Job Search Automation System...
echo.

REM Check Python version
echo 📋 Checking Python version...
python --version

REM Create virtual environment
echo.
echo 🔧 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo.
echo ✨ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Install Playwright browsers
echo.
echo 🌐 Installing Playwright browsers...
playwright install chromium

REM Copy environment file
echo.
echo 📝 Setting up environment variables...
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file - please update with your settings
) else (
    echo ⚠️ .env file already exists, skipping...
)

REM Create necessary directories
echo.
echo 📁 Creating necessary directories...
if not exist data mkdir data
if not exist logs mkdir logs

echo.
echo ✅ Setup complete!
echo.
echo To start the application:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the application: python app.py
echo 3. Open your browser to: http://localhost:5000
echo.
pause
