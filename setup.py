import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["forms","ui_files"],
}
setup(
  name="myscript",
  version="0.0.1",
  description="SQL-test application!",
  options={
    "build_exe": build_exe_options
  },
  executables=[Executable('run.py',
                          base='Win32GUI',
                          targetName='setup.exe',
                          )]
)
