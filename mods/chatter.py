import asyncio
import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils.cog import Cog
from utils.embed import Embeds
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import UbuntuCorpusTrainer

class Chatbot(Cog):
    def __init__(self, *args, **kwargs):
        self.chatbot = ChatBot('aleBot')
        self.chatbot.set_trainer(UbuntuCorpusTrainer)
        self.chatbot.train()

    async def on_message(self, ctx):
        if ctx.message.author.id == 168118999337402368:
            response = self.chatbot.get_response(ctx.message.content)
            await ctx.send(response)

def setup(bot):
    bot.add_cog(Chatbot(bot))