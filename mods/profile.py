import discord
from discord.ext import commands
from utils.dataIO import dataIO
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
        self.profiles = dataIO.load_json(self.profilepath)

    @commands.command(name="profile")
    async def getprofile(self, ctx, user:discord.User=None):
        # Check if a user is specified
        if user is None:
            user = ctx.message.author

        userid = str(user.id)
        # Check if specified user has a profile already, if they don't, make one
        if userid in self.profiles:
            pass
        else:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = None
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            dataIO.save_json(self.profilepath, self.profiles)

        profile = self.profiles[userid]

        emb = Embeds.create_embed(self, ctx, user.name, 0x00aaff)

        emb.set_thumbnail(url=user.avatar_url)

        if profile["Description"] != None:
            emb.description = profile["Description"]
        else:
            emb.description = "This user hasn't set a description yet!"


        if profile["Title"] != None:
            emb.add_field(name="Title", value="[{}]".format(profile["Title"]), inline=False)

        emb.add_field(name="Kudos", value=str(profile["Kudos"]))

        if profile["Married"] != None:
            marriedto = await self.bot.get_user_info(profile["Married"])
            emb.add_field(name="Married To", value=":heart: {} :heart:".format(marriedto.name), inline=False)

        await ctx.send(embed=emb)   
    
    @commands.command(name="marry")
    async def marry(self, ctx, user:discord.User):
        if ctx.message.author == user:
            await ctx.send("You can't marry yourself!")
            return
        authid = str(ctx.message.author.id)
        userid = str(user.id)
        # Check if specified user has a profile already, if they don't, make one
        if authid not in self.profiles:
            self.profiles[authid] = {}
            self.profiles[authid]["Description"] = None
            self.profiles[authid]["Title"] = None
            self.profiles[authid]["Married"] = None
            self.profiles[authid]["Kudos"] = 0
            dataIO.save_json(self.profilepath, self.profiles)
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = None
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            dataIO.save_json(self.profilepath, self.profiles)

        authprofile = self.profiles[authid]
        userprofile = self.profiles[userid]

        msg = await ctx.send("Do you, {}, take {}'s hand in marriage?".format(user.name, ctx.message.author.name))
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")

        def check(reaction, reactor):
            return reactor == user and str(reaction.emoji) == '✅' and reaction.message == msg or reactor == user and str(reaction.emoji) == '❎' and reaction.message == msg

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Reaction timed out.")
            await msg.delete()
        else:
            if str(reaction.emoji) == '✅':
                await ctx.send("Temp Confirm Msg")
            if str(reaction.emoji) == '❎':
                await ctx.send("Request has been denied. Better luck next time, {}!".format(ctx.message.author.name))


    @commands.command(name="divorce")
    async def divorce(self, ctx):
        pass

    @commands.command(name="givekudos")
    async def givekudos(self, ctx, user: discord.User):
        if ctx.message.author == user:
            await ctx.send("You can't give yourself Kudos!")
            return
        userid = str(user.id)
        # Check if specified user has a profile already, if they don't, make one
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = None
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 1
            dataIO.save_json(self.profilepath, self.profiles)
        else:
            profile = self.profiles[userid]
            profile["Kudos"] = profile["Kudos"] + 1
            self.profiles[userid] = profile
            dataIO.save_json(self.profilepath, self.profiles)
        await ctx.send("You gave kudos to {}!".format(user.mention))

    @commands.command(name="setdesc")
    async def setdesc(self, ctx, *, content : str):
        if len(content) > 25:
            await ctx.send("Descriptions have a character limit of 25 characters!")
        user = ctx.message.author
        userid = str(user.id)
        # Check if specified user has a profile already, if they don't, make one
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = content
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            dataIO.save_json(self.profilepath, self.profiles)
        else:
            profile = self.profiles[userid]
            profile["Description"] = content
            self.profiles[userid] = profile
            dataIO.save_json(self.profilepath, self.profiles)
        await ctx.send("Description set to {}".format(content))

    @commands.command(name="setattrib")
    @checks.is_owner()
    async def setattrib(self, ctx, user:discord.User, attrib, *, content:str):
        userid = str(user.id)
        # Check if specified user has a profile already, if they don't, make one
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = None
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            dataIO.save_json(self.profilepath, self.profiles)

        profile = self.profiles[userid]
    
        if attrib.lower() == "description":
            profile["Description"] = content
            self.profiles[userid] = profile
            dataIO.save_json(self.profilepath, self.profiles)
            await ctx.send("User {}'s description set to {}".format(user.name, content))

        if attrib.lower() == "title":
            profile["Title"] = content
            self.profiles[userid] = profile
            dataIO.save_json(self.profilepath, self.profiles)
            await ctx.send("User {}'s title was set to {}".format(user.name, content))
        
        if attrib.lower() == "kudos":
            message = ''.join(content)
            split = message.split(' ')
            if split[0] == "remove":
                profile = self.profiles[userid]
                profile["Kudos"] = profile["Kudos"] - int(split[1])
                self.profiles[userid] = profile
                dataIO.save_json(self.profilepath, self.profiles)
                await ctx.send("Removed {} Kudos from {}'s profile!".format(split[1], user.name))
            if split[0] == "add":
                profile = self.profiles[userid]
                profile["Kudos"] = profile["Kudos"] + int(split[1])
                self.profiles[userid] = profile
                dataIO.save_json(self.profilepath, self.profiles)
                await ctx.send("Added {} Kudos to {}'s profile!".format(split[1], user.name))

def check_folders():
    if not os.path.exists("data"):
        print("Creating data folder...")
        os.makedirs("data")


def check_files():
    f = "data/profiles.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty profiles.json...")
        dataIO.save_json(f, {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Profiles(bot))