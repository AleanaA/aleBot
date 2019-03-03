import asyncio
import discord
import inspect
import aiohttp
import utils
import re
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from config import config
from utils.config import Config
from utils.embed import Embeds

class Unshared(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group(name='unshared',
                description="Manage servers the bot does not share with owner.",
                brief="Manage servers the bot does not share with owner.")
    @commands.is_owner()
    async def unshared(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = Embeds.create_embed(self, ctx,
            "Unshared Servers",
            0xffff00,
            "Please issue a valid subcommand!\nAvailable options are:",
            Com1 = ["leave", "Leaves all servers the bot does not share with the owner.", False],
            Com2 = ["list", "Lists all servers the bot does not share with the owner.", False])
            await ctx.message.channel.send(embed=emb)

    @unshared.command(name='leave')
    async def leaveunshared(self, ctx):
        embed = Embeds.create_embed(self, ctx,
        "Bot left unshared servers",
        0x00ffff)
        owner = self.bot.AppInfo.owner
        servers = ""
        unavailable_servers = 0
        unshared_servers = 0
        for server in self.bot.guilds:
            check = server.get_member(owner.id)
            botuser = server.get_member(self.bot.user.id)
            if server.unavailable:
                unavailable_servers += 1
            else:
                if check == None:
                    unshared_servers += 1
                    servers += "**ID:** {0}\n**Owner:** {1}\n**Owner ID:** {2}\n**Members:** {3}\n**Join Date:** {4}".format(str(server.id), server.owner, server.owner.id, str(server.member_count),botuser.joined_at.strftime("%b %d, %Y; %I:%M %p"))
                    embed.add_field(name="Server Name: {0}".format(server.name), value=servers)
                    await server.leave()
                    await owner.send(embed=embed)
        if unavailable_servers == 1:
            await ctx.message.channel.send("{0} server is unavailable, skipping.".format(str(unavailable_servers)))
        elif unavailable_servers != 0:
            await ctx.message.channel.send("{0} servers are unavailable, skipping.".format(str(unavailable_servers)))
        if unshared_servers == 1:
            await ctx.message.channel.send("{0} server was left because bot does not share it with owner!".format(str(unshared_servers)))
        elif unshared_servers != 0:
            await ctx.message.channel.send("{0} servers were left because bot does not share them with owner!".format(str(unshared_servers)))
        else:
            await ctx.message.channel.send("No servers were left because bot shares all servers with owner!")

    @unshared.command(name='list')
    async def listunshared(self, ctx):
        embed = discord.Embed()
        embed.title = "Unshared Server List"
        embed.colour = 0x00ffff
        owner = self.bot.AppInfo.owner
        for server in self.bot.guilds:
            check = server.get_member(owner.id)
            botuser = server.get_member(self.bot.user.id)
            if check == None:
                servers = "**ID:** {0}\n**Owner:** {1}\n**Owner ID:** {2}\n**Members:** {3}\n**Join Date:** {4}".format(str(server.id), server.owner, server.owner.id, str(server.member_count),botuser.joined_at.strftime("%b %d, %Y; %I:%M %p"))
                embed.add_field(name="Server Name: {0}".format(server.name), value=servers, inline=False)        
        await owner.send(embed=embed)

def setup(bot):
    bot.add_cog(Unshared(bot))