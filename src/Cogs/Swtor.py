from discord.ext.commands import Cog, context, command
from random import choice


class Swtor(Cog):
    def __init__(self, bot):
        self.bot = bot

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
