@echo off
REM Quick Build Script for Windows
REM Use this if you're building directly on Windows

echo ========================================
echo Stock Management - Windows Build Script
echo ========================================
echo.

REM Check Python installation
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/5] Installing build dependencies...
pip install -r requirements_build.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/5] Creating icon (if needed)...
if not exist "icon.ico" (
    echo Creating default icon...
    python -c "from PIL import Image, ImageDraw; img = Image.new('RGB', (256, 256), color=(33, 150, 243)); draw = ImageDraw.Draw(img); draw.text((80, 100), 'SM', fill=(255, 255, 255)); img.save('icon.ico')"
    if %errorlevel% equ 0 (
        echo Icon created: icon.ico
    ) else (
        echo Warning: Could not create icon, using default
    )
) else (
    echo Icon already exists: icon.ico
)

echo.
echo [3/5] Creating LICENSE.txt (if needed)...
if not exist "LICENSE.txt" (
    (
        echo Stock Management Application License
        echo.
        echo Copyright ^(c^) 2025 Your Company
        echo.
        echo This software is provided for use by authorized clients only.
        echo All rights reserved.
        echo.
        echo For support and updates, contact: support@yourcompany.com
    ) > LICENSE.txt
    echo LICENSE.txt created
) else (
    echo LICENSE.txt already exists
)

echo.
echo [4/5] Building executable with PyInstaller...
echo This may take several minutes...
pyinstaller --clean build_config.spec
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller build failed!
    pause
    exit /b 1
)

echo.
echo [5/5] Checking build output...
if exist "dist\StockManagement\StockManagement.exe" (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable created: dist\StockManagement\StockManagement.exe
    echo.
    echo Next steps:
    echo 1. Download MongoDB Windows binary
    echo 2. Extract to mongodb\ folder
    echo 3. Install Inno Setup
    echo 4. Compile installer_setup.iss
    echo.
    echo See DEPLOYMENT_GUIDE.md for details
    echo.
) else (
    echo [ERROR] Build completed but executable not found!
    pause
    exit /b 1
)

pause
