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
    
    @commands.command(name='roll')
    async def roll(self, ctx, dice, sides):
        rolling = []

        try:
            if 'd' in sides:
                for x in range(int(sides.split('d')[0])):
                        rolling.append(randint(int(dice),int(roll.split('d')[1])))
            else:
                for x in range(int(sides)):
                        rolling.append(randint(int(dice),int(sides)))
        except Exception as err:
            await ctx.send("An issue occurred trying to roll.")
        
        await ctx.send('You rolled: \n{0} which has a total of\n------\n{1}'.format("\n".join(str(x) for x in rolling), sum(rolling)))

def setup(bot):
    bot.add_cog(Roll(bot))