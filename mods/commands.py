import asyncio
import discord
import math
import inspect
import datetime
import aiohttp
import utils
import json
import requests
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import config
from utils.embed import Embeds
from utils.config import Config

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help',
                hidden=True)
    async def help(self, ctx):
        emb = Embeds.create_embed(self, ctx, "Help", color=0x00ff00, message="https://aleanaazure.xyz/doku.php?id=alebot")
        await ctx.send(embed=emb)

    @commands.command(name='testnotif')
    async def testnotif(self, ctx, title, body):
        notif = {}
        notif["value1"] = title
        notif["value2"] = body
        requests.post("", data=notif)

def setup(bot):
    bot.add_cog(Commands(bot))