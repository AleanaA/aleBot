import asyncio
import discord
import inspect
import aiohttp
import os
import re
import subprocess
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils.embed import Embeds

class BotDebug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='eval',
                description="Owner Only!",
                brief="Owner Only!",
                aliases=['debug', 'Eval', 'Debug'])
    @commands.is_owner()
    async def debug(self, ctx, *, code : str):
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        env = {
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'return': code
        }
        env.update(globals())
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), title="Python Eval", description=python.format(type(e).__name__ + ': ' + str(e))))
            return
        await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x0094ff), title="Python Eval", description=python.format(result)))
    
    @commands.command(name='sys')
    @commands.is_owner()
    async def sys(self, ctx, *, cmd : str):
        cmd = cmd.split(' ')
        print(cmd)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            await ctx.message.channel.send("```{}```".format(e))
            return
        try:
            out, err = process.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            out, err = process.communicate()
        print("\n{}".format(re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]').sub('', out.decode('utf8'))))
        print("\n{}".format(re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]').sub('', err.decode('utf8'))))
        if out.decode('utf8') != '':
            output = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]').sub('', out.decode('utf8'))
        else:
            output = None
        if err.decode('utf8') != '':
            error = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]').sub('', err.decode('utf8'))
        else:
            error = None

        if output and error:
            result = "{}\n{}".format(output, error)
        elif output:
            result = output
        elif error:
            result = error
        else:
            result = "Nothing to show"
        await ctx.message.channel.send("```{}```".format(result))

    @commands.command(name='exec',
                description="Owner Only!",
                brief="Owner Only!")
    @commands.is_owner()
    async def exec(self, ctx, *, code : str):
        code = code.strip('``` ')
        python = '```py\n{}\n```'
        result = None
        env = {
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'return': code
        }
        env.update(globals())
        try:
            result = exec(code, env)
        except Exception as e:
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), title="Python Exec", description=python.format(type(e).__name__ + ': ' + str(e))))
            return
        await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x0094ff), title="Python Exec", description=python.format(result)))

    @commands.command(name='usereval',
                description="Owner Only!",
                brief="Owner Only!")
    @commands.is_owner()
    async def userdebug(self, ctx, user:discord.Member, *, code : str):
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        env = {
            'self': self,
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'user': user,
            'return': code
        }
        env.update(globals())
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), title="Python Eval", description=python.format(type(e).__name__ + ': ' + str(e))))
            return
        await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x0094ff), title="Python Eval", description=python.format(result)))


def setup(bot):
    bot.add_cog(BotDebug(bot))