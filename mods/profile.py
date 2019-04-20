import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils.embed import Embeds
import os
import asyncio
import time
import datetime
import collections

class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.epoch = datetime.datetime.utcfromtimestamp(0)
        self.profilepath = "data/profiles.json"
        self.profiles = dataIO.load_json(self.profilepath)

    @commands.command(name="profile")
    async def getprofile(self, ctx, user:discord.User=None):
        # Check if a user is specified
        if user is None:
            user = ctx.message.author

        userid = str(user.id)
        # Check if specified user has a profile already, if they don't, make one
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = None
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            self.profiles[userid]["xp"] = 0
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
            marriedto = self.bot.get_user(profile["Married"])
            emb.add_field(name="Married To", value=":heart: {} :heart:".format(marriedto.name), inline=False)

        emb.add_field(name="XP", value=str(profile["xp"]), inline=False)

        await ctx.send(embed=emb)   
    
    @commands.command(name="marry")
    async def marry(self, ctx, user:discord.User):
        if ctx.message.author == user:
            await ctx.send("You can't marry yourself!")
            return
        if user == self.bot.user:
            await ctx.send("I'm a robot silly, I can't marry anyone!")
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
            self.profiles[userid]["xp"] = 0
            dataIO.save_json(self.profilepath, self.profiles)
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = None
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            self.profiles[userid]["xp"] = 0
            dataIO.save_json(self.profilepath, self.profiles)

        authprofile = self.profiles[authid]
        userprofile = self.profiles[userid]

        if userprofile["Married"] != None:
            await ctx.send("This user is already married!")
            return

        msg = await ctx.send("Do you, {}, take {}'s hand in marriage?".format(user.name, ctx.message.author.name))
        await msg.add_reaction("✅")
        await msg.add_reaction("❎")

        def check(reaction, reactor):
            return reactor == user and str(reaction.emoji) == '✅' and reaction.message.id == msg.id or reactor == user and str(reaction.emoji) == '❎' and reaction.message.id == msg.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Reaction timed out.")
            await msg.delete()
        else:
            if str(reaction.emoji) == '✅':
                authprofile["Married"] = user.id
                userprofile["Married"] = ctx.message.author.id
                self.profiles[authid] = authprofile
                self.profiles[userid] = userprofile
                dataIO.save_json(self.profilepath, self.profiles)
                await ctx.send("Congratulations {}, you and {} are now married!".format(ctx.message.author.name, user.name))
                await msg.delete()
            if str(reaction.emoji) == '❎':
                await ctx.send("Request has been denied. Better luck next time, {}!".format(ctx.message.author.name))
                await msg.delete()


    @commands.command(name="divorce")
    async def divorce(self, ctx):
        userid = str(ctx.message.author.id)
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = None
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            self.profiles[userid]["xp"] = 0
            dataIO.save_json(self.profilepath, self.profiles)
        authprofile = self.profiles[userid]
        if authprofile["Married"] is None:
            await ctx.send("You aren't married, {}!".format(ctx.message.author.name))
            return
        
        marriedto = self.bot.get_user(authprofile["Married"])
        userprofile = self.profiles[str(authprofile["Married"])]
    
        authprofile["Married"] = None
        userprofile["Married"] = None
        self.profiles[userid] = authprofile
        self.profiles[str(authprofile["Married"])] = userprofile
        dataIO.save_json(self.profilepath, self.profiles)
        await ctx.send("{}, {} divorced you!".format(marriedto.mention, ctx.message.author.name))

    @commands.command(name="givekudos")
    @commands.cooldown(1, 86400, type=commands.BucketType.user)
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
            self.profiles[userid]["xp"] = 0
            dataIO.save_json(self.profilepath, self.profiles)
        else:
            profile = self.profiles[userid]
            profile["Kudos"] = profile["Kudos"] + 1
            self.profiles[userid] = profile
            dataIO.save_json(self.profilepath, self.profiles)
        await ctx.send("You gave kudos to {}!".format(user.mention))

    @commands.command(name="setdesc")
    async def setdesc(self, ctx, *, content : str):
        if len(content) > 50:
            await ctx.send("Descriptions have a character limit of 50 characters!")
            return
        user = ctx.message.author
        userid = str(user.id)
        # Check if specified user has a profile already, if they don't, make one
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = content
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            self.profiles[userid]["xp"] = 0
            dataIO.save_json(self.profilepath, self.profiles)
        else:
            profile = self.profiles[userid]
            profile["Description"] = content
            self.profiles[userid] = profile
            dataIO.save_json(self.profilepath, self.profiles)
        await ctx.send("Description set to {}".format(content))

    @commands.command(name="setattrib")
    @commands.is_owner()
    async def setattrib(self, ctx, user:discord.User, attrib, *, content:str):
        userid = str(user.id)
        # Check if specified user has a profile already, if they don't, make one
        if userid not in self.profiles:
            self.profiles[userid] = {}
            self.profiles[userid]["Description"] = None
            self.profiles[userid]["Title"] = None
            self.profiles[userid]["Married"] = None
            self.profiles[userid]["Kudos"] = 0
            self.profiles[userid]["xp"] = 0
            dataIO.save_json(self.profilepath, self.profiles)

        profile = self.profiles[userid]
    
        if attrib.lower() == "description":
            profile["Description"] = content
            dataIO.save_json(self.profilepath, self.profiles)
            await ctx.send("User {}'s description set to {}".format(user.name, content))

        if attrib.lower() == "title":
            profile["Title"] = content
            dataIO.save_json(self.profilepath, self.profiles)
            await ctx.send("User {}'s title was set to {}".format(user.name, content))
        
        if attrib.lower() == "kudos":
            message = ''.join(content)
            split = message.split(' ')
            if split[0] == "remove":
                profile["Kudos"] = profile["Kudos"] - int(split[1])
                dataIO.save_json(self.profilepath, self.profiles)
                await ctx.send("Removed {} Kudos from {}'s profile!".format(split[1], user.name))
            if split[0] == "add":
                profile["Kudos"] = profile["Kudos"] + int(split[1])
                dataIO.save_json(self.profilepath, self.profiles)
                await ctx.send("Added {} Kudos to {}'s profile!".format(split[1], user.name))

        if attrib.lower() == "xp":
            profile['xp'] = int(content)
            dataIO.save_json(self.profilepath, self.profiles)
            await ctx.send("Set {}'s xp to {}!".format(user.name, content))

    def user_add_xp(self, user_id, xp):
        # Check if specified user has a profile already, if they don't, make one
        if str(user_id) not in self.profiles:
            self.profiles[user_id] = {}
            self.profiles[user_id]["Description"] = None
            self.profiles[user_id]["Title"] = None
            self.profiles[user_id]["Married"] = None
            self.profiles[user_id]["Kudos"] = 0
            self.profiles[user_id]["xp"] = xp
            dataIO.save_json(self.profilepath, self.profiles)
        else:
            profile = self.profiles[str(user_id)]
            try:
                profile['xp'] += xp
            except KeyError:
                profile['xp'] = xp
            dataIO.save_json(self.profilepath, self.profiles)

    @commands.command(name="xplb")
    async def xplb(self, ctx):
        lbtext =''
        usercount = 0
        xplbls = {}
        for userid, dic in self.profiles.items():
            try:
                user = self.bot.get_user(int(userid))
            except ValueError:
                pass
            try:
                if user.bot == False:
                    xplbls[str(user)] = dic['xp']
            except KeyError:
                pass
        sortedlb = sorted(xplbls, key=lambda x: xplbls[x], reverse=True)
        for value in sortedlb:
            if usercount != 10:
                lbtext += "{} - {} XP\n".format(value, xplbls[value])
                usercount += 1
        await ctx.send("```{}```".format(lbtext))

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