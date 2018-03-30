# Bot token goes here, can be found on here: https://discordapp.com/developers/applications/me
Token = 'token'

# Bot prefix, for any commands you run 
# Example: rb!help
Prefix = 'rb!'

# Set the level the console will log at. 
# Values can be 'debug', 'info', 'warn', 'error', 'critical', or left blank to disable logging
LogLevel = 'warn'

# User and role ids for commands go here
Owner = ownerid
Admin =  adminid
Supervisor = svid
Moderator = modid
Apprentice = appid
Event = eventid

# Channels for the Announce and Log commands, as well as rooBot's Auddit log channel
AnnounceChannel = annid
LogChannel = logid
AudditChannel = audid

# Modules for commands go here.
# Do *NOT* mess with this if you don't know what you're doing.
# This is here for those that would like to make additions and customize their bot,
# but can easily prevent you from using commands if you delete the existing modules.
Modules = [
    'mods.moderate',
    'mods.emotes',
    'mods.commands'
]
