import sys
from cx_Freeze import setup, Executable

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="TP 01- Computação Gráfica",
    version="1.0",
    description="TP 01- Computação Gráfica",
    executables=[Executable("main.py", base=base)],
)