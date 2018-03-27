## Discord Rich Presence support for Counter-Strike: Global Offensive!

Written in Python 3.6.4, using a [Discord RPC module](https://github.com/suclearnub/python-discord-rpc) and the [game state integration system](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) that CS:GO uses.

The installer uses [PyVDF](https://github.com/amreuland/PyVDF).

### Notice: This program is completely safe and won't get you banned.

# How does it work?

Once you feed CS:GO a specific and custom configuration file, it will start sending information over to a local HTTP server on your machine for it to use. So I thought about linking it to Discord's Rich Presence system, and it works beautifully!

# Installation, usage

## Recommended:

1. Download the [latest release](https://github.com/Tenrys/csgo_richpresence/releases/latest)'s zip file.
2. Extract the zip file somewhere you judge appropriate for a program that you won't be touching.
3. Run `csgo_richpresence_installer.exe` in there, read carefully and follow its instructions.
4. You should now have installed the program! It will run automatically next time you start Windows, in the background.
    - If you wish to uninstall it, run `csgo_richpresence_installer.exe` with the `--uninstall` command line option.

## Manual:

1. Place the `gamestate_integration_discordrpc.cfg` file from this repository in the `cfg` folder located in your game's installation directory. The game should now be trying to send info to the program when you restart it. (port `3000` is used by default in both the file and program)
2. Launch the program, **keep it open until you're done playing**.
    - If you don't want to install Python and everything else, use the [latest release](https://github.com/Tenrys/csgo_richpresence/releases/latest)'s executable.

Your Discord status will now change according to what is happening in the game!

## Command line options:

### Main program:

- `--port, -P`: Use a different port other than the default (`3000`) one for the HTTP server if issues arise. Don't forget to change the config file accordingly! If you do need to, you'll need to reinstall the config file into your game folders.
- `--silent, -S`: Tries to hide the program's window. Should work most of the time, used by default when the program gets installed.

### (Un)installer:

- `--uninstall, -U`: Instead of installing the program, the installer will remove the registry key that makes it run on startup.

# Support

Only Windows is supported, because it's not like anyone plays CS:GO on any other operating system anyway... Right?

Keep in mind this is meant to be a fun project for me to improve my Python skills, so it might not be perfect. It should work relatively good anyway, but don't hesitate to create an issue with the error log inside if it bugs out. I'll be glad to help!

# Known bugs

- None!

# Planned

- Support for other operating systems?
