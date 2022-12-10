# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas += [("open-file-folder-icon.png", "D:\\python\\check_passwords\\icons\\open-file-folder-icon.png", "icons"),
            ("red-round-close-x-icon.png", "D:\\python\\check_passwords\\icons\\red-round-close-x-icon.png", "icons"),
            ("cleanuper-logo.ico", "D:\\python\\check_passwords\\icons\\cleanuper-logo.ico", "icons")]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Chrome-Pass-Cleanup',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='D:\\python\\check_passwords\\icons\\cleanuper-logo.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
