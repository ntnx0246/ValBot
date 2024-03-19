import requests
import asyncio
import io
import aiohttp
import discord

API_URL = "https://vlrggapi.vercel.app/"


async def get_news_json():
    async with aiohttp.ClientSession() as session:  
        async with session.get(f"{API_URL}/news") as response:
            json = await response.json()
    return json

async def get_games_json():
    async with aiohttp.ClientSession() as session:  
        async with session.get(f"{API_URL}/match/upcoming") as response:
            json = await response.json()
    return json

async def get_player_json(region: str):
    async with aiohttp.ClientSession() as session:  
        async with session.get(f"{API_URL}/stats/{region}/99999") as response:
            json = await response.json()
    return json


async def send_news_embed(interaction: discord.Interaction, number_of_articles: int):
    news_data = await get_news_json()
    news_items = news_data['data']['segments'][:number_of_articles]  # Get the first 5 news items

    embeds = []
    for item in news_items:
        embed = discord.Embed(
            title=item['title'],
            description=item['description'],
            color=discord.Color.blue()
        )
        embed.set_author(name=item['author'])
        embed.add_field(name="Date", value=item['date'], inline=False)
        embed.add_field(name="Read More", value=f"[Click Here](https://vlr.gg{item['url_path']})", inline=False)
        embeds.append(embed)

    # Send the embeds in separate messages
    for embed in embeds:
        await interaction.followup.send(embed=embed)
    
async def send_upcoming_games_embed(interaction: discord.Interaction, number_of_games: int):
    games_data = await get_games_json()
    games = games_data['data']['segments'][:number_of_games] 

    embeds = []
    for game in games:
        embed = discord.Embed(
            title=game['team1'] + ' ' + game['score1'] + " vs " + game['team2'] + ' ' + game['score2'],
            description="Time Until Match: " + game['time_until_match'],
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=game['tournament_icon'])
        embed.set_footer(text="Tournament Name " + game['tournament_name'] + " Round Info " + game['round_info'])
        embed.add_field(name="Match Link", value=f"[Click Here](https://vlr.gg{game['match_page']})", inline=False)
        embeds.append(embed)

    # Send the embeds in separate messages
    for embed in embeds:
        await interaction.followup.send(embed=embed)
        
async def send_player_embed(interaction: discord.Interaction, player_name: str, region: str):
    player_data = await get_player_json(region)
    # print(player_data)
    # try:
    player_list = player_data['data']['segments']
    for player in player_list:
        print(player)
        if player['player'] == player_name:
            embed = discord.Embed(
            title=player['player'],
            description="Org: " + player['org'] + " Acs: " + player['kill_deaths'] + " K/D: " + player['average_combat_score'] + " ADR: " + player['kills_per_round'] + " KPR: " + player['assists_per_round'] + " FKPR: " + player['first_deaths_per_round'] + " FDPR: " + player['headshot_percentage'] + " HS%: " + player['clutch_success_percentage'],
            color=discord.Color.blue()
            )
        await interaction.followup.send(embed=embed)
            
    # except:
    #     await interaction.followup.send("Player not found (I will try to fix this so it does not happen but make sure player name and region is spelled correctly)")
    #     return