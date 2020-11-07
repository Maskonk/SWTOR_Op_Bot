from discord.ext.commands import Cog, context, command, errors
from discord.utils import get
from datetime import datetime
from json import load, dump
from dateutil.parser import parse
from calendar import month_name, day_name
from random import choice
from Utils.Errors import SignUpError
from Utils.ReactionUtils import check_valid_reaction
from re import sub


class Operations(Cog):
    def __init__(self, bot, ops):
        self.bot = bot
        self.operations = {"s&v": "Scum and Villainy", "tfb": "Terror From Beyond", "kp": "Karagga's Palace",
                           "ev": "Eternity Vault", "ec": "Explosive Conflict", "df": "Dread Fortress",
                           "dp": "Dread Palace", "dxun": "Dxun", "gftm": "Gods from the Machine",
                           "tc": "Toborro's Courtyard", "cm": "Colossal Monolith", "gq": "Geonosian Queen",
                           "wb": "World Boss", "gf": "Group finder", "other": "Other activity", "eyeless": "Eyeless",
                           "xeno": "Xenoanalyst", "rav": "Ravagers", "tos": "Temple of Sacrifice"}
        self.sizes = sizes = {"1": {"Tank": 0, "Dps": 1, "Healer": 0}, "4": {"Tank": 1, "Dps": 1, "Healer": 1},
                              "8": {"Tank": 2, "Dps": 4, "Healer": 2}, "16": {"Tank": 2, "Dps": 10, "Healer": 4},
                              "1t5d": {"Tank": 1, "Dps": 5, "Healer": 2}, "1h5d": {"Tank": 2, "Dps": 5, "Healer": 1},
                              "6d": {"Tank": 1, "Dps": 6, "Healer": 1}, "24": {"Tank": 3, "Dps": 15, "Healer": 6}}
        self.difficulties = {"sm": "Story Mode", "hm": "Veteran Mode", "nim": "Master Mode", "vm": "Veteran mode",
                             "mm": "Master Mode"}
        self.ops = ops

    @command(aliases=["ops", "operations", "list"])
    async def list_all_operations(self, ctx: context) -> None:
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
    async def list_operation(self, ctx: context, op_number: int) -> None:
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
        dt = await self.parse_date(op["Date"], op["Time"])
        msg = await self.make_operation_message(dt, op, str(op_number))

        message = await ctx.send(msg)
        await message.delete(delay=10)

    @command(aliases=["new", "new_op", "create", "c"])
    async def new_operation(self, ctx: context, operation: str, difficulty: str, side: str, size: str,
                            date: str, time: str, *notes) -> None:
        """
        Create a new operation.
        :param operation: The operation to be created.
        :param difficulty: The difficulty of the operation.
        :param side: The side the operation is to take place.
        :param size: The size of the operation.
        :param date: The date of the operation.
        :param time: The start time of the operation.
        :param notes: Any notes for the operation.
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

        if not await self.validate_side_input(side):
            message = await ctx.send("That is not a valid side.")
            await message.delete(delay=10)
            return

        if not notes:
            notes = ""
        else:
            notes = " ".join(notes)

        op_keys = list(self.ops.get(str(ctx.guild.id), {0: None}).keys())
        if op_keys:
            op_id = int(op_keys[-1]) + 1
        else:
            op_id = 1

        if operation.lower() == "random":
            operation = await self.get_random_operation()
            while operation in ["wb", "gf", "other"]:
                operation = await self.get_random_operation()

        op = {"Operation": operation,
              "Size": size,
              "Difficulty": difficulty,
              "Side": side,
              "Date": date,
              "Time": time,
              "Notes": notes,
              "Owner_name": ctx.author.display_name,
              "Owner_id": ctx.author.id,
              "Post_id": None,
              "Channel_id": ctx.channel.id,
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

        dt = await self.parse_date(date, time)
        msg = await self.make_operation_message(dt, op, str(op_id))
        message = await ctx.send(msg)

        try:
            await message.pin()
        except Exception as e:
            print(e)

        op["Post_id"] = message.id
        self.ops[str(ctx.guild.id)] = self.ops.get(str(ctx.guild.id), {})
        self.ops[str(ctx.guild.id)][str(op_id)] = op
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
        r = await self.add_to_operation(op, op_number, ctx.guild.id, ctx.author.display_name, main_role, alt_role)
        if r:
            await ctx.message.add_reaction('\U0001f44d')

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
        await self.write_operation(op, op_number, ctx.guild.id,)

        await ctx.message.add_reaction('\U0001f44d')

    @command(aliases=["update"])
    async def update_operation(self, ctx: context, op_number: str, attribute: str, *value: str) -> None:
        """
        Updates the given attribute for the operation. Restricted to the creator or an admin.
        :param op_number: The operation id.
        :param attribute: Attribute to change.
        :param value: The new value of the attribute.
        """
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if not await self.is_owner_or_admin(ctx, op):
            await ctx.send("You are not authorised to use this command. Only an Admin or the person who created "
                           "this operation may update it.")
            return

        if attribute.capitalize() not in ["Operation", "Date", "Time", "Size", "Difficulty", "Side", "Notes"]:
            await ctx.send("That is not a valid attribute to update.")

        if not value and attribute.capitalize() != "Notes":
            await ctx.send("You have not supplied a value to update to.")
            return
        elif attribute.capitalize() == "Notes" and not value:
            value = ""
        elif attribute.capitalize() == "Notes":
            value = " ".join(value)
        else:
            value = value[0]

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
        elif attribute.capitalize() == "Side":
            if not await self.validate_side_input(value):
                message = await ctx.send("That is not a valid side.")
                await message.delete(delay=10)
                return

        op[attribute.capitalize()] = value

        await self.write_operation(op, op_number, ctx.guild.id)
        await ctx.message.add_reaction('\U0001f44d')

    @command(aliases=["delete"])
    async def delete_operation(self, ctx: context, op_number: str) -> None:
        """
        Deletes a given operation. Restricted to the creator or an admin.
        :param op_number: The operation id.
        """
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if not await self.is_owner_or_admin(ctx, op):
            await ctx.send("You are not authorised to use this command. Only an Admin or the person who created "
                           "this operation may update it.")
            return

        message = await ctx.fetch_message(op["Post_id"])
        await message.unpin()

        self.ops[str(ctx.guild.id)].pop(op_number)
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

        await ctx.message.add_reaction('\U0001f44d')

    @command(aliases=["remove"])
    async def remove_sign_up(self, ctx: context, op_number: str, name: str) -> None:
        """
        Removes the given name from the sign ups.
        :param op_number: The id of the operation.
        :param name: The name of the person to be removed.
        """
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if not await self.is_owner_or_admin(ctx, op):
            await ctx.send("You are not authorised to use this command. Only an Admin or the person who created "
                           "this operation may update it.")
            return

        op = await self.remove_signup(op, name)

        await self.write_operation(op, op_number, ctx.guild.id)

        await ctx.message.add_reaction('\U0001f44d')

    @command(aliases=["add"])
    async def add_sign_up(self, ctx: context, op_number: str, sign_up_name: str, main_role: str, alt_role=None) -> None:
        """
        Adds the given name to the sign ups.
        :param op_number: The id of the operation.
        :param sign_up_name: The name of the person to be added.
        :param main_role: The main role of the person to be added.
        :param alt_role: The alt role of the person to be added.
        """
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))

        r = await self.add_to_operation(op, op_number, ctx.guild.id, sign_up_name, main_role, alt_role)
        if r:
            await ctx.message.add_reaction('\U0001f44d')

    @command(aliases=["howto"])
    async def user_guide(self, ctx: context) -> None:
        """
        A basic user guide on how to use the bot.
        """
        msg = "**Basic user guide:**\n__Creating a new operation:__```-new <operation> <mode> <side> <size> <date> " \
              "<time>``` Will create a new operation, Example:```-new TFB MM Imp 8 22/10/20 19:00```" \
              "Will create a new 8m Terror From Beyond Master Mode Imperial side on the 22nd of October 2020 at 19:00 "\
              "CET. The operation is the short code not the full name.\n\n__Signing up__\nOnce an operation has been " \
              "created anyone can sign up using the following```-sign <operation number> <main role> " \
              "<alternative role>```Will add you to the sign ups for the operation. Alternative role is optional. " \
              "Example:```-sign 1 Tank DPS``` Will add you as a Tank and backup DPS to operation number one.\n\n" \
              "__Changing roles:__\nUsing the sign up command again with different roles will automatically change " \
              "the roles you are signed up as.\n\n__Removing your sign up__\n```-unsign <operation number>``` " \
              "Will remove your sign up from the operation."
        await ctx.send(msg)

    @command(aliases=["random"])
    async def random_operation(self, ctx: context):
        operation = await self.get_random_operation()
        await ctx.send(f"The random operation is: {operation}")

    async def validate_operation_input(self, op: str) -> bool:
        """
        Checks the users input to ensure the operation input is valid.
        :param op: The Operation input by the user.
        :return: Booleon True if the operation input is valid.
        """
        return op.lower() in self.operations.keys() or op.lower() in self.operations.values() or op.lower() == "random"

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
        for i, user in enumerate(op["Sign-ups"]["Reserve"]):
            if user_nick in user:
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

        if main_role == "Any":
            roles = ["Dps", "Tank", "Healer"]

            for role in roles:
                found = False
                for user in op["Sign-ups"][role]:
                    if user_nick + " (Any)" in user:
                        found = True
                        break
                if found:
                    return False
            else:
                return True

        else: 
            for user in op["Sign-ups"][main_role]:
                if user_nick in user:
                    break
            else:
                main_change = True

        if alt_role and alt_role != "Any":
            if user_nick not in op["Sign-ups"][f"Alternate_{alt_role}"]:
                alt_change = True
        elif not alt_role:
            roles = ["Tank", "Dps", "Healer"]
            for role in roles:
                if user_nick in op["Sign-ups"][f"Alternate_{role}"]:
                    alt_change = True
        return main_change or alt_change

    async def add_signup(self, op: dict, sign_up_name, main_role, alt_role: str = None) -> dict:
        """
        Adds a user with given name and roles to the given operation
        :param op: The operation to be updated.
        :param sign_up_name: The user's nick name.
        :param main_role: The main role of the user.
        :param alt_role: Optional alternative role of the user.
        :return: dict: The updated operation. 
        """
        if main_role == "Any":
            op = await self.add_any_signup(op, sign_up_name)
        elif alt_role == "Any":
            name = f"{sign_up_name} (Any)"
            op["Sign-ups"][main_role] += [name]

            alt_roles = ["Tank", "Healer", "Dps"]
            alt_roles.remove(main_role)

            for r in alt_roles:
                op["Sign-ups"][f"Alternate_{r}"] += [sign_up_name]
        else:
            if alt_role:
                name = f"{sign_up_name} ({alt_role})"
                if main_role != "Reserve":
                    op["Sign-ups"][f"Alternate_{alt_role}"] += [sign_up_name]
            else:
                name = sign_up_name

            op["Sign-ups"][main_role] += [name]
        op["Signed"] += 1
        return op

    async def add_any_signup(self, op: dict, sign_up_name) -> dict:
        """
        Adds a user with given name to any role as they are available (Dps > Healer > Tank)
        Note: No changes are made if all roles are full.
        :param op: The operation to be updated.
        :param sign_up_name: The user's nick name.
        :return: dict: The updated operation. 
        """
        roles = ["Dps", "Healer", "Tank"]
        name = f"{sign_up_name} (Any)"

        for role in roles:
            if (not await self.check_role_full(op, role)):
                roles.remove(role)
                op["Sign-ups"][role] += [name]

                for r in roles:
                    op["Sign-ups"][f"Alternate_{r}"] += [sign_up_name]
                return op

        # if it gets here -> all roles were full & nothing changed
        return op    

    @staticmethod
    async def remove_signup(op: dict, user_nick) -> dict:
        """
        Attempts to removes the user with given name from the operation.
        :param op: The operation to be updated.
        :param user_nick: The user's nick name.
        :return: dict: The updated operation. 
        """
        for role in ["Tank", "Healer", "Dps"]:
            for i, user in enumerate(op["Sign-ups"][role]):
                name = sub("\s\(\w+\)", "", user)
                if user_nick == name:
                    op["Sign-ups"][role].pop(i)
            if user_nick in op["Sign-ups"][f"Alternate_{role}"]:
                op["Sign-ups"][f"Alternate_{role}"].remove(user_nick)
        for i, user in enumerate(op["Sign-ups"]["Reserve"]):
            name = sub("\s\(\w+\)", "", user)
            if user_nick == name:
                op["Sign-ups"]["Reserve"].pop(i)
        op["Signed"] -= 1
        return op

    @staticmethod
    async def validate_time_input(date: str, time: str) -> bool:
        """
        Checks the users input to ensure the date and time inputs are valid and not yet passed.
        :param date: The Date input by the user.
        :param time: The Time input by the user.
        :return: Booleon True if the date and time inputs are valid.
        """
        dt = parse(f"{date} {time}")
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
        guild = self.bot.get_guild(750036082518917170)
        dps_emoji = get(guild.emojis, name='DPS')
        heal_emoji = get(guild.emojis, name='Healer')
        tank_emoji = get(guild.emojis, name='Tank')
        operation_name = self.operations[op['Operation'].lower()]
        difficulty = self.difficulties[op['Difficulty'].lower()]
        notes = op["Notes"]
        extension = await self.date_extention(dt.day)
        msg = f"{op_id}: {op['Size']}m {operation_name} {difficulty} {op['Side']}\n{day_name[dt.weekday()]} the " \
              f"{extension} of {month_name[dt.month]} " \
              f"starting at {dt.time().strftime('%H:%M')} CET."
        if notes:
            msg += f"\n({notes})\n"
        msg += f"Current signups:\n"
        for tank in op['Sign-ups']['Tank']:
            msg += f"\n{tank_emoji} - {tank}"
        for i in range(self.sizes[str(op['Size'])]["Tank"] - len(op['Sign-ups']['Tank'])):
            msg += f"\n{tank_emoji} - "
        for dps in op['Sign-ups']['Dps']:
            msg += f"\n{dps_emoji} - {dps}"
        for i in range(self.sizes[str(op['Size'])]["Dps"] - len(op['Sign-ups']['Dps'])):
            msg += f"\n{dps_emoji} - "
        for heal in op['Sign-ups']['Healer']:
            msg += f"\n{heal_emoji} - {heal}"
        for i in range(self.sizes[str(op['Size'])]["Healer"] - len(op['Sign-ups']['Healer'])):
            msg += f"\n{heal_emoji} - "
        msg += "\nReserves: "
        for res in op['Sign-ups']['Reserve']:
            msg += f"{res}"
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

    async def validate_size_input(self, size: int) -> bool:
        """
        Checks the users input to ensure the size input is valid.
        :param size: The size input by the user.
        :return: Booleon True if the size input is valid.
        """
        return str(size) in self.sizes.keys()

    async def edit_pinned_message(self, op: dict, op_number: str, guild_id: int) -> None:
        """
        Edits the pinned message for the operation.
        :param op: The operation details dictionary.
        :param op_number: The operation id.
        """
        dt = await self.parse_date(op["Date"], op["Time"])
        msg = await self.make_operation_message(dt, op, op_number)
        guild = self.bot.get_guild(guild_id)
        channel = guild.get_channel(op["Channel_id"])
        message = get(await channel.history(limit=100).flatten(), id=op["Post_id"])

        # message = await ctx.fetch_message(op["Post_id"])
        await message.edit(content=msg)

    @staticmethod
    async def is_owner_or_admin(ctx: context, op: dict) -> bool:
        """
        Checks if the user is the owner of the given operation or an Admin.
        :param op: The Operation details dictionary.
        :return: Booleon True is the user owns the operation or is an Admin.
        """
        return ctx.author.id in [op["Owner_id"], 168009927015661568]

    @staticmethod
    async def validate_role(role: str) -> str:
        """
        Checks the role given is valid and converts any short hand role to the proper name.
        :param role: The role of the user.
        :return: The long version of the users role.
        """
        if role.lower() in ["t", "tank", "d", "dps", "h", "heals", "healer", "heal", "a", "any", "r", "reserve"]:
            if role[0].lower() == "t":
                return "Tank"
            elif role[0].lower() == "d":
                return "Dps"
            elif role[0].lower() == "h":
                return "Healer"
            elif role[0].lower() == "a":
                return "Any"
            elif role[0].lower() == "r":
                return "Reserve"
        else:
            return ""

    @staticmethod
    async def parse_date(date: str, time: str) -> datetime:
        """
        Takes a date and time as a string and returns a datetime object.
        :param date: The given date.
        :param time: The given time
        :return: datetime object of the given date and time.
        """
        return parse(f"{date} {time}")

    @staticmethod
    async def date_extention(number: int) -> str:
        """
        Gives number extension for date.
        :param number: The date number the extension is for.
        :return: String of the Number extension.
        """
        if number % 10 == 1:
            return '%dst' % number
        if number % 10 == 2:
            return '%dnd' % number
        if number % 10 == 3:
            return '%drd' % number
        if (number % 10 >= 4) or (number % 10 == 0):
            return '%dth' % number

    @staticmethod
    async def validate_side_input(side: str) -> str:
        """
        Checks the side given is valid and converts names to a standard.
        :param side: The side the operation is to take place
        :return: The standard name of the side or None if invalid.
        """
        if side.lower() in ["imp", "imps", "imperial", "i"]:
            return "Imp"
        elif side.lower() in ["rep", "reps", "republic", "pub", "r"]:
            return "Rep"
        else:
            return None

    async def write_operation(self, op: dict, op_number: id, guild_id: int) -> None:
        """
        Edits the pinned message and writes the new ops dictionary to the Ops.json file
        :param op: The operation details dictionary.
        :param op_number: The operation id.
        """
        await self.edit_pinned_message(op, op_number, guild_id)

        self.ops[str(guild_id)][str(op_number)] = op
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    async def check_role_full(self, op: dict, role: str) -> bool:
        """
        Checks if the given role is full.
        :param op: The operations details dictionary.
        :param role: The role to check.
        :return: Bool True if the operation is full.
        """
        if role == "Reserve" or role == "Any":
            return False
        elif len(op["Sign-ups"][role]) >= self.sizes[str(op["Size"])][role]:
            return True

    async def get_random_operation(self) -> str:
        return choice(list(self.operations.keys()))

    async def add_to_operation(self, op: dict, op_number: str, guild_id:int, sign_up_name: str,
                               main_role: str, alt_role: str = None) -> None:
        """
        Adds the given user to the sign ups. (validates parameters)
        :param op: The operation to add the person to.
        :param op_number: The id of the operation.
        :param sign_up_name: The name of the person to be added.
        :param main_role: The main role of the person to be added.
        :param alt_role: The alternative role of the person to be added.
        """
        if not op:
            raise SignUpError("There is no Operation with that number.")

        main_role = await self.validate_role(main_role)
        if not main_role:
            raise SignUpError("Main role is not valid. Please enter a valid role.")

        if alt_role:
            alt_role = await self.validate_role(alt_role)
            if not alt_role:
                raise SignUpError("Alternative role is not valid. Please enter a valid role.")
            elif main_role == alt_role:
                alt_role = None
            elif alt_role == "Reserve":
                raise SignUpError("Alt role can not be reserve. If you wish to sign as a reserve please select it as "
                                  "the main role.")
        elif main_role == "Reserve":
            raise SignUpError("You must add a alternative role to sign as reserve.")

        if await self.check_duplicate(op, sign_up_name):
            if not await self.check_role_change(op, sign_up_name, main_role, alt_role):
                raise SignUpError("You have already signed-up for that operation.")
            elif await self.check_role_full(op, main_role):
                raise SignUpError("That role is full. Your role has not been changed.")
            else:
                op = await self.remove_signup(op, sign_up_name)
        elif op["Signed"] >= sum(self.sizes[str(op["Size"])].values()) and main_role != "Reserve":
            op["Sign-ups"]["Reserve"] += [f"{sign_up_name} ({main_role})"]
            await self.write_operation(op, op_number, guild_id)
            raise SignUpError("This operation is full you have been placed as a reserve.")
        else:
            if await self.check_role_full(op, main_role):
                if not alt_role:
                    op["Sign-ups"]["Reserve"] += [f"{sign_up_name} ({main_role})"]
                    await self.write_operation(op, op_number, guild_id)
                    raise SignUpError("That role is full you have been placed as a reserve.")
                elif await self.check_role_full(op, alt_role):
                    op["Sign-ups"]["Reserve"] += [f"{sign_up_name} ({main_role})"]
                    await self.write_operation(op, op_number, guild_id)
                    raise SignUpError("Those roles are full you have been placed as a reserve.")
                else:
                    temp_role = main_role
                    main_role = alt_role
                    alt_role = temp_role
                    # await ctx.send(f"{temp_role} is full. You have been signed as {main_role}.")
                    del temp_role

        op = await self.add_signup(op, sign_up_name, main_role, alt_role)

        await self.write_operation(op, op_number, guild_id)
        return True

    @sign_up.error
    @add_sign_up.error
    async def sign_up_error_handler(self, ctx: context, error):
        if isinstance(error, errors.CommandInvokeError):
            message = await ctx.send(error.__cause__)
            await message.delete(delay=10)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Runs when a reaction is added to a message. Used for reaction based sign ups.
        """
        for id, op in self.ops.get(str(payload.guild_id), {}).items():
            if op["Post_id"] == payload.message_id:
                break
        else:
            return
        role = await check_valid_reaction(payload.emoji.name)
        if not role:
            return
        try:
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            await self.add_to_operation(op, id, payload.guild_id, user.display_name, role, None)
        except SignUpError:
            pass

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """
        Runs when a reaction is removed from a message. Used for reaction based sign ups.
        """
        for id, op in self.ops.get(str(payload.guild_id), {}).items():
            if op["Post_id"] == payload.message_id:
                break
        else:
            return
        role = await check_valid_reaction(payload.emoji.name)
        if not role:
            return
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        if not await self.check_role_change(op, user.display_name, role, None):
            op = await self.remove_signup(op, user.display_name)
            await self.write_operation(op, id, payload.guild_id)