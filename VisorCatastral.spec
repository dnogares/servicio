# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\arnyd\\.gemini\\antigravity\\playground\\final-singularity\\backend/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\arnyd\\.gemini\\antigravity\\playground\\final-singularity\\frontend/dist', 'frontend/dist'), ('C:\\Users\\arnyd\\.gemini\\antigravity\\playground\\final-singularity\\backend/logic', 'logic')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='VisorCatastral',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
