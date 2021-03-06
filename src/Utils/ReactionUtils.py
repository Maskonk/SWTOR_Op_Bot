async def check_valid_reaction(reaction: str) -> tuple:
    emojis = {"🇹": ("Tank", None), "🇩": ("Dps", None), "🇭": ("Healer", None),
              "tank": ("Tank", None), "healer": ("Healer", None), "dps": ("Dps", None),
              "tankdps": ("Dps", "Tank"), "tankheal": ("Healer", "Tank"), "dpshealer": ("Healer", "Dps"),
              "tankdpshealer": ("Any", None), "pepedeeps": ("Dps", None), "pepehels": ("Healer", None),
              "tonkdeeps": ("Dps", "Tank"), "tonkhels": ("Healer", "Tank"), "depshels": ("Dps", "Healer"),
              "tripelpower": ("Any", None), "pepetonk": ("Tank", None),}
    if reaction.lower() in emojis.keys():
        role = emojis[reaction.lower()]
    else:
        role = None
    return role
