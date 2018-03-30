import asyncio
import discord
import inspect
import re
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils import checks
from utils.cog import Cog
from config import emotes
from config import config
from config.config import BACKUP_TAGS
from utils.json import load_json
from utils.checks import InvalidUsage

emb = discord.Embed()
color = emb.color

class Response:

    """
    Response class for commands
    """

    def __init__(self, content, reply=True, delete=0):
        self.content = content
        self.reply = reply
        self.delete = delete

class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.db = bot.db
        self.req = bot.req
    @commands.command(name='eval',
                description="Owner Only!",
                brief="Owner Only!",
                aliases=['debug', 'Eval', 'Debug'])
    @checks.is_owner()
    async def debug(self, ctx, *, code : str):
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        auth = ctx.message.author
        authmen = auth.mention

        env = {
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'author': ctx.message.author
        }

        env.update(globals())
        if code == '':
            emb.title = "An Error Occured"
            emb.description = emotes.rooBooli + " What do you want me to evaluate " + authmen + "?"
            emb.colour = color(0xff0000)
            await ctx.message.channel.send(embed=emb)
        try:
            result = eval(code, env)
            if inspect.isawaitable(result):
                result = await result
        except Exception as e:
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0xff0000), title="Python Eval", description=python.format(type(e).__name__ + ': ' + str(e))))
            return

        await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x0094ff), title="Python Eval", description=python.format(result)))

    @commands.command(name='ping',
                description="Ping!",
                brief="Ping!",
                aliases=['Ping', 'Ping!'])
    async def ping(self, ctx):
        await ctx.message.channel.send(ctx.message.author.mention + " " + emotes.rooBot)

    @commands.command(name='say',
                description="Text Command",
                brief="Text Command",
                aliases=[])
    @checks.is_event()
    async def say(self, ctx, *content):
        msg = " ".join(content)
        auth = ctx.message.author
        authmen = auth.mention

        emb.title = emotes.rooHappy
        emb.description = msg
        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.rooBooli + " What do you want me to say " + authmen + "?"
            emb.colour = color(0xff0000)
            await ctx.message.channel.send(embed=emb)
        else:
            await ctx.message.delete()
            await ctx.message.channel.send(embed=emb)

    @commands.command(name='Announce',
                description="Allows select users to make an announcement!",
                brief="Creates an announcement!",
                aliases=['announce', 'ANNOUNCE'])
    @checks.is_event()
    async def announce(self, ctx, *content):
        msg = ' '.join(content)
        auth = ctx.message.author
        authmen = auth.mention
        ANNOUNCE = self.bot.get_channel(config.AnnounceChannel)
        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.rooBooli + " What do you want me to announce " + authmen + "?"
            emb.colour = color(0xff0000)
            await ctx.message.channel.send(embed=emb)
        else:
            await ANNOUNCE.send(emotes.rooAww + " " + authmen + " - @everyone " + msg)
            await ctx.message.delete()
            await ctx.message.channel.send(emotes.rooBot + " Announcement Created")

    @commands.command(name='log',
                description="Allows select users to make a log entry!",
                brief="Creates a log entry!",
                aliases=['LOG', 'Log'])
    @checks.is_appr()
    async def log(self, ctx, *content):
        msg = ' '.join(content)
        auth = ctx.message.author
        authmen = auth.mention
        LOG = self.bot.get_channel(config.LogChannel)

        emb.title = emotes.rooHappy + " " + auth.name + " logged a message!"
        emb.description = msg
        emb.colour = discord.Colour(0x0094ff)

        if msg == '':
            emb.title = "An Error Occured"
            emb.description = emotes.rooBooli + " What do you want me to add to the log " + authmen + "?"
            emb.colour = color(0xff0000)
            await ctx.message.channel.send(embed=emb)
        else:
            await LOG.send(embed=emb)
            await ctx.message.delete()
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff2c), description=emotes.rooBot + " Log Added"))

    @commands.command(name='die',
                description="Shuts down the bot",
                brief="Shuts down the bot",
                aliases=['sd', 'shutdown'])
    @checks.is_owner()
    async def die(self, ctx):
        print(str(ctx.message.author) + " triggered a shutdown!")
        await ctx.message.channel.send(embed=discord.Embed(description=emotes.rooBooli + " Alright, I'll shut down... Good night " + ctx.message.author.mention, color=0x0035ff))
        await self.bot.logout()

    async def c_tags(self):
        """
        Get a list of all tags
        {prefix}tags
        """
        if not self.bot.dbfailed:
            cursor = await self.db.get_db().table(self.bot.config.dbtable_tags).run(self.db.db)
            if not cursor.items:
                return Response(":warning: No tags exist (yet)", delete=10)
            tags = [x['name'] for x in cursor.items]
        else:
            tags = load_json(BACKUP_TAGS)
            if not tags:
                return Response(":warning: No tags found in the backup tags file", delete=10)
        return Response(":pen_ballpoint: **Tags**\n`{}`".format('`, `'.join(tags)), delete=60)

    async def c_createtag(self, message):
        """
        Create a tag
        {prefix}createtag <"name"> <"tag">
        """
        content = re.findall('"([^"]*)"', message.content)
        if len(content) == 2:
            name, content = content
            data = {"name": name, "content": content}
            await self.db.insert(self.bot.config.dbtable_tags, data)
            return Response(":thumbsup:", delete=10)
        else:
            raise InvalidUsage()

    async def c_deletetag(self, message):
        """
        Delete a tag
        {prefix}deletetag <"name">
        """
        content = re.findall('"([^"]*)"', message.content)
        if len(content) == 1:
            name = content[0]
            delete = await self.db.delete(self.bot.config.dbtable_tags, name)
            if int(delete['skipped']) != 0:
                return Response(":warning: Could not delete `{}`, does not exist".format(name), delete=10)
            return Response(":thumbsup:", delete=10)
        else:
            raise InvalidUsage()

    async def c_tag(self, message, tag):
        """
        Returns a tag
        {prefix}tag <name>
        """
        content = message.content.replace(
            '{}tag '.format(self.config.prefix), '')
        if not self.bot.dbfailed:
            get = await self.db.get_db().table(self.bot.config.dbtable_tags).get(content).run(self.db.db)
            if get is None:
                return Response(":warning: No tag named `{}`".format(content), delete=10)
            else:
                return Response(get['content'])
        else:
            get = load_json(BACKUP_TAGS)
            if not get:
                return Response(":warning: No tags found in the backup tags file", delete=10)
            else:
                get = get.get(content, default=None)
                if get is None:
                    return Response(":warning: No tag with that name in the backup tags file", delete=10)
                else:
                    return Response(get)

    async def c_cleartags(self):
        """
        Clears all tags
        {prefix}cleartags
        """
        await self.db.delete(self.bot.config.dbtable_tags)
        return Response(":thumbsup:", delete=10)

def setup(bot):
    bot.add_cog(Commands(bot))