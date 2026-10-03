EDY P2P CHAT
============

This project is a graphical P2P TCP chat.

- Windows: Kivy GUI + PyInstaller -> EXE
- Android: Kivy GUI + Buildozer -> APK
- The same main.py is used for both.
- Port: TCP 5000
- Server listens on 0.0.0.0
- Client connects to the server IP.
- Messages are newline-framed so multiple messages do not get merged.

IMPORTANT
---------
This app does not solve NAT/CGNAT by itself. If two devices are on separate
networks, use a reachable IP or a virtual network such as the one you are
already testing. The app itself is only the chat layer.

WINDOWS EXE
-----------
On Windows PowerShell/CMD:

1. Open this folder.
2. Run:
   build_windows.bat

The result will be:
   dist\EdyP2PChat.exe

PyInstaller supports one-file/windowed Windows packaging. If Kivy installation
has an issue with your current Python, use a supported Python version in a
separate virtual environment.

ANDROID APK
-----------
Buildozer is normally run in Linux/WSL rather than native Windows.

Inside Ubuntu/WSL, install the required build tools and then:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -U pip
    pip install buildozer cython

Then inside this project:

    buildozer -v android debug

The APK will be placed in the bin/ directory.

FIRST TEST
----------
1. Run EdyP2PChat.exe on the laptop.
2. Click Start Server.
3. On Android, open Edy P2P Chat.
4. Enter the laptop's reachable IP (for example the IP of your virtual
   network).
5. Click Connect.
6. Send messages from either side.

The GUI has:
- Start Server
- Connect
- Disconnect
- IP input
- Chat history
- Message input
- Connection status
