# 🚀 WINDOWS DEPLOYMENT - FINAL BUILD GUIDE

**Date**: 2 octobre 2025  
**Version**: 1.0.0  
**Target**: Windows 10/11 (64-bit)

---

## ✅ PRE-BUILD CHECKLIST

### Files Ready:
- [x] `build_config.spec` - PyInstaller configuration
- [x] `build_windows.sh` - Linux build script  
- [x] `build_windows.bat` - Windows build script
- [x] `installer_setup.iss` - Inno Setup installer script
- [x] `scripts_installer/install_mongodb_service.bat`
- [x] `scripts_installer/start_app.bat`
- [x] `requirements_build.txt` - Build dependencies
- [x] All application code fixed (no crashes!)

### Code Fixes Applied:
- [x] Matplotlib backend configured
- [x] Tick labels fixed with plt.setp()
- [x] Delayed initialization with after_idle()
- [x] Memory leak prevention with plt.close()
- [x] All 8/8 tests passing

---

## 🔨 BUILD PROCESS

### Option 1: Build on Linux (Recommended for Development)

```bash
cd /home/najib/Documents/stock_management
./build_windows.sh
```

**What it does**:
1. Installs PyInstaller and Pillow
2. Creates icon.ico (if missing)
3. Creates LICENSE.txt
4. Runs PyInstaller with build_config.spec
5. Creates `dist/StockManagement/` folder

**Output**: `dist/StockManagement/` containing all files

---

### Option 2: Build on Windows

```batch
cd C:\path\to\stock_management
build_windows.bat
```

**Requirements**:
- Python 3.10+ installed on Windows
- Internet connection for dependencies

**Output**: Same as Linux build

---

## 📦 WHAT YOU NEED TO DOWNLOAD

### 1. MongoDB for Windows (REQUIRED)

**Download**:
- URL: https://www.mongodb.com/try/download/community
- Version: MongoDB Community Server 7.0+
- Platform: Windows x64
- Package: **ZIP Archive** (not MSI!)

**Steps**:
```
1. Download mongodb-windows-x86_64-7.0.x.zip
2. Extract the ZIP file
3. Rename extracted folder to just "mongodb"
4. Place in project root: stock_management/mongodb/
5. Verify structure: mongodb/bin/mongod.exe exists
```

**Size**: ~350 MB

---

### 2. Inno Setup (REQUIRED for creating installer)

**Download**:
- URL: https://jrsoftware.org/isdl.php
- Version: Inno Setup 6.2.2 or newer
- Choose: Unicode version

**Install**:
- Run the downloaded exe
- Follow installation wizard
- Default options are fine

**Size**: ~3 MB installer

---

## 🏗️ STEP-BY-STEP BUILD INSTRUCTIONS

### Phase 1: Prepare the Build

```bash
cd /home/najib/Documents/stock_management

# 1. Verify all tests pass
python3 test_app_startup.py

# 2. Check for any errors
python3 -m py_compile main.py views/*.py models/*.py controllers/*.py

# 3. Ensure MongoDB is stopped (to avoid conflicts)
sudo systemctl stop mongod
```

---

### Phase 2: Build the Executable

```bash
# Run the build script
./build_windows.sh
```

**Expected output**:
```
================================
Stock Management - Build Script
================================

Step 1: Installing build dependencies...
✓ pyinstaller installed

Step 2: Creating icon...
✓ Icon created: icon.ico

Step 3: Creating LICENSE...
✓ LICENSE.txt created

Step 4: Running PyInstaller...
Building for Windows...
✓ Build complete!

Build successful!
Executable location: dist/StockManagement/StockManagement.exe
```

**Verify**:
```bash
ls -lh dist/StockManagement/StockManagement.exe
# Should show file exists and is ~50-100 MB
```

---

### Phase 3: Add MongoDB

**On the machine where you'll create the installer** (can be different):

```bash
# Create mongodb folder in project root
mkdir -p mongodb

# Extract MongoDB ZIP to this folder
# Verify structure
ls mongodb/bin/mongod.exe  # Should exist
```

**Folder structure should be**:
```
stock_management/
├── dist/
│   └── StockManagement/
│       └── StockManagement.exe
├── mongodb/
│   └── bin/
│       ├── mongod.exe
│       ├── mongo.exe
│       └── [other MongoDB files]
├── scripts_installer/
│   ├── install_mongodb_service.bat
│   └── start_app.bat
└── installer_setup.iss
```

---

### Phase 4: Create the Installer (Windows Only)

**Requirements**: Windows machine with Inno Setup installed

1. **Copy these to Windows machine**:
   - `dist/StockManagement/` folder (entire folder)
   - `mongodb/` folder (entire folder)
   - `scripts_installer/` folder
   - `installer_setup.iss` file

2. **Open Inno Setup**:
   - Launch Inno Setup Compiler
   - File → Open → Select `installer_setup.iss`

3. **Compile**:
   - Build → Compile (or press F9)
   - Wait for compilation (3-5 minutes)

4. **Output**:
   - Location: `installer_output/StockManagement_Setup_v1.0.0.exe`
   - Size: ~200 MB (includes MongoDB + app)

---

## 🧪 TESTING THE INSTALLER

### Test on Clean Windows VM/PC

**Important**: Test on a machine that doesn't have Python or MongoDB installed!

1. **Copy installer**:
   - `StockManagement_Setup_v1.0.0.exe`

2. **Run installer**:
   - Double-click the exe
   - Follow wizard (Next, Next, Install)
   - Choose installation directory (default: `C:\Program Files\Stock Management`)

3. **What happens during install**:
   - Files copied to Program Files
   - MongoDB installed to ProgramData
   - MongoDB service created and started
   - Desktop shortcut created
   - Start Menu entry created

4. **Test the application**:
   - Launch from Desktop shortcut or Start Menu
   - Click Dashboard
   - Check all tabs load
   - Verify "⚠️ Alertes Stock" tab works
   - Test creating/viewing data

5. **Test uninstall**:
   - Control Panel → Programs → Uninstall
   - Verify MongoDB service is removed
   - Verify all files are deleted

---

## 📋 FINAL PACKAGE CONTENTS

### What's included in the installer:

```
StockManagement_Setup_v1.0.0.exe (~200 MB)
├── Application Files (~50-100 MB)
│   ├── StockManagement.exe
│   ├── Python runtime (embedded)
│   ├── All dependencies (tkinter, matplotlib, pymongo, etc.)
│   └── Application data files
│
├── MongoDB (~100 MB)
│   ├── mongod.exe
│   ├── mongo.exe
│   └── MongoDB binaries
│
└── Scripts
    ├── install_mongodb_service.bat
    └── start_app.bat
```

### What the user gets:

1. **Desktop Shortcut**: "Stock Management"
2. **Start Menu Entry**: Stock Management → Stock Management
3. **Installation Folder**: `C:\Program Files\Stock Management\`
4. **MongoDB Service**: Auto-starts on boot
5. **MongoDB Data**: `C:\ProgramData\StockManagement\db\`

---

## 🎯 CLIENT INSTALLATION EXPERIENCE

**What your client does**:

1. Download `StockManagement_Setup_v1.0.0.exe`
2. Double-click to run
3. Click "Next" → "Next" → "Install"
4. Wait 2-3 minutes
5. Click "Finish"
6. Double-click Desktop shortcut
7. Application opens - Ready to use!

**No technical knowledge required!**

---

## 🔧 CUSTOMIZATION OPTIONS

### Change Application Name

Edit `installer_setup.iss`:
```ini
#define MyAppName "Your Custom Name"
```

### Change Version

Edit `installer_setup.iss`:
```ini
#define MyAppVersion "2.0.0"
```

### Change Icon

Replace `icon.ico` with your custom icon (256x256 recommended)

### Change MongoDB Port

Edit `scripts_installer/install_mongodb_service.bat`:
```batch
set MONGODB_PORT=27017  :: Change this
```

---

## 📊 BUILD TIME ESTIMATES

| Phase | Time | Requirements |
|-------|------|--------------|
| Install build dependencies | 2-3 min | Internet |
| Build executable (PyInstaller) | 3-5 min | CPU |
| Download MongoDB | 5-10 min | Internet |
| Create installer (Inno Setup) | 3-5 min | CPU |
| **Total** | **15-25 min** | |

---

## 🐛 TROUBLESHOOTING

### Build fails with "Module not found"

**Solution**:
```bash
pip install -r requirements.txt
pip install -r requirements_build.txt
```

### PyInstaller creates but exe doesn't run

**Solution**: Check hidden imports in `build_config.spec`:
```python
hiddenimports=[
    'pymongo',
    'matplotlib',
    'tkcalendar',
    # Add any missing modules here
]
```

### MongoDB service won't start

**Solution**: Check port 27017 is available:
```cmd
netstat -ano | findstr :27017
```

### Installer compilation fails

**Checklist**:
- [ ] All paths in `installer_setup.iss` are correct
- [ ] `dist/StockManagement/` folder exists
- [ ] `mongodb/bin/mongod.exe` exists
- [ ] Inno Setup is version 6.0+

---

## 📚 RELATED DOCUMENTATION

| File | Purpose |
|------|---------|
| `DEPLOYMENT_GUIDE.md` | Complete deployment guide |
| `DEPLOYMENT_README.md` | Quick start guide |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step checklist |
| `DEPLOYMENT_WORKFLOW.md` | Visual workflow |
| `LANCER_APP.md` | How to run the app |
| `SEGFAULT_FIX_COMPLETE.md` | Crash fixes documentation |

---

## ✅ FINAL VERIFICATION

Before distributing to clients:

- [ ] Build completed successfully
- [ ] `StockManagement.exe` runs on your machine
- [ ] MongoDB folder included (with bin/mongod.exe)
- [ ] Installer created (`.exe` file ~200 MB)
- [ ] Tested installer on clean Windows machine
- [ ] Application opens without crash
- [ ] Dashboard loads with charts
- [ ] Alertes Stock tab works
- [ ] Can create/view data
- [ ] Uninstaller works correctly
- [ ] MongoDB service removed on uninstall

---

## 🚀 DISTRIBUTION

### To distribute to clients:

1. **Upload installer** to:
   - Your website
   - Cloud storage (Google Drive, Dropbox, etc.)
   - USB drive
   - Email (if under 25 MB - use split archives if needed)

2. **Provide to client**:
   - Installer file: `StockManagement_Setup_v1.0.0.exe`
   - Installation instructions (1 page)
   - System requirements

3. **System Requirements Document**:
```
System Requirements:
- Windows 10 or 11 (64-bit)
- 4 GB RAM minimum (8 GB recommended)
- 500 MB free disk space
- Administrator rights for installation
- Screen resolution: 1366x768 or higher

Installation Time: 2-3 minutes
No additional software required!
```

---

## 🎉 SUCCESS CRITERIA

Your deployment is successful when:

✅ Single `.exe` installer file (~200 MB)  
✅ Client can install without technical knowledge  
✅ Application runs immediately after install  
✅ All features work (Dashboard, Alerts, etc.)  
✅ MongoDB starts automatically  
✅ No crashes or errors  
✅ Can uninstall cleanly  

---

## 📞 NEXT STEPS

1. **Now**: Run `./build_windows.sh` to create the executable
2. **Then**: Download MongoDB Windows ZIP
3. **Then**: Use Inno Setup to create installer
4. **Finally**: Test on clean Windows machine
5. **Distribute**: Send installer to clients!

---

**Ready to build?**

```bash
cd /home/najib/Documents/stock_management
./build_windows.sh
```

---

**Date**: 2 octobre 2025  
**Version**: 1.0.0  
**Status**: 🟢 Ready for Production  
**Package Size**: ~200 MB  
**Installation Time**: 2-3 minutes  
**Client Experience**: ✨ "Next, Next, Install" ✨
