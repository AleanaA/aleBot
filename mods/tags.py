import discord
from discord.ext import commands
from utils.dataIO import fileIO
from utils.embed import Embeds as emb
import os
import asyncio
import time
from datetime import datetime
import re 

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = fileIO("data/tags.json", "load")  

    def FindURL(self, string): 
        # findall() has been used  
        # with valid conditions for urls in string 
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
        return url 

    @commands.command(name="tag")
    @commands.guild_only()
    async def tag(self, ctx, name:str, mention:discord.Member=None):
        for tag in self.tags:
            if tag["Guild"] == ctx.message.guild.id:
                if tag["Name"] == name:
                    timestamp_str = tag["Creation"]
                    timestamp_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    author = self.bot.get_user(tag["Creator"])
                    embed = emb.create_embed(self, ctx, tag["Name"], None, tag["Content"])
                    embed.set_footer(text=author.name, icon_url=author.avatar_url)
                    embed.timestamp = timestamp_obj
                    try:
                        embed.set_image(url=self.FindURL(tag["Content"]))
                    except Exception:
                        pass
                    if mention:
                        men = mention.mention
                    else:
                        men = None
                    await ctx.send(men, embed=embed)
                    await ctx.message.delete()
                    return
                else:
                    foundtag = False
        if foundtag == False:
            await ctx.send("Unable to find tag `{}`".format(name))

    @commands.command(name="+tag")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def mktag(self, ctx, name : str, *, content : str):
        Guild = ctx.message.guild
        Author = ctx.message.author
        Creation = ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        for tag in self.tags:
            if tag["Guild"] == ctx.message.guild.id:
                if tag["Name"] == name:
                    await ctx.send("Unable to create duplicate tag")
                    return        
        if len(content) < 1:
            await ctx.send("Unable to create tag with empty string")
            return
        if len(content) > 2000:
            await ctx.send("Unable to create tag with character count over 2000")
            return
        self.tags.append({"Guild": Guild.id, "Creator": Author.id, "Creation": Creation, "Name": name, "Content": content})
        await ctx.send("Tag {0} was created with content:\n```{1}```".format(name, content))
        fileIO("data/tags.json", "save", self.tags)

    @commands.command(name="-tag")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def rmtag(self, ctx, name:str):
        to_remove = []
        for tag in self.tags:
            if tag["Guild"] == ctx.message.guild.id:
                if tag["Name"] == name or name == "*":
                    to_remove.append(tag)
        if not to_remove == []:
            for tag in to_remove:
                self.tags.remove(tag)
            fileIO("data/tags.json", "save", self.tags)
            if not name == "*":
                await ctx.send("Tag {0} removed successfully".format(tag["Name"]))
            else:
                await ctx.send("All tags successfully removed.")
        else:
            await ctx.send("Unable to remove tag. Unknown tag.")

    @commands.command(name="tags")
    @commands.guild_only()
    async def lstags(self, ctx):
        taglist = ""
        for tag in self.tags:
            if tag["Guild"] == ctx.message.guild.id:
                taglist += "{}, ".format(tag["Name"])
        if not taglist == "":
            await ctx.send("Tag list:\n```{}```".format(taglist[:-2]))
        else:
            await ctx.send("There are no tags on this server!")


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