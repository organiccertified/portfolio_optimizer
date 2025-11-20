#!/bin/bash

echo "========================================"
echo "   OPTIMIZED PORTFOLIO OPTIMIZER"
echo "========================================"
echo

echo "Step 1: Installing Python dependencies..."
cd backend
pip install -r optimized_requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    echo "Please make sure Python and pip are installed."
    exit 1
fi

echo
echo "Step 2: Starting Optimized Backend Server..."
python optimized_app.py &
BACKEND_PID=$!

echo
echo "Step 3: Waiting for backend to start..."
sleep 3

echo
echo "Step 4: Starting Frontend..."
cd ..
npm start &
FRONTEND_PID=$!

echo
echo "========================================"
echo "   SUCCESS! Optimized Portfolio Optimizer Started"
echo "========================================"
echo
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo
echo "Features:"
echo "- Advanced portfolio optimization"
echo "- Multiple selection strategies"
echo "- Real-time caching"
echo "- Enhanced UI/UX"
echo "- Comprehensive error handling"
echo
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait

