import asyncio
import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils import checks
from utils.cog import Cog
from config import emotes

class Emotes(Cog):
    @commands.command(name='Wut',
                    description="emotes.rooWut",
                    brief="emotes.rooWut",
                    aliases=['wut'])
    async def Wut(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooWut)

    @commands.command(name='Whine',
                    description="emotes.rooWhine",
                    brief="emotes.rooWhine",
                    aliases=['whine'])
    async def Whine(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooWhine)

    @commands.command(name='W',
                    description="emotes.rooW",
                    brief="emotes.rooW",
                    aliases=['w'])
    async def W(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooW)

    @commands.command(name='VV',
                    description="emotes.rooVV",
                    brief="emotes.rooVV",
                    aliases=['vv'])
    async def VV(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooVV)

    @commands.command(name='Think',
                   description="emotes.rooThink",
                    brief="emotes.rooThink",
                    aliases=['think'])
    async def Think(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooThink)

    @commands.command(name='Nap',
                    description="emotes.rooNap",
                    brief="emotes.rooNap",
                    aliases=['nap'])
    async def Nap(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooSleep)

    @commands.command(name='Sip',
                    description="emotes.rooSip",
                    brief="emotes.rooSip",
                    aliases=['sip'],
)
    async def Sip(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooSip)

    @commands.command(name='Sellout',
                    description="emotes.rooSellout",
                    brief="emotes.rooSellout",
                    aliases=['sellout'],
)
    async def Sellout(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooSellout)

    @commands.command(name='Scared',
                    description="emotes.rooScared",
                    brief="emotes.rooScared",
                    aliases=['scared'],
)
    async def Scared(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooScared)

    @commands.command(name='REE',
                    description="emotes.rooREE",
                    brief="emotes.rooREE",
                    aliases=['ree'],
)
    async def REE(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooREE)

    @commands.command(name='POG',
                    description="emotes.rooPOG",
                    brief="emotes.rooPOG",
                    aliases=['pog'],
)
    async def POG(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooPog)

    @commands.command(name='Pew',
                    description="emotes.rooPewPew",
                    brief="emotes.rooPewPew",
                    aliases=['pew'],
)
    async def Pew(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooPew)

    @commands.command(name='Nom',
                    description="emotes.rooNom",
                    brief="emotes.rooNom",
                    aliases=['nom'],
)
    async def Nom(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooNom)

    @commands.command(name='Magic',
                    description="emotes.rooMagic",
                    brief="emotes.rooMagic",
                    aliases=['magic'],
)
    async def Magic(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooMagic)

    @commands.command(name='Joose',
                    description="emotes.rooJoose",
                    brief="emotes.rooJoose",
                    aliases=['joose'],
)
    async def Joose(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooJoose)

    @commands.command(name='Hep',
                    description="emotes.rooHelp",
                    brief="emotes.rooHep",
                    aliases=['hep'],
)
    async def Hep(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooHep)

    @commands.command(name='Happy',
                    description="emotes.rooHappy",
                    brief="emotes.rooHappy",
                    aliases=['happy'],
)
    async def Happy(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooHappy)

    @commands.command(name='Fite',
                    description="emotes.rooFite",
                    brief="emotes.rooFite",
                    aliases=['fite'],
)
    async def Fite(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooFite)

    @commands.command(name='Fat',
                    description="emotes.rooFat",
                    brief="emotes.rooFat",
                    aliases=['fat'],
)
    async def Fat(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooFite)

    @commands.command(name='EZ',
                    description="emotes.rooEZ",
                    brief="emotes.rooEZ",
                    aliases=['ez'],
)
    async def EZ(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooEZ)

    @commands.command(name='Duck',
                    description="emotes.rooDuck",
                    brief="emotes.rooDuck",
                    aliases=['duck'],
)
    async def Duck(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooDuck)

    @commands.command(name='Devil',
                    description="emotes.rooDevil",
                    brief="emotes.rooDevil",
                    aliases=['devil'],
)
    async def Devil(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooDevil)

    @commands.command(name='Derp',
                    description="emotes.rooDerp",
                    brief="emotes.rooDerp",
                    aliases=['derp'],
)
    async def Derp(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooDerp)

    @commands.command(name='Dab',
                    description="emotes.rooDab",
                    brief="emotes.rooDab",
                    aliases=['dab'],
)
    async def Dab(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooDab)

    @commands.command(name='Cry',
                    description="emotes.rooCry",
                    brief="emotes.rooCry",
                    aliases=['cry'],
)
    async def Cry(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooCry)

    @commands.command(name='Booli',
                    description="emotes.rooBooli",
                    brief="emotes.rooBooli",
                    aliases=['booli'],
)
    async def Booli(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooBooli)

    @commands.command(name='Blind',
                    description="emotes.rooBling",
                    brief="emotes.rooBlind",
                    aliases=['blind'],
)
    async def Blind(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooBlind)

    @commands.command(name='Bless',
                    description="emotes.rooBless",
                    brief="emotes.rooBless",
                    aliases=['bless'],
)
    async def Bless(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooBless)

    @commands.command(name='Blank',
                    description="emotes.rooBlank",
                    brief="emotes.rooBlank",
                    aliases=['blank'],
)
    async def Blank(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooBlank)

    @commands.command(name='Aww',
                    description="emotes.rooAww",
                    brief="emotes.rooAww",
                    aliases=['aww'],
)
    async def Aww(self, ctx):
        await ctx.message.delete()
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooAww)

def setup(bot):
    bot.add_cog(Emotes(bot))