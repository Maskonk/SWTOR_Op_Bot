async def check_valid_reaction(reaction: str) -> tuple:
    emojis = {"🇹": ("Tank", None), "🇩": ("Dps", None), "🇭": ("Healer", None),
              "Tank": ("Tank", None), "Healer": ("Healer", None), "Dps": ("Dps", None)}
    if reaction.capitalize() in emojis.keys():
        role = emojis[reaction.capitalize()]
    else:
        role = None
    return role
