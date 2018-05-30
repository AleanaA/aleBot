import os
import configparser
import logging
import asyncio
import inspect
import discord
import time
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils import checks
from utils.config import Config
from utils.cog import Cog

config = configparser.ConfigParser()

class Profile(Cog):
    @commands.command(name='profile',
                description="",
                brief="")
    @checks.is_owner()
    async def profile(self, ctx):
        if os.path.exists('data/profiles/{}.ini'.format(ctx.message.author.id)):
            config.read('data/profiles/{}.ini'.format(ctx.message.author.id))
            embed = discord.Embed(color=0x00aaff)
            embed.set_author(name="Profile for " + str(ctx.message.author),icon_url=ctx.message.author.avatar_url)
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            embed.add_field(name="Name", value=config['PROFILE']['Name'], inline=False)
            embed.add_field(name="Description", value=config['PROFILE']['Description'], inline=False)
            embed.add_field(name="Rep", value=config['PROFILE']['Rep'], inline=False)
            await ctx.message.channel.send(embed=embed)
        else:
            config['PROFILE'] = {'Name': ctx.message.author.name,
                                'Description': 'None',
                                'Rep': '0'}
            with open('data/profiles/{}.ini'.format(ctx.message.author.id), 'w') as configfile:
                config.write(configfile)
            await ctx.message.channel.send("w.i.p")

    @commands.command(name='+rep',
                description="",
                brief="")
    @checks.is_owner()
    async def prep(self, ctx):
        config.read('data/profiles/{}.ini'.format(ctx.message.author.id))
        config['PROFILE']['Rep'] = str(int(config['PROFILE']['Rep']) + 1)
        with open('data/profiles/{}.ini'.format(ctx.message.author.id), 'w') as configfile:
            config.write(configfile)
        await ctx.message.channel.send("w.i.p")

    @commands.command(name='-rep',
                description="",
                brief="")
    @checks.is_owner()
    async def mrep(self, ctx):
        config.read('data/profiles/{}.ini'.format(ctx.message.author.id))
        config['PROFILE']['Rep'] = str(int(config['PROFILE']['Rep']) - 1)
        with open('data/profiles/{}.ini'.format(ctx.message.author.id), 'w') as configfile:
            config.write(configfile)
        await ctx.message.channel.send("w.i.p")

    @commands.command(name='desc',
                description="",
                brief="")
    @checks.is_owner()
    async def desc(self, ctx, *desc):
        config.read('data/profiles/{}.ini'.format(ctx.message.author.id))
        await ctx.message.channel.send(desc)
        config['PROFILE']['Description'] = " ".join(desc)
        with open('data/profiles/{}.ini'.format(ctx.message.author.id), 'w') as configfile:
            config.write(configfile)
        await ctx.message.channel.send("w.i.p")

def setup(bot):
    bot.add_cog(Profile(bot))