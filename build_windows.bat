@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo EDY P2P CHAT - Windows EXE Builder
echo ==========================================
echo.

py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.12 is not installed.
    echo.
    echo Install Python 3.12 x64 first, then run this file again.
    echo Your existing Python 3.14 can stay installed.
    echo.
    pause
    exit /b 1
)

echo Creating a separate virtual environment...
if not exist ".venv312\Scripts\python.exe" (
    py -3.12 -m venv .venv312
)

call ".venv312\Scripts\activate.bat"

echo.
echo Updating pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Installing Kivy and PyInstaller...
python -m pip install "kivy[base]" pyinstaller

if errorlevel 1 (
    echo.
    echo ERROR: Kivy/PyInstaller installation failed.
    echo Do not continue. Send me the error shown above.
    pause
    exit /b 1
)

echo.
echo Building EXE...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name EdyP2PChat main.py

if errorlevel 1 (
    echo.
    echo ERROR: EXE build failed.
    echo Send me the error shown above.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo SUCCESS!
echo EXE:
echo %CD%\dist\EdyP2PChat.exe
echo ==========================================
pause
