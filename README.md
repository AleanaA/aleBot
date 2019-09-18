# ![aleBot](https://i.imgur.com/WA6U3qM.png)

## aleBot is another multipurpose bot, but it's modular!

### Support

[If you need assistance setting up the bot, or adding to it, come join the support server!](https://discord.gg/eJhG4Tq)

### Setup

1. Ensure you have [Git](https://git-scm.com/downloads) installed.
2. Open Git Bash in a folder somewhere, and run `git clone https://github.com/AleanaA/aleBot.git`
3. Ensure you have Python and pip installed, and added to your path. The bot was built using [Python 3.7.4,](https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe) so that's your best bet.
4. In the root directory of the bot, run `python -m pip -U -r requirements.txt` on windows, or `python3 -m pip -U -r requirements.txt` on Linux.
5. Create a bot account over on the [Discord developers page.](https://discordapp.com/developers/applications/me)
6. Setup the config file in the `config` folder. This includes copying `config.example.ini` to `config.ini` and adding your bot token, your user id, and your prefix
7. That's it! Run the bot with either `run.bat` or `run.sh` and you should be good to go!


### Usage
Using aleBot is fairly straightforward, however you do need to have some prior knowledge of coding to make full use of it!  
To download a cog, you can use the cogloader's download command, or zipdl command.

Usage of these commands is as follows:  
```
cog download name URLtopy  
cog zipdl URLtozip
```
cog download will attempt to load your cog, you'll need to ensure you have the required dependencies for the cog before it will load correctly.  
Note that cog zipdl will not attempt to load your cog in any way.

Cogs can be manually loaded using the cog load command, ensuring you notate the folder and cog file.  
```
cog load autoload.Cogloader cogloader  
cog load Debug debug
```

The file structure for the mods folder, and expected followed listing, is as follows:  
mods  
├autoload  
│├autoloaded cog folders  
││├cog py file  
││└any extras for the cog, such as configs, utils, etc.  
├non-autoloaded cog folders and downloaded/zipdl cog folders  
│├cog py file  
│└any extras for the cog, such as configs, utils, etc.  