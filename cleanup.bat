@echo off
echo Killing any lingering Ada processes...
taskkill /F /IM electron.exe /T 2>nul
taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM node.exe /T 2>nul
echo Cleaned up.
