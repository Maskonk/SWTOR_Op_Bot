from discord.ext.commands import Bot
from discord import Game, Intents
from discord.ext import commands
from Cogs.Operations import Operations
from Cogs.Swtor import Swtor
from json import load
from Utils.ReactionUtils import *

bot_prefix = "-"
with open('./token.txt', 'r') as f:
    token = f.read()

with open('./Ops.json', 'r') as f:
    ops = load(f)

with open('./config.json', 'r') as f:
    config = load(f)

intents = Intents.default()
intents.members = True
client = Bot(command_prefix=bot_prefix, intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=Game(name='SWTOR'))
    print("Online")


@client.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("That is not a valid command. Please use **.help** for a list of all commands.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You are not authorized to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You have missed {error.param} from the command. Use .help <command_name> for exactly "
                       f"what is required.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("The bot does not currently have permissions to perform this action.")
    else:
        print(error)
        await ctx.send("An error has occurred with this command, please try again, if this persists please report it "
                       "to Gatters.")


@client.command(aliases=["code", "Code"])
async def github(ctx):
    """Link to the github repo for this bot."""
    await ctx.send("The bot is written in Python using the discord.py framework. The code is available here: "
                   "https://github.com/Maskonk/SWTOR_Op_Bot")

client.add_cog(Operations(client, ops, config))
client.add_cog(Swtor(client, config))
client.run(token)
