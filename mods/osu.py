import asyncio
import discord
import requests
from osuapi import OsuApi, AHConnector, enums
from discord.ext import commands
from utils.embed import Embeds
from utils.config import Config
from utils.cog import Cog

class Osu:
    def __init__(self, bot):
        if bot.config.osuapi == None:
            bot.unload_extension("mods.osu")
        else:
            self.osuapi = OsuApi(bot.config.osuapi, connector=AHConnector())
            self.bot = bot 
    
    @commands.command(name='osu')
    async def osu(self, ctx, mode, *, user : str):
        modes={
            "standard": enums.OsuMode.osu,
            "taiko": enums.OsuMode.taiko,
            "mania": enums.OsuMode.mania,
            "catch": enums.OsuMode.ctb,
            }
        if mode not in modes:
            await ctx.send("Please specify a valid mode.")
            return

        players = await self.osuapi.get_user(user, mode=modes[mode])

        if players:
            player = players[0]
            emb = Embeds.create_embed(self, ctx, player.username, color=0xbb1177, message=mode,
                                    Info=["Player Info", "Playcount - {}\nLevel - {}\nCountry - {}".format(player.playcount, player.level, player.country), True],
                                    Stats=["Player Stats", "Rank - {}\nPP - {}\nAccuracy - {}".format(player.pp_rank, player.pp_raw, player.accuracy), True])
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Osu(bot))