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
from mpd import MPDClient

player = MPDClient()

class MPD(Cog):
    @commands.group(name='mpd',
                 description="Command for MPD managing.")
    async def mpd(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed()
            emb.title = "MPD Client " + emotes.Warn
            emb.colour = 0xffff00
            emb.description = "Please issue a valid subcommand!\nAvailable options are:"
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
            await ctx.message.channel.send(embed=emb)
    
    @mpd.command(name='back',
                description="Plays the previous song in the queue.")
    @checks.is_owner()
    async def back(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        player.previous()
        await ctx.message.channel.send("Playing previous song in the current queue.")
        player.close()
        player.disconnect()

    @mpd.command(name='play',
                description="Starts playing what's in the queue.")
    @checks.is_owner()
    async def play(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        player.play()
        await ctx.message.channel.send("Started the current queue.")
        player.close()
        player.disconnect()

    @mpd.command(name='skip',
                description="Skips the currently playing song.")
    @checks.is_owner()
    async def skip(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        player.next()
        await ctx.message.channel.send("Playing the next song in the current queue")
        player.close()
        player.disconnect()

    @mpd.command(name='pause',
                description="Pauses the currently playing song.")
    @checks.is_owner()
    async def pause(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        player.pause()
        await ctx.message.channel.send("Paused the currently playing song.")
        player.close()
        player.disconnect()

    @mpd.command(name='clear',
                description="Stops and clears the current queue.")
    @checks.is_owner()
    async def clear(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        player.clear()
        await ctx.message.channel.send("Cleared the current queue.")
        player.close()
        player.disconnect()

    @mpd.command(name='shuffle',
                description="Shuffles the current queue.")
    @checks.is_owner()
    async def shuffle(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        player.shuffle()
        await ctx.message.channel.send("Shuffled the current queue.")
        player.close()
        player.disconnect()

    @mpd.command(name='shownext',
                description="Shows the next song in the current queue.")
    async def shownext(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        print(player.status())
        nextsong = player.status().get('nextsong')
        await ctx.message.channel.send("Next up: {0} by {1}".format(player.playlistinfo()[int(nextsong)]['title'], player.playlistinfo()[int(nextsong)]['artist']))
        player.close()
        player.disconnect()

    @mpd.command(name='np',
                description="Shows the song currently playing.")
    async def np(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        try:
            await ctx.message.channel.send("Currently playing {0} by {1}.".format(player.currentsong()['title'], player.currentsong()['artist']))
        except KeyError:
            await ctx.message.channel.send("Nothing seems to be playing, or an error occured.")
        player.close()
        player.disconnect()

    @mpd.command(name='playlist',
                description="Add a playlist to the current queue.")
    @checks.is_owner()
    async def playlist(self, ctx, *playlist):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        playlist = ' '.join(playlist)
        player.load(playlist)
        await ctx.message.channel.send("Loaded playlist '{0}'".format(playlist))
        player.close()
        player.disconnect()

    @mpd.command(name='playlists',
                description="List all available playlists.")
    @checks.is_owner()
    async def playlists(self, ctx):
        ip = "localhost"
        port = "6600"
        player.connect(ip, int(port))
        playlists = player.listplaylists()
        reply = ""
        for playlist in playlists:
            playlistlist = "Playlist: {0}\n".format(playlist['playlist'])
            reply += playlistlist
        await ctx.message.channel.send("__Playlists__\n\n{0}".format(reply))
        player.close()
        player.disconnect()

def setup(bot):
    bot.add_cog(MPD(bot))