#!/bin/bash
# Deployment script for PythonAnywhere
# This script helps prepare your project for deployment

echo "🚀 Preparing Portfolio Optimizer for PythonAnywhere deployment..."
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

# Step 2: Check if wsgi.py exists
echo "📝 Step 2: Checking WSGI configuration..."
if [ ! -f "wsgi.py" ]; then
    echo "⚠️  Warning: wsgi.py not found. Please create it manually."
    echo "   See PYTHONANYWHERE_DEPLOYMENT.md for instructions."
else
    echo "✅ wsgi.py found"
    echo "⚠️  Remember to update the username in wsgi.py!"
fi
echo ""

# Step 3: Check backend files
echo "🔍 Step 3: Checking backend files..."
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

# Step 4: Summary
echo "📋 Deployment Checklist:"
echo "   [ ] Build folder created (build/)"
echo "   [ ] Backend files ready (backend/production_app.py)"
echo "   [ ] WSGI file configured (wsgi.py) - UPDATE USERNAME!"
echo "   [ ] Upload files to PythonAnywhere"
echo "   [ ] Install dependencies: pip install --user -r backend/production_requirements.txt"
echo "   [ ] Configure web app in PythonAnywhere dashboard"
echo "   [ ] Set static file mappings"
echo "   [ ] Reload web app"
echo ""
echo "✅ Project is ready for deployment!"
echo ""
echo "📖 For detailed instructions, see: PYTHONANYWHERE_DEPLOYMENT.md"

