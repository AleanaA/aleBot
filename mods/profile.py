import discord
from discord.ext import commands
from utils.dataIO import fileIO
from utils.cog import Cog
from utils.embed import Embeds
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
        # Check if a user is specified
        if user == None:
            user = ctx.message.author
        # Check if specified user has a profile already, if they don't, make one
        if user.id in self.profiles:
            profile = self.profiles[user.id]
        else:
            self.profiles.append({"User": user.id, "Married": None, "Description": None, "Title": None})
            fileIO("data/profiles.json", "save", self.profiles)
            profile = self.profiles[user.id]
        # Check for description
        if profile["Description"] != None:
            profiledesc = profile["Description"]
        else:
            profiledesc = "This user hasn't set a description yet!"

        emb = Embeds.create_embed(self, ctx, user.name, 0x00aaff, profiledesc)
        # Check for title        
        if profile["Title"] != None:
            emb.add_field(name="Title", value=profile["Title"], inline=False)
        # Check for marriage
        if profile["Married"] != None:
            marriedto = await self.bot.get_user_info(profile["Married"])
            emb.add_field(name="Married To", value=marriedto.name, inline=False)
        else:
            emb.add_field(name="Married To", value="This user isn't married!")
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