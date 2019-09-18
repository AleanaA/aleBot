import asyncio
import discord
import inspect
import aiohttp
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils.config import Config
from utils.embed import Embeds

class BotOptions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='bot',
                    description="Manage settings for the bot.",
                    brief="Manage settings for the bot.")
    @commands.is_owner()
    async def manbot(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.channel.send("Please enter a valid subcommand")

    @manbot.command(name='invite',
                description="Gets the bots invite url!",
                brief="Gets the bots invite url!",
                aliases=['Invite'])
    async def invite(self, ctx):
        emb = discord.Embed()
        emb.title = "Invite URL"
        emb.description = "<https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=8>".format(str(self.bot.user.id))
        emb.colour = 0x00ffff
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.message.channel.send(embed=emb)

    @manbot.command(name='avatar',
                    description="Changes the bots avatar!",
                    brief="Changes the bots avatar!",
                    aliases=['Avatar'])
    async def avatar(self, ctx, msg):
        self.aiosession = aiohttp.ClientSession(loop=self.bot.loop)
        emb = discord.Embed()
        emb.title = "Avatar Changed!"
        emb.colour = 0x00ff00
        picture = msg.strip('<>')
        emb.set_thumbnail(url=msg)
        emb.description = "Avatar successfully changed to " + msg

        async with self.aiosession.get(picture) as res:
            await self.bot.user.edit(avatar=await res.read())
            await ctx.message.channel.send(embed=emb)

    @manbot.command(name='username',
                    description="Changes the bots username!",
                    brief="Changes the bots username!",
                    aliases=['Username'])
    async def username(self, ctx, msg):
        emb = discord.Embed()
        emb.title = "Username Changed!"
        emb.colour = 0x00ff00
        emb.set_thumbnail(url=self.bot.user.avatar_url)
        emb.description = "Username successfully changed to " + msg
        await self.bot.user.edit(username=msg)
        await ctx.message.channel.send(embed=emb)

    @manbot.command(name='die',
                    description="Shuts down the bot, or restarts it while under pm2.",
                    brief="Shuts down the bot",
                    aliases=['sd', 'shutdown'])
    async def die(self, ctx):
        print(str(ctx.message.author) + " triggered a shutdown!")
        await ctx.message.channel.send(embed=discord.Embed(description=self.bot.user.name + " is now shutting down... " + ctx.message.author.mention, color=0x0035ff))
        await self.bot.logout()

#    Update command, to be fixed, as of now goes based on the old module system and won't function correctly.
#    @manbot.command(name='update',
#                description="Update the bot through git.",
#                brief="Update the bot through git.")
#    async def update(self, ctx):
#        process = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)
#        out, err = process.communicate()
#        emb = discord.Embed()
#        emb.title = "Bot Updater"
#        emb.colour = 0x00aaff
#        msg = ''
#        for cog in config.Modules:
#                try:
#                    self.bot.unload_extension(cog)
#                    self.bot.load_extension(cog)
#                    msg += '+Successfully reloaded mod {0}\n\n'.format(cog)
#                except Exception as e:
#                    msg += '-Error reloading mod {0}\n-{1}: {2}\n\n'.format(cog, type(e).__name__, e)
#        emb.description = "Bot has updated to the latest commit in repository.\nAll mods in `config.py` have attempted to be reloaded.\nIt is advised that you restart if anything outside the mods folder was updated."
#        emb.add_field(name="Cog Loader", value="```diff\n{}```".format(msg), inline=False)
#        if len(out.decode('utf8')) <= 500:
#            emb.add_field(name="Update Output", value="```http\n{}```".format(out.decode('utf8')), inline=False)
#        else:
#            emb.add_field(name="Update Output", value="```md\n#Output longer than 500 chars, see text file for output.```", inline=False)
#        print("Bot has updated to the latest commit in repository.\nAll mods in `config.py` have attempted to be reloaded.\nIt is advised that you restart if anything outside the mods folder was updated.")
#        print(msg)
#        print(out.decode('utf8'))
#        with open("output.txt","w+") as f:
#            f.write(out.decode('utf8'))
#        await ctx.message.channel.send(embed=emb)
#        if len(out.decode('utf8')) >=500:
#            await ctx.message.channel.send(file=discord.File('output.txt'))
#        os.remove('output.txt')


def setup(bot):
    bot.add_cog(BotOptions(bot))
