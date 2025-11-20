@echo off
echo ========================================
echo   PORTFOLIO OPTIMIZER (ANACONDA)
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
pip install -r simple_requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo Step 3: Starting Backend Server...
start "Backend" cmd /k "conda activate portfolio-optimizer && cd backend && python simple_app.py"

echo.
echo Step 4: Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo Step 5: Starting Frontend...
cd ..
start "Frontend" cmd /k "npm start"

echo.
echo ========================================
echo   SUCCESS! Portfolio Optimizer Started
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo The app will open in your browser automatically.
echo Close the backend and frontend windows to stop the servers.
echo.
pause
