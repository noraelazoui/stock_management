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

REM Launch the application
echo Launching application...
start "" "%~dp0StockManagement.exe"

exit
