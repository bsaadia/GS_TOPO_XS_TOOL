# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import copy_metadata

datas = []
binaries = []
datas += copy_metadata('pyproj')
binaries += collect_dynamic_libs('rtree')


block_cipher = None


a = Analysis(
    ['GS_XSECTION_V2.py'],
    pathex=[r'C:\Users\saadia\Documents\0_WORK\XSECTION_DEVELOPMENT\program'],
    binaries=binaries,
    datas=datas,
    hiddenimports=['rasterio.sample','rasterio.vrt','rasterio._features'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas += [('img\TREA-logo1_rgb_hi.png',r'C:\Users\saadia\Documents\0_WORK\XSECTION_DEVELOPMENT\program\img\TREA-logo1_rgb_hi.png', "DATA")]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GS_XSECTION_V2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='GS_XSECTION_V2',
)
