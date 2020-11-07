async def check_valid_reaction(reaction: str) -> str:
    standard = {"🇹": "Tank", "🇩": "Dps", "🇭": "Healer"}
    if reaction in standard.keys():
        role = standard[reaction]
    elif reaction.capitalize() in ["Tank", "Healer", "Dps"]:
        role = reaction.capitalize()
    else:
        role = None
    return role
