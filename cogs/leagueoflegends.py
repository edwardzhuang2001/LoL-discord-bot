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

        try:
            if ranked_data[0]['queueType'] == 'RANKED_SOLO_5x5':
                try:
                    ranked_solo_rank = ranked_data[0]['tier'] + ' ' + \
                        ranked_data[0]['rank'] + ' ' + \
                        str(ranked_data[0]['leaguePoints']) + ' ' + 'LP'
                    ranked_solo_winloss = str(ranked_data[0]['wins']) + '/' + str(ranked_data[0]['losses'])
                    ranked_solo_winrate = str(round(ranked_data[0]['wins'] / (ranked_data[0]['wins'] + ranked_data[0]['losses']) * 100)) + '%'
                except:
                    ranked_solo_rank = '---'
                    ranked_solo_winloss = '---'
                    ranked_solo_winrate = '---'

                try:
                    ranked_flex_rank = ranked_data[1]['tier'] + ' ' + \
                        ranked_data[1]['rank'] + ' ' + \
                        str(ranked_data[1]['leaguePoints']) + ' ' + 'LP'
                    ranked_flex_winloss = str(ranked_data[1]['wins']) + '/' + str(ranked_data[1]['losses'])
                    ranked_flex_winrate = str(round(ranked_data[1]['wins'] / (ranked_data[1]['wins'] + ranked_data[1]['losses']) * 100)) + '%'
                except:
                    ranked_flex_rank = '---'
                    ranked_flex_winloss = '---'
                    ranked_flex_winrate = '---'
            elif ranked_data[0]['queueType'] == 'RANKED_FLEX_SR':
                try:
                    ranked_solo_rank = ranked_data[1]['tier'] + ' ' + \
                        ranked_data[1]['rank'] + ' ' + \
                        str(ranked_data[1]['leaguePoints']) + ' ' + 'LP'
                    ranked_solo_winloss = str(ranked_data[1]['wins']) + '/' + str(ranked_data[1]['losses'])
                    ranked_solo_winrate = str(round(ranked_data[1]['wins'] / (ranked_data[1]['wins'] + ranked_data[1]['losses']) * 100)) + '%'
                except:
                    ranked_solo_rank = '---'
                    ranked_solo_winloss = '---'
                    ranked_solo_winrate = '---'

                try:
                    ranked_flex_rank = ranked_data[0]['tier'] + ' ' + \
                        ranked_data[0]['rank'] + ' ' + \
                        str(ranked_data[0]['leaguePoints']) + ' ' + 'LP'
                    ranked_flex_winloss = str(ranked_data[0]['wins']) + '/' + str(ranked_data[0]['losses'])
                    ranked_flex_winrate = str(round(ranked_data[0]['wins'] / (ranked_data[0]['wins'] + ranked_data[0]['losses']) * 100)) + '%'
                except:
                    ranked_flex_rank = '---'
                    ranked_flex_winloss = '---'
                    ranked_flex_winrate = '---'
        except:
            ranked_solo_rank = '---'
            ranked_solo_winloss = '---'
            ranked_solo_winrate = '---'
            ranked_flex_rank = '---'
            ranked_flex_winloss = '---'
            ranked_flex_winrate = '---'
            highest_rank_emblem = 'https://i.imgur.com/boyn68O.png'

        try:
            if ranked_solo_rank.split()[0] == 'CHALLENGER' or ranked_flex_rank.split()[0] == 'CHALLENGER':
                highest_rank_emblem = 'https://i.imgur.com/mS3O3lO.png'
            elif ranked_solo_rank.split()[0] == 'GRANDMASTER' or ranked_flex_rank.split()[0] == 'GRANDMASTER':
                highest_rank_emblem = 'https://i.imgur.com/My23dLO.png'
            elif ranked_solo_rank.split()[0] == 'MASTER' or ranked_flex_rank.split()[0] == 'MASTER':
                highest_rank_emblem = 'https://i.imgur.com/OVBHr69.png'
            elif ranked_solo_rank.split()[0] == 'DIAMOND' or ranked_flex_rank.split()[0] == 'DIAMOND':
                highest_rank_emblem = 'https://i.imgur.com/a4sMR4R.png'
            elif ranked_solo_rank.split()[0] == 'PLATINUM' or ranked_flex_rank.split()[0] == 'PLATINUM':
                highest_rank_emblem = 'https://i.imgur.com/8xizso8.png'
            elif ranked_solo_rank.split()[0] == 'GOLD' or ranked_flex_rank.split()[0] == 'GOLD':
                highest_rank_emblem = 'https://i.imgur.com/9w9eA7u.png'
            elif ranked_solo_rank.split()[0] == 'SILVER' or ranked_flex_rank.split()[0] == 'SILVER':
                highest_rank_emblem = 'https://i.imgur.com/0YqAEEk.png'
            elif ranked_solo_rank.split()[0] == 'BRONZE' or ranked_flex_rank.split()[0] == 'BRONZE':
                highest_rank_emblem = 'https://i.imgur.com/O8OmrdJ.png'
            elif ranked_solo_rank.split()[0] == 'IRON' or ranked_flex_rank.split()[0] == 'IRON':
                highest_rank_emblem = 'https://i.imgur.com/299uEYM.png'
        except:
            pass

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
        embed.set_thumbnail(url=highest_rank_emblem)

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
            embed.set_image(url=f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Tryndamere_1.jpg')
        else:
            embed.set_image(url=f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion_mastery_names[0]}_0.jpg')

        embed.set_footer(text='Information requested by ' + ctx.author.name)

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
