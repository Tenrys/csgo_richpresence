## Discord Rich Presence support for Counter-Strike: Global Offensive!

Made in Python 3.6.4, using the [Discord RPC module](https://github.com/suclearnub/python-discord-rpc) and the [game state integration system](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) that CS:GO uses.

#### Notice: This program is completely safe and won't get you banned.

# Installation, usage

1. Place the `gamestate_integration_discordrpc.cfg` file in the `cfg` folder located in your game's installation directory. The game should now be trying to send info to the program when you restart it.
2. Launch the program, **keep it open until you're done playing**.
    - If you're a Windows user, all you should have to do is run the latest binary available in the [Releases](https://github.com/Tenrys/csgo_richpresence/releases) section.
    - For other operating systems... I highly doubt CS:GO is even available for them in the first place so, figure it out yourself. You shouldn't need anything other than Python 3.6.4.
3. Watch your Discord status change according to what is happening in the game!

# Support

Keep in mind this is meant to be a fun project for me to improve my Python skills, so it might not be perfect. It should work relatively good anyway, but don't hesitate to create an issue with the error log inside if it bugs out. I'll be glad to help!

# Known bugs

- The "elapsed" time field tends to reset a lot when playing, so it's not accurate at all. I don't think there's anything I can do about it since I update the presence quite frequently while in game and Discord doesn't seem to make use of the timestamp I send. It's only really accurate in the menu since nothing happens there.

# Features planned

- [ ] Run automatically whenever the game starts and quit when it exits (might be difficult to do and too much effort)
- [ ] Install the required file automatically (good luck finding the CS:GO install directory)
