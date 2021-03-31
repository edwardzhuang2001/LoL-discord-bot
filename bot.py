import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')
token = ''

@client.event
async def on_ready():
    print("Online.")

client.run(token)