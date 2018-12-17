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
        self.profiles = fileIO("data/profiles.json", "load")

    @commands.command(name="profile")
    async def getprofile(self, ctx, user:discord.User=None):
        if user:
            self.tags.append({"User": Guild.id, "Married": None, "Creation": Creation, "Name": name, "Content": content})
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
        if ctx.message.author.id == self.bot.config.owner:
            pass
        else:
            pass


def check_folders():
    if not os.path.exists("data"):
        print("Creating data folder...")
        os.makedirs("data")

def check_files():
    f = "data/profiles.json"
    if not fileIO(f, "check"):
        print("Creating empty profiles.json...")
        fileIO(f, "save", [])

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Profiles(Cog))