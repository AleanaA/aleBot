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
    @commands.command(name='testhelp',
                hidden=True)
    async def testhelp(self, ctx):
        emb = Embeds.create_embed(self, ctx, "Help")
        for command in list(self.bot.commands):
            if command.description == "":
                desc = "No description!"
            else:
                desc = command.description

            if command.hidden != True:
                emb.add_field(name=command, value=desc, inline=False)
        await ctx.send(embed=emb)

    @commands.command(name='ping',
                description="Ping!",
                brief="Ping!",
                aliases=['Ping', 'Ping!'])
    async def ping(self, ctx):
        await ctx.message.channel.send(ctx.message.author.mention + " " + str(math.ceil(self.bot.latency * 1000)) + " ms")

    @commands.command(name='cat',
                description="Kitty!")
    async def cat(self, ctx):
        isVideo = True
        while isVideo:
            r = requests.get('http://aws.random.cat/meow')
            parsed_json = r.json()
            if parsed_json['file'].endswith('.mp4'):
                pass
            else:
                isVideo = False
        embed = discord.Embed()
        embed.set_image(url=parsed_json['file'])
        await ctx.message.channel.send(embed=embed)

    @commands.command(name='dog',
                description="Puppo!")
    async def dog(self, ctx):
        isVideo = True
        while isVideo:
            r = requests.get('https://random.dog/woof.json')
            parsed_json = r.json()
            if parsed_json['url'].endswith('.mp4'):
                pass
            else:
                isVideo = False
        embed = discord.Embed()
        embed.set_image(url=parsed_json['url'])
        await ctx.send(embed=embed)
    
    @commands.command(name='pay')
    async def payuser(self, ctx, who:discord.User=None, amount=None):
        emb = Embeds.create_embed(self, ctx, title="Payment", color=0x00ffff)
        if who == None:
            emb.description = "No user!"
            await ctx.send(embed=emb)
            return
        if amount == None:
            emb.description = "Empty amount!"
            await ctx.send(embed=emb)
            return
        if "$" not in amount:
            amount = "${}".format(amount)
        emb.description = "{} paid {} to {}!".format(ctx.message.author.name, amount, who.name)
        await ctx.send(embed=emb)
def setup(bot):
    bot.add_cog(Commands(bot))