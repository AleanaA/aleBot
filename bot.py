import asyncio
import inspect
import discord
import logging
import time
import os
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import config
from utils.config import Config
from mods.profile import Profiles

class Object(object):
    pass

emb = discord.Embed()
class bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.loop = kwargs.pop('loop', asyncio.get_event_loop())
        self.config = Config('config/config.ini')
        self.token = self.config.token
        command_prefix = kwargs.pop('command_prefix', commands.when_mentioned_or(self.config.prefix))
        super().__init__(command_prefix=command_prefix, *args, **kwargs)
        self.owner = None
        self.start_time = time.time()
        self.own_task = None
        self.last_message = None
        self.command_messages = {}
        self.messages_seen = 0
        self.remove_command('help')
    
    async def on_message(self, ctx):
        self.messages_seen += 1
        await self.process_commands(ctx)

    def __del__(self):
        self.loop.set_exception_handler(lambda *args, **kwargs: None)
    async def on_command_error(self, ctx, e):
        emb.title = ("An Error Occured")
        emb.colour = discord.Color(0xff0000)
        emb.description = str(e)
        if isinstance(e, commands.MissingRequiredArgument):
            print(str(e) + " - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, commands.CommandInvokeError):
            print(str(e) + " - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, commands.BadArgument):
            print(str(e) + " - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, commands.NotOwner):
            print("User " + str(ctx.message.author) + " lacked permission! - Command - " + ctx.message.content)
        elif isinstance(e, commands.MissingPermissions):
            print("User " + str(ctx.message.author) + " lacked permission! - Command - " + ctx.message.content)
        elif isinstance(e, commands.CommandOnCooldown):
            await ctx.send("You cannot do that yet.")

    async def on_connect(self):
        loading = discord.Activity(type=3, name="Loading Bars...")
        await self.change_presence(status=discord.Status.dnd, activity=loading)

    async def on_ready(self):
        self.appinfo = await self.application_info()
        await self.wait_until_ready()
        owner = self.appinfo.owner
        embed=discord.Embed(title="Invite URL", url="https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=8".format(str(self.user.id)), description=self.user.name + " has just loaded.", color=0x05d1dc)
        embed.set_author(name=owner.name,icon_url=owner.avatar_url)
        embed.set_thumbnail(url=self.user.avatar_url)
        game = discord.Activity(type=self.config.activity, name=self.config.status + " | {0}help".format(self.config.prefix))
        await self.change_presence(activity=game)
        print("---------------------------------------")
        print("Logged in as " + self.user.name)
        print("")
        print("Current Shared Servers:")
        notsharedcount = 0
        for server in self.guilds:
            ownercheck = self.appinfo.owner
            check = server.get_member(ownercheck.id)
            if check != None:
                print("Server ID: "+str(server.id)+" | Server Name: "+server.name)
        print("")
        print("Current Unshared Servers:")
        for server in self.guilds:
            ownercheck = self.appinfo.owner
            check = server.get_member(ownercheck.id)
            if check == None:
                print("Server ID: {0} | Server Name: {1} | Server Owner: {2}".format(server.id, server.name, server.owner))
                notsharedcount = notsharedcount+1
        embed.add_field(name="Total Users", value=len(set(self.get_all_members())))
        embed.add_field(name="Total Servers", value=str(len(self.guilds)))
        try:
            await owner.send(embed=embed)
        except Exception as e:
            print("Unable to DM owner.")
        print("")
        print("---------------------------------------")
        print("Remember to invite your bot to your server!")
        print("https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=8".format(str(self.user.id)))
        print("---------------------------------------")
        for cog in config.Modules:
                try:
                    self.load_extension(cog)
                except Exception as e:
                    msg = 'Failed to load mod {0}\n{1}: {2}'.format(cog, type(e).__name__, e)
                    print(msg)

    async def on_guild_join(self, server:discord.Guild):
        print("Bot has joined a server: {}".format(server.name))

    async def on_guild_remove(self, server:discord.Guild):
        print("Bot has left a server: {}".format(server.name))

    def run(self):
        super().run(self.config.token)

    def die(self):
        try:
            self.loop.stop()
            tasks = asyncio.gather(*asyncio.Task.all_tasks(), loop=self.loop)
            tasks.cancel()
            self.loop.run_forever()
            tasks.exception()
        except Exception as e:
            print(e)