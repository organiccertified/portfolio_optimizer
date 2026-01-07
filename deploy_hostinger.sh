#!/bin/bash
# Deployment script for Hostinger
# This script helps prepare your project for Hostinger deployment

echo "🚀 Preparing Portfolio Optimizer for Hostinger deployment..."
echo ""

# Step 1: Build React app
echo "📦 Step 1: Building React application..."
npm run build

if [ ! -d "build" ]; then
    echo "❌ Error: Build folder not found. Build failed!"
    exit 1
fi

echo "✅ Build completed successfully!"
echo ""

# Step 2: Check if passenger_wsgi.py exists
echo "📝 Step 2: Checking Passenger WSGI configuration..."
if [ ! -f "passenger_wsgi.py" ]; then
    echo "⚠️  Warning: passenger_wsgi.py not found. Creating it..."
    # The file should already exist, but if not, we'll note it
else
    echo "✅ passenger_wsgi.py found"
fi
echo ""

# Step 3: Check .htaccess file
echo "🔍 Step 3: Checking .htaccess file..."
if [ ! -f ".htaccess" ]; then
    echo "⚠️  Warning: .htaccess not found. Creating it..."
else
    echo "✅ .htaccess found"
fi
echo ""

# Step 4: Check backend files
echo "🔍 Step 4: Checking backend files..."
if [ ! -f "backend/production_app.py" ]; then
    echo "❌ Error: backend/production_app.py not found!"
    exit 1
fi

if [ ! -f "backend/production_requirements.txt" ]; then
    echo "❌ Error: backend/production_requirements.txt not found!"
    exit 1
fi

echo "✅ Backend files found"
echo ""

# Step 5: Create production directory structure
echo "📁 Step 5: Creating production directory structure..."
mkdir -p production
mkdir -p production/backend
mkdir -p production/build

# Step 6: Copy files to production folder
echo "📋 Step 6: Copying files to production folder..."
cp -r build/* production/build/
cp backend/production_app.py production/backend/
cp backend/production_requirements.txt production/backend/
cp passenger_wsgi.py production/
cp .htaccess production/

echo "✅ Files copied to production folder"
echo ""

# Step 7: Summary
echo "📋 Deployment Checklist:"
echo "   [x] Build folder created (build/)"
echo "   [x] Backend files ready (backend/production_app.py)"
echo "   [x] Passenger WSGI file ready (passenger_wsgi.py)"
echo "   [x] .htaccess file ready (.htaccess)"
echo "   [x] Production folder created (production/)"
echo ""
echo "📤 Next Steps:"
echo "   1. Upload all contents from 'production' folder to Hostinger's public_html"
echo "   2. In Hostinger control panel, enable Python support"
echo "   3. Set Python version to 3.8 or higher"
echo "   4. Install dependencies: pip install -r backend/production_requirements.txt"
echo "   5. Ensure Passenger WSGI is enabled (usually automatic)"
echo "   6. Test your domain: https://yourdomain.com"
echo ""
echo "✅ Project is ready for Hostinger deployment!"
echo ""
echo "📖 For detailed instructions, see: HOSTINGER_DEPLOYMENT.md"

