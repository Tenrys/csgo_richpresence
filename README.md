## Discord Rich Presence support for Counter-Strike: Global Offensive!

Written in Python 3.6.4, using a [Discord RPC module](https://github.com/suclearnub/python-discord-rpc) and the [game state integration system](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) that CS:GO uses.

#### Notice: This program is completely safe and won't get you banned.

# Installation, usage

1. Place the `gamestate_integration_discordrpc.cfg` file from this repository in the `cfg` folder located in your game's installation directory. The game should now be trying to send info to the program when you restart it. (port `3000` is used by default)
2. Launch the program, **keep it open until you're done playing**.
    - If you're a Windows user, all you should have to do is run the [latest release](https://github.com/Tenrys/csgo_richpresence/releases/latest)'s executable.
    - For other operating systems... I highly doubt CS:GO is even available for them in the first place, so figure it out yourself. You shouldn't need anything else other than Python 3.6.4.
3. Watch your Discord status change according to what is happening in the game!

Yup, no need to setup your own Discord application!

# Support

Keep in mind this is meant to be a fun project for me to improve my Python skills, so it might not be perfect. It should work relatively good anyway, but don't hesitate to create an issue with the error log inside if it bugs out. I'll be glad to help!

# Known bugs

- None!

# Features planned

- [ ] Add "silent" option to not show any console at all
- [ ] Add "port" launch option to pick whichever port you want to use for the server
- [ ] "Installer" to run on startup with "silent" launch option
- [ ] Only have the HTTP server up if the game is running
- [ ] Install the required file automatically (good luck finding the CS:GO install directory)
