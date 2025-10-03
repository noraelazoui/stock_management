# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Stock Management Application
Builds a standalone executable with all dependencies
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files and hidden imports
datas = []
datas += collect_data_files('tkcalendar')
datas += collect_data_files('pymongo')
datas += collect_data_files('matplotlib')

# Hidden imports that PyInstaller might miss
hiddenimports = []
hiddenimports += collect_submodules('pymongo')
hiddenimports += collect_submodules('matplotlib')
hiddenimports += collect_submodules('mplcursors')
hiddenimports += collect_submodules('tkcalendar')
hiddenimports += [
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'numpy',
    'datetime',
    'bson',
    'gridfs',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='StockManagement',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='StockManagement',
)
