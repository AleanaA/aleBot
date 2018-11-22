import asyncio
import discord
class Embeds:
    
    def create_embed(self, title, color, message, **field):
        emb = discord.Embed()
        emb.title = title
        emb.description = message
        emb.color = color
        for value in field:
            emb.add_field(name=field, value=value)
        return emb