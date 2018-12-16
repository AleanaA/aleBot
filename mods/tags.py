import discord
from discord.ext import commands
from utils.dataIO import fileIO
from utils.cog import Cog
from utils.embed import Embeds as emb
import os
import asyncio
import time

class Tags(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = fileIO("data/tags.json", "load")

    @commands.group(name="tag")
    async def tag(self, ctx, name:str, mention:discord.Member=None):
        if ctx.invoked_subcommand is None:
            for tag in self.tags:
                if tag["Guild"] == ctx.message.guild.id:
                    if tag["Name"] == name:
                        author = await self.bot.get_user_info(tag["Creator"])
                        embed = emb.create_embed(self, ctx, tag["Name"], None, tag["Content"])
                        embed.set_footer(text=author.name, icon_url=author.avatar_url)
                        embed.timestamp = tag["Creation"]
                        await ctx.send(embed=embed)

    @tag.command(name="add")
    async def addtag(self, ctx, name : str, *, content : str):
        Guild = ctx.message.guild
        Author = ctx.message.author
        Creation = time.time()
        if len(content) < 1:
            await ctx.send("Unable to create tag with empty string")
            return
        if len(content) > 500:
            await ctx.send("Unable to create tag with character count over 500")
            return
        self.tags.append({"Guild": Guild.id, "Creator": Author.id, "Creation": Creation, "Name": name, "Content": content})
        await ctx.send("Tag {0} was created with content:\n```{1}```".format(name, content))
        fileIO("data/tags.json", "save", self.tags)

def check_folders():
    if not os.path.exists("data"):
        print("Creating data folder...")
        os.makedirs("data")

def check_files():
    f = "data/tags.json"
    if not fileIO(f, "check"):
        print("Creating empty tags.json...")
        fileIO(f, "save", [])

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Tags(bot))