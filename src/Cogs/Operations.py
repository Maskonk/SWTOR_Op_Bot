from discord.ext.commands import Cog, context, command, check
from discord.ext import commands
from datetime import datetime
from json import load, dump


# TODO: Role validation
class Operations(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.operations = {"s&v": "Scum and Villainy", "tfb": "Terror From Beyond", "kp": "Karagga's Palace",
                           "ev": "Eternity Vault", "ec": "Explosive Conflict", "df": "Dread Fortress",
                           "dp": "Dread Palace", "dxun": "Dxun", "gftm": "Gods from the Machine",
                           "tc": "Toborro's Courtyard", "cm": "Colossal Monolith", "gq": "Geonosian Queen",
                           "wb": "World Boss", "gf": "Group finder", "other": "Other activity", "eyeless": "Eyeless",
                           "xeno": "Xenoanalyst", "rav": "Ravagers", "tos": "Temple of Sacrifice"}
        self.sizes = {4: [1, 1, 1], 8: [2, 4, 2], 16: [2, 10, 4]}
        with open('./Ops.json', 'r') as f:
            self.ops = load(f)

    @command(aliases=["ops", "operations", "list"])
    async def list_all_operations(self, ctx) -> None:
        """
        Lists all operations currently stored for the server.
        """
        ops = self.ops.get(str(ctx.guild.id))
        if not ops:
            await ctx.send("There are currently no active operations listed for this server.")
            return
        msg = "The Operations I currently have listed are: \n"
        for op in ops:
            msg += f"{op}: {ops[op]['Operation'].upper()} {ops[op]['Size']}m {ops[op]['Difficulty']} " \
                   f"at {ops[op]['Time']} on {ops[op]['Date']} organiser {ops[op]['Owner_name']}\n"
        message = await ctx.send(msg)
        await ctx.message.delete(delay=30)
        await message.delete(delay=30)

    @command(aliases=["op", "operation", "show"])
    async def list_operation(self, ctx, op_number: int) -> None:
        """
        List a spefic operations details.
        :param op_number: The id of the operation.
        """
        await ctx.message.delete()
        if str(op_number) not in self.ops.get(str(ctx.guild.id)).keys():
            message = await ctx.send("There is no operation with that number.")
            await message.delete(delay=10)
            return

        op = self.ops.get(str(ctx.guild.id)).get(str(op_number))
        dt = datetime.strptime(f"{op['Date']} {op['Time']}", "%d/%m/%y %H:%M")
        msg = await self.make_operation_message(dt, op, str(op_number))

        message = await ctx.send(msg)
        await message.delete(delay=10)

    @command(aliases=["new", "new_op", "create", "c"])
    async def new_operation(self, ctx, operation: str, difficulty: str, size: int, date: str, time: str) -> None:
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

        if not await self.validate_difficulty_input(difficulty):
            message = await ctx.send("That is not a valid difficulty.")
            await message.delete(delay=10)
            return

        if not await self.validate_size_input(size):
            message = await ctx.send("That is not a valid size.")
            await message.delete(delay=10)
            return

        op_id = int(list(self.ops.get(str(ctx.guild.id), {0: None}).keys())[-1]) + 1
        op = {"Operation": operation,
              "Size": size,
              "Difficulty": difficulty,
              "Date": date,
              "Time": time,
              "Owner_name": ctx.author.display_name,
              "Owner_id": ctx.author.id,
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
        msg = await self.make_operation_message(dt, op, str(op_id))
        message = await ctx.send(msg)

        try:
            await message.pin()
        except Exception as e:
            print(e)

        op["Post_id"] = message.id
        self.ops[str(ctx.guild.id)] = self.ops.get(str(ctx.guild.id), {})
        self.ops[str(ctx.guild.id)][op_id] = op
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    @command(aliases=["sign", "join"])
    async def sign_up(self, ctx: context, op_number: str, main_role: str, alt_role: str = None) -> None:
        """
        Signup to a given operation with the given roles.
        :param op_number: The operation id to sign up to.
        :param main_role: The main role to sign up as.
        :param alt_role: Optional alternative role to sign up as.
        """
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if await self.check_duplicate(op, ctx.author.display_name):
            if not await self.check_role_change(op, ctx.author.display_name, main_role, alt_role):
                await ctx.send("You have already signed-up for that operation.")
                return
            else:
                op = await self.remove_signup(op, ctx.author.display_name)

        if alt_role:
            name = f"{ctx.author.display_name} ({alt_role.capitalize()})"
            op["Sign-ups"][f"Alternate_{alt_role.capitalize()}"] += [ctx.author.display_name]
        else:
            name = ctx.author.display_name

        op["Sign-ups"][main_role.capitalize()] += [name]
        op["Signed"] += 1

        await self.edit_pinned_message(ctx, op, op_number)

        self.ops[str(ctx.guild.id)][str(op_number)] = op
        print(self.ops)
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    @command(aliases=["unsign", "quit", "ihateyouall"])
    async def unsign_up(self, ctx: context, op_number: str) -> None:
        """
        Remove sign up from the given operation.
        :param op_number: The operation id to remove sign up from.
        """
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if not await self.check_duplicate(op, ctx.author.display_name):
            await ctx.send("You are not currently signed up to that operation.")
            return

        op = await self.remove_signup(op, ctx.author.display_name)
        await self.edit_pinned_message(ctx, op, op_number)

        self.ops[str(ctx.guild.id)][str(op_number)] = op
        print(self.ops)
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    @command(aliases=["update"])
    async def update_operation(self, ctx: context, op_number: str, attribute: str, value: str) -> None:
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not await self.is_owner_or_admin(ctx, op):
            await ctx.send("You are not authorised to use this command.")
            return

        if attribute.capitalize() not in ["Operation", "Date", "Time", "Size", "Difficulty"]:
            await ctx.send("That is not a valid attribute to update.")


        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if attribute.capitalize() == "Operation":
            if not await self.validate_operation_input(value):
                await ctx.send("That is not a valid operation.")
                return
        elif attribute.capitalize() == "Date":
            if not await self.validate_time_input(value, op["Time"]):
                message = await ctx.send("That date has already passed.")
                await message.delete(delay=10)
                return
        elif attribute.capitalize() == "Time":
            if not await self.validate_time_input(op["Date"], value):
                message = await ctx.send("That date has already passed.")
                await message.delete(delay=10)
                return
        elif attribute.capitalize() == "Difficulty":
            if not await self.validate_difficulty_input(value):
                message = await ctx.send("That is not a valid difficulty.")
                await message.delete(delay=10)
                return
        elif attribute.capitalize() == "Size":
            if not await self.validate_size_input(int(value)):
                message = await ctx.send("That is not a valid size.")
                await message.delete(delay=10)
                return

        op[attribute.capitalize()] = value

        await self.edit_pinned_message(ctx, op, op_number)

        self.ops[str(ctx.guild.id)][str(op_number)] = op
        print(self.ops)
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    async def validate_operation_input(self, op: str) -> bool:
        """
        Checks the users input to ensure the operation input is valid.
        :param op: The Operation input by the user.
        :return: Booleon True if the operation input is valid.
        """
        return op.lower() in self.operations.keys() or op.lower() in self.operations.values()

    @staticmethod
    async def check_duplicate(op: dict, user_nick: str) -> bool:
        """
        Checks if the user is already signed up to the given operation.
        :param op: The operation details dictionary.
        :param user_nick: The users nickname
        :return: Booleon True if the user is already signed up to the operation.
        """
        sign_ups = op["Sign-ups"]["Tank"] + op["Sign-ups"]["Dps"] + op["Sign-ups"]["Healer"]
        for sign in sign_ups:
            if user_nick in sign:
                return True
        return False

    @staticmethod
    async def check_role_change(op: dict, user_nick: str, main_role: str, alt_role: str) -> bool:
        """
        Checks if the user has changed their role.
        :param op: The operation details dictionary.
        :param user_nick: The users nickname
        :param main_role: The new main role of the user.
        :param alt_role: The optional alternative role of the user.
        :return: Booleon True if the user has changed one of both of the roles they are signing up as.
        """
        alt_change = False
        main_change = False
        for user in op["Sign-ups"][main_role.capitalize()]:
            if user_nick in user:
                break
        else:
            main_change = True

        if alt_role:
            if user_nick not in op["Sign-ups"][f"Alternate_{alt_role.capitalize()}"]:
                alt_change = True

        return main_change or alt_change

    @staticmethod
    async def remove_signup(op: dict, user_nick) -> dict:
        for role in ["Tank", "Healer", "Dps"]:
            for i, user in enumerate(op["Sign-ups"][role]):
                if user_nick in user:
                    op["Sign-ups"][role].pop(i)
            if user_nick in op["Sign-ups"][f"Alternate_{role}"]:
                op["Sign-ups"][f"Alternate_{role}"].remove(user_nick)
        return op

    @staticmethod
    async def validate_time_input(date: str, time: str) -> bool:
        """
        Checks the users input to ensure the date and time inputs are valid and not yet passed.
        :param date: The Date input by the user.
        :param time: The Time input by the user.
        :return: Booleon True if the date and time inputs are valid.
        """
        dt = datetime.strptime(f"{date} {time}", "%d/%m/%y %H:%M")
        if dt < datetime.today():
            return False
        else:
            return True

    async def make_operation_message(self, dt: datetime, op: dict, op_id: str) -> str:
        """
        Composes operation message.
        :param dt: The Datetime object of the operation
        :param op: The operation details dictionary.
        :param op_id: The id of the operation.
        :return: String of the message to send composed of the operations details.
        """
        operation_name = self.operations[op['Operation'].lower()]
        msg = f"{op['Size']}m {operation_name} {op['Difficulty'].capitalize()} on {dt.date().day}/{dt.date().month}/{dt.date().year} " \
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
        msg += f"\nTo sign up use -sign {op_id} <role> <alt role>"
        return msg

    @staticmethod
    async def validate_difficulty_input(difficulty: str) -> bool:
        """
        Checks the users input to ensure the difficulty input is valid.
        :param difficulty: The difficulty input by the user.
        :return: Booleon True if the difficulty input is valid.
        """
        return difficulty.lower() in ["sm", "hm", "nim", "na", "vm", "mm"]

    @staticmethod
    async def validate_size_input(size: int) -> bool:
        """
        Checks the users input to ensure the size input is valid.
        :param size: The size input by the user.
        :return: Booleon True if the size input is valid.
        """
        return size in [4, 8, 16, 24]

    async def edit_pinned_message(self, ctx: context, op: dict, op_number: str) -> None:
        """
        Edits the pinned message for the operation.
        :param op: The operation details dictionary.
        :param op_number: The operation id.
        """
        dt = datetime.strptime(f"{op['Date']} {op['Time']}", "%d/%m/%y %H:%M")
        msg = await self.make_operation_message(dt, op, op_number)

        message = await ctx.fetch_message(op["Post_id"])
        await message.edit(content=msg)

    @staticmethod
    async def is_owner_or_admin(ctx, op):
        return ctx.author.id in [op["Owner_id"], 1]
