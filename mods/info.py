import asyncio
import discord
import inspect
import aiohttp
import utils
import os
import math
import re
import datetime
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

class Info(Cog):
    @commands.command(name='stats')
    async def stats(self, ctx):
        time_then = time.monotonic()
        ping = math.floor(self.bot.latency * 1000)
        prefix = self.bot.config.prefix
        owner = await self.bot.get_user_info(self.bot.config.owner)
        info = discord.__version__
        servers = len(self.bot.guilds)
        messages_seen = str(self.bot.messages_seen)
        members = 0
        bots = 0
        channels = 0
        roles = 0
        online = 0
        dnd = 0
        offline = 0
        idle = 0
        onmobile = 0
        second = time.time() - self.bot.start_time
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        week, day = divmod(day, 7)
        memberlist = []
        for guild in self.bot.guilds:
            for member in guild.members:
                if member in memberlist:
                    break
                else:
                    memberlist.append(member)
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
                if member.is_on_mobile():
                    onmobile += 1
            for channel in guild.channels:
                channels += 1
            for role in guild.roles:
                roles += 1
        pid = os.getpid()
        py = psutil.Process(pid)

        embed=Embeds.create_embed(self, ctx, "Bot stats", None, None, 
        CPU=["CPU Usage", py.cpu_percent(), True],
        Memory=["Memory Usage (MB)", round(py.memory_info()[0]/1024/1024, 2), True],
        Owner=["Owner", owner, True],
        Ping=["Ping", str(ping) + ' ms', True],
        DPyVer=["Discord.py version", info, True],
        Prefix=["Bot prefix", prefix, True],
        Servers=["Servers", servers, True],
        Messages=["Messages seen", messages_seen, True],
        Users=["Users", members, True],
        Bots=["Bots", bots, True],
        Channels=["Channels", channels, True],
        Roles=["Roles", roles, True],
        Online=["Online", online, True],
        DND=["Do not disturb", dnd, True],
        Idle=["Idle", idle, True],
        Offline=["Offline", offline, True],
        Mobile=["On Mobile", onmobile, True],
        Commands=["Commands", len(self.bot.commands), True],
        Uptime=["Uptime", "**%d** weeks, **%d** days, **%d** hours, **%d** minutes, **%d** seconds" % (week, day, hour, minute, second), True],
        Source=["Source Code", "https://github.com/AleanaA/aleBot - Created by Aleana#2643", False],
        Support=["Support Server", "https://discord.gg/eJhG4Tq", False])
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        await ctx.message.channel.send(embed=embed)

    @commands.command(name='server',
            description="Show information on a server!",
            brief="Show a server!",
            aliases=[])
    async def server(self, ctx, *server):
        if not server:
            server = ctx.message.guild
        else:
            server = self.bot.get_guild(int(server[0]))
        
        if server == None:
            await ctx.message.channel.send(embed=discord.Embed(title="Unknown server", description="The bot probably isn't in that server!", color=0xff0000))
            return

        roles = [role.name for role in server.role_hierarchy]
        del roles[-1]
        rolecount = len(roles)
        channelcount = len(server.text_channels)+len(server.voice_channels)
        embed=discord.Embed(color=0x00aaff)
        embed.set_author(name="Server info for " + str(server.name),icon_url=server.icon_url)
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name="Owner", value=server.owner, inline=False)
        embed.add_field(name="ID", value=server.id, inline=False)
        embed.add_field(name="Server Created", value=server.created_at.strftime("%b %d, %Y; %I:%M %p"), inline=False)
        embed.add_field(name="Members", value=server.member_count, inline=False)
        if rolecount != 0:
            embed.add_field(name="Highest Role", value=roles[0], inline=False)
            embed.add_field(name="Roles", value=rolecount, inline=False)
        if len(server.categories) != 0:
            embed.add_field(name="Categories",value=len(server.categories), inline=False)
        if channelcount != 0:
            embed.add_field(name="Channels",value=channelcount, inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        embed.timestamp = ctx.message.created_at
        await ctx.message.channel.send(embed=embed)

    @commands.command(name='user',
                description="Show a users info!",
                brief="Show user info!",
                aliases=[])
    async def user(self, ctx, *user: discord.Member):
        self.config = Config('config/config.ini')
        if not user:
            user = ctx.message.author
        else:
            user = user[0]

        if user.is_on_mobile():
            mobile = "Yes"
        else:
            mobile = "No"

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
            activity = None
        elif user.activity.type == 0:
            activity = "Playing **{}**".format(user.activity.name)
        elif user.activity.type == 1:
            activity = "Streaming **{}**".format(user.activity.name)
        elif user.activity.type == 2:
            activity = "Listening to **{0}**\n*For more info, run `{1}spotify @user`*".format(user.activity.title, self.config.prefix)
        elif user.activity.type == 3: # Users shouldn't have this type yet, however it's here to catch it for Bots and SelfBot users.
            activity = "Watching **{}**".format(user.activity.name)

        roles = [role.name for role in user.roles]
        del roles[0]
        rolecount = len(roles)

        embed = Embeds.create_embed(self, ctx, None, user.color, None,
        nick=["Nickname", user.display_name, True],
        ID=["ID", user.id, True],
        join=["Joined Server", user.joined_at.strftime("%b %d, %Y; %I:%M %p"), True],
        created=["Account Created", user.created_at.strftime("%b %d, %Y; %I:%M %p"), True],
        status=["Status", status, True],
        mobile=["On mobile", mobile, True])

        embed.set_author(name="User info for " + str(user),icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)

        if activity != None:
            embed.add_field(name="Activity", value=activity, inline=False)
        if rolecount > 0:
            embed.add_field(name="Highest Role", value=user.top_role, inline=True)
            embed.add_field(name="Total Roles", value=rolecount, inline=True)
        if user.voice:
            embed.add_field(name="Voice Channel", value=user.voice.channel, inline=True)
            if user.voice.deaf == True and user.voice.mute == True:
                embed.add_field(name="Voice State", value="Server Muted and Deafened", inline=True)
            elif user.voice.deaf == True:
                embed.add_field(name="Voice State", value="Server Deafened", inline=True)
            elif user.voice.mute == True:
                embed.add_field(name="Voice State", value="Server Muted", inline=True)
            elif user.voice.self_deaf == True:
                embed.add_field(name="Voice State", value="Deafened", inline=True)
            elif user.voice.self_mute == True:
                embed.add_field(name="Voice State", value="Muted", inline=True)
            else:
                embed.add_field(name="Voice State", value="Open", inline=True)
        await ctx.message.channel.send(embed=embed)

    @commands.command(name='spotify',
                description="Show a users profile!",
                brief="Show a profile!",
                aliases=[])
    async def spotify(self, ctx, *user: discord.Member):
        if not user:
            user = ctx.message.author
        else:
            user = user[0]
        if user.activity:
            if user.activity.name == "Spotify":
                embed=Embeds.create_embed(self, ctx, None, user.color, None,
                artist=["Artists",user.activity.artist,True],
                songtitle=["Title",user.activity.title,True],
                album=["Album",user.activity.album,False],
                duration=["Duration",str(datetime.timedelta(seconds=round(float(str(user.activity.duration.total_seconds()))))),False],
                url=["Track URL","https://open.spotify.com/track/{}".format(user.activity.track_id),False])

                embed.set_author(name="Spotify info for " + str(user),icon_url=user.avatar_url)
                embed.set_image(url=user.activity.album_cover_url)

                await ctx.message.channel.send(embed=embed)
            else:
                embed=Embeds.create_embed(self, ctx, "Spotify Error", 0xff0000, "{} is not listening to spotify, tell them to listen to some music!".format(user.mention))
                await ctx.message.channel.send(embed=embed)
        else:
            embed=Embeds.create_embed(self, ctx, "Spotify Error", 0xff0000, "{} is not listening to spotify, tell them to listen to some music!".format(user.mention))
            await ctx.message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))