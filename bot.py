import asyncio
import inspect
import discord
import logging
import time
import os
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils import checks
from utils.config import Config

if config.LogLevel == 'debug':
    logging.basicConfig(level=logging.DEBUG)
elif config.LogLevel == 'info':
    logging.basicConfig(level=logging.INFO)
elif config.LogLevel == 'warn':
    logging.basicConfig(level=logging.WARNING)
elif config.LogLevel == 'error':
    logging.basicConfig(level=logging.ERROR)
elif config.LogLevel == 'critical':
    logging.basicConfig(level=logging.CRITICAL)
else:
    print("A log level was not specified, so nothing will be logged to console!")

logging.basicConfig(filename='rooBot.log',level=logging.INFO)
logging.basicConfig(filename='rooBot.debug.log',level=logging.DEBUG)

class Object(object):
    pass

emb = discord.Embed()
emb.title = ("An Error Occured")
emb.colour = discord.Colour(0xff0000)
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

    def __del__(self):
        self.loop.set_exception_handler(lambda *args, **kwargs: None)
    async def on_command_error(self, ctx, e):
        emb.description = emotes.Error + " " + str(e)
        if isinstance(e, commands.MissingRequiredArgument):
            print(str(e) + " - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, commands.CommandInvokeError):
            print(str(e) + " - Command - " + ctx.message.content)
            if 'Forbidden' in str(e):
                await ctx.message.channel.send(embed=emb)
            elif 'NotFound' in str(e):
                await ctx.message.channel.send(embed=emb)
            elif 'NameError' in str(e):
                await ctx.message.channel.send(embed=emb)
            elif 'HTTPException' in str(e):
                await ctx.message.channel.send(embed=emb)
            elif 'SyntaxError' in str(e):
                await ctx.message.channel.send(embed=emb)
            elif 'TypeError' in str(e):
                await ctx.message.channel.send(embed=emb)
            elif 'AttributeError' in str(e):
                await ctx.message.channel.send(embed=emb)
        elif isinstance(e, commands.BadArgument):
            print(str(e) + " - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, checks.No_Owner):
            print("User " + str(ctx.message.author) + " lacked permission! - Command - " + ctx.message.content)
            emb.description = emotes.Warn + " Only Aleana can use this command " + ctx.message.author.mention + "!"
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, checks.No_Admin):
            emb.description = emotes.Warn + " Only Admins can use this command " + ctx.message.author.mention + "!"
            print("User " + str(ctx.message.author) + " lacked permission! - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, checks.No_Super):
            emb.description = emotes.Warn + " Only Supervisors can use this command " + ctx.message.author.mention + "!"
            print("User " + str(ctx.message.author) + " lacked permission! - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, checks.No_Mod):
            emb.description = emotes.Warn + " Only Moderators can use this command " + ctx.message.author.mention + "!"
            print("User " + str(ctx.message.author) + " lacked permission! - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, checks.No_Appr):
            emb.description = emotes.Warn + " Only Apprentices can use this command " + ctx.message.author.mention + "!"
            print("User " + str(ctx.message.author) + " lacked permission! - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)
        elif isinstance(e, checks.No_Event):
            emb.description = emotes.Warn + " Only Event Hosts can use this command " + ctx.message.author.mention + "!"
            print("User " + str(ctx.message.author) + " lacked permission! - Command - " + ctx.message.content)
            await ctx.message.channel.send(embed=emb)


    async def on_ready(self):
        await self.wait_until_ready()
        game = discord.Game(type=0, name=self.config.status + " | {0}help".format(self.config.prefix))
        await self.change_presence(activity=game)
        print("---------------------------------------")
        print("Logged in as " + self.user.name)
        print("Current servers:")
        for server in self.guilds:
            print(server.name)
        print("---------------------------------------")
        for cog in config.Modules:
                try:
                    self.load_extension(cog)
                except Exception as e:
                    msg = 'Failed to load mod {0}\n{1}: {2}'.format(cog, type(e).__name__, e)
                    print(msg)

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