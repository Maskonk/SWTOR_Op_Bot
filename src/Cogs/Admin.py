from discord.ext.commands import Cog, command, context
from discord.utils import get
from datetime import datetime
from json import dump
from .Operations import Operations
from calendar import month_name, day_name


class Admin(Cog):
    def __init__(self, bot, ops):
        self.bot = bot
        self.ops = ops

    @command(hidden=True)
    async def delete_all(self, ctx: context) -> None:
        """
        Deletes all operations for the given server.
        """
        self.ops[str(ctx.guild.id)] = []
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

    @command(hidden=True)
    async def reset_ids(self, ctx: context) -> None:
        ops = self.ops.get(str(ctx.guild.id), ())
        i = 1
        temp = {}
        print(ops.keys())
        for op in ops.values():
            await self.edit_pinned_message(op, i, ctx.guild.id)
            temp[i] = op
            i += 1
        self.ops[str(ctx.guild.id)] = temp
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)

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
        operation_name = Operations.operations[op['Operation'].lower()]
        difficulty = Operations.difficulties[op['Difficulty'].lower()]
        notes = op["Notes"]
        size = sum(Operations.sizes[str(op['Size'])].values())
        extension = await Operations.date_extension(dt.day)
        msg = f"{op_id}: {size}m {operation_name} {difficulty} {op['Side']}\n{day_name[dt.weekday()]} the " \
              f"{extension} of {month_name[dt.month]} " \
              f"starting at {dt.time().strftime('%H:%M')} CET."
        if notes:
            msg += f"\n({notes})\n"
        msg += f"Current signups:\n"
        for tank in op['Sign-ups']['Tank']:
            msg += f"\n{tank_emoji} - {tank}"
        for i in range(Operations.sizes[str(op['Size'])]["Tank"] - len(op['Sign-ups']['Tank'])):
            msg += f"\n{tank_emoji} - "
        for dps in op['Sign-ups']['Dps']:
            msg += f"\n{dps_emoji} - {dps}"
        for i in range(Operations.sizes[str(op['Size'])]["Dps"] - len(op['Sign-ups']['Dps'])):
            msg += f"\n{dps_emoji} - "
        for heal in op['Sign-ups']['Healer']:
            msg += f"\n{heal_emoji} - {heal}"
        for i in range(Operations.sizes[str(op['Size'])]["Healer"] - len(op['Sign-ups']['Healer'])):
            msg += f"\n{heal_emoji} - "
        msg += "\nReserves: "
        for res in op['Sign-ups']['Reserve']:
            msg += f"{res}, "

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

