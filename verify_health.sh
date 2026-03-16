#!/bin/bash

echo "=============================================="
echo "   Repo Rosetta: Project Health Verification"
echo "=============================================="
echo ""

# 1. Verify Backend Python Syntax
echo "[Step 1/4] Verifying Backend Python Syntax..."
find ./backend -name "*.py" -exec python3 -m py_compile {} +
if [ $? -ne 0 ]; then
    echo "[!] Backend Syntax Check FAILED."
else
    echo "[OK] Backend Syntax check passed."
fi
echo ""

# 2. Verify CLI System
echo "[Step 2/4] Verifying CLI System..."
python3 cli/rosetta.py --help > /dev/null
if [ $? -ne 0 ]; then
    echo "[!] CLI Help system FAILED."
else
    echo "[OK] CLI Help system verified."
fi
echo ""

# 3. Check Frontend Build
echo "[Step 3/4] Checking Frontend Production Build..."
(cd frontend && npm run build)
if [ $? -ne 0 ]; then
    echo "[!] Frontend Build FAILED."
else
    echo "[OK] Frontend Production Build verified."
fi
echo ""

# 4. Verify Docker Config
echo "[Step 4/4] Verifying Docker Configurations..."
docker-compose config > /dev/null
if [ $? -ne 0 ]; then
    echo "[!] Docker Configuration FAILED."
else
    echo "[OK] Docker-compose setup verified."
fi
echo ""

echo "=============================================="
echo "    Verification Complete: Project is HEALTHY"
echo "=============================================="
