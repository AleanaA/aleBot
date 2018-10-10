import asyncio
import discord
import inspect
import datetime
import aiohttp
import utils
import json
import requests
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils import checks
from utils.config import Config
from utils.cog import Cog

class Commands(Cog):
    def __init__(self, *args, **kwargs):
        self.config = Config('config/config.ini')
        
    @commands.command(name='ping',
                description="Ping!",
                brief="Ping!",
                aliases=['Ping', 'Ping!'])
    async def ping(self, ctx):
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.Done)

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
        msg = ' '.join(content)
        auth = ctx.message.author
        authmen = auth.mention
        ANNOUNCE = discord.utils.get(self.bot.get_all_channels(), guild__name=ctx.message.guild.name, name='announcements')

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

    @commands.command(name='user',
                description="Show a users info!",
                brief="Show user info!",
                aliases=[])
    async def user(self, ctx, *user: discord.Member):
        owner = await self.bot.get_user_info(self.config.owner)
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
            activity = None
        elif user.activity.type == 0:
            activity = "Playing **{}**".format(user.activity.name)
        elif user.activity.type == 1:
            activity = "Streaming **{}**".format(user.activity.name)
        elif user.activity.type == 2:
            activity = "Listening to **{0}**\n*For more info, run `{1}spotify @user`*".format(user.activity.title, self.config.prefix)
        elif user.activity.type == 3: # Users shouldn't have this type yet, however it's here to catch it for Bots and SelfBot users.
            activity = "Watching **{}**".format(user.activity.name)

        title = ""
        if user.id == self.bot.user.id:
            title += "[Me!]\n"
        if user.id == 168118999337402368:
            title += "[Developer]\n"
        if user.id == owner.id:
            title += "[Bot Owner]\n"
        if user.bot == True:
            title += "[Bot]\n"
        if user.id == ctx.message.guild.owner_id:
            title += "[Server Owner]\n"
        
        roles = [role.name for role in user.roles]
        del roles[0]
        rolecount = len(roles)
        embed=discord.Embed(color=user.color)
        embed.set_author(name="User info for " + str(user),icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        if title != "":
            embed.add_field(name="Titles", value=title, inline=False)
        embed.add_field(name="Nickname", value=user.display_name, inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%b %d, %Y; %I:%M %p"), inline=False)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%b %d, %Y; %I:%M %p"), inline=False)
        embed.add_field(name="Status", value=status, inline=False)
        if activity != None:
            embed.add_field(name="Activity", value=activity, inline=False)
        if rolecount > 0:
            embed.add_field(name="Highest Role", value=user.top_role, inline=False)
            embed.add_field(name="Roles", value=rolecount, inline=False)
        if user.voice:
            embed.add_field(name="Voice Channel", value=user.voice.channel, inline=False)
            if user.voice.deaf == True and user.voice.mute == True:
                embed.add_field(name="Voice State", value="Server Muted and Deafened", inline=False)
            elif user.voice.deaf == True:
                embed.add_field(name="Voice State", value="Server Deafened", inline=False)
            elif user.voice.mute == True:
                embed.add_field(name="Voice State", value="Server Muted", inline=False)
            elif user.voice.self_deaf == True:
                embed.add_field(name="Voice State", value="Deafened", inline=False)
            elif user.voice.self_mute == True:
                embed.add_field(name="Voice State", value="Muted", inline=False)
            else:
                embed.add_field(name="Voice State", value="Open", inline=False)
        embed.set_footer(text="Requested by {0}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        embed.timestamp = ctx.message.created_at
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
        if user.activity.name == "Spotify":
            embed=discord.Embed(color=user.activity.color)
            embed.set_author(name="Spotify info for " + str(user),icon_url=user.avatar_url)
            embed.set_image(url=user.activity.album_cover_url)
            embed.add_field(name="Artists", value=user.activity.artist)
            embed.add_field(name="Title", value=user.activity.title)
            embed.add_field(name="Album", value=user.activity.album, inline=False)
            embed.add_field(name="Duration", value=str(datetime.timedelta(seconds=round(float(str(user.activity.duration.total_seconds()))))), inline=False)
            embed.add_field(name="Track URL", value="https://open.spotify.com/track/{}".format(user.activity.track_id), inline=False)
            embed.set_footer(text="Requested by {0}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed.timestamp = ctx.message.created_at
            await ctx.message.channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Spotify Error", description="{} is not listening to spotify, tell them to listen to some music!".format(user.mention), color=0xff0000)
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

    @commands.command(name='fact',
                description="Get a fact!",
                brief="Get a fact!",
                aliases=['Fact', 'Fact!'])
    async def fact(self, ctx):
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.Done)
    
    @commands.command(name='cat',
                description="Kitty!")
    async def cat(self, ctx):
        isVideo = True
        while isVideo:
            r = requests.get('http://aws.random.cat/meow')
            parsed_json = r.json()
            if parsed_json['file'].endswith('.mp4'):
                pass
            else:
                isVideo = False
        embed = discord.Embed()
        embed.set_image(url=parsed_json['file'])
        await ctx.message.channel.send(embed=embed)

    @commands.command(name='dog',
                description="Puppo!")
    async def dog(self, ctx):
        isVideo = True
        while isVideo:
            r = requests.get('https://random.dog/woof.json')
            parsed_json = r.json()
            if parsed_json['url'].endswith('.mp4'):
                pass
            else:
                isVideo = False
        embed = discord.Embed()
        embed.set_image(url=parsed_json['url'])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))