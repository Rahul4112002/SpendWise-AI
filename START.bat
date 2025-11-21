@echo off
echo ========================================
echo PennyWise AI - InTech Problem Statement 1
echo Autonomous Financial Coaching Agent
echo ========================================
echo.

echo STEP 1: Starting Backend Server...
echo.
cd backend
start "PennyWise Backend" cmd /k ".venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak > nul

echo.
echo STEP 2: Starting Frontend Server...
echo.
cd ..\frontend
start "PennyWise Frontend" cmd /k "npm start"

echo.
echo ========================================
echo PennyWise AI is starting...
echo ========================================
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Frontend will be available at: http://localhost:3000
echo.
echo Please wait for both servers to start completely.
echo Your browser will open automatically.
echo.
echo To stop: Close both terminal windows
echo ========================================

pause
