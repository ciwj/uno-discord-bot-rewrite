# Uno Discord Bot Rewrite

The uno bot rewrite is an optimized version of my [previous discord.py uno bot](https://github.com/ciwj/uno-bot),
written with the discord.py library, and in collaboration with Github user bluusocks.
The bot is intended to allow you to play uno in a discord server.

## Dependencies

The following modules are required for this project.
- [python-dotenv v0.15.0](https://pypi.org/project/python-dotenv/)
- [discord.py v1.6.0](https://discordpy.readthedocs.io/en/latest/intro.html#installing)


## Installation

A Discord bot account must be made for this, instructions for which can be found [here](https://discordpy.readthedocs.io/en/latest/discord.html).
The bot will require admin privileges.

A Discord server is required as well, which requires setting up channels, roles, and permissions.
The bare minimum for the server includes:

- A main lobby channel
- Hidden channels for each player
- A role for each channel that allows viewing the respective channel. This must be named "Player #", where # is the respective role number indexing from 1-10.

Once the Discord-side setup is complete, the repository must be downloaded to a directory and a .env file must be made. The format of the .env file is:

```dotenv
DISCORD_TOKEN=YOURTOKENHERE
GUILD_NAME=YOURSERVERNAMEHERE
MAIN_CHANNEL_ID=CHANNELIDHERE
PLAYER_0_CHANNEL=CHANNELIDHERE
PLAYER_1_CHANNEL=CHANNELIDHERE
PLAYER_2_CHANNEL=CHANNELIDHERE
PLAYER_3_CHANNEL=CHANNELIDHERE
PLAYER_4_CHANNEL=CHANNELIDHERE
PLAYER_5_CHANNEL=CHANNELIDHERE
PLAYER_6_CHANNEL=CHANNELIDHERE
PLAYER_7_CHANNEL=CHANNELIDHERE
PLAYER_8_CHANNEL=CHANNELIDHERE
PLAYER_9_CHANNEL=CHANNELIDHERE
```

Channel IDs can be obtained by turning on Discord's developer mode and right-clicking a channel.
Once the .env file is complete, main.py can be run to start the bot.

## Usage

The default command prefix is !, which can be changed in main.py under the prefix variable. 
To get a list of commands, type !help in the server with the bot. To get details on each command, type !help commandName.

## License

The license can be found here:
[MIT License](https://choosealicense.com/licenses/mit/)