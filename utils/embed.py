import asyncio
import discord
import requests
from utils.config import Config

class Embeds:
    def create_embed(self, ctx):
        emb = discord.Embed()
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        emb.timestamp = ctx.message.created_at
        emb.colour = 0x005aff
        print(Config('config/config.ini').embedname)
        if Config('config/config.ini').embedname == True:
            try:
                request = requests.get(ctx.command.cog.url)
                if request.status_code == 200:
                    emb.set_author(name=ctx.command.cog_name, url=ctx.command.cog.url)
                else:
                    emb.set_author(name=ctx.command.cog_name)
            except:
                emb.set_author(name=ctx.command.cog_name)
        return emb