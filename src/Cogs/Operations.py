from discord.ext.commands import Cog, context, command, errors, Bot
from discord.utils import get
from datetime import datetime
from json import load, dump
from dateutil.parser import parse
from calendar import month_name, day_name
from random import choice
from src.Utils.Errors import SignUpError
from src.Utils.ReactionUtils import check_valid_reaction
from src.Utils.SignupUtils import SignupUtils
from src.Utils.Validators import Validators
from typing import Optional


class Operations(Cog):
    sizes = {"1": {"Tank": 0, "Dps": 1, "Healer": 0}, "4": {"Tank": 1, "Dps": 1, "Healer": 1},
             "8": {"Tank": 2, "Dps": 4, "Healer": 2}, "16": {"Tank": 2, "Dps": 10, "Healer": 4},
             "1t5d": {"Tank": 1, "Dps": 5, "Healer": 2}, "1h5d": {"Tank": 2, "Dps": 5, "Healer": 1},
             "6d": {"Tank": 1, "Dps": 6, "Healer": 1}, "24": {"Tank": 3, "Dps": 15, "Healer": 6},
             "dwt": {"Tank": 1, "Dwt": 1, "Dps": 4, "Healer": 2}, "dwh": {"Tank": 2, "Dps": 4, "Dwh": 1, "Healer": 1},
             "6dw": {"Tank": 1, "Dwt": 1, "Dps": 4, "Dwh": 1, "Healer": 1}}
    operations = {"s&v": "Scum and Villainy", "tfb": "Terror From Beyond", "kp": "Karagga's Palace",
                  "ev": "Eternity Vault", "ec": "Explosive Conflict", "df": "Dread Fortress",
                  "dp": "Dread Palace", "dxun": "Dxun", "gftm": "Gods from the Machine",
                  "tc": "Toborro's Courtyard", "cm": "Colossal Monolith", "gq": "Geonosian Queen",
                  "wb": "World Boss", "gf": "Group finder", "other": "Other activity", "eyeless": "Eyeless",
                  "xeno": "Xenoanalyst", "rav": "Ravagers", "tos": "Temple of Sacrifice"}
    difficulties = {"sm": "Story Mode", "hm": "Veteran Mode", "nim": "Master Mode", "vm": "Veteran mode",
                         "mm": "Master Mode", "na": ""}

    def __init__(self, bot: Bot, ops: dict, config: dict):
        self.bot = bot
        self.ops = ops
        self.config = config

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
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_operation_channel(ctx.channel.id, config):
            return

        if not await Validators.validate_operation_input(operation, self.operations):
            await ctx.send("That is not a valid operation.")
            return

        if not await Validators.validate_time_input(date, time):
            message = await ctx.send("That date has already passed.")
            await message.delete(delay=10)
            return

        if not await Validators.validate_difficulty_input(difficulty):
            message = await ctx.send("That is not a valid difficulty.")
            await message.delete(delay=10)
            return

        size = await Validators.validate_size_input(size, self.sizes)
        if not size:
            message = await ctx.send("That is not a valid size.")
            await message.delete(delay=10)
            return

        if not await Validators.validate_side_input(side):
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
            operation = await self.get_random_operation(self.operations)
            while operation in ["wb", "gf", "other"]:
                operation = await self.get_random_operation(self.operations)

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
                  "Roster": [],
                  "Reserves": []
              }}

        dt = await self.parse_date(date, time)
        msg = await self.make_operation_message(dt, op, str(op_id))
        message = await ctx.send(msg)

        await message.pin()
        op["Post_id"] = message.id
        self.ops[str(ctx.guild.id)] = self.ops.get(str(ctx.guild.id), {})
        self.ops[str(ctx.guild.id)][str(op_id)] = op
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    @command(aliases=["sign", "join"])
    async def sign_up(self, ctx: context, op_number: str, main_role: str, alt_role: Optional[str] = None) -> None:
        """
        Signup to a given operation with the given roles.
        :param op_number: The operation id to sign up to.
        :param main_role: The main role to sign up as.
        :param alt_role: Optional alternative role to sign up as.
        """
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_sign_up_channel(ctx.channel.id, config):
            return
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
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_sign_up_channel(ctx.channel.id, config):
            return
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if not await SignupUtils.check_duplicate(op, ctx.author.display_name):
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
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_sign_up_channel(ctx.channel.id, config):
            return
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
            if not await Validators.validate_operation_input(value, self.operations):
                await ctx.send("That is not a valid operation.")
                return
        elif attribute.capitalize() == "Date":
            if not await Validators.validate_time_input(value, op["Time"]):
                message = await ctx.send("That date has already passed.")
                await message.delete(delay=10)
                return
        elif attribute.capitalize() == "Time":
            if not await Validators.validate_time_input(op["Date"], value):
                message = await ctx.send("That date has already passed.")
                await message.delete(delay=10)
                return
        elif attribute.capitalize() == "Difficulty":
            if not await Validators.validate_difficulty_input(value):
                message = await ctx.send("That is not a valid difficulty.")
                await message.delete(delay=10)
                return
        elif attribute.capitalize() == "Size":
            value = await Validators.validate_size_input(value, self.sizes)
            if not value:
                message = await ctx.send("That is not a valid size.")
                await message.delete(delay=10)
                return
        elif attribute.capitalize() == "Side":
            if not await Validators.validate_side_input(value):
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
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_sign_up_channel(ctx.channel.id, config):
            return
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))
        if not op:
            message = await ctx.send("There is no Operation with that number.")
            await message.delete(delay=10)
            return

        if not await self.is_owner_or_admin(ctx, op):
            await ctx.send("You are not authorised to use this command. Only an Admin or the person who created "
                           "this operation may update it.")
            return

        try:
            message = await ctx.fetch_message(op["Post_id"])
            await message.unpin()
        except Exception as e:
            pass

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
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_sign_up_channel(ctx.channel.id, config):
            return
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
    async def add_sign_up(self, ctx: context, op_number: str, sign_up_name: str, main_role: str,
                          alt_role: Optional[str] = None) -> None:
        """
        Adds the given name to the sign ups.
        :param op_number: The id of the operation.
        :param sign_up_name: The name of the person to be added.
        :param main_role: The main role of the person to be added.
        :param alt_role: The alt role of the person to be added.
        """
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_sign_up_channel(ctx.channel.id, config):
            return
        op = self.ops.get(str(ctx.guild.id), {}).get(str(op_number))

        r = await self.add_to_operation(op, op_number, ctx.guild.id, sign_up_name, main_role, alt_role)
        if r:
            await ctx.message.add_reaction('\U0001f44d')

    @command(aliases=["howto"])
    async def user_guide(self, ctx: context) -> None:
        """
        A basic user guide on how to use the bot.
        """
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_swtor_channel(ctx.channel.id, config):
            return
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
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_swtor_channel(ctx.channel.id, config):
            return
        operation = await self.get_random_operation(self.operations)
        await ctx.send(f"The random operation is: {operation}")

    @staticmethod
    async def add_signup(op: dict, sign_up_name: str, main_role: str, alt_role: Optional[str] = None) -> dict:
        """
        Adds a user with given name and roles to the given operation. Should never be called for reserve.
        :param op: The operation to be updated.
        :param sign_up_name: The user's nick name.
        :param main_role: The main role of the user.
        :param alt_role: Optional alternative role of the user.
        :return: dict: The updated operation. 
        """
        if main_role == "Any":
            op = await Operations.add_any_signup(op, sign_up_name)
        else:
            op["Sign-ups"]["Roster"] += [{"name": sign_up_name, "main-role": main_role, "alt-role": alt_role}]

        op["Signed"] += 1
        return op

    @staticmethod
    async def add_any_signup(op: dict, sign_up_name: str) -> dict:
        """
        Adds a user with given name to any role as they are available (Dps > Healer > Tank)
        Note: No changes are made if all roles are full.
        :param op: The operation to be updated.
        :param sign_up_name: The user's nick name.
        :return: dict: The updated operation. 
        """
        roles = ["Dps", "Healer", "Tank"]

        for role in roles:
            if not await Operations.check_role_full(op, role):
                roles.remove(role)
                op["Sign-ups"]["Roster"] += [{"name": sign_up_name, "main-role": role, "alt-role": "Any"}]
                op["Signed"] += 1
                return op

        return op    

    @staticmethod
    async def add_reserve(op: dict, sign_up_name: str, reserve_role: str, main: Optional[bool] = False) -> dict:
        """
        Adds a user with given name as a reserve with their preferred role
        :param op: The operation to be updated.
        :param sign_up_name: The user's nick name.
        :param reserve_role: The user's reserve role.
        :param main: If the user should be moved to the main roster or not.
        :return: dict: The updated operation. 
        """
        op["Sign-ups"]["Reserves"] += [{"name": sign_up_name, "role": reserve_role, "move-main": main}]
        return op

    @staticmethod
    async def remove_signup(op: dict, user_nick: str) -> dict:
        """
        Attempts to removes the user with given name from the operation.
        :param op: The operation to be updated.
        :param user_nick: The user's nick name.
        :return: dict: The updated operation. 
        """
        for i, user in enumerate(op["Sign-ups"]["Roster"]):
            if user_nick == user.get("name", None):
                op["Sign-ups"]["Roster"].pop(i)
                break
        for i, user in enumerate(op["Sign-ups"]["Reserves"]):
            if user_nick == user.get("name", None):
                op["Sign-ups"]["Reserves"].pop(i)
                break
        op["Signed"] -= 1
        return op

    async def make_operation_message(self, dt: datetime, op: dict, op_id: str) -> str:
        """
        Composes operation message.
        :param dt: The Datetime object of the operation
        :param op: The operation details dictionary.
        :param op_id: The id of the operation.
        :return: String of the message to send composed of the operations details.
        """
        guild = self.bot.get_guild(750036082518917170)
        emojis = {
            "Tank": get(guild.emojis, name='Tank'),
            "Dwt": get(guild.emojis, name='DwT'),
            "Dps": get(guild.emojis, name='DPS'),
            "Dwh": get(guild.emojis, name='DwH'),
            "Healer": get(guild.emojis, name='Healer')
        }
        operation_name = self.operations[op['Operation'].lower()]
        difficulty = self.difficulties[op['Difficulty'].lower()]
        notes = op["Notes"]
        size = sum(op["Size"][1].values())
        extension = await self.date_extension(dt.day)
        msg = f"{op_id}: {size}m {operation_name} {difficulty} {op['Side']}\n{day_name[dt.weekday()]} the " \
              f"{extension} of {month_name[dt.month]} " \
              f"starting at {dt.time().strftime('%H:%M')} CET. "
        if notes:
            msg += f"\n({notes})\n"
        msg += f"Current signups:\n"
        for r in ["Tank", "Dwt", "Dps", "Dwh", "Healer"]:
            signups = await self.find_role(op, r)
            for s in signups:
                if s.get("alt-role", None):
                    alt_role = f"({s.get('alt-role', None)})"
                else:
                    alt_role = ""
                msg += f"\n{emojis[r]} - {s.get('name')} {alt_role}"
            for _ in range(op["Size"][1].get(r, 0) - len(signups)):
                msg += f"\n{emojis[r]} - "

        msg += "\nReserves: "
        for res in op['Sign-ups']['Reserves']:
            msg += f"{res.get('name')} ({res.get('role', '')}), "

        msg += f"\nTo sign up use -sign {op_id} <role> <alt role>"
        return msg

    async def edit_pinned_message(self, op: dict, op_number: str, guild_id: int) -> None:
        """
        Edits the pinned message for the operation.
        :param op: The operation details dictionary.
        :param op_number: The operation id.
        :param guild_id: The id of the guild.
        """
        dt = await self.parse_date(op["Date"], op["Time"])
        msg = await self.make_operation_message(dt, op, op_number)
        guild = self.bot.get_guild(guild_id)
        channel = guild.get_channel(op["Channel_id"])
        message = get(await channel.history(limit=150).flatten(), id=op["Post_id"])
        if not message:
            message = get(await channel.history(limit=500).flatten(), id=op["Post_id"])

        await message.edit(content=msg)

    async def is_owner_or_admin(self, ctx: context, op: dict) -> bool:
        """
        Checks if the user is the owner of the given operation or an Admin.
        :param op: The Operation details dictionary.
        :return: Booleon True is the user owns the operation or is an Admin.
        """
        server_admins = self.config.get(str(ctx.guild.id), {}).get("Admins", [])
        return ctx.author.id in ([op["Owner_id"], 168009927015661568, 165463629171261440] + server_admins)

    @staticmethod
    async def parse_date(date: str, time: str) -> datetime:
        """
        Takes a date and time as a string and returns a datetime object.
        :param date: The given date.
        :param time: The given time
        :return: datetime object of the given date and time.
        """
        return parse(f"{date} {time}", dayfirst=True)

    @staticmethod
    async def date_extension(number: int) -> str:
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

    @staticmethod
    async def check_role_full(op: dict, role: str) -> bool:
        """
        Checks if the given role is full.
        :param op: The operations details dictionary.
        :param role: The role to check.
        :return: Bool True if the operation is full.
        """
        if role == "Reserve" or role == "Any":
            return False
        elif len(await Operations.find_role(op, role)) >= op["Size"][1].get(role, 0):
            return True
        return False

    @staticmethod
    async def get_random_operation(operations: dict) -> str:
        """
        Returns a random operation from the keys of the given dictionary.
        :param operations: Dictionary of the operations to choose from.
        :return: str name of the random operation.
        """
        return choice(list(operations.keys()))

    async def add_to_operation(self, op: dict, op_number: str, guild_id:int, sign_up_name: str,
                               main_role: str, alt_role: Optional[str] = None) -> bool:
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

        main_role = await Validators.validate_role(main_role)
        if not main_role:
            raise SignUpError("Main role is not valid. Please enter a valid role.")

        if alt_role:
            alt_role = await Validators.validate_role(alt_role)
            if not alt_role:
                raise SignUpError("Alternative role is not valid. Please enter a valid role.")
            elif main_role == alt_role:
                alt_role = None
            elif alt_role == "Reserve":
                raise SignUpError("Alt role can not be reserve. If you wish to sign as a reserve please select it as "
                                  "the main role.")
        elif main_role == "Reserve":
            raise SignUpError("You must add a alternative role to sign as reserve.")

        if await SignupUtils.check_duplicate(op, sign_up_name):
            if not await SignupUtils.check_role_change(op, sign_up_name, main_role, alt_role):
                raise SignUpError("You have already signed-up for that operation.")
            elif await self.check_role_full(op, main_role):
                raise SignUpError("That role is full. Your role has not been changed.")
            else:
                op = await self.remove_signup(op, sign_up_name)
        elif op["Signed"] >= sum(op["Size"][1].values()) and main_role != "Reserve":
            op = await self.add_reserve(op, sign_up_name, main_role, True)
            await self.write_operation(op, op_number, guild_id)
            raise SignUpError("This operation is full you have been placed as a reserve.")
        else:
            if await Operations.check_role_full(op, main_role):
                if not alt_role:
                    if main_role in ["Dwt", "Dwh"]:
                        main_role = "Dps"
                    else:
                        op = await self.add_reserve(op, sign_up_name, main_role, True)
                        await self.write_operation(op, op_number, guild_id)
                        raise SignUpError("That role is full you have been placed as a reserve.")
                elif await self.check_role_full(op, alt_role):
                    if main_role in ["Dwt", "Dwh"] or alt_role in ["Dwt", "Dwh"]:
                        alt_role = main_role
                        main_role = "Dps"
                    else:
                        op = await self.add_reserve(op, sign_up_name, main_role, True)
                        await self.write_operation(op, op_number, guild_id)
                        raise SignUpError("Those roles are full you have been placed as a reserve.")
                else:
                    temp_role = main_role
                    main_role = alt_role
                    alt_role = temp_role
                    del temp_role

        if main_role == "Reserve":
            op = await Operations.add_reserve(op, sign_up_name, alt_role, False)
        else:
            op = await Operations.add_signup(op, sign_up_name, main_role, alt_role)

        await self.write_operation(op, op_number, guild_id)
        return True

    @sign_up.error
    @add_sign_up.error
    @new_operation.error
    @update_operation.error
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
            await self.add_to_operation(op, id, payload.guild_id, user.display_name, role[0], role[1])
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
        if not await SignupUtils.check_role_change(op, user.display_name, role[0], role[1]):
            op = await self.remove_signup(op, user.display_name)
            await self.write_operation(op, id, payload.guild_id)

    @staticmethod
    async def count_role(op: dict, role: str) -> int:
        signups = op.get("Sign-ups", {}).get("Roster", [])
        count = 0
        for s in signups:
            if s.get("main-role", None) == role:
                count += 1
        return count

    @staticmethod
    async def find_role(op: dict, role: str) -> list:
        signups = op.get("Sign-ups", {}).get("Roster", [])
        role_signed = []
        for s in signups:
            if s.get("main-role", None) == role:
                role_signed += [s]

        return role_signed
