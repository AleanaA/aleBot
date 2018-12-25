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
        self.profilepath = "data/options.json"
        self.profiles = dataIO.load_json(self.profilepath)

    @commands.command(name='options',
                    description="Changes options for the current server",
                    brief="Changes server options.")
    async def servoptions(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = Embeds.create_embed(self, ctx,
            "Server Manager " + emotes.Warn,
            0xffff00,
            "Please issue a valid subcommand!\nAvailable options are:",
            Com1 = ["Placeholder", "Placeholder", False],
            Com2 = ["Placeholder", "Placeholder", False])
            await ctx.message.channel.send(embed=emb)
            
def check_folders():
    if not os.path.exists("data"):
        print("Creating data folder...")
        os.makedirs("data")


def check_files():
    f = "data/options.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty options.json...")
        dataIO.save_json(f, {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Options(bot))