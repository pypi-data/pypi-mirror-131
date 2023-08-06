from typing import Union
from inspect import getmembers

class Cogs:
    @staticmethod
    def listener(cls, name:str):
        def deco(coro):
            coro._cog_listener = name
            return coro
        return deco

    def setup(self, bot):
        for n, coro in getmembers(self):
            if hasattr(coro, "_cog_listener"):
                bot.add_listener(coro, coro._cog_listener)
