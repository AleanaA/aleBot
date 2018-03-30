from collections import OrderedDict
from rooBot import rooBot

class CogMeta(type):
    def __prepare__(cls, *args, **kwargs):
        # Use an OrderedDict for the class body.
        return OrderedDict()

class Cog(metaclass=CogMeta):
    def __init__(self, bot:rooBot):
        self._bot = bot

    @property
    def bot(self):
        return self._bot

    @classmethod
    def setup(cls, bot:rooBot):
        bot.add_cog(cls(bot))