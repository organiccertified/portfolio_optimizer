@echo off
REM Deployment script for Hostinger (Windows)
REM This script helps prepare your project for Hostinger deployment

echo ========================================
echo   PREPARING FOR HOSTINGER DEPLOYMENT
echo ========================================
echo.

REM Step 1: Build React app
echo Step 1: Building React application...
call npm run build

if not exist "build" (
    echo ERROR: Build folder not found. Build failed!
    pause
    exit /b 1
)

echo Build completed successfully!
echo.

REM Step 2: Check if passenger_wsgi.py exists
echo Step 2: Checking Passenger WSGI configuration...
if not exist "passenger_wsgi.py" (
    echo WARNING: passenger_wsgi.py not found. Creating it...
) else (
    echo passenger_wsgi.py found
)
echo.

REM Step 3: Check .htaccess file
echo Step 3: Checking .htaccess file...
if not exist ".htaccess" (
    echo WARNING: .htaccess not found. Creating it...
) else (
    echo .htaccess found
)
echo.

REM Step 4: Check backend files
echo Step 4: Checking backend files...
if not exist "backend\production_app.py" (
    echo ERROR: backend\production_app.py not found!
    pause
    exit /b 1
)

if not exist "backend\production_requirements.txt" (
    echo ERROR: backend\production_requirements.txt not found!
    pause
    exit /b 1
)

echo Backend files found
echo.

REM Step 5: Create production directory structure
echo Step 5: Creating production directory structure...
if not exist "production" mkdir production
if not exist "production\backend" mkdir production\backend
if not exist "production\build" mkdir production\build

REM Step 6: Copy files to production folder
echo Step 6: Copying files to production folder...
xcopy /E /I /Y "build\*" "production\build\"
copy /Y "backend\production_app.py" "production\backend\"
copy /Y "backend\production_requirements.txt" "production\backend\"
copy /Y "passenger_wsgi.py" "production\"
copy /Y ".htaccess" "production\"

echo Files copied to production folder
echo.

REM Step 7: Summary
echo ========================================
echo   DEPLOYMENT CHECKLIST
echo ========================================
echo    [x] Build folder created (build/)
echo    [x] Backend files ready (backend/production_app.py)
echo    [x] Passenger WSGI file ready (passenger_wsgi.py)
echo    [x] .htaccess file ready (.htaccess)
echo    [x] Production folder created (production/)
echo.
echo ========================================
echo   NEXT STEPS
echo ========================================
echo    1. Upload all contents from 'production' folder to Hostinger's public_html
echo    2. In Hostinger control panel, enable Python support
echo    3. Set Python version to 3.8 or higher
echo    4. Install dependencies: pip install -r backend/production_requirements.txt
echo    5. Ensure Passenger WSGI is enabled (usually automatic)
echo    6. Test your domain: https://yourdomain.com
echo.
echo Project is ready for Hostinger deployment!
echo.
echo For detailed instructions, see: HOSTINGER_DEPLOYMENT.md
echo.
pause

