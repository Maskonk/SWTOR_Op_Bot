from json import load

# with open('../Ops.json', 'r') as f:
#     ops = load(f)


async def find_operation_by_id(ops, guild_id: str, op_id: str):
    guild = ops.get(str(guild_id), {})
    for op in guild.values():
        if op["Post_id"] == int(op_id):
            return op




# a = find_operation_by_id("323229951098748928", "774060104374943786")
# print(a)
