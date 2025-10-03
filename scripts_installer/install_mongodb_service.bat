@echo off
REM MongoDB Service Installation Script for Windows
REM This script installs MongoDB as a Windows service

SET APP_DIR=%~1
SET DATA_DIR=%PROGRAMDATA%\StockManagement

echo ========================================
echo Installing MongoDB Service
echo ========================================
echo.

REM Create data directories
echo Creating data directories...
if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
if not exist "%DATA_DIR%\db" mkdir "%DATA_DIR%\db"
if not exist "%DATA_DIR%\logs" mkdir "%DATA_DIR%\logs"

REM Create MongoDB config file
echo Creating MongoDB configuration...
(
echo systemLog:
echo   destination: file
echo   path: %DATA_DIR%\logs\mongodb.log
echo   logAppend: true
echo storage:
echo   dbPath: %DATA_DIR%\db
echo net:
echo   port: 27017
echo   bindIp: 127.0.0.1
) > "%APP_DIR%\mongodb\mongod.cfg"

REM Install MongoDB as service
echo Installing MongoDB as Windows service...
"%APP_DIR%\mongodb\bin\mongod.exe" --config "%APP_DIR%\mongodb\mongod.cfg" --install --serviceName "StockManagementMongoDB" --serviceDisplayName "Stock Management Database"

if %errorlevel% equ 0 (
    echo MongoDB service installed successfully!
) else (
    echo Failed to install MongoDB service.
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete
echo ========================================
exit /b 0
