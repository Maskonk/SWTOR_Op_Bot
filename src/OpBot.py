from discord.ext.commands import Bot
from discord import Game
from discord.ext import commands
from Cogs.Operations import Operations
from Cogs.Swtor import Swtor
from json import load
from Utils.ReactionUtils import find_operation_by_id, check_valid_reaction

bot_prefix = "-"
with open('./token.txt', 'r') as f:
    token = f.read()

with open('./Ops.json', 'r') as f:
    ops = load(f)

client = Bot(command_prefix=bot_prefix)


@client.event
async def on_ready():
    await client.change_presence(activity=Game(name='SWTOR'))
    print("Online")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
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


@client.event
async def on_raw_reaction_add(payload):
    """
    Runs when a reaction is added to a message. Used for reaction based sign ups.
    """
    op = await find_operation_by_id(ops, payload.guild_id, payload.message_id)
    if not op:
        return
    role = await check_valid_reaction(payload.emoji.name)
    print(role)

client.add_cog(Operations(client, ops))
client.add_cog(Swtor(client))
client.run(token)
