import asyncio
import discord
from pushbullet import Pushbullet
from discord.ext import commands
from utils.embed import Embeds
from utils.config import Config

class Attention(commands.Cog):
    def __init__(self, bot):
        if bot.config.pb == None:
            bot.unload_extension("mods.attention")
        else:
            self.pb = Pushbullet(bot.config.pb)
            self.bot = bot 
            self.whitelisted = [168118999337402368,493608568201936927,162349100396707840,168141723019640832]

    @commands.command(name="alert")
    @commands.cooldown(1, 1800, type=commands.BucketType.user)
    async def alert(self, ctx, *, alert:str):
        self.pb.push_note("{} sent an alert:".format(ctx.message.author), alert)
        await ctx.send("An alert was sent to the bot owner!\nPlease note, you won't be able to send another alert for 30 minutes!")

    @commands.command(name="hey")
    async def hey_listen(self, ctx, *, alert:str):
        if ctx.message.author.id in self.whitelisted:
            self.pb.push_note("{} wants your attention:".format(ctx.message.author.name), alert)
            await ctx.send("Conner was notified that you wanted his attention!")

def setup(bot):
    bot.add_cog(Attention(bot))