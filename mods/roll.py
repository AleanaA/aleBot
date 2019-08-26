import asyncio
import discord
import aiohttp
from random import randint
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name='roll')
    async def roll(self, ctx, dice, sides):
        rolling = []

        try:
            if 'd' in sides:
                for x in range(int(dice)):
                        rolling.append(randint(1,int(sides[1:])))
            else:
                for x in range(int(dice)):
                        rolling.append(randint(1,int(sides)))
        except Exception as err:
            await ctx.send(err)
        
        await ctx.send('You rolled: \n{0}\nWhich has a total of\n------\n{1}'.format("\n".join(str(x) for x in rolling), sum(rolling)))

    @roll.command(name='charroll')
    async def charroll(self, ctx):
        stats = []

        for x in range(4):
            stats.append(randint(1,6))

        await ctx.send('Your characters stats are: {}'.format(", ".join(srt(x) for x in stats)))

def setup(bot):
    bot.add_cog(Roll(bot))