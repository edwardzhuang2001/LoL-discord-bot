import discord
from discord.ext import commands
import os
import requests
import json

RIOT_TOKEN = os.getenv('RIOT_TOKEN')


# currently everything is only for NA server
class LoL(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        r = requests.get(f'https://na1.api.riotgames.com/lol/status/v4/platform-data?api_key={RIOT_TOKEN}')
        print(r.status_code)

    @commands.command()
    async def opgg(self, ctx, *, username):
        username = username.replace(' ', '%20')
        await ctx.send(f'https://na.op.gg/summoner/userName={username}')

    @commands.command()
    async def profile(self, ctx, *, username):

        username = username.replace(' ', '%20')

        r = requests.get(f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={RIOT_TOKEN}')

        summoner_data = json.loads(r.text)
        summoner_id = summoner_data['id']
        summoner_level = 'Level ' + str(summoner_data['summonerLevel'])
        summoner_name = summoner_data['name']
        profile_icon = summoner_data['profileIconId']

        r = requests.get(f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={RIOT_TOKEN}')

        ranked_data = json.loads(r.text)
        ranked_solo_rank = ranked_data[0]['tier'] + ' ' + \
            ranked_data[0]['rank'] + ' ' + \
            str(ranked_data[0]['leaguePoints']) + ' ' + 'LP'
        ranked_solo_winloss = str(ranked_data[0]['wins']) + '/' + str(ranked_data[0]['losses'])
        ranked_solo_winrate = str(round(ranked_data[0]['wins'] / (ranked_data[0]['wins'] + ranked_data[0]['losses']) * 100)) + '%'
        ranked_flex_rank = ranked_data[1]['tier'] + ' ' + \
            ranked_data[1]['rank'] + ' ' + \
            str(ranked_data[1]['leaguePoints']) + ' ' + 'LP'
        ranked_flex_winloss = str(ranked_data[1]['wins']) + '/' + str(ranked_data[1]['losses'])
        ranked_flex_winrate = str(round(ranked_data[1]['wins'] / (ranked_data[1]['wins'] + ranked_data[1]['losses']) * 100)) + '%'

        r = requests.get(f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={RIOT_TOKEN}')

        champion_mastery_data = json.loads(r.text)
        champion_mastery_ids = [champion_mastery_data[i]['championId'] for i in range(5)]
        champion_mastery_names = []

        r = requests.get('http://ddragon.leagueoflegends.com/cdn/11.7.1/data/en_US/champion.json')

        champion_data = json.loads(r.text)['data']

        for i in range(5):
            for champion in champion_data:
                if champion_mastery_ids[i] == int(champion_data[champion]['key']):
                    champion_mastery_names.append(champion_data[champion]['name'])

        embed = discord.Embed(description=summoner_level, colour=0x800080)
        embed.set_author(name=summoner_name, icon_url=f'http://ddragon.leagueoflegends.com/cdn/11.7.1/img/profileicon/{profile_icon}.png')

        embed.add_field(name='Ranked Solo', value=ranked_solo_rank, inline=True)
        embed.add_field(name='Winrate', value=ranked_solo_winrate, inline=True)
        embed.add_field(name='Wins/Losses', value=ranked_solo_winloss, inline=True)

        embed.add_field(name='Ranked Flex', value=ranked_flex_rank, inline=True)
        embed.add_field(name='Winrate', value=ranked_flex_winrate, inline=True)
        embed.add_field(name='Wins/Losses', value=ranked_flex_winloss, inline=True)

        embed.add_field(name='Highest Mastery Champions', value=champion_mastery_names[0] + ', ' + \
            champion_mastery_names[1] + ', ' + \
            champion_mastery_names[2] + ', ' + \
            champion_mastery_names[3] + ', ' + \
            champion_mastery_names[4], inline=True)
        if summoner_name == 'AIready':
            embed.set_image(url=f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion_mastery_names[0]}_0.jpg')
        else:
            embed.set_image(url=f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Tryndamere_1.jpg')

        await ctx.send(embed=embed)

    # @commands.command()
    # async def live(self, ctx, *, username):
    #     await ctx.send()

    # @commands.command()
    # async def recent(self, ctx, *, username):
    #     await ctx.send()

    # @commands.command()
    # async def champion_mastery(self, ctx, *, username):
    #     await ctx.send()


def setup(client):
    client.add_cog(LoL(client))
