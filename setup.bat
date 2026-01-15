@echo off
REM Setup Script for Hostel Management System
REM This script runs the initial setup command which creates:
REM - Admin group
REM - Hotel instance
REM - Admin user account
REM - System settings (tax and discount)

setlocal enabledelayedexpansion

REM Get the project directory
set PROJECT_DIR=%~dp0

REM Check if virtual environment exists
if not exist "%PROJECT_DIR%venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating one...
    python -m venv "%PROJECT_DIR%venv"
    if errorlevel 1 (
        echo Error: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)

REM Activate virtual environment
call "%PROJECT_DIR%venv\Scripts\activate.bat"

echo.
echo ============================================
echo Hostel Management System - Setup
echo ============================================
echo.
echo This script will help you set up:
echo   1. Admin Group
echo   2. Hotel Information
echo   3. Admin User Account
echo   4. System Settings (Tax and Discount)
echo.

REM Upgrade pip, setuptools, and wheel first
echo Upgrading pip, setuptools, and wheel...
cd /d %PROJECT_DIR%
python -m pip install --upgrade pip setuptools wheel

if errorlevel 1 (
    echo Error: Failed to upgrade pip/setuptools!
    pause
    exit /b 1
)

REM Install requirements
echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies!
    echo Please check your requirements.txt file
    pause
    exit /b 1
)

echo.
echo Running database migrations...
python manage.py migrate

if errorlevel 1 (
    echo Error: Migration failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Starting Setup Wizard...
echo ============================================
echo.

REM Run the setup command
python manage.py create_hotel

if errorlevel 1 (
    echo.
    echo Error: Setup command failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo You can now run the application with: run.bat
echo.
pause
