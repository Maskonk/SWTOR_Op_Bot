from discord.ext.commands import Bot
from discord import Game
from discord.ext import commands
from src.Cogs.Operations import Operations

bot_prefix = "-"
with open('./token.txt', 'r') as f:
    token = f.read()

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
    await ctx.send("The code for this bot is not currently available at this time but will be uploaded soon.")

@client.event
async def on_reaction_add(reaction, user):
    print(reaction.message)

client.add_cog(Operations(client))
client.run(token)
