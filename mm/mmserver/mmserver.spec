# -*- mode: python -*-
import os
import tools.packaging.pyinstaller_hooks as hook

a = Analysis(['/Users/josephferraro/Development/Python/mmserver/mmserver.py'],
             pathex=['/Users/josephferraro/Development/Python/pyinstaller'],
             hiddenimports=[],
             hookspath=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=0,
          name=os.path.join('dist', 'mmserver'),
          debug=False,
          strip=None,
          upx=True,
          console=True)

coll = COLLECT( exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               hook.datas,
               docfiles,
               strip=None,
               upx=True,
               name=os.path.join('dist', 'mmserver'))