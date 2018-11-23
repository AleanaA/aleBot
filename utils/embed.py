import asyncio
import discord
class Embeds:

    def create_embed(self, title, color, message, **field):
        emb = discord.Embed()
        if title not '':
            emb.title = title
        if message not '':
            emb.description = message
        if color not '':
            emb.color = color
        for value in field:
            emb.add_field(name=field[value][0], value=field[value][1], inline=field[value][2])
        return emb