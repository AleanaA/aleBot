import asyncio
import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils import checks
from utils.cog import Cog
from utils.config import Config
from config import emotes
#from config import config

class Moderation(Cog):        
    @commands.command(name='Unban',
                    description="Unbans a user",
                    brief="Unbans a user",
                    aliases=['unban'])
    @checks.is_mod()
    async def unban(self, ctx, userName, *reason):
        self.config = Config('config/config.ini')
        AUDDIT = self.bot.get_channel(self.config.auddit)
        server = ctx.message.guild
        auth = ctx.message.author
        rsn = " ".join(reason)
        banned = await self.bot.get_user_info(userName)
        action = "Unbanned"
        if rsn == "":
            rsn = "No Reason Specified"
        embed=discord.Embed(title=str(banned), url=banned.avatar_url, color=0x00ff00)
        embed.set_author(name=auth.name,icon_url=auth.avatar_url)
        embed.set_thumbnail(url=banned.avatar_url)
        embed.add_field(name="Action", value=action, inline=True)
        embed.add_field(name="Reason", value=rsn, inline=True)
        await server.unban(banned, reason=rsn)
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.rooFite + " {0} was successfully unbanned!".format(str(banned))))
        await AUDDIT.send(embed=embed)

    @commands.command(name='Kick',
                    description="Kicks a user",
                    brief="Kicks a user",
                    aliases=['kick'])
    @checks.is_appr()
    async def kick(self, ctx, userName: discord.Member, *reason):
        self.config = Config('config/config.ini')
        AUDDIT = self.bot.get_channel(self.config.auddit)
        server = ctx.message.guild
        auth = ctx.message.author
        rsn = " ".join(reason)
        action = "Kicked"
        if rsn == "":
            rsn = "No Reason Specified"
        embed=discord.Embed(title=str(userName), url=userName.avatar_url, color=0xff0000)
        embed.set_author(name=auth.name,icon_url=auth.avatar_url)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.add_field(name="Action", value=action, inline=True)
        embed.add_field(name="Reason", value=rsn, inline=True)
        await server.kick(userName, reason=rsn)
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.rooFite + " {0} was successfully kicked!".format(str(userName))))
        await AUDDIT.send(embed=embed)

    @commands.command(name='Ban',
                    description="Bans a user",
                    brief="Bans a user",
                    aliases=['ban'])
    @checks.is_mod()
    async def ban(self, ctx, userName: discord.User, *reason):
        self.config = Config('config/config.ini')
        AUDDIT = self.bot.get_channel(self.config.auddit)
        server = ctx.message.guild
        auth = ctx.message.author
        rsn = " ".join(reason)
        action = "Banned"
        if rsn == "":
            rsn = "No Reason Specified"
        embed=discord.Embed(title=str(userName), url=userName.avatar_url, color=0xff0000)
        embed.set_author(name=auth.name,icon_url=auth.avatar_url)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.add_field(name="Action", value=action, inline=True)
        embed.add_field(name="Reason", value=rsn, inline=True)
        await server.ban(userName, reason=rsn)
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.rooFite + " {0} was successfully banned!".format(str(userName))))
        await AUDDIT.send(embed=embed)

    @commands.command(name='BanID',
                    description="Bans a user",
                    brief="Bans a user",
                    aliases=['banid'])
    @checks.is_mod()
    async def banid(self, ctx, userName, *reason):
        self.config = Config('config/config.ini')
        AUDDIT = self.bot.get_channel(self.config.auddit)
        server = ctx.message.guild
        auth = ctx.message.author
        rsn = " ".join(reason)
        banned = await self.bot.get_user_info(userName)
        action = "Banned"
        if rsn == "":
            rsn = "No Reason Specified"
        embed=discord.Embed(title=str(banned), url=banned.avatar_url, color=0xff0000)
        embed.set_author(name=auth.name,icon_url=auth.avatar_url)
        embed.set_thumbnail(url=banned.avatar_url)
        embed.add_field(name="Action", value=action, inline=True)
        embed.add_field(name="Reason", value=rsn, inline=True)
        await server.ban(banned, reason=rsn)
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.rooFite + " {0} was successfully banned!".format(str(banned))))
        await AUDDIT.send(embed=embed)

    @commands.command(name='Softban',
                    description="Bans a user, then unbans them, deleting their messages.",
                    brief="Softbans a user",
                    aliases=['softban'])
    @checks.is_mod()
    async def softban(self, ctx, userName: discord.User, *reason):
        self.config = Config('config/config.ini')
        AUDDIT = self.bot.get_channel(self.config.auddit)
        server = ctx.message.guild
        auth = ctx.message.author
        rsn = " ".join(reason)
        action = "Softbanned"
        if rsn == "":
            rsn = "No Reason Specified"
        embed=discord.Embed(title=str(userName), url=userName.avatar_url, color=0xff0000)
        embed.set_author(name=auth.name,icon_url=auth.avatar_url)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.add_field(name="Action", value=action, inline=True)
        embed.add_field(name="Reason", value=rsn, inline=True)
        embed.add_field(name="ID", value=str(userName.id), inline=True)
        embed.set_footer(text=emotes.rooFite)
        await server.ban(userName, reason=rsn)
        await server.unban(userName, reason=rsn)
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.rooFite + " {0} was successfully softbanned!".format(str(userName))))
        await AUDDIT.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))