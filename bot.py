import discord
from discord import app_commands
import asyncio
from dotenv import load_dotenv
import os
import Tools.database as database

# Load environment variables
load_dotenv('token.env')

# Retrieve the bot token and channel ID from the environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
channel_id = os.getenv('CHANNEL_ID')

# Set up intents for the bot
intents = discord.Intents.default()
intents.messages = True 
client = discord.Client(intents=intents)

# Initialize the command tree for the client
tree = app_commands.CommandTree(client)
    

@tree.command(name="news", description="Get news about Val stuff idk")
async def slash_command(interaction: discord.Interaction, number_of_articles: app_commands.Range[int, 1, 10] = 3):    
    await interaction.response.defer()
    await database.send_news_embed(interaction, number_of_articles)  

@tree.command(name="upcoming_matches", description="Get info abt upcoming matches likely won't work :D")
async def slash_command(interaction: discord.Interaction, number_of_games: app_commands.Range[int, 1, 10] = 3):    
    await interaction.response.defer()
    await database.send_upcoming_games_embed(interaction, number_of_games)
    
@tree.command(name="player_info", description="Get info abt a specific player")
async def slash_command(interaction: discord.Interaction, player_name: str = "TenZ", region: str = "na"):    
    await interaction.response.defer()
    await database.send_player_embed(interaction, player_name, region) 

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event 
async def on_message(message):
    if message.author == client.user:
        return
    
    # if str(message.channel.id) == str(channel_id):
    #     await message.channel.send('Hello!')

async def setup():
    # Sync to a specfic guild
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    await tree.sync()

client.setup_hook = setup

client.run(BOT_TOKEN)
