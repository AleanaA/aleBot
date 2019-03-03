import asyncio
import discord
import inspect
import aiohttp
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils.config import Config
from utils.embed import Embeds

class CogLoader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group(name='cog',
                    description="Command for Cog management.",
                    brief="Command for Cog management.")
    @commands.is_owner()
    async def cog(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = Embeds.create_embed(self, ctx,
            "Cog Loader",
            0xffff00,
            "Please issue a valid subcommand!\nAvailable options are:",
            Com1 = ["load", "Loads a cog into the bot.", False],
            Com2 = ["unload", "Unloads a cog loaded into the bot.", False],
            Com3 = ["reload", "Reloads a cog loaded into the bot.", False],
            Com4 = ["list", "Lists all cogs loaded into the bot."])
            await ctx.message.channel.send(embed=emb)

    @cog.command(name='load',
                description="Loads a cog",
                brief="Loads a cog")
    async def load(self, ctx, mod):
        cog = "mods." + mod
        emb = discord.Embed()
        emb.title = "Cog Loader"
        try:
            self.bot.load_extension(cog)
            emb.description = "Loaded cog `" + mod + "` successfully"
            emb.colour = 0x00ff00
            await ctx.message.channel.send(embed=emb)
            print("User " + str(ctx.message.author) + " loaded module " + mod)
        except Exception as e:
            emb.description = 'Failed to load mod {0}\n{1}: {2}'.format(cog, type(e).__name__, e)
            emb.colour = 0xff0000
            await ctx.message.channel.send(embed=emb)

    @cog.command(name='unload',
                description="Unloads a cog",
                brief="Unloads a cog")
    async def unload(self, ctx, mod):
        cog = "mods." + mod.lower()
        emb = discord.Embed()
        emb.title = "Cog Loader"
        if mod.lower() == "cogloader":
            emb.description = "Unable to unload Cog Loader."
            emb.colour = 0xff0000
            await ctx.message.channel.send(embed=emb)
            return
        try:
            self.bot.unload_extension(cog)
            emb.description = "Unloaded cog `" + mod + "` successfully"
            emb.colour = 0x00ff00
            await ctx.message.channel.send(embed=emb)
            print("User " + str(ctx.message.author) + " unloaded module " + mod)
        except Exception as e:
            emb.description = 'Failed to unload mod {0}\n{1}: {2}'.format(cog, type(e).__name__, e)
            emb.colour = 0xff0000
            await ctx.message.channel.send(embed=emb)

    @cog.command(name='reload',
                description="Reloads a cog",
                brief="Reloads a cog")
    async def reload(self, ctx, mod):
        cog = "mods." + mod
        emb = discord.Embed()
        emb.title = "Cog Loader"
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            emb.description = "Reloaded cog `" + mod + "` successfully"
            emb.colour = 0x00ff00
            await ctx.message.channel.send(embed=emb)
            print("User " + str(ctx.message.author) + " reloaded module " + mod)
        except Exception as e:
            emb.description = 'Failed to reload mod {0}\n{1}: {2}'.format(cog, type(e).__name__, e)
            await ctx.message.channel.send(embed=emb)

    @cog.command(name='list',
                description="Lists loaded cogs",
                brief="Lists loaded cogs")
    async def list(self, ctx):
        emb = discord.Embed()
        emb.title = "Loaded Cogs"
        emb.colour = 0x00ffff
        emb.description = '\n'.join(list(self.bot.cogs.keys()))
        await ctx.message.channel.send(embed=emb)

def setup(bot):
    bot.add_cog(CogLoader(bot))