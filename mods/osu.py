import asyncio
import discord
import requests
from osuapi import OsuApi, AHConnector, enums
from discord.ext import commands
from utils.embed import Embeds
from utils.config import Config
from utils.cog import Cog

class Osu:
    def __init__(self, bot):
        if bot.config.osuapi == None:
            bot.unload_extension("mods.osu")
        else:
            self.bot = bot
            self.osu = OsuApi(bot.config.osuapi, connector=AHConnector())