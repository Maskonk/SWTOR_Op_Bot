from discord.ext.commands import Cog, command, context

class Admin(Cog):
    def __init__(self, bot, ops):
        self.bot = bot
        self.ops = ops


