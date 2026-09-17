@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==============================
echo   Travel Price Finder
echo ==============================
echo.
pip install -q fastapi uvicorn 2>nul
echo Starting server on http://localhost:8080 ...
start "" "http://localhost:8080"
python app.py
pause
