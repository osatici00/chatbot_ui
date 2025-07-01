#!/bin/bash

echo "Starting ChatGPT UI Demo..."
echo

echo "Installing dependencies..."
echo

echo "Installing frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "Failed to install frontend dependencies"
    exit 1
fi

echo
echo "Installing backend dependencies..."
cd ../backend
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install backend dependencies"
    exit 1
fi

echo
echo "Starting services..."
echo

echo "Starting backend server on port 8001..."
python app.py &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting frontend server on port 3000..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo
echo "====================================================="
echo "  ChatGPT UI Demo is running!"
echo "  Backend:  http://localhost:8001"
echo "  Frontend: http://localhost:3000"
echo "====================================================="
echo
echo "Press Ctrl+C to stop all services"

# Trap ctrl-c and call cleanup
cleanup() {
    echo
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Services stopped."
    exit 0
}

trap cleanup INT

# Wait for processes
wait 