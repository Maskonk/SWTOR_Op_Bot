from discord.ext.commands import Cog, command, context, check
from discord.utils import get
from datetime import datetime
from json import dump
from .Operations import Operations
from calendar import month_name, day_name


class Admin(Cog):
    def __init__(self, bot, ops: dict, config: dict):
        self.bot = bot
        self.ops = ops
        self.config = config

    async def is_server_admin(self, ctx: context) -> bool:
        admins = self.config.get(str(ctx.guild.id), {}).get("Admins", [])
        return ctx.author.id in admins or ctx.author.id in [168009927015661568, 165463629171261440]

    @command(hidden=True, aliases=["da", "deleteall"])
    async def delete_all(self, ctx: context) -> None:
        """
        Deletes all operations for the given server.
        """
        if not await self.is_server_admin(ctx):
            await ctx.send("You are not authorized to use this command.")
            return
        ops = self.ops.get(str(ctx.guild.id), ())
        for op in ops.values():
            channel = ctx.guild.get_channel(op["Channel_id"])
            try:
                message = get(await channel.history(limit=300).flatten(), id=op["Post_id"])
                await message.unpin()
            except Exception as e:
                pass
        self.ops[str(ctx.guild.id)] = {}
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)
        await ctx.message.add_reaction('\U0001f44d')

    @command(hidden=True, aliases=["ri", "resetids"])
    async def reset_ids(self, ctx: context) -> None:
        """
        Resets the ids of all operations for the server starting at one.
        """
        if not await self.is_server_admin(ctx):
            await ctx.send("You are not authorized to use this command.")
            return
        ops = self.ops.get(str(ctx.guild.id), ())
        i = 1
        temp = {}
        for op in ops.values():
            await self.edit_pinned_message(op, i, ctx.guild.id)
            temp[str(i)] = op
            i += 1
        self.ops[str(ctx.guild.id)] = temp
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)
        await ctx.message.add_reaction('\U0001f44d')

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
        operation_name = Operations.operations[op['Operation'].lower()]
        difficulty = Operations.difficulties[op['Difficulty'].lower()]
        notes = op["Notes"]
        size = sum(op["Size"][1].values())
        extension = await Operations.date_extension(dt.day)
        msg = f"{op_id}: {size}m {operation_name} {difficulty} {op['Side']}\n{day_name[dt.weekday()]} the " \
              f"{extension} of {month_name[dt.month]} " \
              f"starting at {dt.time().strftime('%H:%M')} CET. "
        if notes:
            msg += f"\n({notes})\n"
        msg += f"Current signups:\n"
        for r in ["Tank", "Dwt", "Dps", "Dwh", "Healer"]:
            signups = await Operations.find_role(op, r)
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
        """
        dt = await Operations.parse_date(op["Date"], op["Time"])
        msg = await self.make_operation_message(dt, op, op_number)
        guild = self.bot.get_guild(guild_id)
        channel = guild.get_channel(op["Channel_id"])
        message = get(await channel.history(limit=300).flatten(), id=op["Post_id"])

        await message.edit(content=msg)




