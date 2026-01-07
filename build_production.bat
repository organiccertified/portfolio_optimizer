@echo off
echo ========================================
echo   BUILDING PRODUCTION VERSION
echo ========================================
echo.

echo Step 1: Installing frontend dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies!
    pause
    exit /b 1
)

echo.
echo Step 2: Building React app for production...
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Failed to build React app!
    pause
    exit /b 1
)

echo.
echo Step 3: Creating production directory structure...
if not exist "production" mkdir production
if not exist "production\backend" mkdir production\backend
if not exist "production\build" mkdir production\build

echo.
echo Step 4: Copying production files...
xcopy /E /I /Y "build\*" "production\build\"
copy /Y "backend\production_app.py" "production\backend\"
copy /Y "backend\production_requirements.txt" "production\backend\"
if exist "passenger_wsgi.py" copy /Y "passenger_wsgi.py" "production\"
if exist ".htaccess" copy /Y ".htaccess" "production\"

echo.
echo Step 5: Creating deployment files...
echo # Portfolio Optimizer Production Build > production\README.md
echo. >> production\README.md
echo This is the production build of the Portfolio Optimizer. >> production\README.md
echo. >> production\README.md
echo To deploy: >> production\README.md
echo 1. Upload all files to your web server >> production\README.md
echo 2. Install Python dependencies: pip install -r backend/production_requirements.txt >> production\README.md
echo 3. Run: python backend/production_app.py >> production\README.md

echo.
echo ========================================
echo   PRODUCTION BUILD COMPLETED!
echo ========================================
echo.
echo Production files are in the 'production' folder.
echo Upload these files to your Hostinger hosting.
echo.
echo Next steps:
echo 1. Upload production folder contents to your domain
echo 2. Set up Python environment on Hostinger
echo 3. Install dependencies and run the app
echo.
pause

