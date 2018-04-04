from collections import OrderedDict
from bot import bot

class CogMeta(type):
    def __prepare__(cls, *args, **kwargs):
        # Use an OrderedDict for the class body.
        return OrderedDict()

class Cog(metaclass=CogMeta):
    def __init__(self, bot:bot):
        self._bot = bot

    @property
    def bot(self):
        return self._bot

    @classmethod
    def setup(cls, bot:bot):
        bot.add_cog(cls(bot))