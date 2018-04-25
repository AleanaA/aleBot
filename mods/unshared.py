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

class Unshared(Cog):

    @commands.group(name='unshared',
                description="Manage servers the bot does not share with owner.")
    @checks.is_owner()
    async def unshared(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed()
            emb.title = "Unshared Servers " + emotes.Warn
            emb.colour = 0xffff00
            emb.description = "Please issue a valid subcommand!\nAvailable options are:"
            emb.add_field(name="Leave", value="Leaves all servers the bot does not share with owner.", inline=False)
            emb.add_field(name="List", value="Lists all servers the bot does not share with owner.", inline=False)
            await ctx.message.channel.send(embed=emb)

    @unshared.command(name='leave')
    async def leaveunshared(self, ctx):
        embed = discord.Embed()
        embed.title = "Bot left unshared servers"
        embed.color = 0x00ffff
        config = Config('config/config.ini')
        owneruser = await self.bot.get_user_info(config.owner)
        owner = config.owner
        servers = ""
        for server in self.bot.guilds:
            check = server.get_member(owner)
            botuser = server.get_member(self.bot.user.id)
            if check == None:
                servers += "**ID:** {0}\n**Owner:** {1}\n**Owner ID:** {2}\n**Members:** {3}\n**Join Date:** {4}".format(str(server.id), server.owner, server.owner.id, str(server.member_count),botuser.joined_at.strftime("%b %d, %Y; %I:%M %p"))
                embed.add_field(name="Server Name: {0}".format(server.name), value=servers)
                await server.leave()
                await owneruser.send(embed=embed)
                return await ctx.message.channel.send(emotes.Done)
            await ctx.message.channel.send(emotes.Error + " No unshared servers.")
                

    @unshared.command(name='list')
    async def listunshared(self, ctx):
        embed = discord.Embed()
        embed.title = "Unshared Server List"
        embed.color = 0x00ffff
        config = Config('config/config.ini')
        owneruser = await self.bot.get_user_info(config.owner)
        owner = config.owner
        servers = ""
        for server in self.bot.guilds:
            check = server.get_member(owner)
            botuser = server.get_member(self.bot.user.id)
            if check == None:
                servers += "**ID:** {0}\n**Owner:** {1}\n**Owner ID:** {2}\n**Members:** {3}\n**Join Date:** {4}".format(str(server.id), server.owner, server.owner.id, str(server.member_count),botuser.joined_at.strftime("%b %d, %Y; %I:%M %p"))
                embed.add_field(name="Server Name: {0}".format(server.name), value=servers)
                await owneruser.send(embed=embed)
                return await ctx.message.channel.send(emotes.Done)
            await ctx.message.channel.send(emotes.Error + " No unshared servers.")

def setup(bot):
    bot.add_cog(Unshared(bot))