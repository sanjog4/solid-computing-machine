@echo off
TITLE Launching Web Ada...
cd /d "c:\Users\sanjo\OneDrive\ada_v2-main"

echo ========================================
echo    Launching Web Ada (Browser Version)
echo ========================================
echo.

:: Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

:: Kill any existing processes to avoid port conflicts
echo [1/4] Cleaning up old processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: Start Backend Server
echo [3/4] Starting Backend Server (Port 8000)...
start "Ada Backend" /min cmd /c "cd /d c:\Users\sanjo\OneDrive\ada_v2-main && venv\Scripts\python.exe backend\server.py"

echo Waiting for Backend to be ready...
:BACKEND_WAIT
timeout /t 2 /nobreak >nul
curl -s http://localhost:8000/status >nul
if %errorlevel% neq 0 (
    echo Backend not ready yet...
    goto BACKEND_WAIT
)
echo Backend is UP!

:: Open browser
echo.
echo [4/4] Launching Web Ada in your default browser...
start http://localhost:5173

echo.
echo ========================================
echo    Ada is now running!
echo ========================================
echo.
echo IMPORTANT: Keep the background windows open!
echo Closing them will stop the Ada servers.
echo.
echo To stop Ada, close the background server windows
echo.
pause
