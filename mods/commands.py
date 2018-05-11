import asyncio
import discord
import inspect
import datetime
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

class Commands(Cog):
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

    @commands.command(name='profile',
                description="Show a users profile!",
                brief="Show a profile!",
                aliases=[])
    async def profile(self, ctx, *user: discord.Member):
        self.config = Config('config/config.ini')
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
            activity = "None"
        elif user.activity.type == 0:
            activity = "Playing **{}**".format(user.activity.name)
        elif user.activity.type == 1:
            activity = "Streaming **{}**".format(user.activity.name)
        elif user.activity.type == 2:
            activity = "Listening to **{0} - {1} | For more info, run `!spotify @user`**".format(user.activity.artist, user.activity.title)
        elif user.activity.type == 3: # Users shouldn't have this type yet, however it's here to catch it for Bots and SelfBot users.
            activity = "Watching **{}**".format(user.activity.name)

        title = ""
        if user.id == 168118999337402368:
            title += "[Developer]\n"
        if user.id == 393275164273410050:
            title += "[Tester]\n"
        if user.id == 218200635693072384:
            title += "[Tester]\n"
        if user.id == 205577405069262848:
            title += "[Tester]\n"
        if user.id == 272614137660702720:
            title += "[Tester]\n"
        if user.id == 162349100396707840:
            title += "[Close Friend]\n"
        if user.id == 168141723019640832:
            title += "[Close Friend]\n"
        if user.id == owner.id:
            title += "[Bot Owner]\n"
        roles = [role.name for role in user.roles]
        del roles[0]
        rolecount = len(roles)
        if title == "":
            title = "None"
        embed=discord.Embed(color=user.color)
        embed.set_author(name="User info for " + str(user),icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Titles", value=title, inline=False)
        embed.add_field(name="Nickname", value=user.display_name, inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%b %d, %Y; %I:%M %p"), inline=False)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%b %d, %Y; %I:%M %p"), inline=False)
        embed.add_field(name="Status", value=status, inline=False)
        embed.add_field(name="Activity", value=activity, inline=False)
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
        self.config = Config('config/config.ini')
        owner = await self.bot.get_user_info(self.config.owner)
        if not user:
            user = ctx.message.author
        else:
            user = user[0]
        if user.activity.name == "Spotify":
            embed=discord.Embed(color=ctx.message.author.activity.color)

            embed.set_author(name="Spotify info for " + str(user),icon_url=user.avatar_url)

            embed.set_thumbnail(url=user.activity.album_cover_url)

            embed.add_field(name="Artist", value=user.activity.artist)
            embed.add_field(name="Title", value=user.activity.title)
            embed.add_field(name="Album", value=user.activity.album)
            time = str(datetime.timedelta(seconds=round(float(user.activity.duration))))
            embed.add_field(name="Duration", value=time)
            embed.add_field(name="Track URL", value="https://open.spotify.com/track/{}".format(user.activity.track_id))

            embed.set_footer(text="Requested by {0}".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            embed.timestamp = ctx.message.created_at
            await ctx.message.channel.send(embed=embed)
        else:
            embed=discord.Embed(title="Error", description="User is not listening to spotify", color=user.color)
            await ctx.message.channel.send(embed=embed)
def setup(bot):
    bot.add_cog(Commands(bot))