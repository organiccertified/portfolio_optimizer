@echo off
echo ========================================
echo   OPTIMIZED PORTFOLIO OPTIMIZER (CONDA)
echo ========================================
echo.

echo Step 1: Activating Anaconda environment...
call conda activate portfolio-optimizer
if %errorlevel% neq 0 (
    echo Creating new conda environment...
    conda create -n portfolio-optimizer python=3.11 -y
    call conda activate portfolio-optimizer
)

echo.
echo Step 2: Installing Python dependencies...
cd backend
pip install -r optimized_requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    echo Please check your conda environment.
    pause
    exit /b 1
)

echo.
echo Step 3: Starting Optimized Backend Server...
start "Backend (Conda)" cmd /k "conda activate portfolio-optimizer && cd backend && python optimized_app.py"

echo.
echo Step 4: Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo Step 5: Starting Frontend...
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
echo Environment: portfolio-optimizer (Conda)
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

