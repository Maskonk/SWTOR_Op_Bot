from discord.ext.commands import Cog, context, command
from random import choice
from Utils.Validators import Validators
from typing import Optional


class Swtor(Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.operations = {"s&v": "Scum and Villainy", "tfb": "Terror From Beyond", "kp": "Karagga's Palace",
                           "ev": "Eternity Vault", "ec": "Explosive Conflict", "df": "Dread Fortress",
                           "dp": "Dread Palace", "dxun": "Dxun", "gftm": "Gods from the Machine",
                           "tc": "Toborro's Courtyard", "cm": "Colossal Monolith", "gq": "Geonosian Queen",
                           "wb": "World Boss", "gf": "Group finder", "other": "Other activity", "eye": "Eyeless",
                           "xeno": "Xenoanalyst", "rav": "Ravagers", "tos": "Temple of Sacrifice"}
        self.config = config

    @command()
    async def spec(self, ctx: context, tag: Optional[str] = "all", side: Optional[str] = "imp") -> None:
        """
        Returns a random spec for a given role.
        :param tag: Tag to search for:
        :param side: If the side is Republic.
        """
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_swtor_channel(ctx.channel.id, config):
            return
        specs = {"Hatred": ["assassin", "shadow", "dwt", "dps", "dot", "sin", "melee", "mdps"],
                 "Deception": ["assassin", "shadow", "dwt", "dps", "burst", "sin", "melee", "mdps"],
                 "Lightning": ["sorcerer", "sage", "dwh", "dps", "burst", "sorc", "ranged", "rdps"],
                 "Madness": ["sorcerer", "sage", "dwh", "dps", "dot", "sorc", "ranged", "rdps"],
                 "Virulence": ["sniper", "gunslinger", "dps", "dot", "ranged", "rdps"],
                 "Engineering": ["sniper", "gunslinger", "dps", "ranged", "rdps"],
                 "Marksman": ["sniper", "gunslinger", "dps", "burst", "ranged", "rdps"],
                 "Concealment": ["operative", "scoundrel", "dps", "dwh", "burst", "op", "melee", "mdps"],
                 "Lethality": ["operative", "scoundrel", "dps", "dwh", "dot", "op", "melee", "mdps"],
                 "Fury": ["marauder", "sentinel", "dps", "mara", "sent", "melee", "mdps"],
                 "Carnage": ["marauder", "sentinel", "dps", "mara", "sent", "burst", "melee", "mdps"],
                 "Annihilation": ["marauder", "sentinel", "dps", "mara", "sent", "dot", "melee", "mdps"],
                 "Vengeance": ["juggernaut", "guardian", "dps", "dwt", "jugg", "dot", "melee", "mdps"],
                 "Rage": ["juggernaut", "guardian", "dps", "dwt", "jugg", "burst", "melee", "mdps"],
                 "Arsenal": ["mercenary", "commando", "dps", "dwh", "burst", "merc", "ranged", "rdps"],
                 "Innovative Ordinance": ["mercenary", "commando", "dps", "dwh", "dot", "merc", "ranged", "rdps"],
                 "Advanced Prototype": ["powertech", "vanguard", "dps", "dwt", "burst", "pt", "vg", "melee", "mdps"],
                 "Pyrotech": ["powertech", "vanguard", "dps", "dwt", "dot", "pt", "vg", "melee", "mdps"],
                 "Medicine": ["operative", "scoundrel", "heal", "op"],
                 "Bodyguard": ["mercenary", "commando", "heal", "merc"],
                 "Corruption": ["sorcerer", "sage", "heal", "sorc"],
                 "Darkness": ["assassin", "shadow", "tank", "sin"],
                 "Immortal": ["juggernaut", "guardian", "tank", "jugg"],
                 "Shield Tech": ["powertech", "vanguard", "tank", "pt", "vg"]}
        translations = {"Hatred": "Serenity", "Deception": "Infiltration", "Lightning": "Telekinetics",
                        "Madness": "Balance", "Virulence": "Dirty Fighting", "Engineering": "Saboteur",
                        "Marksman": "Sharpshooter", "Concealment": "Scrapper", "Lethality": "Ruffian",
                        "Fury": "Concentration", "Carnage": "Combat", "Annihilation": "Watchman",
                        "Vengeance": "Vigilance", "Rage": "Focus", "Arsenal": "Gunnery",
                        "Innovative Ordinance": "Assault Specialist", "Advanced Prototype": "Tactics",
                        "Pyrotech": "Plasmatech", "Medicine": "Sawbones", "Bodyguard": "Combat Medic",
                        "Corruption": "Seer", "Darkness": "Kinetic Combat", "Immortal": "Defense",
                        "Shield Tech": "Shield Specialist"}

        select = []
        if tag in ["all", "a"]:
            select = list(specs.keys())
        else:
            for spec in specs.keys():
                if tag.lower() in specs[spec]:
                    select.append(spec)
            if not select:
                await ctx.send("There are no results found with that tag.")
                return
        chosen = choice(select)
        if side.lower() in ["rep", "pub", "r", "republic"]:
            chosen = translations[chosen]
        await ctx.send(f"The spec chosen is: {chosen}")

    @command()
    async def op_codes(self, ctx: context):
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_swtor_channel(ctx.channel.id, config):
            return
        msg = ""
        for op in self.operations.keys():
            msg += f"{op.capitalize()}: {self.operations[op]}\n"
        await ctx.send(msg)

    @command(aliases=["guide"])
    async def command_guide(self, ctx: context):
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_swtor_channel(ctx.channel.id, config):
            return
        await ctx.send("A full guide to all bot commands is here: "
                       "https://github.com/Maskonk/SWTOR_Op_Bot/wiki/Operation-Commands.")

    @command()
    async def ask(self, ctx: context, *question) -> None:
        """
        8-ball style command. Ask a question and it will gives a response.
        :param question:  The question asked.
        """
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_swtor_channel(ctx.channel.id, config):
            return
        responses = ["Don't count on it.", "The Dark Council have decreed so.", "Only if you want it bad enough.",
                     "My sources say no.", "Very doubtful.", "Outlook not so good.", "Ask again later.",
                     "Try asking your GM.", "Better not tell you now.", "Reply hazy try again.", "Outlook good.",
                     "You are not supposed to know that yet.", "Most likely",
                     "Please contact your Republic Senator for more information this query.",
                     "Of the 14,000,605 possible futures I saw only one it occurred.",
                     "You are more likely to win the lottery", "The answers lies inside of yourself.",
                     "The answer to that question is the same as the answer to Will people ever stop bugging me "
                     "with question? All times of day and night I get these random ass question, Who the fuck wants to "
                     "know if they should have toast for breakfast at four in the bloody morning!",
                     "New phone who's this?", "The answer guys on the shitter at the moment can I take a message?",
                     "Only if Gatters says yes.", "How much are you willing to pay for an answer?",
                     "You have reached the wrong number please hang up and try again."]
        responses += config.get("Ask", [])
        await ctx.send(f"Oh magic ball {' '.join(question)}\nThe magic ball says:\n{choice(responses)}")

    @command()
    async def excuse(self, ctx: context, subject: str = "attend") -> None:
        """
        Provides an silly excuse for not attending a session.
        """
        config = self.config.get(str(ctx.guild.id), {})
        if not await Validators.validate_swtor_channel(ctx.channel.id, config):
            return
        excuse_list = {
            "attend": {"opening": "I can't make it", "excuses": [
                "my sister's boyfriend's neighbour's best friend's duck died, they are giving it a Viking funeral.",
                "my electricity provider decided to be greener so cut all power it gets from "
                "fossil fuels. Unfortunately this means they can't power as many homes including mine.",
                "a goose stole my PCs power cable.",
                "I am pretty sure assassins are after me so I have to go into hiding.",
                "my brother joined a cult that worships Gatters as their deity, I have to go shock him to his senses.",
                "my religion believes that the world ends next week and it is my duty to make as much chaos and "
                "mayhem as I can, so that even if it doesn't it looks like it has.", "I am too busy farming credits.",
                "I am partying in my stronghold with some Twi'lek dancers.",
                "my slave rebelled and now I can't find my gear.", "I have become a toxic PvPer now.",
                "this GF PuG I am in can't kill this boss.", "there is no one to carry me.",
                "the latest bug prevents me joining.", "I bought all the Operation achievements I missed and am now "
                "looking for a NiM Dxun group since my achievements say I am a pro NiM player.", "I'm quiting SWTOR.",
                "I am too busy dummy parsing."]},
            "dps": {"opening": "My numbers are low because", "excuses": ["I was doing mechanics.", "I'm not Qdobs.",
                                                                         "I had to move.", "I'm a clicker.",
                                                                         "my keybinds are messed up.",
                                                                         "someone ninja pulled", "I'm a healer.",
                                                                         "It was Story mode, who cares?"]},
            "heal": {"opening": "I couldn't heal you because", "excuses": ["I don't like you.",
                                                                           "I asked the other healer to do it, blame "
                                                                           "them.", "you were line of sighting me.",
                                                                           "I'm a Sniper."]},
            "agro": {"opening": "I lost agro because", "excuses": ["someone ninja pulled.", "my taunt was on cooldown.",
                                                                   "the Marauder taunted.", "the Sorc pulled me.",
                                                                   "my co-tank is sabotaging me.",
                                                                   "Jonas wasn't my co-tank.", "I'm a DPS", ]}}
        opener = excuse_list.get(subject.lower(), {}).get("opening", [])
        excuses = excuse_list.get(subject.lower(), {}).get("excuses", [])
        excuses += config.get("Excuses", {}).get(subject.lower(), [])
        if excuses:
            await ctx.send(f"{opener} {choice(excuses)}")
        else:
            await ctx.send("There are not excuses for that.")
