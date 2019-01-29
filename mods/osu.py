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
        if bot.config.osu == None:
            bot.unload_extension("mods.osu")
        else:
            self.osuapi = OsuApi(bot.config.osu, connector=AHConnector())
            self.bot = bot 
    
    @commands.command(name='osu')
    async def osu(self, ctx, mode, *, user : str):
        mode = mode.lower()
        modes={
            "standard": enums.OsuMode.osu,
            "taiko": enums.OsuMode.taiko,
            "mania": enums.OsuMode.mania,
            "catch": enums.OsuMode.ctb,
            }
        formattedmodes={
            "standard": "osu!Standard",
            "taiko": "osu!Taiko",
            "mania": "osu!Mania",
            "catch": "osu!Catch",
            }
        if mode not in modes:
            await ctx.send("Please specify a valid mode.")
            return

        players = await self.osuapi.get_user(user, mode=modes[mode])

        if players:
            player = players[0]
            emb = Embeds.create_embed(self, ctx, formattedmodes[mode], color=0xbb1177, message=None,
                                    Info=["Player Info", "Playcount - {:,}\nLevel - {:,}\nCountry - {}".format(player.playcount, int(round(player.level)), player.country), True],
                                    Stats=["Player Stats", "Rank - {:,}\nPP - {:,}\nAccuracy - {}%".format(player.pp_rank, round(player.pp_raw, 2), round(player.accuracy,2)), True])
            emb.set_author(name=player.username, url="https://osu.ppy.sh/users/{}".format(player.user_id))
            emb.set_thumbnail(url="https://a.ppy.sh/{}?1487388464.png".format(player.user_id))
            await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Osu(bot))