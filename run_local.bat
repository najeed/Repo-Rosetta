@echo off
echo Starting Repo Rosetta Local (Non-Docker)...

echo [1/4] Installing/Verifying Python dependencies...
python -m pip install -r backend/requirements.txt

echo [2/4] Installing/Verifying Frontend dependencies...
cd frontend
call npm install
cd ..

echo [1/2] Launching Backend API...
start cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Launching Frontend Dashboard...
cd frontend
start cmd /k "npm run dev"

echo.
echo ==============================================
echo    Backend: http://localhost:8000
echo    Frontend: http://localhost:3001
echo ==============================================
echo.
pause
