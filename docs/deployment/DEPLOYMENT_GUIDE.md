# Complete Windows Deployment Guide
## Stock Management Application - One-Click Installer

**Version**: 1.0.0  
**Date**: October 2025  
**Target**: Windows 10 and higher

---

## 📋 Overview

This guide shows you how to create a complete Windows installer that includes:
- ✅ Python application bundled as EXE
- ✅ MongoDB database embedded
- ✅ All Python libraries included
- ✅ Automatic service installation
- ✅ One-click "Next, Next, Install" experience

**Result**: A single `.exe` installer that your clients can run without any technical knowledge.

---

## 🎯 What Your Client Will Experience

1. **Double-click** `StockManagement_Setup_v1.0.0.exe`
2. **Click "Next"** through the wizard
3. **Choose installation location** (optional)
4. **Click "Install"**
5. **Application launches automatically**

✅ No Python installation needed  
✅ No MongoDB installation needed  
✅ No manual configuration needed  
✅ Everything works immediately

---

## 🛠️ Prerequisites for Building

### On Your Linux Machine:
```bash
# Install PyInstaller and dependencies
pip install pyinstaller pillow

# Or from requirements.txt
pip install -r requirements.txt
```

### On Windows Machine (for final installer creation):
1. **Inno Setup**: Download from https://jrsoftware.org/isinfo.php
2. **MongoDB Windows Binary**: Download from https://www.mongodb.com/try/download/community

---

## 📦 Step-by-Step Build Process

### Step 1: Build the Python Application (on Linux)

```bash
cd /home/najib/Documents/stock_management

# Run the build script
./build_windows.sh
```

This creates: `dist/StockManagement/` folder with the executable and all dependencies.

**What it does**:
- Creates `icon.ico` (if needed)
- Creates `LICENSE.txt` (if needed)
- Builds standalone executable with PyInstaller
- Bundles all Python libraries
- Includes tkinter, matplotlib, pymongo, etc.

### Step 2: Download MongoDB for Windows

1. Go to: https://www.mongodb.com/try/download/community
2. Select:
   - **Version**: Latest stable (e.g., 7.0)
   - **Platform**: Windows
   - **Package**: ZIP (not MSI)
3. Download and extract

### Step 3: Prepare MongoDB Files

Create folder structure:
```
stock_management/
├── dist/
│   └── StockManagement/       ← From PyInstaller
├── mongodb/                    ← Create this
│   └── bin/
│       ├── mongod.exe
│       ├── mongo.exe
│       └── (other MongoDB files)
├── scripts_installer/          ← Already created
│   ├── install_mongodb_service.bat
│   └── start_app.bat
└── installer_setup.iss         ← Already created
```

**Copy MongoDB files**:
```bash
# On Windows, copy MongoDB bin folder to:
mongodb/bin/
```

### Step 4: Transfer to Windows Machine

Transfer these folders/files to your Windows machine:
```
✓ dist/StockManagement/
✓ mongodb/
✓ scripts_installer/
✓ data/
✓ icon.ico
✓ LICENSE.txt
✓ README.md
✓ installer_setup.iss
```

You can use:
- USB drive
- Network share
- Cloud storage (Google Drive, Dropbox)
- Git repository

### Step 5: Create Installer with Inno Setup (on Windows)

1. **Install Inno Setup** on Windows machine
2. **Open** Inno Setup Compiler
3. **File → Open** → Select `installer_setup.iss`
4. **Build → Compile**
5. Wait for compilation (may take several minutes)

**Output**: `installer_output/StockManagement_Setup_v1.0.0.exe`

This is your final installer! 🎉

---

## 📁 Complete Folder Structure

```
stock_management/
│
├── main.py                          # Main application
├── config.py                        # Configuration
├── requirements.txt                 # Python dependencies
│
├── models/                          # Application models
│   ├── __init__.py
│   ├── database.py
│   ├── article.py
│   ├── fabrication.py
│   └── ...
│
├── views/                           # Application views
│   ├── __init__.py
│   ├── article_view.py
│   ├── fabrication_view.py
│   ├── dashbord_view.py
│   └── ...
│
├── controllers/                     # Application controllers
│   ├── __init__.py
│   ├── article_controller.py
│   └── ...
│
├── data/                            # Data files
│   └── gestion.db
│
├── BUILD FILES (created):
│
├── build_config.spec                # PyInstaller configuration
├── build_windows.sh                 # Build script (Linux)
├── icon.ico                         # Application icon
├── LICENSE.txt                      # License file
│
├── DEPLOYMENT FILES:
│
├── installer_setup.iss              # Inno Setup script
│
├── scripts_installer/               # Installer scripts
│   ├── install_mongodb_service.bat  # MongoDB service installer
│   └── start_app.bat                # Application launcher
│
├── mongodb/                         # MongoDB files (add manually)
│   └── bin/
│       ├── mongod.exe
│       ├── mongo.exe
│       └── ...
│
├── dist/                            # Build output
│   └── StockManagement/
│       ├── StockManagement.exe      # Main executable
│       ├── (many DLL files)
│       └── (Python libraries)
│
└── installer_output/                # Final installer
    └── StockManagement_Setup_v1.0.0.exe  ← DISTRIBUTE THIS!
```

---

## 🔧 Configuration Files Explained

### 1. `build_config.spec` - PyInstaller Configuration

```python
# Specifies how to build the executable
- Includes all Python libraries
- Bundles tkinter, matplotlib, pymongo
- Creates standalone EXE
- No console window (GUI only)
- Includes icon
```

### 2. `installer_setup.iss` - Inno Setup Script

```ini
# Creates Windows installer
- Installs application files
- Installs MongoDB as Windows service
- Creates desktop shortcut
- Creates Start Menu entries
- Handles uninstallation
- Multi-language support (English/French)
```

### 3. `install_mongodb_service.bat` - MongoDB Service Installer

```batch
# Runs during installation
- Creates data directories
- Creates MongoDB config
- Installs MongoDB as Windows service
- Starts service automatically
```

---

## 🚀 Testing the Installer

### Before Distribution:

1. **Test on clean Windows 10/11 VM**
2. **Run installer**:
   ```
   StockManagement_Setup_v1.0.0.exe
   ```
3. **Verify**:
   - ✓ Application installs without errors
   - ✓ MongoDB service starts
   - ✓ Application launches
   - ✓ Database connection works
   - ✓ All features work correctly
   - ✓ Desktop shortcut works
   - ✓ Start Menu shortcut works

4. **Test uninstaller**:
   - Uninstall from Control Panel
   - Verify MongoDB service is removed
   - Verify all files are removed

---

## 📦 Distribution

### File to Distribute:
```
StockManagement_Setup_v1.0.0.exe
```

**Size**: ~150-200 MB (includes MongoDB)

### Client Instructions:

Create a simple document for your clients:

---

**Stock Management Installation Guide**

1. Double-click `StockManagement_Setup_v1.0.0.exe`
2. Click "Next"
3. Accept the license agreement
4. Choose installation location (or keep default)
5. Click "Install"
6. Wait for installation to complete
7. Click "Finish"

The application will launch automatically!

**Desktop Shortcut**: Double-click "Stock Management" icon to start
**Start Menu**: Find "Stock Management" in your programs

**Uninstall**: Control Panel → Programs → Uninstall Stock Management

---

## 🔍 What Gets Installed

### Application Files:
```
C:\Program Files\Stock Management\
├── StockManagement.exe          # Main application
├── mongodb\                     # Database files
│   └── bin\
│       └── mongod.exe
├── scripts\
│   ├── install_mongodb_service.bat
│   └── start_app.bat
└── (many library files)
```

### Data Files:
```
C:\ProgramData\StockManagement\
├── db\                          # Database files
└── logs\                        # Log files
    └── mongodb.log
```

### Windows Service:
```
Service Name: StockManagementMongoDB
Display Name: Stock Management Database
Status: Running (automatic start)
```

---

## 🐛 Troubleshooting

### Build Issues

**Problem**: PyInstaller fails to build
```bash
# Solution: Install missing dependencies
pip install pyinstaller pillow
pip install -r requirements.txt
```

**Problem**: Missing imports in executable
```python
# Solution: Add to hiddenimports in build_config.spec
hiddenimports += ['missing_module']
```

### Installer Issues

**Problem**: Inno Setup compilation fails
```
# Solution: Check file paths in installer_setup.iss
# Ensure all Source files exist
```

**Problem**: MongoDB service fails to install
```
# Solution: Ensure MongoDB files are in mongodb/bin/
# Run installer as Administrator
```

### Runtime Issues

**Problem**: Application doesn't start
```
# Check: MongoDB service is running
# Open Services → Find "Stock Management Database"
# Start if stopped
```

**Problem**: Database connection fails
```
# Check: mongodb.log in C:\ProgramData\StockManagement\logs\
# Verify port 27017 is not blocked
```

---

## 🔒 Security Considerations

### For Production:

1. **Code Signing**: Sign the installer and EXE
   ```bash
   # Use signtool on Windows
   signtool sign /f certificate.pfx /p password installer.exe
   ```

2. **MongoDB Security**:
   - Enable authentication in production
   - Use strong passwords
   - Restrict network access (localhost only)

3. **Firewall Rules**:
   - MongoDB only listens on localhost (127.0.0.1)
   - No external access by default

---

## 📋 Checklist Before Distribution

- [ ] Application builds successfully
- [ ] All features tested and working
- [ ] Icon is professional and clear
- [ ] LICENSE.txt is complete
- [ ] README.md is included
- [ ] Installer tested on clean Windows 10
- [ ] Installer tested on Windows 11
- [ ] Uninstaller works correctly
- [ ] MongoDB service installs properly
- [ ] MongoDB service starts automatically
- [ ] Application launches after installation
- [ ] Desktop shortcut works
- [ ] Start Menu shortcut works
- [ ] Data persists after restart
- [ ] No errors in logs
- [ ] File size is acceptable (<500MB)

---

## 🆘 Support and Updates

### Creating Update Installers:

1. **Increment version** in `installer_setup.iss`:
   ```ini
   #define MyAppVersion "1.0.1"
   ```

2. **Rebuild** with updated version

3. **Distribute** update installer

Inno Setup can detect existing installations and upgrade them.

### Automated Updates:

Consider implementing:
- Auto-update checker in application
- Download new installer from server
- Notify users of updates

---

## 📊 Installer Size Breakdown

| Component | Size | Notes |
|-----------|------|-------|
| Python EXE + Libraries | ~80 MB | PyInstaller bundle |
| MongoDB | ~50 MB | Database engine |
| Application Data | ~5 MB | Your code, images |
| Installer Overhead | ~15 MB | Compression, scripts |
| **Total** | **~150 MB** | Single EXE file |

---

## 🎨 Customization

### Change Application Icon:

Replace `icon.ico` with your custom icon (256x256 recommended)

### Change Installer Appearance:

Edit `installer_setup.iss`:
```ini
WizardStyle=modern          # or "classic"
WizardImageFile=setup.bmp   # Custom wizard image
```

### Add More Languages:

```ini
[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
```

---

## ✅ Quick Start Summary

### For Building:

```bash
# 1. Build on Linux
./build_windows.sh

# 2. Download MongoDB Windows binary
# (manual download)

# 3. Transfer to Windows
# (copy files)

# 4. Compile with Inno Setup
# (use Inno Setup Compiler)

# 5. Distribute installer
# StockManagement_Setup_v1.0.0.exe
```

### For Client:

```
1. Double-click installer
2. Next → Next → Install
3. Done! ✓
```

---

## 📞 Additional Resources

- **PyInstaller**: https://pyinstaller.org/
- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **MongoDB Windows**: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
- **Icon Converters**: https://convertio.co/png-ico/

---

## 🎉 Success!

Once you complete these steps, you'll have a professional Windows installer that:
- ✅ Requires zero technical knowledge to install
- ✅ Includes everything needed to run
- ✅ Installs MongoDB automatically
- ✅ Creates shortcuts for easy access
- ✅ Can be uninstalled cleanly
- ✅ Works on Windows 10 and 11

**Your clients will just click "Next, Next, Install" and it works!** 🚀

---

*For technical support or questions about deployment, refer to the troubleshooting section above.*
