@echo off

del release.zip

pyinstaller -F -n csgo_richpresence --distpath . main.py
pyinstaller -F -n csgo_richpresence_installer --distpath . install.py

zip release.zip csgo_richpresence.exe
zip release.zip csgo_richpresence_installer.exe
zip release.zip README.md
zip release.zip gamestate_integration_discordrpc.cfg
