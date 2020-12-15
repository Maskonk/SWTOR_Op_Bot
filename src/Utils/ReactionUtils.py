async def check_valid_reaction(reaction: str) -> str:
    emojis = {"🇹": "Tank", "🇩": "Dps", "🇭": "Healer", "Tank": "Tank", "Healer": "Healer", "Dps": "Dps"}
    if reaction.capitalize() in emojis.keys():
        role = emojis[reaction.capitalize()]
    else:
        role = None
    return role
