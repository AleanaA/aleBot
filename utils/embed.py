import asyncio
import discord
class Embeds:
    def create_embed(ctx, title, color, message, **field):
        emb = discord.Embed()
        if title:
            emb.title = title
        if message:
            emb.description = message
        if color:
            emb.color = color
        for value in field:
            emb.add_field(name=field[value][0], value=field[value][1], inline=field[value][2])
        emb.set_footer(text="Requested by {}".format())
        return emb