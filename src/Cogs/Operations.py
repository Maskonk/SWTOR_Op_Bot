from discord.ext.commands import Cog, context, command
from discord.ext import commands
from datetime import datetime
from json import load, dump


class Operations(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.operations = {"s&v": "Scum and Villainy", "tfb": "Terror From Beyond", "kp": "Karagga's Palace",
                           "ev": "Eternity Vault", "ec": "Explosive Conflict", "df": "Dread Fortress",
                           "dp": "Dread Palace", "dxun": "Dxun", "gftm": "Gods from the Machine",
                           "tc": "Toborro's Courtyard", "cm": "Colossal Monolith", "gq": "Geonosian Queen",
                           "wb": "World Boss", "gf": "Group finder", "other": "Other activity", "eyeless": "Eyeless",
                           "xeno": "Xenoanalyst"}
        with open('./Ops.json', 'r') as f:
            self.ops = load(f)

    @command(aliases=["ops", "operations", "list"])
    async def list_all_operations(self, ctx):
        """
        Lists all operations currently stored.
        """
        ops = self.ops.get(str(ctx.guild.id))
        if not ops:
            await ctx.send("There are currently no active operations listed for this server.")
            return
        msg = "The Operations I currently have listed are: \n"
        for op in ops:
            # owner = ctx.guild.get_member(ops[op]['Owner'])
            msg += f"{op}: {ops[op]['Operation']} {ops[op]['Size']}m {ops[op]['Difficulty']} " \
                   f"at {ops[op]['Time']} on {ops[op]['Date']} organiser {ops[op]['Owner']}\n"
        message = await ctx.send(msg)
        await ctx.message.delete(delay=30)
        await message.delete(delay=30)

    @command(aliases=["op", "operation", "show"])
    async def list_operation(self, ctx, op_number: int):
        """
        List a spefic operation
        :param op_number: The id of the operation.
        """
        await ctx.message.delete()
        if str(op_number) not in self.ops.get(str(ctx.guild.id)).keys():
            message = await ctx.send("There is no operation with that number.")
            await message.delete(delay=10)
            return

        op = self.ops.get(str(ctx.guild.id)).get(str(op_number))
        dt = datetime.strptime(f"{op['Date']} {op['Time']}", "%d/%m/%y %H:%M")
        msg = await self.make_operation_message(ctx, dt, op, op_number)

        message = await ctx.send(msg)
        await message.delete(delay=10)

    @command(aliases=["new", "new_op", "create", "c"])
    async def new_operation(self, ctx, operation: str, difficulty: str, size: int, date: str, time: str):
        """
        Create a new operation.
        :param operation: The operation to be created.
        :param difficulty: The difficulty of the operation.
        :param size: The size of the operation.
        :param date: The date of the operation.
        :param time: The start time of the operation.
        """
        if not await self.validate_operation_input(operation):
            await ctx.send("That is not a valid operation.")
            return

        if not await self.validate_time_input(date, time):
            message = await ctx.send("That date has already passed.")
            await message.delete(delay=10)
            return

        op_id = int(list(self.ops.get(str(ctx.guild.id), {0: None}).keys())[-1]) + 1
        op = {"Operation": operation,
              "Size": size,
              "Difficulty": difficulty,
              "Date": date,
              "Time": time,
              "Owner": ctx.author.nick,
              "Post_id": None,
              "Open": True,
              "Signed": 0,
              "Sign-ups": {
                "Tank": [],
                "Dps": [],
                "Healer": [],
                "Reserve": [],
                "Alternate_Tank": [],
                "Alternate_Dps": [],
                "Alternate_Healer": []
            }}

        dt = datetime.strptime(f"{date} {time}", "%d/%m/%y %H:%M")
        msg = await self.make_operation_message(ctx, dt, op, op_id)
        message = await ctx.send(msg)
        op["Post_id"] = message.id
        self.ops[str(ctx.guild.id)] = self.ops.get(str(ctx.guild.id), {})
        self.ops[str(ctx.guild.id)][op_id] = op
        print(self.ops)
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    @command(aliases=["sign", "join"])
    async def sign_up(self, ctx: context, op_number: str, main_role: str, secondary_role: str = None):
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if secondary_role:
            name = f"{ctx.author.nick} ({secondary_role.capitalize()})"
            op["Sign-ups"][f"Alternate_{secondary_role.capitalize()}"] += [ctx.author.nick]
        else:
            name = ctx.author.nick

        op["Sign-ups"][main_role.capitalize()] += [name]
        op["Signed"] += 1
        self.ops[str(ctx.guild.id)][str(op_number)] = op
        print(self.ops)
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    @staticmethod
    async def make_operation_message(ctx: context, dt: datetime, op: dict, op_id: int):
        """
        Composes operation message.
        :param dt: The Datetime of the operation
        :param op: The operation dictionary.
        :param op_id: The id of the operation.
        """
        msg = f"{op['Size']}m {op['Operation']} {op['Difficulty']} on {dt.date().day}/{dt.date().month}/{dt.date().year} " \
              f"starting at {dt.time().hour}:{dt.time().minute} CEST.\nCurrent signups:\nTanks: "
        for tank in op['Sign-ups']['Tank']:
            msg += f"{tank}, "
        msg += "\nHealers: "
        for heal in op['Sign-ups']['Healer']:
            msg += f"{heal}, "
        msg += "\nDPS: "
        for dps in op['Sign-ups']['Dps']:
            msg += f"{dps}, "
        msg += "\nReserves: "
        for res in op['Sign-ups']['Reserve']:
            msg += f"{res}, "
        msg += f"\nTo sign up use -sign {op_id}"
        return msg

    async def validate_operation_input(self, op: str):
        return op.lower() in self.operations.keys() or op.lower() in self.operations.values()

    async def validate_time_input(self, date: str, time: str):
        dt = datetime.strptime(f"{date} {time}", "%d/%m/%y %H:%M")
        if dt < datetime.today():
            return False
        else:
            return True
