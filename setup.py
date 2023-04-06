import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame"], "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Soccer Dodge",
    version="1.0",
    description="Soccer Dodge Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("SoccerDodge.py", base=base)]
)