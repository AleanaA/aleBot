import asyncio
import discord

class Embeds:
    def create_embed(self, ctx, title, color=None, message=None, **field):
        emb = discord.Embed()
        if title:
            emb.title = title
        if message:
            emb.description = message
        if color:
            emb.color = color
        for value in field:
            emb.add_field(name=field[value][0], value=field[value][1], inline=field[value][2])
        emb.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        emb.timestamp = ctx.message.created_at
        return emb