# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for macOS 智能连点器
"""

import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Collect all pynput submodules
hiddenimports = collect_submodules('pynput')
hiddenimports += ['AppKit', 'Foundation', 'Quartz', 'WebKit']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('static', 'static'),
        ('backend', 'backend'),
    ],
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
    name='连点器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No terminal window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='连点器',
)

app = BUNDLE(
    coll,
    name='连点器.app',
    icon='app_icon.icns',
    bundle_identifier='com.jx3.autoclicker',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSAppleEventsUsageDescription': '此应用需要控制其他应用程序',
        'NSAccessibilityUsageDescription': '此应用需要辅助功能权限以模拟键盘和鼠标操作',
        'CFBundleName': '连点器',
        'CFBundleDisplayName': 'macOS 智能连点器',
        'CFBundleShortVersionString': '1.0.1',
    },
)
