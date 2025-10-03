# Stock Management - Windows Deployment Quick Start

## 🎯 Goal
Create a single `.exe` installer that includes everything:
- ✅ Python application
- ✅ MongoDB database
- ✅ All dependencies
- ✅ "Next, Next, Install" experience

## 🚀 Quick Start (3 Options)

### Option A: Build on Linux → Transfer to Windows → Create Installer

```bash
# On Linux
cd /home/najib/Documents/stock_management
./build_windows.sh

# Transfer to Windows:
# - dist/StockManagement/
# - All other files

# On Windows:
# - Download MongoDB
# - Use Inno Setup to compile
```

### Option B: Build Everything on Windows

```batch
# On Windows
cd C:\path\to\stock_management
build_windows.bat

# Then:
# - Download MongoDB
# - Use Inno Setup to compile
```

### Option C: Use Pre-built Components

If someone already built the application:
1. Get `dist/StockManagement/` folder
2. Download MongoDB
3. Use Inno Setup

## 📥 What You Need to Download

### 1. MongoDB for Windows
**URL**: https://www.mongodb.com/try/download/community

**Settings**:
- Version: 7.0 (or latest stable)
- Platform: Windows x64
- Package: **ZIP** (not MSI)

**Download Size**: ~50 MB

**After Download**:
```
Extract to: stock_management/mongodb/
Should contain: mongodb/bin/mongod.exe
```

### 2. Inno Setup (Windows Only)
**URL**: https://jrsoftware.org/isdl.php

**Download**: InnoSetup-6.x.x.exe

**Install**: Run installer, use default settings

**Size**: ~2 MB

## 📋 File Checklist

Before creating the installer, you need:

```
✓ dist/StockManagement/          (from PyInstaller)
✓ mongodb/bin/                    (from MongoDB download)
✓ scripts_installer/              (already in project)
✓ icon.ico                        (created by build script)
✓ LICENSE.txt                     (created by build script)
✓ README.md                       (this file)
✓ installer_setup.iss             (already in project)
```

## 🔨 Building Step-by-Step

### Step 1: Build Python Application

**On Linux**:
```bash
./build_windows.sh
```

**On Windows**:
```batch
build_windows.bat
```

**Output**: `dist/StockManagement/` folder

**Time**: 2-5 minutes

### Step 2: Add MongoDB

1. Download MongoDB ZIP from link above
2. Extract the ZIP file
3. Copy the entire extracted folder to: `mongodb/`
4. Verify `mongodb/bin/mongod.exe` exists

### Step 3: Create Installer

**On Windows**:

1. Open **Inno Setup Compiler**
2. Click **File → Open**
3. Select `installer_setup.iss`
4. Click **Build → Compile**
5. Wait 2-5 minutes

**Output**: `installer_output/StockManagement_Setup_v1.0.0.exe`

**Size**: ~150-200 MB

## ✅ Test Before Distribution

### Test Installation:

1. **Use a clean Windows VM** (Windows 10 or 11)
2. **Run installer**: `StockManagement_Setup_v1.0.0.exe`
3. **Click through**: Next → Accept → Install
4. **Verify**:
   - Application launches
   - MongoDB service is running
   - Can create/view data
   - Desktop shortcut works
   - Start Menu shortcut works

### Test Uninstallation:

1. **Open**: Control Panel → Programs and Features
2. **Find**: Stock Management
3. **Uninstall**: Follow wizard
4. **Verify**:
   - Files are removed
   - MongoDB service is removed
   - Shortcuts are removed

## 📦 What Your Client Gets

**Single File**: `StockManagement_Setup_v1.0.0.exe`

**Installation Experience**:
```
1. Double-click installer
2. Accept license
3. Choose location (optional)
4. Click Install
5. Done! Application opens
```

**No Other Requirements**:
- ❌ No Python installation
- ❌ No MongoDB installation
- ❌ No environment setup
- ❌ No configuration
- ✅ Just works!

## 🐛 Common Issues

### Build Fails: "Module not found"

**Solution**:
```bash
pip install -r requirements_build.txt
```

### Installer Compilation Fails

**Check**:
- All files in correct locations
- MongoDB files exist in `mongodb/bin/`
- Inno Setup is installed

### Application Won't Start

**Check**:
- Run installer as Administrator
- MongoDB service is running (Services → Stock Management Database)
- Check logs in `C:\ProgramData\StockManagement\logs\`

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| `DEPLOYMENT_GUIDE.md` | Complete detailed guide |
| `DEPLOYMENT_README.md` | This quick start guide |
| `build_config.spec` | PyInstaller configuration |
| `installer_setup.iss` | Inno Setup script |
| `build_windows.sh` | Linux build script |
| `build_windows.bat` | Windows build script |

## 🎓 Learning Resources

- **PyInstaller**: https://pyinstaller.org/en/stable/
- **Inno Setup**: https://jrsoftware.org/ishelp/
- **MongoDB on Windows**: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/

## 💬 Support

For questions or issues:

1. Check `DEPLOYMENT_GUIDE.md` for detailed instructions
2. Review troubleshooting section
3. Check logs in application folder

## 🎉 Success Criteria

Your deployment is successful when:

✅ Single installer file created  
✅ Installer runs on clean Windows 10/11  
✅ No errors during installation  
✅ Application launches automatically  
✅ MongoDB service starts  
✅ Can create and view data  
✅ Uninstaller works cleanly  

## 📊 Quick Reference

| Task | Command/Tool |
|------|--------------|
| Build app (Linux) | `./build_windows.sh` |
| Build app (Windows) | `build_windows.bat` |
| Download MongoDB | https://www.mongodb.com/try/download/community |
| Download Inno Setup | https://jrsoftware.org/isdl.php |
| Create installer | Open `installer_setup.iss` in Inno Setup |
| Test installer | Run on clean Windows VM |

---

**Ready to start?** → See `DEPLOYMENT_GUIDE.md` for complete instructions!
