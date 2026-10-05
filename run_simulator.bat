@echo off
REM Educational Bitcoin Mining Simulator - Windows Launcher
REM Double-click this file to run the simulator

echo ========================================
echo Educational Bitcoin Mining Simulator
echo ========================================
echo.
echo EDUCATIONAL ONLY - NO REAL BITCOIN
echo.
echo Starting simulator...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

REM Run the simulator
python main.py

REM If error occurred
if errorlevel 1 (
    echo.
    echo ERROR: The simulator encountered an error.
    echo.
    echo Please check:
    echo 1. All files are in the same folder
    echo 2. Python 3.7+ is installed
    echo 3. Tkinter is available
    echo.
    pause
)
