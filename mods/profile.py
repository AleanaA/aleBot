import discord
from discord.ext import commands
from utils.dataIO import dataIO
from dataIO import load_json, save_json
from utils.cog import Cog
from utils.embed import Embeds
from utils import checks
import os
import asyncio
import time
from datetime import datetime

class Profiles:
    def __init__(self, bot):
        self.bot = bot
        self.profilepath = "data/profiles.json"
        self.profiles = load_json(self.profilepath)

    @commands.command(name="profile")
    async def getprofile(self, ctx, user:discord.User=None):
        # Check if a user is specified
        if user == None:
            user = ctx.message.author
        # Check if specified user has a profile already, if they don't, make one
        if user.id not in self.profiles:
            self.profiles[user.id] = {}
            self.profiles[user.id]["Description"] = None
            self.profiles[user.id]["Title"] = None
            self.profiles[user.id]["Married"] = None
    
        profile = self.profiles[user.id]

        emb = Embeds.create_embed(self, ctx, user.name, 0x00aaff)

        emb.set_thumbnail(url=user.avatar_url)

        if profile["Description"] != None:
            emb.description = profile["Description"]
        else:
            emb.description = "This user hasn't set a description yet!"

        if profile["Title"] != None:
            emb.add_field(name="Title", value="[{}]".format(profile["Title"]), inline=False)

        if profile["Married"] != None:
            marriedto = await self.bot.get_user_info(profile["Married"])
            emb.add_field(name="Married To", value=":heart: {} :heart:".format(marriedto.name), inline=False)

        await ctx.send(embed=emb)   
    
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