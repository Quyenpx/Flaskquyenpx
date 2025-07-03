@echo off
echo 🪟 Flask Multi Store - Windows Setup
echo ====================================

echo 🔍 Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo 📦 Installing Flask...
pip install flask

echo 🚀 Starting Flask application...
echo 🌐 Website will be available at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop
echo.

python app_with_templates.py

pause
