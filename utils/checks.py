import os
import discord.utils
from discord.ext import commands
from config import config

class No_Event(commands.CommandError): pass
class No_Appr(commands.CommandError): pass
class No_Mod(commands.CommandError): pass
class No_Super(commands.CommandError): pass
class No_Admin(commands.CommandError): pass
class No_Owner(commands.CommandError): pass
class InvalidUsage(commands.CommandError): pass

def is_owner_check(message):
    if message.author.id == config.Owner:
        return True
    raise No_Owner()

def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))

def is_admin_check(message):
    if config.Admin in [role.id for role in message.author.roles]:
        return True
    elif message.author.id == config.Owner:
        return True
    raise No_Admin

def is_admin():
    return commands.check(lambda ctx: is_admin_check(ctx.message))

def is_super_check(message):
    if config.Supervisor in [role.id for role in message.author.roles]:
        return True
    elif config.Admin in [role.id for role in message.author.roles]:
        return True
    elif message.author.id == config.Owner:
        return True
    raise No_Super

def is_super():
    return commands.check(lambda ctx: is_super_check(ctx.message))

def is_mod_check(message):
    if config.Moderator in [role.id for role in message.author.roles]:
        return True
    elif config.Supervisor in [role.id for role in message.author.roles]:
        return True
    elif config.Admin in [role.id for role in message.author.roles]:
        return True
    elif message.author.id == config.Owner:
        return True
    raise No_Mod

def is_mod():
    return commands.check(lambda ctx: is_mod_check(ctx.message))

def is_appr_check(message):
    if config.Apprentice in [role.id for role in message.author.roles]:
        return True
    elif config.Moderator in [role.id for role in message.author.roles]:
        return True
    elif config.Supervisor in [role.id for role in message.author.roles]:
        return True
    elif config.Admin in [role.id for role in message.author.roles]:
        return True
    elif message.author.id == config.Owner:
        return True
    raise No_Appr

def is_appr():
    return commands.check(lambda ctx: is_appr_check(ctx.message))

def is_event_check(message):
    if config.Event in [role.id for role in message.author.roles]:
        return True
    raise No_Event

def is_event():
    return commands.check(lambda ctx: is_event_check(ctx.message))