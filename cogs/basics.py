import discord
from discord.ext import commands


class Basics(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity = discord.Game('.help for a list of available commands'))
        print("Online.")

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title = 'Rift Herald Help', description = 'Type .help <command> to find out more about a command.', colour = 0x800080)
        embed.add_field(name = 'Commands', value = '`help`,`opgg`,`profile`')
        
        await ctx.send(embed = embed)

    @commands.command()
    async def servers(self, ctx):
        servers = []
        count = 0
        
        for guild in self.client.guilds:
            servers.append(guild.name)
            count += 1

        await ctx.send([count, servers])


def setup(client):
    client.add_cog(Basics(client))