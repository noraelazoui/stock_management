@echo off
REM Start Stock Management Application
REM This script starts MongoDB service and launches the application

echo Starting Stock Management...

REM Check if MongoDB service is running
sc query StockManagementMongoDB | find "RUNNING" > nul
if %errorlevel% neq 0 (
    echo Starting MongoDB service...
    net start StockManagementMongoDB
    timeout /t 3 /nobreak > nul
)

REM Get parent directory and launch application
echo Launching application...
set "SCRIPT_DIR=%~dp0"
set "APP_DIR=%SCRIPT_DIR%.."
start "" "%APP_DIR%\StockManagement.exe"

exit
