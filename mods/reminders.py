'''
Script for reminders, all credit for this script goes to Twentysix26
https://github.com/Twentysix26/26-Cogs/blob/master/remindme/remindme.py
'''
import discord
from discord.ext import commands
from utils.dataIO import fileIO
import os
import asyncio
import time
import logging

class RemindMe:
    """Never forget anything anymore."""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = fileIO("data/reminders.json", "load")
        self.units = {"second" : 1,"minute": 60, "hour": 3600, "day": 86400, "week": 604800, "month": 2592000, "year": 31104000}

    @commands.command(pass_context=True)
    async def remind(self, ctx, who : discord.User, quantity : int, time_unit : str, *, text : str):
        """Sends you <text> when the time is up
        Accepts: minutes, hours, days, weeks, month
        Example:
        [p]remindme 3 days Have sushi with Asu and JennJenn"""
        time_unit = time_unit.lower()
        author = ctx.message.author
        s = ""
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
        self.reminders.append({"ID" : who.id, "AUTHOR" : author.id, "FUTURE" : future, "TEXT" : text})
        logger.info("{} ({}) set a reminder for {} ({}).".format(author.name, author.id, who.name, who.id))
        await ctx.send("I will remind {} of that in {} {}.".format(who.name, str(quantity), time_unit + s))
        fileIO("data/reminders.json", "save", self.reminders)

    @commands.command(pass_context=True)
    async def forgetme(self, ctx):
        """Removes all your upcoming notifications"""
        author = ctx.message.author
        to_remove = []
        for reminder in self.reminders:
            if reminder["ID"] == author.id:
                to_remove.append(reminder)

        if not to_remove == []:
            for reminder in to_remove:
                self.reminders.remove(reminder)
            fileIO("data/reminders.json", "save", self.reminders)
            await ctx.send("All your notifications have been removed.")
        else:
            await ctx.send("You don't have any upcoming notification.")

    async def check_reminders(self):
        while self is self.bot.get_cog("RemindMe"):
            to_remove = []
            for reminder in self.reminders:
                if reminder["FUTURE"] <= int(time.time()):
                    try:
                        user = await self.bot.get_user_info(reminder["ID"])
                        author = await self.bot.get_user_info(reminder["AUTHOR"])
                        if reminder["ID"] == reminder["AUTHOR"]:
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