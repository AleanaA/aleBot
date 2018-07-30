import asyncio
import discord
import inspect
import datetime
import aiohttp
import utils
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils import checks
from utils.config import Config
from utils.cog import Cog

class Voice(Cog):

    @commands.command(name='play')
    @checks.is_event()
    async def play(self, ctx):
        config = Config('config/config.ini')
        bot = ctx.message.guild.get_member(self.bot.user.id)
        owner = ctx.message.author
        state = bot.voice
        if not state:
            voice = await owner.voice.channel.connect(timeout=120.0, reconnect=True)
            source = discord.FFmpegPCMAudio(config.stream)
            voice.play(source)
            await ctx.message.channel.send("Playback started!")
        else:
            await bot.move_to(owner.voice.channel)
            await ctx.message.channel.send("Moved channels!")
    
    @commands.command(name='stop')
    @checks.is_event()
    async def stop(self, ctx):
        bot = ctx.message.guild.get_member(self.bot.user.id)
        owner = ctx.message.author
        state = bot.voice
        if state:
            await ctx.message.guild.voice_client.disconnect()
            await ctx.message.channel.send("Disconnected!")
        else:
            await ctx.message.channel.send("Not in a voice channel!")

def setup(bot):
    bot.add_cog(Voice(bot))
