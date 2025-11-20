@echo off
echo ========================================
echo   OPTIMIZED PORTFOLIO OPTIMIZER
echo ========================================
echo.

echo Step 1: Installing Python dependencies...
cd backend
pip install -r optimized_requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Please make sure Python and pip are installed.
    pause
    exit /b 1
)

echo.
echo Step 2: Starting Optimized Backend Server...
start "Backend" cmd /k "cd backend && python optimized_app.py"

echo.
echo Step 3: Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo Step 4: Starting Frontend...
cd ..
start "Frontend" cmd /k "npm start"

echo.
echo ========================================
echo   SUCCESS! Optimized Portfolio Optimizer Started
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Features:
echo - Advanced portfolio optimization
echo - Multiple selection strategies
echo - Real-time caching
echo - Enhanced UI/UX
echo - Comprehensive error handling
echo.
echo The app will open in your browser automatically.
echo Close the backend and frontend windows to stop the servers.
echo.
pause
