from discord.ext.commands import Cog
from discord.ext import commands
from json import load


class Operations(Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('./Ops.json', 'r') as f:
            self.ops = load(f)

    @commands.command(aliases=["list", "operations"])
    async def list_all_operations(self, ctx):
        """Lists all operations currently stored."""
        msg = "The Operations I currently have listed are: \n"
        c = 1
        for op in self.ops:
            if self.ops[op]["guild"] == ctx.guild.id:
                guild = self.bot.get_guild(self.ops[op]["guild"])
                owner = guild.get_member(self.ops[op]['owner'])
                msg += f"{c}: {self.ops[op]['operation']} {self.ops[op]['size']}m {self.ops[op]['difficulty']} " \
                       f"at {self.ops[op]['time']} on {self.ops[op]['date']} organiser {owner.nick}\n"
                c += 1
        await ctx.send(msg)

    @commands.command()
    async def list_operation(self, ctx, op_number):
        pass