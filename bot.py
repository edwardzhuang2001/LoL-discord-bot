import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')
TOKEN = ''

@client.event
async def on_ready():
    print("Online.")

@client.command()
async def opgg(ctx, *, username):
    username = username.replace(' ', '%20')
    await ctx.send(f'https://na.op.gg/summoner/userName={username}')

client.run(TOKEN)