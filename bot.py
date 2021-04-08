# heroku is connected to github
# just push changes to github and they will be live within 5 min

import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='.', help_command=None)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(DISCORD_TOKEN)
