@echo off
REM ====================================================================
REM  Stock Management - Installer Creation Script for Windows
REM  Run this script on Windows after installing Inno Setup
REM ====================================================================

echo.
echo ====================================================================
echo   Stock Management - Creating Installer
echo ====================================================================
echo.

REM Show current directory
echo Current directory: %CD%
echo.

REM Check for files
echo Checking for required files...
if exist "installer_setup.iss" (
    echo [OK] installer_setup.iss found
) else (
    echo [ERROR] installer_setup.iss NOT FOUND!
)

if exist "dist\StockManagement" (
    echo [OK] dist\StockManagement found
) else (
    echo [ERROR] dist\StockManagement NOT FOUND!
)

if exist "mongodb" (
    echo [OK] mongodb folder found
) else (
    echo [ERROR] mongodb folder NOT FOUND!
)

if exist "scripts_installer" (
    echo [OK] scripts_installer found
) else (
    echo [ERROR] scripts_installer NOT FOUND!
)

echo.

REM Check if installer script exists
if not exist "installer_setup.iss" (
    echo ERROR: installer_setup.iss not found in current directory!
    echo.
    echo Please make sure you:
    echo 1. Extracted windows_package.zip completely
    echo 2. Are running this script FROM the extracted folder
    echo.
    pause
    exit /b 1
)

REM Check if Inno Setup is installed (try multiple locations)
set INNO_PATH=
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set INNO_PATH=C:\Program Files ^(x86^)\Inno Setup 6\ISCC.exe
)
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe
)

if "%INNO_PATH%"=="" (
    echo ERROR: Inno Setup not found!
    echo.
    echo Searched in:
    echo   - C:\Program Files (x86)\Inno Setup 6\
    echo   - C:\Program Files\Inno Setup 6\
    echo.
    echo Please install Inno Setup from: https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 1
)

echo Found Inno Setup at: %INNO_PATH%
echo.

REM Create output directory
if not exist "installer_output" mkdir installer_output

echo Creating installer...
echo.

REM Compile the installer
"%INNO_PATH%" "installer_setup.iss"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================================
    echo   SUCCESS! Installer created successfully!
    echo ====================================================================
    echo.
    echo Output: installer_output\StockManagement_Setup_v1.0.0.exe
    echo Size: ~200 MB
    echo.
    echo You can now distribute this installer to your clients!
    echo.
    echo Client installation: Just double-click and follow Next, Next, Install
    echo.
) else (
    echo.
    echo ====================================================================
    echo   ERROR: Installer creation failed!
    echo ====================================================================
    echo.
    echo Please check the error messages above.
    echo.
)

pause
