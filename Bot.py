from discord.ext.commands import Bot
from discord import Game
from discord.ext import commands
from json import load

bot_prefix = "-"
with open('token.txt', 'r') as f:
    token = f.read()

client = Bot(command_prefix=bot_prefix)

@client.event
async def on_ready():
    await client.change_presence(activity=Game(name='SWTOR'))
    print("Online")

@client.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send("An error has occurred with this command, please try again, if this persists please report it "
                   "to Gatters.")

client.run(token)