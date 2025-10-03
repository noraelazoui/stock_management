# Windows Deployment Checklist
## Complete Step-by-Step Verification

Use this checklist to ensure everything is ready for deployment.

---

## 📋 Pre-Build Checklist

### Development Environment
- [ ] Python 3.8+ installed
- [ ] All application features tested and working
- [ ] No errors in application
- [ ] Database connections work
- [ ] All views display correctly

### Required Files
- [ ] `main.py` exists
- [ ] `requirements.txt` exists
- [ ] All model files in `models/` folder
- [ ] All view files in `views/` folder
- [ ] All controller files in `controllers/` folder
- [ ] `config.py` configured correctly

### Build Files Created
- [ ] `build_config.spec` created
- [ ] `build_windows.sh` created (Linux)
- [ ] `build_windows.bat` created (Windows)
- [ ] `requirements_build.txt` created
- [ ] `installer_setup.iss` created
- [ ] `scripts_installer/` folder created
- [ ] `install_mongodb_service.bat` created
- [ ] `start_app.bat` created

---

## 🔨 Build Phase Checklist

### Install Dependencies
- [ ] Run: `pip install -r requirements_build.txt`
- [ ] Verify: `pyinstaller --version` works
- [ ] Verify: `python -c "import pymongo"` works
- [ ] Verify: `python -c "import matplotlib"` works
- [ ] Verify: `python -c "import tkcalendar"` works

### Create Icon
- [ ] Icon file exists: `icon.ico`
- [ ] Icon is 256x256 pixels (recommended)
- [ ] Icon looks professional
- [ ] Icon file size < 100 KB

### Create License
- [ ] `LICENSE.txt` created
- [ ] Company name filled in
- [ ] Contact information added
- [ ] Copyright year is correct

### Build Executable
- [ ] Run build script (Linux: `./build_windows.sh` or Windows: `build_windows.bat`)
- [ ] Build completes without errors
- [ ] Output folder exists: `dist/StockManagement/`
- [ ] Executable exists: `dist/StockManagement/StockManagement.exe`
- [ ] DLL files present in dist folder
- [ ] Python libraries bundled

---

## 📥 MongoDB Preparation Checklist

### Download MongoDB
- [ ] Visit: https://www.mongodb.com/try/download/community
- [ ] Select Platform: Windows x64
- [ ] Select Package: ZIP (not MSI)
- [ ] Download completed
- [ ] File size is ~50-100 MB

### Extract MongoDB
- [ ] Create folder: `mongodb/`
- [ ] Extract ZIP to `mongodb/`
- [ ] Verify structure: `mongodb/bin/mongod.exe` exists
- [ ] Verify structure: `mongodb/bin/mongo.exe` exists
- [ ] Other MongoDB files present

---

## 📦 Installer Preparation Checklist

### File Organization
```
Project root should have:
- [ ] dist/StockManagement/          [From PyInstaller]
- [ ] mongodb/bin/                    [From MongoDB download]
- [ ] scripts_installer/              [Created earlier]
- [ ] icon.ico                        [Created earlier]
- [ ] LICENSE.txt                     [Created earlier]
- [ ] README.md                       [Optional]
- [ ] installer_setup.iss             [Created earlier]
```

### Verify File Paths
- [ ] All `Source:` paths in `installer_setup.iss` are correct
- [ ] No missing files or folders
- [ ] File names match exactly (case-sensitive)

### Install Inno Setup (Windows Only)
- [ ] Download from: https://jrsoftware.org/isdl.php
- [ ] Install Inno Setup
- [ ] Verify installation: Open Inno Setup Compiler

---

## 🏗️ Create Installer Checklist

### Compile with Inno Setup
- [ ] Open Inno Setup Compiler
- [ ] File → Open → Select `installer_setup.iss`
- [ ] Check for any syntax errors (should be none)
- [ ] Build → Compile
- [ ] Compilation starts
- [ ] No errors during compilation
- [ ] Compilation completes successfully

### Verify Output
- [ ] Output folder created: `installer_output/`
- [ ] Installer file exists: `StockManagement_Setup_v1.0.0.exe`
- [ ] File size is 150-250 MB
- [ ] File icon shows correctly (if you view in Explorer)

---

## 🧪 Testing Checklist

### Pre-Test Preparation
- [ ] Create clean Windows 10/11 VM (or use clean machine)
- [ ] No Python installed
- [ ] No MongoDB installed
- [ ] No previous versions of your app

### Installation Test
- [ ] Copy installer to test machine
- [ ] Double-click installer
- [ ] Installer window appears
- [ ] Welcome screen shows
- [ ] License agreement shows
- [ ] Can select installation location
- [ ] Can choose desktop icon option
- [ ] "Install" button works
- [ ] Installation progresses without errors
- [ ] MongoDB service installs
- [ ] No error messages appear
- [ ] Installation completes
- [ ] "Finish" button works

### Post-Installation Verification
- [ ] Application launches automatically
- [ ] No console window appears
- [ ] Application window appears correctly
- [ ] All tabs/views are visible
- [ ] Desktop shortcut created (if selected)
- [ ] Start Menu shortcut created
- [ ] Installation folder exists: `C:\Program Files\Stock Management\`
- [ ] Data folder exists: `C:\ProgramData\StockManagement\`

### Windows Service Check
- [ ] Open Services (services.msc)
- [ ] Find "Stock Management Database" service
- [ ] Service status is "Running"
- [ ] Service startup type is "Automatic"

### Functionality Test
- [ ] Application connects to database (no errors)
- [ ] Can view articles
- [ ] Can view fabrications
- [ ] Can view dashboard
- [ ] Can view inventory
- [ ] All filters work
- [ ] All buttons work
- [ ] Can add new data
- [ ] Can edit data
- [ ] Data persists after closing and reopening
- [ ] Charts display correctly
- [ ] No error messages or crashes

### Uninstallation Test
- [ ] Open Control Panel → Programs and Features
- [ ] Find "Stock Management"
- [ ] Right-click → Uninstall
- [ ] Uninstaller runs
- [ ] All files removed from Program Files
- [ ] MongoDB service stopped
- [ ] MongoDB service removed from Services
- [ ] Desktop shortcut removed
- [ ] Start Menu shortcuts removed
- [ ] No errors during uninstallation

### Optional: Data Persistence Test
- [ ] Note: Data folder may remain after uninstall (by design)
- [ ] Check: `C:\ProgramData\StockManagement\` still exists (optional)
- [ ] Can manually delete if needed

---

## 📤 Distribution Checklist

### Final Verification
- [ ] Installer tested on at least 2 different machines
- [ ] Installer works on Windows 10
- [ ] Installer works on Windows 11
- [ ] All features verified working
- [ ] No critical bugs found

### Prepare for Distribution
- [ ] Rename installer if needed (e.g., add date)
- [ ] Create checksum (optional): `certutil -hashfile installer.exe SHA256`
- [ ] Create release notes document
- [ ] Create user manual or quick start guide
- [ ] Prepare support contact information

### Distribution Methods
- [ ] Upload to file sharing service (Google Drive, Dropbox, etc.)
- [ ] Send via email (if file size allows)
- [ ] Put on USB drives
- [ ] Upload to company server
- [ ] Create download link for clients

### Client Communication
- [ ] Prepare email template with:
  - [ ] Download link
  - [ ] Installation instructions
  - [ ] System requirements
  - [ ] Support contact
- [ ] Prepare "Getting Started" document
- [ ] Prepare troubleshooting guide
- [ ] Set up support channel (email, phone, etc.)

---

## 📋 Client Installation Instructions

### Create this simple document for clients:

```
Stock Management - Installation Guide

STEP 1: Download
- Download StockManagement_Setup_v1.0.0.exe
- File size: ~200 MB
- Save to your Downloads folder

STEP 2: Install
1. Find the downloaded file
2. Double-click to run
3. If Windows shows security warning, click "More info" → "Run anyway"
4. Click "Next" through the installer
5. Accept default settings
6. Click "Install"
7. Wait 2-3 minutes
8. Click "Finish"

STEP 3: Done!
- Application will open automatically
- Desktop shortcut created
- Find in Start Menu: "Stock Management"

NEED HELP?
Contact: support@yourcompany.com
Phone: Your phone number
```

---

## ✅ Final Checklist

Before sending to clients:

- [ ] All tests passed
- [ ] Installer size is reasonable (<300 MB)
- [ ] No errors during installation
- [ ] No errors during use
- [ ] Application looks professional
- [ ] All features work correctly
- [ ] Uninstaller works cleanly
- [ ] Documentation prepared
- [ ] Support plan in place
- [ ] Client instructions created
- [ ] Backup plan for issues

---

## 🎉 Success Criteria

Your deployment is ready when ALL of these are true:

✅ Installer file created  
✅ File size 150-250 MB  
✅ Tested on clean Windows 10  
✅ Tested on clean Windows 11  
✅ Installs without errors  
✅ Application launches  
✅ All features work  
✅ MongoDB service runs  
✅ Data persists  
✅ Uninstaller works  
✅ Documentation complete  
✅ Client instructions ready  

---

## 📞 If Something Goes Wrong

### Build Issues
- **Problem**: PyInstaller fails
- **Check**: All dependencies installed
- **Solution**: `pip install -r requirements_build.txt`

### Installer Issues
- **Problem**: Inno Setup compilation fails
- **Check**: All file paths are correct
- **Solution**: Verify all files exist in correct locations

### Runtime Issues
- **Problem**: Application won't start
- **Check**: MongoDB service is running
- **Solution**: Manually start service in Services

### Support Plan
- [ ] Document common issues
- [ ] Create troubleshooting guide
- [ ] Set up support email
- [ ] Prepare remote assistance tools (TeamViewer, AnyDesk)

---

**Use this checklist every time you create a new installer version!**

Print it out and check off items as you go. This ensures nothing is forgotten.

Good luck! 🚀
