import os
import shutil
import argparse
import winreg
import sys
from PyVDF import PyVDF

os.system("title Discord Rich Presence: Counter-Strike: Global Offensive [Installer]")

parser = argparse.ArgumentParser(prog="csgo_richpresence_installer")
parser.add_argument("-U", "--uninstall", action="store_true", default=False, help="uninstall the program")
args = parser.parse_args()

reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

# find steam's path
steam = winreg.CreateKey(reg, "Software\\Valve\\Steam")
steam_path = None
try:
	steam_path = winreg.QueryValueEx(steam, "SteamPath")[0]
except:
	print("Steam not installed? Aborting install.")
	sys.exit()

# find other eventual game library folders
library_folders = PyVDF(infile=os.path.join(steam_path, "steamapps", "libraryfolders.vdf")).find("LibraryFolders")
library_folders['0'] = os.path.abspath(steam_path) # maximus hacksimus
csgo_dir = None
csgo_dir_found = False
for k, dir in library_folders.items():
	try:
		int(k) # if this works, then run the following code

		csgo_dir = os.path.join(dir, "steamapps", "common", "Counter-Strike Global Offensive")
		if os.path.isdir(csgo_dir) and os.path.isfile(os.path.join(csgo_dir, "csgo.exe")):
			csgo_dir_found = True
			break
	except:
		pass

# everything is in order, install!
if csgo_dir_found:
	print("Found csgo directory!\n")

	if not args.uninstall:
		# intro
		print("You are about to install the CS:GO Discord Rich Presence program on your computer, which will make it run on startup, silently.")
		print("If you want to uninstall it, run this program again with the --uninstall command line option.")
		print("This installer assumes that you are running it in the directory which contains the .cfg file required to get the game state integration working as well as the program's executable. (csgo_richpresence.exe)")
		print("If something errors out, please double check.")
		print("Also, after the installation, if you wish to move the main program to another location, you will have to run this program again.\n")

		reply = None
		while True:
			reply = input("Do you want to continue? [Y/N]").upper()
			if reply == "N" or reply == "Y":
				break
		if reply == "N":
			sys.exit()

		# install cfg file
		print("Installing the game state integration configuration file to your game's cfg folder...")
		cfg_path = os.path.join(os.getcwd(), "gamestate_integration_discordrpc.cfg")
		if os.path.exists(cfg_path):
			try:
				shutil.copyfile(cfg_path, os.path.join(csgo_dir, "csgo", "cfg", "gamestate_integration_discordrpc.cfg"))
				print("Success!")
			except Exception as e:
				print("Error!")
				print(str(e))
		else:
			print("gamestate_integration_discordrpc.cfg not found, step skipped.")
			print("Perhaps you already installed it on your own?")
			print("If not, make sure to run this installer in the directory that contains the file.")

		# install registry key to run program
		print("\nAdding registry key to start the program on Windows startup...")
		exe_path = os.path.join(os.getcwd(), "csgo_richpresence.exe")
		if os.path.exists(exe_path):
			try:
				autorun = winreg.CreateKey(reg, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
				winreg.SetValueEx(autorun, "csgo_richpresence", 0, winreg.REG_SZ, '"{}" --silent'.format(exe_path))
				print("Success!")
			except Exception as e:
				print("Error!")
				print(str(e))
		else:
			print("csgo_richpresence.exe not found, step skipped.")
			print("Make sure to run this installer in the directory that contains the file.")

		input("\nInstallation complete! Press Enter to quit.")
	else:
		# intro
		print("You are about to uninstall the CS:GO Discord Rich Presence program on your computer, which will make it no longer run on startup.")

		reply = None
		while True:
			reply = input("Do you want to continue? [Y/N]").upper()
			if reply == "N" or reply == "Y":
				break
		if reply == "N":
			sys.exit()

		try:
			autorun = winreg.CreateKey(reg, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
			winreg.DeleteValue(autorun, "csgo_richpresence")
			print("Success!")
		except Exception as e:
			print("Error!")
			print(str(e))

		input("\nPress Enter to quit.")
else:
	print("Couldn't find csgo directory, aborting install.")
	sys.exit()