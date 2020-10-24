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
    async def spec(self, ctx: context, role: str = "all") -> None:
        """
        Returns a random spec for a given role.
        :param role:
        :return:
        """
        damage = ["Hatred", "Deception", "Lightning", "Madness", "Virulence", "Engineering", "Marksman", "Concealment",
                  "Lethality", "Fury", "Carnage", "Annihilation", "Vengeance", "Rage", "Arsenal",
                  "Innovative Ordinance", "Advanced Prototype", "Pyrotech", ]
        healer = ["Medicine", "Bodyguard", "Corruption"]
        tank = ["Darkness", "Defense", "Shield Tech"]
        select = []
        if role.lower() == "all":
            select += damage + healer + tank
        elif role.lower() == "dps":
            select = damage
        elif role.lower() == "heals":
            select = healer
        elif role.lower() == "tank":
            select = tank
        else:
            await ctx.send("That is not a valid role. Please choose from All, DPS, Heals or Tank.")
            return
        await ctx.send(f"The spec chosen is: {choice(select)}")

    @command()
    async def op_codes(self, ctx: context):
        msg = ""
        for op in self.operations.keys():
            msg += f"{op.capitalize()}: {self.operations[op]}\n"
        await ctx.send(msg)

    @command(alaises=["guide"])
    async def bot_guide(self, ctx: context):
        await ctx.send("A full guide to all bot commands is here: "
                       "https://github.com/Maskonk/SWTOR_Op_Bot/wiki/Operation-Commands.")
