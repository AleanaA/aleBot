import asyncio
import discord
import requests
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
        AUDDIT = discord.utils.get(self.bot.get_all_channels(), guild__name=ctx.message.guild.name, name='audit')
        if AUDDIT == None:
            return await ctx.message.channel.send("No channel named 'audit'")
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
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.Done + " {0} was successfully unbanned!".format(str(banned))))
        await AUDDIT.send(embed=embed)

    @commands.command(name='Kick',
                    description="Kicks a user",
                    brief="Kicks a user",
                    aliases=['kick'])
    @checks.is_appr()
    async def kick(self, ctx, userName: discord.Member, *reason):
        if ctx.message.author.top_role <= userName.top_role:
            await ctx.message.channel.send(embed=discord.Embed(title="Permission Error", description="You don't have permission to kick that user!", color=0xff0000))
            return
        AUDDIT = discord.utils.get(self.bot.get_all_channels(), guild__name=ctx.message.guild.name, name='audit')
        if AUDDIT == None:
            return await ctx.message.channel.send("No channel named 'audit'")
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
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.Done + " {0} was successfully kicked!".format(str(userName))))
        await AUDDIT.send(embed=embed)

    @commands.command(name='Ban',
                    description="Bans a user",
                    brief="Bans a user",
                    aliases=['ban'])
    @checks.is_mod()
    async def ban(self, ctx, userName: discord.Member, *reason):
        if ctx.message.author.top_role <= userName.top_role:
            await ctx.message.channel.send(embed=discord.Embed(title="Permission Error", description="You don't have permission to kick that user!", color=0xff0000))
            return
        AUDDIT = discord.utils.get(self.bot.get_all_channels(), guild__name=ctx.message.guild.name, name='audit')
        if AUDDIT == None:
            return await ctx.message.channel.send("No channel named 'audit'")
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
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.Done + " {0} was successfully banned!".format(str(userName))))
        await AUDDIT.send(embed=embed)

    @commands.command(name='BanID',
                    description="Bans a user",
                    brief="Bans a user",
                    aliases=['banid'])
    @checks.is_mod()
    async def banid(self, ctx, userName, *reason):
        AUDDIT = discord.utils.get(self.bot.get_all_channels(), guild__name=ctx.message.guild.name, name='audit')
        if AUDDIT == None:
            return await ctx.message.channel.send("No channel named 'audit'")
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
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.Done + " {0} was successfully banned!".format(str(banned))))
        await AUDDIT.send(embed=embed)

    @commands.command(name='Softban',
                    description="Bans a user, then unbans them, deleting their messages.",
                    brief="Softbans a user",
                    aliases=['softban'])
    @checks.is_mod()
    async def softban(self, ctx, userName: discord.Member, *reason):
        if ctx.message.author.top_role <= userName.top_role:
            await ctx.message.channel.send(embed=discord.Embed(title="Permission Error", description="You don't have permission to kick that user!", color=0xff0000))
            return
        AUDDIT = discord.utils.get(self.bot.get_all_channels(), guild__name=ctx.message.guild.name, name='audit')
        if AUDDIT == None:
            return await ctx.message.channel.send("No channel named 'audit'")
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
        embed.set_footer(text=emotes.Done)
        await server.ban(userName, reason=rsn)
        await server.unban(userName, reason=rsn)
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.Done + " {0} was successfully softbanned!".format(str(userName))))
        await AUDDIT.send(embed=embed)

    @commands.group(name='reactions',
                description="Manage reactions!",
                brief="Manage Reactions!")
    @checks.is_mod()
    async def reactions(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed()
            emb.title = "Reaction Manager " + emotes.Warn
            emb.colour = 0xffff00
            emb.description = "Please issue a valid subcommand!\nAvailable options are:"
            emb.add_field(name="Add", value="Add an available reaction to a message.", inline=False)
            emb.add_field(name="Remove", value="Remove a reaction, or all reactions from a message.", inline=False)
            await ctx.message.channel.send(embed=emb)
    
    @reactions.command(name='add')
    async def reactionadd(self, ctx, id, emote):
        reaction = None
        for server in self.bot.guilds:
            for emoji in server.emojis:
                if emote == emoji.name:
                    reaction=emoji
        
        if reaction == None:
            await ctx.message.channel.send("Emote not found.")
            return

        async for message in ctx.message.channel.history():
            foundmsg=0
            if message.id == id:
                await message.add_reaction(reaction)
                foundmsg=1
                return
        if foundmsg == 0:
            await ctx.message.channel.send("Unable to find message")

    @reactions.command(name='remove')
    async def reactionrem(self, ctx, mid):
        message = await ctx.message.channel.history().get(id=mid)
        try:
            await message.clear_reactions()
        except:
            await ctx.message.channel.send("Unable to clear reactions.")
            return
        else:
            await ctx.message.channel.send("Reactions cleared.")
            return
    
    @commands.command(name='serverimage',
                description="Changes the server image!")
    @checks.is_admin()
    async def serverimage(self, ctx, url):
        emb = discord.Embed()
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
            emb.colour = 0xff0000
            emb.description = "An error occured. Unable to get image from url."
            return await ctx.message.channel.send(embed=emb)
        if response.status_code == 404:
            emb.colour = 0xff0000
            emb.description = "404 error occured."
            return await ctx.message.channel.send(embed=emb)
        await ctx.message.guild.edit(icon=response.content)
        emb.colour = 0x00ff00
        emb.description = "Successfully changed the server image!"
        await ctx.message.channel.send(embed=emb)

def setup(bot):
    bot.add_cog(Moderation(bot))