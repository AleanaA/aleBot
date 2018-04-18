import asyncio
import discord
import inspect
import aiohttp
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils import checks
from utils.config import Config
from utils.cog import Cog

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

    @commands.command(name='ping',
                description="Ping!",
                brief="Ping!",
                aliases=['Ping', 'Ping!'])
    async def ping(self, ctx):
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.Done)

    @commands.command(name='invite',
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

    @commands.command(name='avatar',
                description="Changes the bots avatar!",
                brief="Changes the bots avatar!",
                aliases=['Avatar'])
    @checks.is_owner()
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

    @commands.command(name='username',
                description="Changes the bots username!",
                brief="Changes the bots username!",
                aliases=['Username'])
    @checks.is_owner()
    async def username(self, ctx, msg):
        emb = discord.Embed()
        emb.title = "Username Changed!"
        emb.color = 0x00ff00
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        emb.description = "Username successfully changed to " + msg
        await self.bot.user.edit(username=msg)
        await ctx.message.channel.send(embed=emb)

    @commands.command(name='say',
                description="Text Command",
                brief="Text Command",
                aliases=[])
    @checks.is_event()
    async def say(self, ctx, *content):
        emb = discord.Embed()
        msg = " ".join(content)
        auth = ctx.message.author
        authmen = auth.mention
        emb.title = ctx.message.author.name + " said..."
        emb.description = msg

        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.Warn + " What do you want me to say " + authmen + "?"
            emb.color = 0xff0000
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
        emb = discord.Embed()
        self.config = Config('config/config.ini')
        msg = ' '.join(content)
        auth = ctx.message.author
        authmen = auth.mention
        ANNOUNCE = self.bot.get_channel(self.config.announce)

        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.Warn + " What do you want me to announce " + authmen + "?"
            emb.color = 0xff0000
            await ctx.message.channel.send(embed=emb)
        else:
            await ANNOUNCE.send(authmen + " - @everyone " + msg)
            await ctx.message.delete()
            await ctx.message.channel.send(emotes.Done + " Announcement Created")

    @commands.command(name='log',
                description="Allows select users to make a log entry!",
                brief="Creates a log entry!",
                aliases=['LOG', 'Log'])
    @checks.is_appr()
    async def log(self, ctx, *content):
        emb = discord.Embed()
        self.config = Config('config/config.ini')
        msg = ' '.join(content)
        auth = ctx.message.author
        authmen = auth.mention
        LOG = self.bot.get_channel(self.config.log)
        emb.title = emotes.Done + " " + auth.name + " logged a message!"
        emb.description = msg
        emb.colour = discord.Colour(0x0094ff)


        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.Warn + " What do you want me to add to the log " + authmen + "?"
            emb.color = 0xff0000
            await ctx.message.channel.send(embed=emb)
        else:
            await LOG.send(embed=emb)
            await ctx.message.delete()
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff2c), description=emotes.Done + " Log Added"))

    @commands.command(name='die',
                description="Shuts down the bot",
                brief="Shuts down the bot",
                aliases=['sd', 'shutdown'])
    @checks.is_owner()
    async def die(self, ctx):
        print(str(ctx.message.author) + " triggered a shutdown!")
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.Done + " " + self.bot.user.name + " is now shutting down... " + ctx.message.author.mention, color=0x0035ff))
        await self.bot.logout()

    @commands.command(name='profile',
                description="Show a users profile!",
                brief="Show a profile!",
                aliases=[])
    async def profile(self, ctx, *user: discord.Member):
        if not user:
            user = ctx.message.author
        else:
            user = user[0]
        if str(user.status) == "online":
            status = "Online"
        elif str(user.status) == "offline":
            status = "Offline"
        elif str(user.status) == "idle":
            status = "Idle"
        elif str(user.status) == "dnd":
            status = "Do Not Disturb"
        elif str(user.status) == "do_not_disturb": # This is a catch, as a 'Just in case'
            status = "Do Not Disturb"
        if user.activity == None:
            activity = "None"
        elif user.activity.type == 0:
            activity = "**Playing** {}".format(user.activity)
        elif user.activity.type == 1:
            activity = "**Streaming** {}".format(user.activity)
        elif user.activity.type == 2:
            activity = "**Listening to** {}".format(user.activity)
        elif user.activity.type == 3: # Users shouldn't have this type yet, however it's here to catch it for Bots and SelfBot users.
            activity = "**Watching** {}".format(user.activity)

        roles = [role.name for role in user.roles]
        del roles[0]
        rolecount = len(roles)
        embed=discord.Embed(color=user.color, timestamp=ctx.message.created_at.strftime("%b %d, %Y; %I:%M %p"))
        embed.set_author(name="User info for " + str(user),icon_url=user.avatar_url)
        embed.set_image(url=user.avatar_url)
        embed.add_field(name="Nickname", value=user.display_name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%b %d, %Y; %I:%M %p"), inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%b %d, %Y; %I:%M %p"), inline=True)
        embed.add_field(name="Status", value=status, inline=True)
        embed.add_field(name="Activity", value=activity, inline=True)
        embed.add_field(name="Highest Role", value=user.top_role, inline=True)
        embed.add_field(name="Roles", value=rolecount, inline=True))
        if not user.voice:
            embed.add_field(name="Voice Channel", value="User not in a channel.", inline=True)
        else:
            embed.add_field(name="Voice Channel", value=user.voice.channel, inline=True)
        await ctx.message.channel.send(embed=embed)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text="Requested by {}".format(ctx.message.author))
def setup(bot):
    bot.add_cog(Commands(bot))