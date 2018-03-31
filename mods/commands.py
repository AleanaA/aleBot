import asyncio
import discord
import inspect
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils import checks
from utils.config import Config
from utils.cog import Cog


emb = discord.Embed()
color = emb.color

class Commands(Cog):
    @commands.command(name='eval',
                description="Owner Only!",
                brief="Owner Only!",
                aliases=['debug', 'Eval', 'Debug'])
    @checks.is_owner()
    async def debug(self, ctx, *, code : str):
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        auth = ctx.message.author
        authmen = auth.mention

        env = {
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())
        if code == '':
            emb.title = "An Error Occured"
            emb.description = emotes.rooBooli + " What do you want me to evaluate " + authmen + "?"
            emb.colour = color(0xff0000)
            await ctx.message.channel.send(embed=emb)
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), title="Python Eval", description=python.format(type(e).__name__ + ': ' + str(e))))
            return

        await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x0094ff), title="Python Eval", description=python.format(result)))

    @commands.command(name='ping',
                description="Ping!",
                brief="Ping!",
                aliases=['Ping', 'Ping!'])
    async def ping(self, ctx):
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooBot)

    @commands.command(name='say',
                description="Text Command",
                brief="Text Command",
                aliases=[])
    @checks.is_event()
    async def say(self, ctx, *content):
        msg = " ".join(content)
        auth = ctx.message.author
        authmen = auth.mention

        emb.title = emotes.rooHappy
        emb.description = msg
        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.rooBooli + " What do you want me to say " + authmen + "?"
            emb.colour = color(0xff0000)
            await ctx.message.channel.send(embed=emb)
        else:
            await ctx.message.delete()
            await ctx.message.channel.send(embed=emb)

    @commands.command(name='Announce',
                description="Allows select users to make an announcement!",
                brief="Creates an announcement!",
                aliases=['announce', 'ANNOUNCE'])
    @checks.is_event()
    async def announce(self, ctx, *content):
        self.config = Config('config/config.ini')
        msg = ' '.join(content)
        auth = ctx.message.author
        authmen = auth.mention
        ANNOUNCE = self.bot.get_channel(self.config.announce)
        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.rooBooli + " What do you want me to announce " + authmen + "?"
            emb.colour = color(0xff0000)
            await ctx.message.channel.send(embed=emb)
        else:
            await ANNOUNCE.send(emotes.rooAww + " " + authmen + " - @everyone " + msg)
            await ctx.message.delete()
            await ctx.message.channel.send(emotes.rooBot + " Announcement Created")

    @commands.command(name='log',
                description="Allows select users to make a log entry!",
                brief="Creates a log entry!",
                aliases=['LOG', 'Log'])
    @checks.is_appr()
    async def log(self, ctx, *content):
        self.config = Config('config/config.ini')
        msg = ' '.join(content)
        auth = ctx.message.author
        authmen = auth.mention
        LOG = self.bot.get_channel(self.config.log)

        emb.title = emotes.rooHappy + " " + auth.name + " logged a message!"
        emb.description = msg
        emb.colour = discord.Colour(0x0094ff)

        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.rooBooli + " What do you want me to add to the log " + authmen + "?"
            emb.colour = color(0xff0000)
            await ctx.message.channel.send(embed=emb)
        else:
            await LOG.send(embed=emb)
            await ctx.message.delete()
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff2c), description=emotes.rooBot + " Log Added"))

    @commands.command(name='die',
                description="Shuts down the bot",
                brief="Shuts down the bot",
                aliases=['sd', 'shutdown'])
    @checks.is_owner()
    async def die(self, ctx):
        print(str(ctx.message.author) + " triggered a shutdown!")
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.rooBooli + " Alright, I'll shut down... Good night " + ctx.message.author.mention, color=0x0035ff))
        await self.bot.logout()

def setup(bot):
    bot.add_cog(Commands(bot))