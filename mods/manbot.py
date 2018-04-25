import asyncio
import discord
import inspect
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

class BotOptions(Cog):
    
    @commands.group(name='bot',
                    description="Manages settings for the bot.")
    @checks.is_owner()
    async def manbot(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed()
            emb.title = "Bot Manager " + emotes.Warn
            emb.colour = 0xffff00
            emb.description = "Please issue a valid subcommand!\nAvailable options are:"
            emb.add_field(name="Eval", value="Runs debug code, do not use if you don't know what you're doing!", inline=False)
            emb.add_field(name="Invite", value="Gets an invite url for the bot!", inline=False)
            emb.add_field(name="Avatar", value="Changes the bots avatar!", inline=False)
            emb.add_field(name="Username", value="Changes the bots username!", inline=False)
            emb.add_field(name="Die", value="Shuts down the bot, or restarts it while under pm2.", inline=False)
            await ctx.message.channel.send(embed=emb)

    @manbot.command(name='eval',
                description="Owner Only!",
                brief="Owner Only!",
                aliases=['debug', 'Eval', 'Debug'])
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
            'author': ctx.message.author
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


    @manbot.command(name='invite',
                description="Gets the bots invite url!",
                brief="Gets the bots invite url!",
                aliases=['Invite'])
    async def invite(self, ctx):
        emb = discord.Embed()
        emb.title = "Invite URL"
        emb.description = "<https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=8>".format(str(self.bot.user.id))
        emb.color = 0x00ffff
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.message.channel.send(embed=emb)

    @manbot.command(name='avatar',
                    description="Changes the bots avatar!",
                    brief="Changes the bots avatar!",
                    aliases=['Avatar'])
    async def avatar(self, ctx, msg=None):
        self.aiosession = aiohttp.ClientSession(loop=self.bot.loop)
        emb = discord.Embed()
        emb.title = "Avatar Changed!"
        emb.color = 0x00ff00
        picture = msg.strip('<>')
        emb.set_thumbnail(url=msg)
        emb.description = "Avatar successfully changed to " + msg

        async with self.aiosession.get(picture) as res:
            await self.bot.user.edit(avatar=await res.read())
            await ctx.message.channel.send(embed=emb)

    @manbot.command(name='username',
                    description="Changes the bots username!",
                    brief="Changes the bots username!",
                    aliases=['Username'])
    async def username(self, ctx, msg):
        emb = discord.Embed()
        emb.title = "Username Changed!"
        emb.color = 0x00ff00
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        emb.description = "Username successfully changed to " + msg
        await self.bot.user.edit(username=msg)
        await ctx.message.channel.send(embed=emb)

    @manbot.command(name='die',
                    description="Shuts down the bot, or restarts it while under pm2.",
                    brief="Shuts down the bot",
                    aliases=['sd', 'shutdown'])
    async def die(self, ctx):
        print(str(ctx.message.author) + " triggered a shutdown!")
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.Done + " " + self.bot.user.name + " is now shutting down... " + ctx.message.author.mention, color=0x0035ff))
        await self.bot.logout()

def setup(bot):
    bot.add_cog(BotOptions(bot))