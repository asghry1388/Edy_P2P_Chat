[app]

# (str) Title of your application
title = Edy P2P Chat

# (str) Package name
package.name = edyp2pchat

# (str) Package domain
package.domain = org.edy

# (str) Source code where main.py lives
source.dir = .

# (str) Main Python file
source.include_exts = py,png,jpg,kv,atlas,txt

# (str) Application version
version = 1.0

# (str) Requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (list) Android permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 35

# (int) Minimum Android API
android.minapi = 23

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (str) Supported architectures
android.archs = arm64-v8a, armeabi-v7a

# (bool) Warn about Python-for-Android bootstrapping
warn_on_root = 1

[buildozer]

# (int) Log level
log_level = 2
