import discord
from discord.ext import commands
from utils.dataIO import dataIO
from utils.cog import Cog
from utils.embed import Embeds
from config import emotes
from utils import checks
import os
import asyncio
import time
from datetime import datetime

class Options:
    def __init__(self, bot):
        self.bot = bot
        self.serverpath = "data/servers.json"
        self.server = dataIO.load_json(self.serverpath)
        self.defaults = {
            "RankMute": None,
            "RankEvent": None,
            "Rank1": None,
            "Rank2": None,
            "Rank3": None,
            "Audit": None,
            "Logging": None,
            "Announcement": None,
            "Use Embeds": True,
            "Blacklist": []
        }
    
    def defaultopts(self, server, value='all'):
        if value == "all":
            self.server[server] = {}
            for value in self.defaults:
                self.server[server][value] = self.defaults[value]
        elif value in self.defaults:
            self.server[server][value] = self.defaults[value]
        dataIO.save_json(self.serverpath, self.server)

    @commands.group(name='options',
                    description="Changes options for the current server",
                    brief="Changes server options.")
    async def servoptions(self, ctx):
        if str(ctx.message.guild.id) not in self.server:
            self.defaultopts(str(ctx.message.guild.id))
            await ctx.message.send("Server options have been setup!")

        if ctx.invoked_subcommand is None:
            emb = Embeds.create_embed(self, ctx,
            "Server Manager " + emotes.Warn,
            0xffff00,
            "Please issue a valid subcommand!\nAvailable options are:",
            Com1 = ["set", "Sets an options for the current server", False],
            Com2 = ["default", "Resets an option to its default value for the current server", False])
            await ctx.message.channel.send(embed=emb)
            
    @servoptions.command(name='set')
    async def setoption(self, ctx, name, *value):
        if name in self.defaults:
            if isinstance(self.server[str(ctx.message.guild.id)][name], list):
                self.server[str(ctx.message.guild.id)][name].append(value)
            else:
                self.server[str(ctx.message.guild.id)][name] = value
            dataIO.save_json(self.serverpath, self.server)
        else:
            await ctx.send("Not a valid option {}".format(name))
            return
        await ctx.send("Set {}".format(name))

    @servoptions.command(name='default')
    async def defaultoption(self, ctx, name='all'):
        self.defaultopts(str(ctx.message.guild.id), name)
        await ctx.send("Defaulted all options.")

def check_folders():
    if not os.path.exists("data"):
        print("Creating data folder...")
        os.makedirs("data")

def check_files():
    f = "data/servers.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty options.json...")
        dataIO.save_json(f, {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Options(bot))