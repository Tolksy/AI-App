@echo off
echo 🚀 Starting Smart AI Lead Generation Agent...
echo.

echo 📦 Installing frontend dependencies...
call npm install

echo.
echo 🤖 Starting Smart AI Backend...
cd backend
start "Smart AI Backend" cmd /k "python smart_main.py"
cd ..

echo.
echo ⏳ Waiting for AI to initialize...
timeout /t 3 /nobreak >nul

echo.
echo 🌐 Starting Frontend Interface...
start "Frontend Interface" cmd /k "npm run dev"

echo.
echo ✅ Smart AI Lead Generation Agent is starting...
echo.
echo 🎯 Access your intelligent app:
echo    Frontend: http://localhost:5173
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 🤖 Your AI agent is now ready for articulate conversations!
echo.
echo Press any key to exit this window...
pause >nul
