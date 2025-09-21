@echo off
echo.
echo ================================================
echo    AI LEAD GENERATION SYSTEM - STARTUP
echo ================================================
echo.

echo [1/3] Installing Python dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Starting Smart AI Backend...
echo Starting on http://localhost:8000
echo.
start "AI Backend" cmd /k "python smart_main.py"

echo.
echo [3/3] Starting Frontend Interface...
cd ..
npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo Starting on http://localhost:5173
echo.
start "Frontend" cmd /k "npm run dev"

echo.
echo ================================================
echo    SYSTEM STARTUP COMPLETE!
echo ================================================
echo.
echo Your AI Lead Generation System is starting up:
echo.
echo Backend (AI Brain):  http://localhost:8000
echo Frontend (Interface): http://localhost:5173
echo.
echo Features Available:
echo - Real LinkedIn Integration
echo - Advanced Lead Scoring  
echo - Web Scraping Capabilities
echo - Email Automation
echo - Real-Time Analytics
echo - Task Monitoring
echo - Smart AI Conversations
echo.
echo Wait for both windows to finish loading, then go to:
echo http://localhost:5173
echo.
echo Press any key to exit this window...
pause >nul
