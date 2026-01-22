@echo off
REM Detect IP Address, Update VS Code Settings, and Open Frontend in Browser

echo.
echo ========================================
echo    HotelOS Frontend Launcher
echo ========================================
echo.

REM Get the local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4 Address"') do (
    set IP=%%a
    goto :found_ip
)

:found_ip
REM Remove leading spaces from IP
set IP=%IP:~1%

echo Detected IP Address: %IP%
echo.

REM Update VS Code settings.json with the detected IP
echo Updating VS Code settings...
set SETTINGS_FILE=%APPDATA%\Code\User\settings.json
set MAIN_JS_FILE=%CD%\js\main.js
set PORT=5501

REM Use PowerShell to update the JSON settings, removing comments first
powershell -Command "$settingsPath = '%SETTINGS_FILE%'; $content = Get-Content $settingsPath -Raw; $content = $content -replace '//.*', ''; $settings = $content | ConvertFrom-Json; $settings.'liveServer.settings.host' = '%IP%'; $settings | ConvertTo-Json | Set-Content $settingsPath; Write-Host 'VS Code settings updated with IP: %IP%'"

REM Update main.js with the detected IP
echo Updating main.js API URLs...
powershell -Command "$mainJsPath = '%MAIN_JS_FILE%'; $content = Get-Content $mainJsPath -Raw; $content = $content -replace 'http://192\.168\.0\.\d+:8000', 'http://%IP%:8000'; Set-Content $mainJsPath $content; Write-Host 'main.js API URLs updated with IP: %IP%'"

echo.
echo Launching frontend...
echo Opening: http://%IP%:%PORT%
echo.

REM Open the URL in the default browser
start http://%IP%:%PORT%

echo.
echo ========================================
echo    Frontend opened in browser
echo ========================================
echo.
echo IP Address: %IP%
echo Port: %PORT%
echo.
pause
