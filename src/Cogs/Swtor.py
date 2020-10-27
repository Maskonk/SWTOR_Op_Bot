from discord.ext.commands import Cog, context, command
from random import choice


class Swtor(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.operations = {"s&v": "Scum and Villainy", "tfb": "Terror From Beyond", "kp": "Karagga's Palace",
                           "ev": "Eternity Vault", "ec": "Explosive Conflict", "df": "Dread Fortress",
                           "dp": "Dread Palace", "dxun": "Dxun", "gftm": "Gods from the Machine",
                           "tc": "Toborro's Courtyard", "cm": "Colossal Monolith", "gq": "Geonosian Queen",
                           "wb": "World Boss", "gf": "Group finder", "other": "Other activity", "eye": "Eyeless",
                           "xeno": "Xenoanalyst", "rav": "Ravagers", "tos": "Temple of Sacrifice"}

    @command()
    async def spec(self, ctx: context, tag: str, side: str = None) -> None:
        """
        Returns a random spec for a given role.
        :param tag: Tag to search for:
        :param side: If the side is Republic.
        """
        specs = {"Hatred": ["assassin", "shadow", "dwt", "dps", "dot", "sin"],
                 "Deception": ["assassin", "shadow", "dwt", "dps", "burst", "sin"],
                 "Lightning": ["sorcerer", "sage", "dwh", "dps", "burst", "sorc"],
                 "Madness": ["sorcerer", "sage", "dwh", "dps", "dot", "sorc"],
                 "Virulence": ["sniper", "gunslinger", "dps", "dot"], "Engineering": ["sniper", "gunslinger", "dps"],
                 "Marksman": ["sniper", "gunslinger", "dps", "burst"],
                 "Concealment": ["operative", "scoundrel", "dps", "dwh" "burst", "op"],
                 "Lethality": ["operative", "scoundrel", "dps", "dwh" "dot", "op"],
                 "Fury": ["marauder", "sentinel", "dps", "mara", "sent"],
                 "Carnage": ["marauder", "sentinel", "dps", "mara", "sent", "burst"],
                 "Annihilation": ["marauder", "sentinel", "dps", "mara", "sent", "dot"],
                 "Vengeance": ["juggernaut", "guardian", "dps", "dwt", "jugg", "dot"],
                 "Rage": ["juggernaut", "guardian", "dps", "dwt", "jugg", "burst"],
                 "Arsenal": ["mercenary", "commando", "dps", "dwh", "burst", "merc"],
                 "Innovative Ordinance": ["mercenary", "commando", "dps", "dwh", "dot", "merc"],
                 "Advanced Prototype": ["powertech", "vanguard", "dps", "dwt", "burst", "pt", "vg"],
                 "Pyrotech": ["powertech", "vanguard", "dps", "dwt", "dot", "pt", "vg"],
                 "Medicine": ["operative", "scoundrel", "heal", "op"],
                 "Bodyguard": ["mercenary", "commando", "heal", "merc"],
                 "Corruption": ["sorcerer", "sage", "heal" "sorc"],
                 "Darkness": ["assassin", "shadow", "tank", "sin"],
                 "Defense": ["juggernaut", "guardian", "tank", "jugg"],
                 "Shield Tech": ["powertech", "vanguard", "tank", "pt", "vg"]}

        select = []
        for spec in specs.keys():
            if tag.lower() in specs[spec]:
                select.append(spec)
        if not select:
            await ctx.send("There are no results found with that tag.")
            return
        await ctx.send(f"The spec chosen is: {choice(select)}")

    @command()
    async def op_codes(self, ctx: context):
        msg = ""
        for op in self.operations.keys():
            msg += f"{op.capitalize()}: {self.operations[op]}\n"
        await ctx.send(msg)

    @command(aliases=["guide"])
    async def command_guide(self, ctx: context):
        await ctx.send("A full guide to all bot commands is here: "
                       "https://github.com/Maskonk/SWTOR_Op_Bot/wiki/Operation-Commands.")
