# ![aleBot](https://i.imgur.com/WA6U3qM.png)

## aleBot is another multipurpose bot, but it's modular!

### Support

If you need assistance setting up the bot, or adding to it, come join [the support server!](https://discord.gg/M6apruQ)

### Setup

1. Ensure you have [Git](https://git-scm.com/downloads) installed.
2. Open Git Bash in a folder somewhere, and run `git clone https://github.com/AleanaA/aleBot.git`
3. Ensure you have Python and pip installed, and added to your path. The bot was built using [Python 3.5.4,](https://www.python.org/ftp/python/3.5.4/python-3.5.4-amd64.exe) so that's your best bet.
4. In the root directory of the bot, run `python -m pip -U -r requirements.txt` on windows, or `python3 -m pip -U -r requirements.txt` on Linux.
5. Create a bot account over on the [Discord developers page.](https://discordapp.com/developers/applications/me)
6. Setup the config file in the `config` folder. This includes copying `config.example.py` and `config.example.ini` to `config.py` and `config.ini` and adding your bot token, your user id, your prefix, an announcement, log, and auddit log channel.
7. That's it! Run the bot with either `run.bat` or `run.sh` and you should be good to go!

It should be noted that emotes will probably be displayed incorrectly, as you won't have the emotes in `emotes.py`
To fix this, just replace those emote IDs with ones from a server the bot is in, corresponding to the emote.

### Commands

All commands can be listed using the help command, but role required commands are:

- eval - Owner
- die - Owner
- avatar - Owner
- username - Owner
- cog - Owner
- ban - Mod
- banid - Mod
- softban - Mod
- unban - Mod
- kick - Apprentice
- log - Apprentice
- say - Event
- announce - Event

There is an invite command, so if you don't want users to be able to access your bot without permission
be sure to uncheck public bot on the [page where you created your bot!](https://discordapp.com/developers/applications/me)

### Roles

The role permissions work as follows:

- Admin has permission to Admin commands and lower, except Event
- Supervisor has permission to Supervisor commands and lower, except Event
- Moderator has permission to Moderator commands and lower, except Event
- Apprentice has permission to Apprentice commands, and no others.
- Event has permissions to Event commands. All event commands require the user to have the Event role no matter what.

The bot will check for the role name in the list of the users roles. To allow a user to have access to commands, you must give them the corresponding role, as listed above.
