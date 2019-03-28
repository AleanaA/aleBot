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
import random
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import config
from utils.embed import Embeds
from utils.config import Config

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='ping',
                description="Ping!",
                brief="Ping!",
                aliases=['Ping', 'Ping!'])
    async def ping(self, ctx):
        await ctx.message.channel.send(ctx.message.author.mention + " " + str(math.ceil(self.bot.latency * 1000)) + " ms")

    @commands.command(name='createdat')
    async def createdat(self, ctx, id:int):
        created_at=discord.utils.snowflake_time(id).strftime("%b %d, %Y; %I:%M %p")
        emb=Embeds.create_embed(self, ctx, "This snowflake was created at", color=0x00fbff, message=created_at)
        await ctx.send(embed=emb)

    @commands.command(name='stats')
    async def stats(self, ctx):
        ping = math.floor(self.bot.latency * 1000)
        prefix = self.bot.config.prefix
        owner = self.bot.appinfo.owner
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
        memberlist = set(self.bot.get_all_members())
        for member in memberlist:
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
        for guild in self.bot.guilds:
            for channel in guild.channels:
                channels += 1
            for role in guild.roles:
                roles += 1
        pid = os.getpid()
        py = psutil.Process(pid)

        embed=Embeds.create_embed(self, ctx, "Bot stats", None, None)

        embed.add_field(name="CPU Usage", value=py.cpu_percent(), inline=True)
        embed.add_field(name="Memory Usage (MB)", value=round(py.memory_info()[0]/1024/1024, 2), inline=True)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Ping", value=str(ping) + ' ms', inline=True)
        embed.add_field(name="Discord.py version", value=info, inline=True)
        embed.add_field(name="Bot prefix", value=prefix, inline=True)
        embed.add_field(name="Servers", value=servers, inline=True)
        embed.add_field(name="Messages seen", value=messages_seen, inline=True)
        embed.add_field(name="Users", value=len(memberlist), inline=True)
        embed.add_field(name="Bots", value=bots, inline=True)
        embed.add_field(name="Channels", value=channels, inline=True)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.add_field(name="Online", value=online, inline=True)
        embed.add_field(name="Do not disturb", value=dnd, inline=True)
        embed.add_field(name="Idle", value=idle, inline=True)
        embed.add_field(name="Offline", value=offline, inline=True)
        embed.add_field(name="On Mobile", value=onmobile, inline=True)
        embed.add_field(name="Commands", value=len(self.bot.commands), inline=True)
        embed.add_field(name="Uptime", value="**%d** weeks, **%d** days, **%d** hours, **%d** minutes, **%d** seconds" % (week, day, hour, minute, second), inline=True)
        embed.add_field(name="Source Code", value="https://github.com/AleanaA/aleBot - Created by Aleana#2643", inline=False)
        embed.add_field(name="Support Server", value="https://discord.gg/eJhG4Tq", inline=False)

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

        roles = [role.name for role in server.roles]
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
        if not user:
            user = ctx.message.author
        else:
            user = user[0]
        client = ""
        if str(user.mobile_status) != "offline":
            client += "Mobile\n"
        if str(user.web_status) != "offline":
            client += "Web\n"
        if str(user.desktop_status) != "offline":
            client += "Desktop\n"
        
        # List of available statuses. Could change in the future
        statuses = {
            "offline": "Offline",
            "idle": "Idle",
            "dnd": "Do Not Disturb",
            "do_not_disturb": "Do Not Disturb",
            "online": "Online"
        }

        if str(user.status) in statuses:
            status = statuses[str(user.status)]

        # List of available activities. Could change in the future.
        activities = {
            0: "Playing",
            1: "Streaming",
            2: "Listening to",
            3: "Watching"
        }

        if user.activity == None:
            activitystr = None
        elif int(user.activity.type) in activities:
            activitystr = "{} **{}**".format(activities[int(user.activity.type)], user.activity.name)
            if user.activity.type == 2 and user.activity.name == "Spotify":
                activitystr += "\n*For more info, run {}spotify {}*".format(self.bot.config.prefix, user.mention)
        else:
            print("Undefined activity type {}".format(user.activity.type))
        
        roles = [role.name for role in user.roles]
        del roles[0]
        rolecount = len(roles)

        if str(user.color) == "#000000":
            setcolor = discord.Colour(int("%06x" % random.randint(0, 0xFFFFFF), 16))
        else:
            setcolor = user.color

        embed = Embeds.create_embed(self, ctx, None, setcolor, None,
                                    nick=["Nickname", user.display_name, True],
                                    ID=["ID", user.id, True],
                                    join=["Joined Server", user.joined_at.strftime("%b %d, %Y; %I:%M %p"), True],
                                    created=["Account Created", user.created_at.strftime("%b %d, %Y; %I:%M %p"), True],
                                    status=["Status", status, True],
                                    client=["Clients", client, True])

        embed.set_author(name="User info for {} [{}]".format(str(user), user.guild.name),icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        
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
        if activitystr != None:
            embed.add_field(name="Activity", value=activitystr, inline=False)
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
                artists = ", ".join(user.activity.artists)
                embed=Embeds.create_embed(self, ctx, None, user.activity.color, None,
                songtitle=["Title",user.activity.title,False],
                artist=["Artists",artists,False],
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

    @commands.command(name='invite',
                description="Gets the bots invite url!",
                brief="Gets the bots invite url!",
                aliases=['Invite'])
    async def invite(self, ctx):
        emb = discord.Embed()
        emb.title = "Invite URL"
        emb.description = "<https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=8>".format(str(self.bot.user.id))
        emb.colour = 0x00ffff
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.message.channel.send(embed=emb)

def setup(bot):
    bot.add_cog(Info(bot))