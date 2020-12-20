from discord.ext.commands import Cog, command, context
from json import dump


class Admin(Cog):
    def __init__(self, bot, ops):
        self.bot = bot
        self.ops = ops

    @command()
    async def delete_all(self, ctx: context) -> None:
        """
        Deletes all operations for the given server.
        """
        print("Here")
        print(self.ops)
        self.ops[str(ctx.guild.id)] = []
        print(self.ops)
        with open('./Ops.json', 'w') as f:
            dump(self.ops, f)


