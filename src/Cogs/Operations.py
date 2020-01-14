from discord.ext.commands import Cog
from discord.ext import commands
from datetime import datetime
from json import load


class Operations(Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('./Ops.json', 'r') as f:
            self.ops = load(f)

    @commands.command(aliases=["ops", "operations", "list"])
    async def list_all_operations(self, ctx):
        """Lists all operations currently stored."""
        msg = "The Operations I currently have listed are: \n"
        for op in self.ops:
            if self.ops[op]["guild"] == ctx.guild.id:
                guild = self.bot.get_guild(self.ops[op]["guild"])
                owner = guild.get_member(self.ops[op]['owner'])
                msg += f"{op}: {self.ops[op]['operation']} {self.ops[op]['size']}m {self.ops[op]['difficulty']} " \
                       f"at {self.ops[op]['time']} on {self.ops[op]['date']} organiser {owner.nick}\n"
        message = await ctx.send(msg)
        await ctx.message.delete(delay=30)
        await message.delete(delay=30)

    @commands.command(aliases=["op", "operation", "show"])
    async def list_operation(self, ctx, op_number):
        await ctx.message.delete()
        if op_number not in self.ops.keys():
            message = await ctx.send("There is no operation with that number.")
            await message.delete(delay=10)
            return
        if self.ops[op_number]["guild"] != ctx.guild.id:
            message = await ctx.send("That operation does not belong to this guild.")
            await message.delete(delay=10)
            return

        op = self.ops[op_number]
        dt = datetime.strptime(f"{op['date']} {op['time']}", "%m/%d/%y %H:%M")
        if dt < datetime.today():
            message = await ctx.send("That operation has already passed.")
            await message.delete(delay=10)
            return
        msg = f"{op['size']}m {op['operation']} {op['difficulty']} on {dt.date().day}/{dt.date().month}/{dt.date().year} " \
              f"starting at {dt.time().hour}:{dt.time().minute}\nCurrent signups:\nTanks: "
        guild = self.bot.get_guild(op["guild"])
        for tank in op['members']['tanks']:
            t = guild.get_member(tank)
            msg += f"{t.nick}, "
        msg += "\nHealers: "
        for heal in op['members']['healers']:
            h = guild.get_member(heal)
            msg += f"{h.nick}, "
        msg += "\nDPS: "
        for d in op['members']['dps']:
            h = guild.get_member(d)
            msg += f"{h.nick}, "
        msg += f"\nTo sign up see this post: {op['link']}"

        await ctx.send(msg)
