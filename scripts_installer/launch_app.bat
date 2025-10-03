@echo off
REM Stock Management Application Launcher
REM This script ensures MongoDB is running before launching the app

echo ========================================
echo Stock Management Application
echo ========================================
echo.

REM Check if MongoDB service is running
echo Checking MongoDB service...
sc query "StockManagementMongoDB" | find "RUNNING" >nul

if %errorlevel% equ 0 (
    echo MongoDB service is running.
) else (
    echo MongoDB service is not running. Starting...
    net start StockManagementMongoDB
    if %errorlevel% neq 0 (
        echo ERROR: Failed to start MongoDB service.
        echo.
        echo Please contact support.
        pause
        exit /b 1
    )
    echo MongoDB service started successfully.
    REM Wait a moment for MongoDB to be fully ready
    timeout /t 2 /nobreak >nul
)

echo.
echo Launching Stock Management Application...
echo.

REM Launch the application (exe is in parent directory of scripts folder)
start "" "%~dp0..\StockManagement.exe"

REM Close this window after 2 seconds
timeout /t 2 /nobreak >nul
exit
