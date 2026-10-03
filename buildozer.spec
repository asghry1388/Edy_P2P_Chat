[app]

title = Edy P2P Chat
package.name = edyp2pchat
package.domain = org.edy

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 36
android.minapi = 24

android.archs = arm64-v8a

android.accept_sdk_license = True

android.debug_artifact = apk


[buildozer]

log_level = 2
warn_on_root = 1
