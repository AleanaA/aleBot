import asyncio
import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils.cog import Cog

class Tests(Cog):
    @commands.command(name="getmsg")
    async def getmsg(self, ctx, mid):
        for channel in ctx.guild.text_channels:
            try:
                message = await channel.get_message(int(mid))
            except:
                pass
        await ctx.send(message.content)

def setup(bot):
    bot.add_cog(Tests(bot))