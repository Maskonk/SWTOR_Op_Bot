from discord.ext.commands import Cog
from discord.ext import commands
from json import load


class Operations(Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('src/Ops.json', 'r') as f:
            self.ops = load(f)

    @commands.command()
    async def list_ops(self):
        """Lists all operations currently stored."""
        for op in self.ops:
            pass

