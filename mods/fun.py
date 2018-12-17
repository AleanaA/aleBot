import discord
import random
from discord.ext import commands
from utils.dataIO import fileIO
from utils.cog import Cog
from utils.embed import Embeds as emb
from utils import checks
import os
import asyncio
import time
from datetime import datetime

class Fun(Cog):
    @commands.command(name="gif")
    async def gif(self, ctx):
        pass

    @commands.command(name="roll")
    async def roll(self, ctx):
        pass

    @commands.command(name="rps")
    async def rps(self, ctx):
        pass

    @commands.command(name="say")
    async def say(self, ctx):
        pass

    @commands.command(name="nugget")
    async def nugget(self, ctx):
        pass

    @commands.command(name="noodle")
    async def noodle(self, ctx):
        pass

    @commands.command(name="8ball")
    async def eightball(self, ctx):
        messages = ['It is certain',
            'It is decidedly so',
            'Yes definitely',
            'Reply hazy, try again',
            'Ask again later',
            'Concentrate and ask again',
            'My reply is no',
            'Outlook not so good',
            'Very doubtful']
        result = random.choice(messages)
        await ctx.send(result)

    @commands.command(name="aesthtify")
    async def aesthtify(self, ctx):
        pass

    @commands.command(name="dotify")
    async def dotify(self, ctx):
        pass

    @commands.command(name="f")
    async def respects(self, ctx):
        pass

    @commands.command(name="me")
    async def same(self, ctx):
        pass

    @commands.command(name="cookie")
    async def cookie(self, ctx):
        pass

    @commands.command(name="lick")
    async def lick(self, ctx):
        pass

    @commands.command(name="hug")
    async def hug(self, ctx):
        pass

    @commands.command(name="glomp")
    async def glomp(self, ctx):
        pass

    @commands.command(name="bite")
    async def bite(self, ctx):
        pass

    @commands.command(name="kiss")
    async def kiss(self, ctx):
        pass

    @commands.command(name="ckiss")
    async def ckiss(self, ctx):
        pass

    @commands.command(name="kawaii")
    async def kawaii(self, ctx):
        pass

    @commands.command(name="cuddle")
    async def cuddle(self, ctx):
        pass

    @commands.command(name="snuggle")
    async def snuggle(self, ctx):
        pass

    @commands.command(name="slap")
    async def slap(self, ctx):
        pass

    @commands.command(name="ascii")
    async def ascii(self, ctx):
        pass

    @commands.command(name="lewd")
    async def lewd(self, ctx):
        pass

    @commands.command(name="punch")
    async def punch(self, ctx):
        pass

    @commands.command(name="poke")
    async def poke(self, ctx):
        pass

    @commands.command(name="pat")
    async def pat(self, ctx):
        pass

    @commands.command(name="satan")
    async def satan(self, ctx):
        pass

    @commands.command(name="banme")
    async def banme(self, ctx):
        pass

    @commands.command(name="coin")
    async def coin(self, ctx):
        pass

    @commands.command(name="neko")
    async def neko(self, ctx):
        pass

    @commands.command(name="flirt")
    async def flirt(self, ctx):
        pass

    @commands.command(name="sob")
    async def sob(self, ctx):
        pass

    @commands.command(name="steal")
    async def steal(self, ctx):
        pass

    @commands.command(name="kill")
    async def kill(self, ctx, user: discord.User):
        pass

    @commands.command(name="suicide")
    async def suicide(self, ctx):
        pass

    @commands.command(name="purr")
    async def purr(self, ctx):
        pass

    @commands.command(name="rate")
    async def rate(self, ctx, user: discord.User):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        rating = random.choice(numbers)
        await ctx.send("I rate {} as a {}/10!".format(user.name, rating))

    @commands.command(name="moan")
    async def moan(self, ctx):
        pass

    @commands.command(name="pout")
    async def pout(self, ctx):
        pass

    @commands.command(name="blush")
    async def blush(self, ctx):
        pass

    @commands.command(name="pet")
    async def pet(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Fun(bot))