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

client.run(token)