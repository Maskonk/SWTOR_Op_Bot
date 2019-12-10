from discord.ext.commands import Bot
from discord import Game
from discord.ext import commands
from src.Cogs.Operations import Operations

bot_prefix = "-"
with open('src/token.txt', 'r') as f:
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
    else:
        print(error)
        await ctx.send("An error has occurred with this command, please try again, if this persists please report it "
                       "to Gatters.")

client.add_cog(Operations(client))
client.run(token)
