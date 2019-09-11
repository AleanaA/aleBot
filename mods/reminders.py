'''
Script for reminders, all credit for this script goes to Twentysix26
https://github.com/Twentysix26/26-Cogs/blob/master/remindme/remindme.py
'''
import discord
import datetime
from datetime import date
from discord.ext import commands
from utils.dataIO import fileIO
import os
import asyncio
import time
import logging
import utils
from utils.embed import Embeds

class RemindMe(commands.Cog):
    """Never forget anything anymore."""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = fileIO("data/reminders.json", "load")
        self.units = {"second" : 1,"minute": 60, "hour": 3600, "day": 86400, "week": 604800, "month": 2592000, "year": 31104000}

    @commands.command(pass_context=True)
    async def remind(self, ctx, who : str, quantity : int, time_unit : str, *, text : str):
        """Sends you <text> when the time is up
        Accepts: minutes, hours, days, weeks, month
        Example:
        remind me 3 days Have sushi with Asu and JennJenn"""
        time_unit = time_unit.lower()
        author = ctx.message.author
        s = ""
        if who:
            if who == 'me':
                who = author
        if not who:
            who = author
            
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await ctx.send("Invalid time unit. Choose seconds/minutes/hours/days/weeks/months/years")
            return
        if quantity < 1:
            await ctx.send("Quantity must not be 0 or negative.")
            return
        if len(text) > 1960:
            await ctx.send("Text is too long.")
            return
        seconds = self.units[time_unit] * quantity
        future = int(time.time()+seconds)
        time_now = datetime.datetime.now()
        self.reminders.append({"WHO_ID" : who.id, "AUTHOR" : author.id, "FUTURE" : future, "TEXT" : text, "SET" : time_now.strftime("%d/%m/%Y, %I:%M:%S%p")})
        logger.info("{} ({}) set a reminder for {} ({}).".format(author.name, author.id, who.name, who.id))
        await ctx.send("I will remind {} of that in {} {}.".format(who.name, str(quantity), time_unit + s))
        fileIO("data/reminders.json", "save", self.reminders)

    @commands.command(pass_context=True)
    async def unremind(self, ctx, target: int=None):
        """Removes all your upcoming notifications, or one."""
        author = ctx.message.author
        to_remove = []
        if target:
            for a, reminder in enumerate(self.reminders, 1):
                if target == a and reminder["AUTHOR"] == ctx.message.author.id:
                    to_remove.append(reminder)
        else:
            for reminder in self.reminders:
                if reminder["AUTHOR"] == ctx.message.author.id:
                    to_remove.append(reminder)

        if not to_remove == []:
            for reminder in to_remove:
                self.reminders.remove(reminder)
            fileIO("data/reminders.json", "save", self.reminders)
            if not target:
                await ctx.send("All your notifications have been removed.")
            else:
                await ctx.send("{} has been removed from your reminders".format(target))
        else:
            await ctx.send("You don't have any upcoming notification.")

    @commands.command(pass_context=True)
    async def reminders(self, ctx, who: discord.User=None):
        """List all your upcoming reminders"""
        author = ctx.message.author
        reminders = []

        for reminder in self.reminders:
            if who == None:
                if reminder["AUTHOR"] == author.id:
                    reminders.append(reminder)
            else:
                if reminder["WHO_ID"] == who.id:
                    reminders.append(reminder)


        if not reminders:
            if not who:
                emb = Embeds.create_embed(self, ctx, 'Reminders', 0xe74c3c, 'You have no upcoming reminders!')
            else:
                emb = Embeds.create_embed(self, ctx, 'No upcoming rmeinders for {}'.format(who.name), 0xe74c3c, 'You have no upcoming reminders!')
        else:
            if not who:
                emb = discord.Embed(title='Reminders', colour=0x206694)
                for a, b in enumerate(reminders, 1):
                    emb.add_field(name="#{}".format(a), value='{}\nset {}'.format(b["TEXT"], b["SET"]), inline=False)
            else:
                emb = discord.Embed(title='Reminders for {}'.format(who.name), colour=0x206694)
                for a, b in enumerate(reminders, 1):
                    emb.add_field(name="#{}".format(a), value='{}\nset {} by {}'.format(b["TEXT"], b["SET"], b["AUTHOR"]), inline=False)


        await ctx.send(embed=emb)
        
    async def check_reminders(self):
        while self is self.bot.get_cog("RemindMe"):
            to_remove = []
            for reminder in self.reminders:
                if reminder["FUTURE"] <= int(time.time()):
                    try:
                        user = self.bot.get_user(reminder["WHO_ID"])
                        author = self.bot.get_user(reminder["AUTHOR"])
                        if reminder["WHO_ID"] == reminder["AUTHOR"]:
                            await user.send("You asked me to remind you of this:\n{}".format(reminder["TEXT"]))
                        else:
                            await user.send("{} asked me to remind you of this:\n{}".format(author.name, reminder["TEXT"]))
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(reminder)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(reminder)
            for reminder in to_remove:
                self.reminders.remove(reminder)
            if to_remove:
                fileIO("data/reminders.json", "save", self.reminders)
            await asyncio.sleep(5)

def check_folders():
    if not os.path.exists("data"):
        print("Creating data folder...")
        os.makedirs("data")

def check_files():
    f = "data/reminders.json"
    if not fileIO(f, "check"):
        print("Creating empty reminders.json...")
        fileIO(f, "save", [])

def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("remindme")
    if logger.level == 0: # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='data/reminders.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    n = RemindMe(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.check_reminders())
    bot.add_cog(n)
