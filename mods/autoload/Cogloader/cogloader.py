import asyncio
import discord
import inspect
import aiohttp
import requests, zipfile, io, os
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
            await ctx.send("Ensure you run a subcommand!")

    @cog.command(name='load',
                description="Loads a cog",
                brief="Loads a cog")
    async def load(self, ctx, folder, mod):
        cog = "mods.{}.{}".format(folder, mod)
        emb = Embeds.create_embed(self, ctx)
        emb.title = "Load Cog"
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
    async def unload(self, ctx, folder, mod):
        cog = "mods.{}.{}".format(folder, mod)
        emb = Embeds.create_embed(self, ctx)
        emb.title = "Unload Cog"
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
    async def reload(self, ctx, folder, mod):
        cog = "mods.{}.{}".format(folder, mod)
        emb = Embeds.create_embed(self, ctx)
        emb.title = "Reload Cog"
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
        emb = Embeds.create_embed(self, ctx)
        emb.title = "Loaded Cogs"
        emb.colour = 0x00ffff
        for cog in self.bot.cogs:
            cog = self.bot.cogs[cog]
            try:
                emb.add_field(name=cog.qualified_name, value="{}\n{}".format(cog.__class__.__module__, cog.url), inline=False)
            except Exception:
                emb.add_field(name=cog.qualified_name, value="{}".format(cog.__class__.__module__), inline=False)
        await ctx.message.channel.send(embed=emb)

    @cog.command(name='download',
                description="Download a cog and load it!",
                brief="Download a cog")
    async def download(self, ctx, name:str, cogurl:str):
        print("Download triggered for {}".format(name))
        emb = Embeds.create_embed(self, ctx)
        emb.title = "Download Cog"
        emb.colour = 0x00ffff
        try:
            print("Starting get for {}".format(name))
            r = requests.get(cogurl)
            if not os.path.exists("mods/{}".format(name)):
                os.makedirs("mods/{}".format(name))
            with open("mods/{0}/{0}.py".format(name), 'wb') as f:
                print("Writing {}".format(name))
                f.write(r.content)
            emb.description = "Cog successfully downloaded"
        except Exception as e:
            emb.description = "Unable to download cog.\n{}".format(e)
            return
        try:
            print("Attempting to load cog")
            self.bot.load_extension("mods.{0}.{0}".format(name))
            print("Successfully loaded cog")
        except Exception as e:
            print("Failed to load Downloaded cog:")
            print(e)
        await ctx.send(embed=emb)

    @cog.command(name='bulk',
                description="Bulk download a set of cogs or include a cogs utilities from a zip!",
                brief="Download a zip!")
    async def bulkdl(self, ctx, zipurl:str):
        emb = Embeds.create_embed(self, ctx)
        emb.title = "Download Cogs"
        emb.colour = 0x00ffff
        try:
            r = requests.get(zipurl, stream =True)
            check = zipfile.is_zipfile(io.BytesIO(r.content))
            while not check:
                r = requests.get(zipurl, stream =True)
                check = zipfile.is_zipfile(io.BytesIO(r.content))
            else:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall("mods/")
            emb.description = "Cog successfully downloaded"
        except Exception as e:
            emb.description = "Unable to download cog.\n{}".format(e)
            return
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(CogLoader(bot))