# Complete Windows Build Guide

## ⚠️ IMPORTANT: Build MUST Be Done on Windows!

The executable in `dist/` was built on Linux and **will NOT work** on Windows!
You MUST rebuild on a Windows machine.

---

## 📋 Prerequisites (Install on Windows)

1. **Python 3.10+** - https://www.python.org/downloads/
   - ☑ Check "Add Python to PATH" during installation
   
2. **Git** - https://git-scm.com/download/win
   
3. **Inno Setup 6** - https://jrsoftware.org/isdl.php

---

## 🚀 Step-by-Step Build Process

### Step 1: Clone Repository on Windows

Open **PowerShell** or **Command Prompt** and run:

```powershell
cd C:\Users\YourName\Documents
git clone https://github.com/noraelazoui/stock_management.git
cd stock_management
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
pip install pyinstaller
```

### Step 4: Build the Windows Executable

```powershell
# Method 1: Using the spec file
pyinstaller build_files\build_config.spec

# Method 2: Using the batch file
cd build_files
.\build_windows.bat
```

**This will create:** `dist\StockManagement\StockManagement.exe` ✅

### Step 5: Download MongoDB for Windows

1. Download MongoDB Community Server (Windows ZIP):
   https://www.mongodb.com/try/download/community

2. Extract to project folder:
   ```
   stock_management\mongodb\
   ```

### Step 6: Compile the Installer

1. Open File Explorer
2. Navigate to: `build_files\`
3. **Right-click** `installer_setup.iss`
4. Click **Compile**

**This will create:** `installer_output\StockManagement_Setup_v1.0.0.exe` 🎉

### Step 7: Test the Installer

1. Run `StockManagement_Setup_v1.0.0.exe`
2. Complete installation
3. Click **Start Menu** → **Stock Management**
4. Application should launch! ✅

---

## 🎯 Quick Build (Automated)

I've created an automated script for you. Just run:

```powershell
.\BUILD_COMPLETE_PACKAGE.bat
```

This will:
1. ✅ Check Python installation
2. ✅ Create virtual environment
3. ✅ Install dependencies
4. ✅ Build executable with PyInstaller
5. ✅ Verify the .exe was created
6. ✅ Show next steps for Inno Setup

---

## 📂 Expected Structure After Build

```
stock_management\
├── dist\
│   └── StockManagement\
│       └── StockManagement.exe          ← Must have .exe extension!
├── mongodb\
│   └── bin\
│       └── mongod.exe
├── scripts_installer\
│   ├── launch_app.bat
│   ├── start_app.bat
│   └── install_mongodb_service.bat
└── build_files\
    └── installer_setup.iss
```

---

## ✅ Verification Checklist

Before compiling the installer, verify:

- [ ] `dist\StockManagement\StockManagement.exe` exists (8-10 MB)
- [ ] File has `.exe` extension
- [ ] `mongodb\bin\mongod.exe` exists
- [ ] All `.bat` files are in `scripts_installer\`
- [ ] `build_files\installer_setup.iss` exists

---

## 🔧 Troubleshooting

### Problem: "Python not found"
**Solution:** Reinstall Python and check "Add to PATH"

### Problem: "pyinstaller not found"
**Solution:** 
```powershell
pip install pyinstaller
```

### Problem: "No .exe created"
**Solution:** Check `build\build.log` for errors

### Problem: "Inno Setup not found"
**Solution:** Install from https://jrsoftware.org/isdl.php

---

## 📦 Final Package

After successful build, you'll have:
- `installer_output\StockManagement_Setup_v1.0.0.exe` (~200-250 MB)

This is the **complete installer** ready to distribute to clients!

---

## 🎉 Success Criteria

Your build is successful when:
1. ✅ `StockManagement.exe` has `.exe` extension
2. ✅ Double-clicking the exe on Windows works
3. ✅ Installer compiles without errors
4. ✅ Installed app launches from Start Menu
5. ✅ Application connects to MongoDB and works

---

## 📞 Need Help?

If you encounter issues:
1. Check the error message carefully
2. Verify all prerequisites are installed
3. Make sure you're on Windows (not Linux!)
4. Check that all files have correct paths

Good luck! 🚀
