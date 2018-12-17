import discord
from discord.ext import commands
from utils.dataIO import fileIO
from utils.cog import Cog
from utils.embed import Embeds as emb
from utils import checks
import os
import asyncio
import time
from datetime import datetime

class Profiles(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = fileIO("data/profiles.json", "load")

    @commands.command(name="profile")
    async def getprofile(self, ctx, user:discord.User=None):
        if user:
            pass
        else:
            pass
    
    @commands.command(name="marry")
    async def marry(self, ctx, user:discord.User):
        pass

    @commands.command(name="divorce")
    async def divorce(self, ctx):
        pass
    
    @commands.command(name="setprofile")
    async def setprofile(self, ctx, attrib, user:discord.User=None):
        if ctx.message.author.id == self.bot.owner.id:
            pass
        else:
            pass