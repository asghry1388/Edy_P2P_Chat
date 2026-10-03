EDY P2P CHAT - BUILD GUIDE

WHY THE OLD BUILD FAILED
-------------------------
The previous build tried to install Kivy using Python 3.14 and an incompatible
Windows SDL2 dependency. We will keep Python 3.14 installed, but build this
project inside a separate Python 3.12 virtual environment.

STEP 1 - INSTALL PYTHON 3.12
----------------------------
Install Python 3.12 (64-bit) for Windows.
You do NOT need to uninstall Python 3.14.

During installation, enabling the Python Launcher is recommended.

STEP 2 - BUILD THE EXE
----------------------
Open PowerShell inside this project folder and run:

    .\build_windows.bat

The script creates:
    .venv312\
    dist\EdyP2PChat.exe

If it says Python 3.12 is not installed, install Python 3.12 and run it again.

STEP 3 - APK
------------
The APK is built separately with Buildozer under Linux/WSL.
The Windows EXE build does NOT create an APK.
