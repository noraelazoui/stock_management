@echo off
REM =====================================
REM  Complete Windows Build Script
REM  Stock Management Application
REM =====================================

echo.
echo ========================================
echo   Stock Management - Windows Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo [ERROR] main.py not found!
    echo Please run this script from the stock_management directory.
    pause
    exit /b 1
)

echo [OK] Found main.py - we're in the right directory
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Install/upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Install PyInstaller
echo [INFO] Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install PyInstaller!
    pause
    exit /b 1
)
echo [OK] PyInstaller installed
echo.

REM Clean previous build
echo [INFO] Cleaning previous build...
if exist "dist\" rmdir /s /q dist
if exist "build\" rmdir /s /q build
echo [OK] Previous build cleaned
echo.

REM Build the executable
echo ========================================
echo   Building Windows Executable
echo ========================================
echo.
echo [INFO] Running PyInstaller...
echo This may take 2-5 minutes...
echo.

pyinstaller build_files\build_config.spec --clean

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] PyInstaller build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo [OK] Build completed!
echo.

REM Verify the executable was created
if not exist "dist\StockManagement\StockManagement.exe" (
    echo [ERROR] StockManagement.exe was not created!
    echo Check dist\StockManagement\ folder for contents.
    pause
    exit /b 1
)

echo [SUCCESS] StockManagement.exe created successfully!
echo.

REM Show file info
echo ========================================
echo   Build Information
echo ========================================
dir "dist\StockManagement\StockManagement.exe"
echo.

REM Check MongoDB
echo ========================================
echo   Checking MongoDB Files
echo ========================================
echo.

if not exist "mongodb\bin\mongod.exe" (
    echo [WARNING] MongoDB not found!
    echo.
    echo Please download MongoDB Community Server:
    echo https://www.mongodb.com/try/download/community
    echo.
    echo Extract the ZIP and place contents in:
    echo %CD%\mongodb\
    echo.
) else (
    echo [OK] MongoDB files found
)
echo.

REM Final instructions
echo ========================================
echo   Next Steps
echo ========================================
echo.
echo 1. If MongoDB warning above: Download and extract MongoDB
echo.
echo 2. Compile the installer:
echo    - Navigate to: build_files\
echo    - Right-click: installer_setup.iss
echo    - Click: Compile
echo.
echo 3. The installer will be created in:
echo    installer_output\StockManagement_Setup_v1.0.0.exe
echo.
echo 4. Test the installer:
echo    - Run the installer
echo    - Click Start Menu -^> Stock Management
echo    - Application should launch!
echo.
echo ========================================
echo   Build Complete! 
echo ========================================
echo.

pause
