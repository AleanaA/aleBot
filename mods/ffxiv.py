import asyncio
import discord
import aiohttp
import json
import requests
from discord.ext import commands
from utils.embed import Embeds
from utils.config import Config

class FFXIV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ffchar")
    async def ffchar(self, ctx, world, *, name):
        try:
            request = requests.get("https://xivapi.com/character/search?name={0}&server={1}".format(name, world)).content.decode('utf8')
            result = json.loads(request)["Results"][0]
            id = result["ID"]
            character = json.loads(requests.get("https://xivapi.com/character/{}".format(id)).content.decode('utf8'))["Character"]
            server = character["Server"]
            name = character["Name"]
            portrait = character["Portrait"]
            avatar = character["Avatar"]
        except Exception:
            request = requests.get("https://xivapi.com/character/search?name={0}&server={1}".format(name, world)).content.decode('utf8')
            result = json.loads(request)["Results"][0]
            id = result["ID"]
            character = json.loads(requests.get("https://xivapi.com/character/{}".format(id)).content.decode('utf8'))["Character"]
            server = character["Server"]
            name = character["Name"]
            portrait = character["Portrait"]
            avatar = character["Avatar"]
        emb = Embeds.create_embed(self, ctx, "Final Fantasy XIV", None, name)
        emb.set_thumbnail(url=avatar)
        emb.set_image(url=portrait)
        emb.set_author(name=server)
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(FFXIV(bot))