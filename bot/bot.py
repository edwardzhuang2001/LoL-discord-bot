import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '.')
TOKEN = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game("Listening to .opgg username"))
    print("Online.")

@client.command()
async def opgg(ctx, *, username):
    username = username.replace(' ', '%20')
    await ctx.send(f'https://na.op.gg/summoner/userName={username}')

@client.command()
async def profile(ctx, *, username):
    await ctx.send()

@client.command()
async def recent(ctx, *, username):
    await ctx.send()

@client.command()
async def live(ctx, *, username):
    await ctx.send()

client.run(TOKEN)