@echo off
REM Run Django Server and Celery Worker
REM This script starts both the Django development server and the Celery worker

setlocal enabledelayedexpansion

REM Get the project directory
set PROJECT_DIR=%~dp0

REM Check if virtual environment exists
if not exist "%PROJECT_DIR%venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found at %PROJECT_DIR%venv
    echo Please create a virtual environment first with: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call "%PROJECT_DIR%venv\Scripts\activate.bat"

echo.
echo ============================================
echo Starting Hostel Management System
echo ============================================
echo.

REM Get local IP address from Wi-Fi adapter
REM For development, use 0.0.0.0 which binds to all interfaces
setlocal enabledelayedexpansion
set SERVER_IP=0.0.0.0

REM Try to get Wi-Fi adapter IP for display purposes
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /I "Wireless LAN adapter Wi-Fi" -A 5 ^| findstr "IPv4"') do (
    set WIFI_IP=%%a
    set WIFI_IP=!WIFI_IP: =!
    if not "!WIFI_IP!"=="" (
        set DISPLAY_IP=!WIFI_IP!
        goto :found_wifi
    )
)

:found_wifi
if "!DISPLAY_IP!"=="" (
    set DISPLAY_IP=localhost
)

REM Start Django development server in a new window
echo Starting Django development server on 0.0.0.0:8000...
echo You can access it at: http://!DISPLAY_IP!:8000
start "Django Server" cmd /k "cd /d %PROJECT_DIR% && python manage.py runserver 0.0.0.0:8000"

REM Wait a moment for the server to start
timeout /t 2

REM Start Celery worker in a new window
REM Using --pool=solo for Windows compatibility (synchronous pool instead of multiprocessing)
echo Starting Celery worker (Windows mode - synchronous)...
start "Celery Worker" cmd /k "cd /d %PROJECT_DIR% && celery -A backend worker -l info --pool=solo"

echo.
echo ============================================
echo Both services started successfully!
echo Django Server: http://!DISPLAY_IP!:8000
echo Celery Worker: Running in synchronous mode
echo ============================================
echo.
echo Press any key to close this window...
pause
