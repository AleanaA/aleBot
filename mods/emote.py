import asyncio
import discord
import requests
from discord.ext import commands
from utils.embed import Embeds
from utils.config import Config

class Emote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='e',
                description="Manage emotes on the current server!",
                brief="Manage emotes on the current server!")
    @commands.guild_only()
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    async def emote(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = Embeds.create_embed(self, ctx,
            "Emote Manager",
            0xffff00,
            "Please issue a valid subcommand!\nAvailable options are:",
            Com1 = ["Add", "ale!e add <URL> <Name>", False],
            Com2 = ["Del", "Removes an emote from the current server.", False],
            Com3 = ["Rep", "Replaces an emote on the current server.", False],
            Com4 = ["Steal", "Steals an emote to add to the current server.", False])
            await ctx.message.channel.send(embed=emb)

    @emote.command(name='add',
                description="Adds an emote to the current server.")
    async def emoteadd(self, ctx, url, name):
        emb = Embeds.create_embed(self, ctx, "Emote Manager", 0x00ff00, None)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
            emb.colour = 0xff0000
            emb.description = "An error occured. Unable to get emote from url."
            return await ctx.send(embed=emb)
        if response.status_code == 404:
            emb.colour = 0xff0000
            emb.description = "404 error occured."
            return await ctx.send(embed=emb)
        emote = await ctx.guild.create_custom_emoji(name=name, image=response.content)
        emb.description = "Successfully added the emote {0.name} <{1}:{0.name}:{0.id}>!".format(emote, "a" if emote.animated else "")
        await ctx.send(embed=emb)

    @emote.command(name='del',
                description="Removes an emote from the current server.")
    async def emotedel(self, ctx, name):
        emb = Embeds.create_embed(self, ctx, "Emote Manager", 0x00ff00, None)
        emotelist = [x for x in ctx.guild.emojis if x.name == name]
        emote_length = len(emotelist)
        for emote in emotelist:
            await emote.delete()
        if emote_length == 0:
            emb.colour = 0xff0000
            emb.description = "No emotes with the name {} could be found on this server.".format(name)
        elif emote_length == 1:
            emb.description = "Successfully removed the {} emote!".format(name)
        else:
            emb.description = "Successfully removed {} emotes with the name {}.".format(emote_length, name)
        await ctx.send(embed=emb)

    @emote.command(name='rep',
                description="Replaces an emote on the current server.")
    async def emoterep(self, ctx, url, name):
        emote = discord.utils.get(ctx.guild.emojis, name=name)
        emb = Embeds.create_embed(self, ctx, "Emote Manager", 0x00ff00, None)

        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
            emb.colour = 0xff0000
            emb.description = "An error occured. Unable to get emote from url."
            return await ctx.send(embed=emb)
        if response.status_code == 404:
            emb.colour = 0xff0000
            emb.description = "404 error occured."
            return await ctx.send(embed=emb)

        if emote == None:
            emb.colour = 0xff0000
            emb.description = "No emotes with the name {} could be found on this server.".format(name)
        else:
            await emote.delete()
            emote = await ctx.guild.create_custom_emoji(name=name, image=response.content)
            emb.description = "Successfully replaced the emote {0.name} <{1}:{0.name}:{0.id}>!".format(emote, "a" if emote.animated else "")

        await ctx.send(embed=emb)
    
    @emote.command(name='steal')
    async def emotesteal(self, ctx, emotes:commands.Greedy[discord.PartialEmoji]):
        async with ctx.typing():
            fails = 0
            for emote in emotes:
                name = str(emote.name)
                url = str(emote.url)
                try:
                    response = requests.get(url)
                except Exception as e:
                    print(e)
                    fails = fails+1
                try:
                    await ctx.guild.create_custom_emoji(name=name, image=response.content)
                except Exception as e:
                    print(e)
                    fails = fails+1
            await asyncio.sleep(10)
            if fails == 1:
                fs = "emote"
            else:
                fs = "emotes"
            if len(emotes) == 1:
                em = "emote"
            else:
                em = "emotes"
            await ctx.send("Tried to steal {} {}, failed on {} {}.".format(len(emotes), em, fails, fs))

def setup(bot):
    bot.add_cog(Emote(bot))