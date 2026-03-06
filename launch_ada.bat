@echo off
TITLE Launching Ada V2...
cd /d "c:\Users\sanjo\OneDrive\ada_v2-main"

echo [0/3] Cleaning up old processes...
call cleanup.bat

echo [1/3] Activating Virtual Environment...
call venv\Scripts\activate

echo [2/3] Ensuring Frontend is ready...
:: We use start /b to run npm run dev in the background if needed.
:: Note: If it's already running, it might skip, but this ensures it's available.
start /b cmd /c "npm run dev:server"

echo [3/3] Waking up Ada...
python launch_electron.py

pause
