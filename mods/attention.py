import asyncio
import discord
import requests
from discord.ext import commands
from utils.embed import Embeds
from utils.config import Config

class Attention(commands.Cog):
    def __init__(self, bot):
        if bot.config.ifttt == None:
            bot.unload_extension("mods.ifttt")
        else:
            self.ifttt = bot.config.ifttt
            self.bot = bot 

    @commands.command(name="alert")
#    @commands.cooldown(1, 900, type=commands.BucketType.user)
    async def alert(self, ctx, alert):
        alerttt = {}
        alerttt["value1"] = "{} sent an alert:".format(ctx.message.author)
        alerttt["value2"] = str(alert)
        requests.post("https://maker.ifttt.com/trigger/aleBotnotif/with/key/{}".format(self.ifttt), data=alerttt)
        await self.bot.appinfo.owner.send("{} sent an alert:\n{}".format(ctx.message.author, alert))
        await ctx.send("An alert was sent to the bot owner!\nPlease note, you won't be able to send another alert for 15 minutes!")

def setup(bot):
    bot.add_cog(Attention(bot))