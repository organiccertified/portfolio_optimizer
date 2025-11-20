#!/bin/bash

echo "========================================"
echo "   SIMPLE PORTFOLIO OPTIMIZER"
echo "========================================"
echo

echo "Step 1: Installing Python dependencies..."
cd backend
pip install -r simple_requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    echo "Please make sure Python and pip are installed."
    exit 1
fi

echo
echo "Step 2: Starting Backend Server..."
python simple_app.py &
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
echo "   SUCCESS! Portfolio Optimizer Started"
echo "========================================"
echo
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait
