from discord.ext.commands import Cog, command, context, check
from discord.ext import commands
from json import dump


class Admin(Cog):
    def __init__(self, bot, ops: dict, config: dict):
        self.bot = bot
        self.ops = ops
        self.config = config

    async def is_server_admin(self, ctx: context) -> bool:
        admins = self.config.get(str(ctx.guild.id), {}).get("Admins", [])
        return ctx.author.id in admins

    @command(hidden=True)
    @commands.check(is_server_admin)
    async def delete_all(self, ctx: context) -> None:
        """
        Deletes all operations for the given server.
        """
        if not await self.is_server_admin(ctx):
            return
        self.ops[str(ctx.guild.id)] = []
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)





