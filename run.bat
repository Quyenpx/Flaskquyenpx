@echo off
echo 🚀 Flask Multi Store - Quick Start
echo ================================

echo 📦 Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo 📦 Installing Flask...
pip install flask flask-sqlalchemy

echo 🚀 Starting application...
python quick_start.py

pause
