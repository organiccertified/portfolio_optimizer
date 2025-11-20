#!/bin/bash

echo "Starting Portfolio Optimizer..."
echo

echo "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate portfolio-optimizer

echo "Starting Backend Server..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to start..."
sleep 5

echo "Starting Frontend..."
npm start &
FRONTEND_PID=$!

echo
echo "Portfolio Optimizer is starting up!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait
