@echo off
echo ========================================
echo PennyWise AI - Quick Start Script
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.10+
    pause
    exit /b 1
)
echo ✓ Python found
echo.

echo Step 2: Checking Node.js installation...
node --version
if errorlevel 1 (
    echo ERROR: Node.js not found! Please install Node.js 16+
    pause
    exit /b 1
)
echo ✓ Node.js found
echo.

echo Step 3: Checking PostgreSQL...
psql --version
if errorlevel 1 (
    echo WARNING: PostgreSQL not found or not in PATH
    echo Please install PostgreSQL and create a database named 'pennywise'
    echo.
)
echo.

echo ========================================
echo Backend Setup
echo ========================================
cd backend

echo Creating virtual environment...
python -m venv venv
echo ✓ Virtual environment created
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo Checking for .env file...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit backend\.env and add:
    echo    - DATABASE_URL
    echo    - SECRET_KEY
    echo    - GROQ_API_KEY
    echo.
    pause
) else (
    echo ✓ .env file exists
)
echo.

echo Creating uploads directory...
if not exist uploads mkdir uploads
echo ✓ Uploads directory ready
echo.

echo ========================================
echo Frontend Setup
echo ========================================
cd ..\frontend

echo Installing Node.js dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node dependencies
    pause
    exit /b 1
)
echo ✓ Node dependencies installed
echo.

echo Checking for frontend .env file...
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo ✓ Frontend .env created
) else (
    echo ✓ .env file exists
)
echo.

cd ..

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env with your configuration
echo 2. Create PostgreSQL database: createdb pennywise
echo 3. Start backend: cd backend ^& venv\Scripts\activate ^& uvicorn app.main:app --reload
echo 4. Start frontend: cd frontend ^& npm start
echo.
echo Documentation:
echo - SETUP_GUIDE.md - Detailed setup instructions
echo - PROJECT_SUMMARY.md - Complete feature overview
echo - README.md - Project documentation
echo.
pause
