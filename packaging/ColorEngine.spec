# Build only the still-photo engine. FFmpeg/video codecs are not beta features.
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules
root=Path(SPECPATH).resolve().parent
a=Analysis([str(root/'apps/desktop/engine_entry.py')],pathex=[str(root)],
 datas=[(str(root/'apps/web/dist'),'apps/web/dist'),(str(root/'apps/demo'),'apps/demo')],
 hiddenimports=collect_submodules('uvicorn')+collect_submodules('PIL'),
 excludes=['tkinter','matplotlib','IPython','httpx','PyQt5','PyQt6','pytest'],noarchive=False)
a.binaries=[entry for entry in a.binaries if 'ffmpeg' not in entry[0].lower()]
pyz=PYZ(a.pure)
exe=EXE(pyz,a.scripts,[],exclude_binaries=True,name='ColorEngine',console=True,upx=False)
coll=COLLECT(exe,a.binaries,a.datas,strip=False,upx=False,name='ColorEngine')
