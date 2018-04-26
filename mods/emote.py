import asyncio
import discord
import inspect
import aiohttp
import utils
import requests
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils import checks
from utils.config import Config
from utils.cog import Cog

class Emote(Cog):

    @commands.group(name='emote',
                description="Manage emotes on the current server!",
                brief="Manage emotes on the current server!")
    @checks.is_super()
    async def emote(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed()
            emb.title = "Emote Manager " + emotes.Warn
            emb.colour = 0xffff00
            emb.description = "Please issue a valid subcommand!\nAvailable options are:"
            emb.add_field(name="Add", value="Adds an emote to the current server!", inline=False)
            emb.add_field(name="Del", value="Removes an emote from the current server!", inline=False)
            await ctx.message.channel.send(embed=emb)

    @emote.command(name='add',
                description="Adds an emote to the current server!")
    async def emoteadd(self, ctx, name, url):
        emb = discord.Embed()
        emb.title = "Emote Manager"
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
            emb.colour = 0xff0000
            emb.description = "An error occured. Unable to get emotes from url."
            return await ctx.message.channel.send(embed=emb)
        if response.status_code == 404:
            emb.colour = 0xff0000
            emb.description = "404 error occured."
            return await ctx.message.channel.send(embed=emb)
        emote = await ctx.message.guild.create_custom_emoji(name=name, image=response.content)
        emb.colour = 0x00ff00
        emb.description = "Successfully added the emote {0.name} <{1}:{0.name}:{0.id}>!".format(emote, "a" if emote.animated else "")
        await ctx.message.channel.send(embed=emb)

    @emote.command(name='del',
                description="Removes an emote from the current server!")
    async def emotedel(self, ctx, name):
        emb = discord.Embed()
        emb.title = "Emote Manager"
        emotelist = [x for x in ctx.guild.emojis if x.name == name]
        emote_length = len(emotelist)
        if not emotes:
            emb.colour = 0xff0000
            emb.description = "No emotes with the name {} could be found on this server.".format(name)
            return await ctx.message.channel.send(embed=emb)
        for emote in emotelist:
            await emote.delete()
        if emote_length == 1:
            emb.description = "Successfully removed the {} emote!".format(name)
        else:
            emb.description = "Successfully removed {} emotes with the name {}.".format(emote_length, name)
        emb.colour = 0x00ff00
        await ctx.message.channel.send(embed=emb)


def setup(bot):
    bot.add_cog(Emote(bot))