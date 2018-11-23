import asyncio
import discord
import inspect
import aiohttp
import utils
import os
import math
import re
import time
import subprocess
import psutil
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils.embed import Embeds
from utils import checks
from utils.config import Config
from utils.cog import Cog

class BotOptions(Cog):
    @commands.group(name='bot',
                    description="Manage settings for the bot.",
                    brief="Manage settings for the bot.")
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
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), title=emotes.Terminal+" Python Eval", description=python.format(type(e).__name__ + ': ' + str(e))))
            return

        await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x0094ff), title=emotes.Terminal+" Python Eval", description=python.format(result)))


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

    @manbot.command(name='update',
                description="Update the bot through git.",
                brief="Update the bot through git.")
    async def update(self, ctx):
        process = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        emb = discord.Embed()
        emb.title = "Bot Updater"
        emb.color = 0x00aaff
        msg = ''
        for cog in config.Modules:
                try:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                    msg += '+Successfully reloaded mod {0}\n\n'.format(cog)
                except Exception as e:
                    msg += '-Error reloading mod {0}\n-{1}: {2}\n\n'.format(cog, type(e).__name__, e)
        emb.description = "Bot has updated to the latest commit in repository.\nAll mods in `config.py` have attempted to be reloaded.\nIt is advised that you restart if anything outside the mods folder was updated."
        emb.add_field(name="Cog Loader", value="```diff\n{}```".format(msg), inline=False)
        if len(out.decode('utf8')) <= 500:
            emb.add_field(name=emotes.Terminal+" Update Output", value="```http\n{}```".format(out.decode('utf8')), inline=False)
        else:
            emb.add_field(name=emotes.Terminal+" Update Output", value="```md\n#Output longer than 500 chars, see text file for output.```", inline=False)
        print("Bot has updated to the latest commit in repository.\nAll mods in `config.py` have attempted to be reloaded.\nIt is advised that you restart if anything outside the mods folder was updated.")
        print(msg)
        print(out.decode('utf8'))
        f = open("output.txt","w+")
        f.write(out.decode('utf8'))
        f.close()
        await ctx.message.channel.send(embed=emb)
        if len(out.decode('utf8')) >=500:
            await ctx.message.channel.send(file=discord.File('output.txt'))
        os.remove('output.txt')

    async def on_message(self, msg:discord.Message):
        self.bot.messages_seen += 1

    @manbot.command(name='stats')
    async def stats(self, ctx):
        time_then = time.monotonic()
    
        ping = math.floor(self.bot.latency * 1000)
        prefix = self.bot.config.prefix
        owner = await self.bot.get_user_info(self.bot.config.owner)
        info = discord.__version__
        servers = len(self.bot.guilds)
#        messages = len(list(self.bot.messages))
        messages_seen = str(self.bot.messages_seen)
        members = 0
        bots = 0
        channels = 0
        roles = 0
        online = 0
        dnd = 0
        offline = 0
        idle = 0
        second = time.time() - self.bot.start_time
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        week, day = divmod(day, 7)
    
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.status == discord.Status.dnd or member.status == discord.Status.do_not_disturb:
                    dnd += 1
                elif member.status == discord.Status.online:
                    online += 1
                elif member.status ==  discord.Status.offline:
                    offline += 1
                elif member.status == discord.Status.idle:
                    idle += 1
                if not member.bot:
                    members += 1
                else:
                    bots +=  1
            for channel in guild.channels:
                channels += 1
            for role in guild.roles:
                roles += 1



        embed=discord.Embed()
        embed.title = "Bot stats"
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        pid = os.getpid()
        py = psutil.Process(pid)
        embed.add_field(name="CPU Usage", value=py.cpu_percent())
        embed.add_field(name="Memory Usage (MB)", value=round(py.memory_info()[0]/1024/1024, 2))
        embed.set_footer(text='{}'.format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url if ctx.message.author.avatar else ctx.message.author.default_avatar_url)
        embed.add_field(name='Owner', value=owner, inline=True)
        embed.add_field(name='Ping', value=str(ping)+' ms', inline=True)
#        embed.add_field(name='Bot version', value='{}'.format(BOTVERSION), inline=True)
        embed.add_field(name='Discord.py version', value=info, inline=True)
        embed.add_field(name='Bot prefix', value=prefix, inline=True)
        embed.add_field(name='Servers', value=servers, inline=True)
        embed.add_field(name='Messages seen', value=messages_seen, inline=True)
        embed.add_field(name='Users', value=members, inline=True)
        embed.add_field(name='Bots', value=bots, inline=True)
        embed.add_field(name='Channels', value=channels, inline=True)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.add_field(name="Online", value=online, inline=True)
        embed.add_field(name="Do not disturb", value=dnd, inline=True)
        embed.add_field(name="Idle", value=idle, inline=True)
        embed.add_field(name="Offline", value=offline, inline=True)
        embed.add_field(name="Uptime",value="**%d** weeks, **%d** days, **%d** hours, **%d** minutes, **%d** seconds" % (week, day, hour, minute, second), inline=True)

        await ctx.message.channel.send(embed=embed)
def setup(bot):
    bot.add_cog(BotOptions(bot))
