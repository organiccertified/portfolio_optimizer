@echo off
echo Starting Portfolio Optimizer...
echo.
echo Activating conda environment...
call conda activate portfolio-optimizer
echo.
echo Starting Backend Server...
start "Backend" cmd /k "conda activate portfolio-optimizer && cd backend && python app.py"
echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul
echo.
echo Starting Frontend...
start "Frontend" cmd /k "npm start"
echo.
echo Portfolio Optimizer is starting up!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
pause
