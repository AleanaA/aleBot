import asyncio
import discord
import inspect
import aiohttp
import datetime
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import emotes
from config import config
from utils import checks
from utils.config import Config
from utils.cog import Cog
from mpd import MPDClient

player = MPDClient()

class MPD(Cog):
    def __init__(self, *args, **kwargs):
        self.ip = "localhost"
        self.port = "6600"
    @commands.group(name='mpd',
                 description="Command for MPD managing.",
                 brief="Command for MPD managing.")
    async def mpd(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed()
            emb.title = ":musical_note: MPD Client " + emotes.Warn
            emb.colour = 0xffff00
            emb.description = "Please issue a valid subcommand!\nAvailable options are:"
            emb.add_field(name="Server", value="Sets the server to connect to. Defaults to localhost", inline=False)
            emb.add_field(name="Play", value="Starts playing what's in the queue.", inline=False)
            emb.add_field(name="Pause", value="Pauses the currently playing song.", inline=False)
            emb.add_field(name="Skip", value="Skips the currently playing song.", inline=False)
            emb.add_field(name="Back", value="Plays the previous song in the queue.", inline=False)
            emb.add_field(name="Clear", value="Stops and clears the current queue.", inline=False)
            emb.add_field(name="Shuffle", value="Shuffles the current queue.", inline=False)
            emb.add_field(name="ShowNext", value="Shows the next song in the current queue.", inline=False)
            emb.add_field(name="NP", value="Shows the song currently playing.", inline=False)
            emb.add_field(name="Playlists", value="List all available playlists.", inline=False)
            emb.add_field(name="Playlist", value="Add a playlist to the current queue.", inline=False)
            emb.add_field(name="Vol", value="Changes the volume of the mpd server.", inline=False)
            await ctx.message.channel.send(embed=emb)
    
    @mpd.command(name='server',
                description="Sets an alternative server to connect to.")
    @checks.is_owner()
    async def server(self, ctx, ip, *port):
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        self.ip = ip
        if not port:
            self.port = "6600"
        emb.description = "Set the MPD Server to `{0}:{1}`.".format(self.ip, self.port)
        await ctx.message.channel.send(embed=emb)

    @mpd.command(name='back',
                description="Plays the previous song in the queue.")
    @checks.is_owner()
    async def back(self, ctx):
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Playing previous song in the current queue."
        player.connect(self.ip, int(self.port))
        player.previous()
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

    @mpd.command(name='play',
                description="Starts playing what's in the queue.")
    @checks.is_owner()
    async def play(self, ctx):
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Started the current queue."
        player.connect(self.ip, int(self.port))
        player.play()
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

    @mpd.command(name='skip',
                description="Skips the currently playing song.")
    @checks.is_owner()
    async def skip(self, ctx):
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Playing the next song in the current queue"
        player.connect(self.ip, int(self.port))
        player.next()
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

    @mpd.command(name='pause',
                description="Pauses the currently playing song.")
    @checks.is_owner()
    async def pause(self, ctx):
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Paused the currently playing song."
        player.connect(self.ip, int(self.port))
        player.pause()
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

    @mpd.command(name='clear',
                description="Stops and clears the current queue.")
    @checks.is_owner()
    async def clear(self, ctx):
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Cleared the current queue."
        player.connect(self.ip, int(self.port))
        player.clear()
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

    @mpd.command(name='shuffle',
                description="Shuffles the current queue.")
    @checks.is_owner()
    async def shuffle(self, ctx):
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Shuffled the current queue."
        player.connect(self.ip, int(self.port))
        player.shuffle()
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

    @mpd.command(name='np',
                description="Shows the song currently playing.")
    async def np(self, ctx):
        player.connect(self.ip, int(self.port))
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        try:
            nextsong = player.status().get('nextsong')
            time = str(datetime.timedelta(seconds=round(float(player.status().get('elapsed')))))
            length = str(datetime.timedelta(seconds=int(player.currentsong()['time'])))
            emb.colour = 0x00aaff
            emb.description = "Showing the currently playing song."
            emb.add_field(name="Song Name", value=player.currentsong()['title'], inline=False)
            emb.add_field(name="Song Artist", value=player.currentsong()['artist'], inline=False)
            emb.add_field(name="Time", value="`{0} / {1}`".format(time, length), inline=False)
            emb.add_field(name="Next Song", value= "{0} | {1}".format(player.playlistinfo()[int(nextsong)]['title'], player.playlistinfo()[int(nextsong)]['artist']))
            await ctx.message.channel.send(embed=emb)
        except KeyError:
            emb.colour = 0xffff00
            emb.description = "Nothing seems to be playing, or an error occured."
            await ctx.message.channel.send("Nothing seems to be playing, or an error occured.")
        player.close()
        player.disconnect()

    @mpd.command(name='playlist',
                description="Add a playlist to the current queue.")
    @checks.is_owner()
    async def playlist(self, ctx, *playlist):
        player.connect(self.ip, int(self.port))
        playlist = ' '.join(playlist)
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Loaded playlist '{0}'".format(playlist)
        player.load(playlist)
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

    @mpd.command(name='playlists',
                description="List all available playlists.")
    @checks.is_owner()
    async def playlists(self, ctx):
        player.connect(self.ip, int(self.port))
        playlists = player.listplaylists()
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Listing all available playlists."
        reply = ""
        for playlist in playlists:
            playlistlist = "{0}\n\n".format(playlist['playlist'])
            reply += playlistlist
        emb.add_field(name="Playlists", value=reply, inline=False)
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

    @mpd.command(name='vol',
                description="Changes the volume of the server.")
    @checks.is_owner()
    async def vol(self, ctx, volume):
        emb = discord.Embed()
        emb.title = ":musical_note: MPD Client"
        emb.colour = 0x00aaff
        emb.description = "Set the volume to {0}/100".format(volume)
        player.connect(self.ip, int(self.port))
        try:
            player.setvol(volume)
        except Exception as e:
            emb.description = "Error setting volume.\n```{}```".format(e)
        await ctx.message.channel.send(embed=emb)
        player.close()
        player.disconnect()

def setup(bot):
    bot.add_cog(MPD(bot))