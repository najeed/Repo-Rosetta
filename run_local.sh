#!/bin/bash

echo "Starting Repo Rosetta Local (Non-Docker)..."

# Exit on any error
set -e

echo "[1/4] Installing/Verifying Python dependencies..."
python3 -m pip install -r backend/requirements.txt

echo "[2/4] Installing/Verifying Frontend dependencies..."
(cd frontend && npm install)

echo "[1/2] Launching Backend API..."
# Run backend in background
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "[2/2] Launching Frontend Dashboard..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=============================================="
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "=============================================="
echo "Press Ctrl+C to stop both servers."
echo ""

# Handle cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM EXIT

# Keep script running
wait
