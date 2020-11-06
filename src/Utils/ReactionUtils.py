from Cogs.Operations import Operations

async def find_operation_by_id(ops: dict, guild_id: str, op_id: str) -> dict:
    guild = ops.get(str(guild_id), {})
    for op in guild.values():
        if op["Post_id"] == int(op_id):
            return op

async def check_valid_reaction(reaction: str) -> str:
    standard = {"🇹": "Tank", "🇩": "Dps", "🇭": "Healer"}
    if reaction in standard.keys():
        role = standard[reaction]
    elif reaction in ["Tank", "Healer", "DPS"]:
        role = reaction
    else:
        role = None
    return role.capitalize()

