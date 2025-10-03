# Fix: Path Resolution Error in Windows Launcher

## Problem
After compiling and installing on Windows:
- Black screen shows "MongoDB is running"
- Error: "Windows ne trouve pas C:\Program Files\Stock Management\scripts..\StockManagement.exe"
- The path stops at `C:\Program Files\Stock Management\scripts`

## Root Cause
The issue was with how Windows batch files resolve relative paths:

```batch
# WRONG - %~dp0 already has trailing backslash
start "" "%~dp0..\StockManagement.exe"
# Results in: C:\Program Files\Stock Management\scripts\..\StockManagement.exe
# Windows doesn't resolve this properly!
```

The `%~dp0` variable includes a trailing backslash:
- `%~dp0` = `C:\Program Files\Stock Management\scripts\`
- Adding `..\` results in `scripts\..\` which Windows can't resolve

## Solution

Use proper variable assignment to resolve the parent directory:

```batch
# CORRECT - Use intermediate variable
set "SCRIPT_DIR=%~dp0"
set "APP_DIR=%SCRIPT_DIR%.."
start "" "%APP_DIR%\StockManagement.exe"
# Results in properly resolved path!
```

## Files Fixed

### 1. launch_app.bat
**Before:**
```batch
start "" "%~dp0..\StockManagement.exe"
```

**After:**
```batch
set "SCRIPT_DIR=%~dp0"
set "APP_DIR=%SCRIPT_DIR%.."
start "" "%APP_DIR%\StockManagement.exe"
```

### 2. start_app.bat
**Before:**
```batch
start "" "%~dp0..\StockManagement.exe"
```

**After:**
```batch
set "SCRIPT_DIR=%~dp0"
set "APP_DIR=%SCRIPT_DIR%.."
start "" "%APP_DIR%\StockManagement.exe"
```

## Installation Structure

```
C:\Program Files\Stock Management\
├── StockManagement.exe          ← Target file
├── mongodb\
│   └── bin\
├── scripts\                      ← Scripts are here
│   ├── launch_app.bat           ← Must go UP to find exe
│   ├── start_app.bat
│   └── install_mongodb_service.bat
└── data\

C:\ProgramData\StockManagement\
├── db\                          ← MongoDB data
└── logs\
```

## How It Works Now

1. User clicks Start Menu shortcut
2. Windows runs: `C:\Program Files\Stock Management\scripts\launch_app.bat`
3. Script sets variables:
   - `SCRIPT_DIR` = `C:\Program Files\Stock Management\scripts\`
   - `APP_DIR` = `C:\Program Files\Stock Management\scripts\..`
4. Windows resolves `%APP_DIR%\StockManagement.exe` to:
   - `C:\Program Files\Stock Management\StockManagement.exe` ✓
5. Application launches successfully! 🎉

## Testing Steps

1. Pull latest changes from git
2. Rebuild Windows installer on Windows machine
3. Uninstall old version
4. Install new version
5. Click Start Menu → Stock Management
6. Application should launch without errors

## Verification

If you want to test the path resolution in a batch file:
```batch
@echo off
echo Script location: %~dp0
set "SCRIPT_DIR=%~dp0"
set "APP_DIR=%SCRIPT_DIR%.."
echo Parent directory: %APP_DIR%
echo Full exe path: %APP_DIR%\StockManagement.exe
pause
```

## Status
✅ Fixed and pushed to master branch
🔄 Needs to be recompiled on Windows
