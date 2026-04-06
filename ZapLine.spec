# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all Selenium modules, binaries, and data (handles dynamic imports)
datas_selenium, binaries_selenium, hiddenimports_selenium = collect_all('selenium')

a = Analysis(
    ['gui.py'],
    pathex=[],

    # Include Selenium binaries only (no manual msedgedriver)
    binaries=binaries_selenium,

    # Include project assets and Selenium internal data
    datas=[
        ('zapline.ico', 'assets'),
        ('sheet.xlsx', 'assets'),
    ] + datas_selenium,

    # Required to prevent missing module errors from Selenium dynamic imports
    hiddenimports=hiddenimports_selenium,

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ZapLine',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    icon=['zapline.ico'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ZapLine',
)
