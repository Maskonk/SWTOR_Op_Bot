from discord.ext.commands import Cog
from discord.ext import commands
from json import load


class Operations(Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('src/Ops.json', 'r') as f:
            self.ops = load(f)

    @commands.command()
    async def list_ops(self, ctx):
        """Lists all operations currently stored."""
        msg = "The Operations I currently have listed are: \n"
        for op in self.ops:
            msg += f"{op}: {self.ops[op]['operation']} {self.ops[op]['size']}m {self.ops[op]['difficulty']} " \
                   f"at {self.ops[op]['time']} on {self.ops[op]['date']}"
        await ctx.send(msg)

