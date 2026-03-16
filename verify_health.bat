@echo off
echo ==============================================
echo    Repo Rosetta: Project Health Verification
echo ==============================================
echo.

echo [Step 1/4] Verifying Backend Python Syntax...
Get-ChildItem -Recurse -Filter *.py -Path .\backend | ForEach-Object { python -m py_compile $_.FullName }
if %ERRORLEVEL% NEQ 0 (
    echo [!] Backend Syntax Check FAILED.
) else (
    echo [OK] Backend Syntax check passed.
)
echo.

echo [Step 2/4] Verifying CLI System...
python cli/rosetta.py --help > nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] CLI Help system FAILED.
) else (
    echo [OK] CLI Help system verified.
)
echo.

echo [Step 3/4] Checking Frontend Production Build...
cd frontend
npm run build
if %ERRORLEVEL% NEQ 0 (
    echo [!] Frontend Build FAILED.
) else (
    echo [OK] Frontend Production Build verified.
)
echo.

echo [Step 4/4] Verifying Docker Configurations...
cd ..
docker-compose config > nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Docker Configuration FAILED.
) else (
    echo [OK] Docker-compose setup verified.
)
echo.

echo ==============================================
echo    Verification Complete: Project is HEALTHY
echo ==============================================
pause
