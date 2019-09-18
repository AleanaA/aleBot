import asyncio
import discord
import aiohttp
import json
import requests
from discord.ext import commands
from utils.embed import Embeds

class FFXIV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jobs = {
            1: "Gladiator",
            2: "Pugilist",
            3: "Marauder",
            4: "Lancer",
            5: "Archer",
            6: "Conjurer",
            7: "Thaumaturge",
            8: "Carpenter",
            9: "Blacksmith",
            10: "Armorer",
            11: "Goldsmith",
            12: "Leatherworker",
            13: "Weaver",
            14: "Alchemist",
            15: "Culinarian",
            16: "Miner",
            17: "Botanist",
            18: "Fisher",
            19: "Paladin",
            20: "Monk",
            21: "Warrior",
            22: "Dragoon",
            23: "Bard",
            24: "White Mage",
            25: "Black Mage",
            26: "Arcanist",
            27: "Summoner",
            28: "Scholar",
            29: "Rogue",
            30: "Ninja",
            31: "Machinist",
            32: "Dark Knight",
            33: "Astrologian",
            34: "Samurai",
            35: "Red Mage",
            36: "Blue Mage"
        }


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
            activeclass = character["ActiveClassJob"]
            activeclassname = activeclass["JobID"]
            activeclasslevel = activeclass["Level"]
        except Exception:
            request = requests.get("https://xivapi.com/character/search?name={0}&server={1}".format(name, world)).content.decode('utf8')
            result = json.loads(request)["Results"][0]
            id = result["ID"]
            idrequest = requests.get("https://xivapi.com/character/{}".format(id)).content.decode('utf8')
            character = json.loads(idrequest)["Character"]
            server = character["Server"]
            name = character["Name"]
            portrait = character["Portrait"]
            avatar = character["Avatar"]
            activeclass = character["ActiveClassJob"]
            activeclassname = activeclass["JobID"]
            activeclasslevel = activeclass["Level"]
        emb = Embeds.create_embed(self, ctx)
        emb.title = name
        emb.description = server
        emb.set_thumbnail(url=avatar)
        emb.set_image(url=portrait)
        emb.set_author(name="Final Fantasy XIV")
        emb.add_field(name="Active Job", value="{0} - Level {1}".format(self.jobs[activeclassname], activeclasslevel), inline=True)
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(FFXIV(bot))