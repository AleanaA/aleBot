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
from config import emotes
from config import config
from utils import checks
from utils.embed import Embeds
from utils.config import Config
from utils.cog import Cog

class Commands(Cog):
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
        if math.ceil(self.bot.latency * 1000) <= 30:
            emote = emotes.Done
        elif math.ceil(self.bot.latency * 1000) <= 60:
            emote = emotes.Warn
        else:
            emote = emotes.Error
            
        await ctx.message.channel.send(ctx.message.author.mention + " " + str(math.ceil(self.bot.latency * 1000)) + " ms " + emote)

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

    @commands.command(name='Command1', description="This is the first command!")
    async def defname(self, ctx):
        await ctx.send("This would send a normal message!")
        emb = discord.Embed()
        emb.title = "This is an embed!"
        emb.description = "These are pretty nifty when you get the hand of them!"
        emb.color = 0x00ffff # Setting colors is fun!
        emb.set_thumbnail(url=self.bot.user.avatar_url) # Setting a thumbnail for the message uses url's!
        await ctx.send("This would send a normal message *and* and embed!", embed=emb)
        emb.add_field(name="This is a field!", value="They're pretty great!")
        emb.add_field(name="This field isn't inline", value="Because inline is set to false!", inline=False)
        emb.add_field(name="But these fields", value="Because inline is", inline=True)
        emb.add_field(name="are inline!", value="set to true!", inline=True)
        await ctx.send("This would send the new embed!", embed=emb)

def setup(bot):
    bot.add_cog(Commands(bot))