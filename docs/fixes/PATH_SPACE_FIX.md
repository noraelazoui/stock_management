# Fix: Windows Path with Spaces Error

## Problem
When installing the application on Windows and clicking the Start Menu shortcut, users got:
- Black screen showing "MongoDB is running"
- Error popup: "Windows ne trouve pas C:\Programm...exe"

## Root Cause
The error occurred because:
1. The path `C:\Program Files\Stock Management\` contains spaces
2. The launcher scripts weren't correctly navigating from `scripts\` subdirectory to parent directory
3. Path wasn't properly quoted in some places

## Solution Applied

### 1. Fixed `launch_app.bat`
**Location:** `scripts_installer/launch_app.bat`

**Changes:**
- Corrected path to executable: `%~dp0..\StockManagement.exe`
- The `%~dp0` gives us the scripts directory
- Added `..\ ` to go up to parent directory where the exe is located
- Properly quoted all paths

### 2. Fixed `start_app.bat`
**Location:** `scripts_installer/start_app.bat`

**Changes:**
- Same fix: changed `%~dp0StockManagement.exe` to `%~dp0..\StockManagement.exe`

### 3. Restored `install_mongodb_service.bat`
**Location:** `scripts_installer/install_mongodb_service.bat`

**Changes:**
- Restored original version that uses `%PROGRAMDATA%\StockManagement` for data
- Removed dependency on non-existent `data_path.txt` file
- All paths properly quoted

## Installation Structure

```
C:\Program Files\Stock Management\
├── StockManagement.exe          ← Main application
├── mongodb\
│   └── bin\
│       └── mongod.exe
├── scripts\
│   ├── launch_app.bat           ← Start Menu/Desktop shortcut points here
│   ├── start_app.bat
│   └── install_mongodb_service.bat
└── (other files)

C:\ProgramData\StockManagement\   ← MongoDB data location
├── db\
└── logs\
```

## How Shortcuts Work Now

1. User clicks Start Menu or Desktop shortcut
2. Shortcut runs: `C:\Program Files\Stock Management\scripts\launch_app.bat`
3. Script checks/starts MongoDB service
4. Script navigates to parent directory: `%~dp0..`
5. Script launches: `C:\Program Files\Stock Management\StockManagement.exe`
6. Application starts successfully!

## Testing Steps

After rebuilding and reinstalling:

1. ✓ Uninstall old version
2. ✓ Compile new installer with fixed scripts
3. ✓ Install new version
4. ✓ Click Start Menu → Stock Management
5. ✓ Application should launch without errors
6. ✓ No "ne trouve pas" error

## Files Modified

- `scripts_installer/launch_app.bat` - Fixed path
- `scripts_installer/start_app.bat` - Fixed path  
- `scripts_installer/install_mongodb_service.bat` - Restored correct version

## Status
✅ Fixed - Ready for deployment
