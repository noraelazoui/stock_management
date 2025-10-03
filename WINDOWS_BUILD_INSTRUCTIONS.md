# 🪟 Windows Build Instructions

## ⚠️ CRITICAL: Must Build on Windows!

The current `dist/StockManagement` file was built on **Linux** and is missing the `.exe` extension.
**Windows executables MUST be built on Windows machines!**

---

## 🎯 Quick Start

### Option 1: Automated Build (Recommended)

1. Copy this repository to your Windows machine
2. Double-click: **`BUILD_COMPLETE_PACKAGE.bat`**
3. Wait for completion (3-5 minutes)
4. Follow the on-screen instructions

### Option 2: Manual Build

See **BUILD_ON_WINDOWS.md** for detailed step-by-step instructions.

---

## 📋 What You Need (Windows Only)

- ✅ Windows 10/11 (64-bit)
- ✅ Python 3.10+ ([Download](https://www.python.org/downloads/))
- ✅ Git ([Download](https://git-scm.com/download/win))
- ✅ Inno Setup 6 ([Download](https://jrsoftware.org/isdl.php))
- ✅ Internet connection (for MongoDB download)

---

## 🚀 Build Process Overview

```
1. Clone repository on Windows
   ↓
2. Run BUILD_COMPLETE_PACKAGE.bat
   ↓
3. Download MongoDB for Windows
   ↓
4. Compile installer with Inno Setup
   ↓
5. Test the installer
   ↓
6. Distribute to clients! 🎉
```

---

## ✅ Expected Results

After successful build:

```
dist\StockManagement\StockManagement.exe  ← 8-10 MB, has .exe extension
installer_output\StockManagement_Setup_v1.0.0.exe  ← ~200 MB installer
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| No `.exe` extension | You built on Linux! Must build on Windows |
| Python not found | Install Python and check "Add to PATH" |
| PyInstaller fails | Run `pip install --upgrade pyinstaller` |
| Import errors | Run `pip install -r requirements.txt` |

---

## 📞 Questions?

Read the complete guide: **BUILD_ON_WINDOWS.md**

---

**Last Updated:** 3 October 2025  
**Status:** ✅ Scripts fixed and ready for Windows build
