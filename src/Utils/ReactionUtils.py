async def check_valid_reaction(reaction: str) -> tuple:
    emojis = {"🇹": ("Tank", None), "🇩": ("Dps", None), "🇭": ("Healer", None),
              "tank": ("Tank", None), "healer": ("Healer", None), "dps": ("Dps", None),
              "tankdps": ("Dps", "Tank")}
    if reaction.lower() in emojis.keys():
        role = emojis[reaction.lower()]
    else:
        role = None
    return role
