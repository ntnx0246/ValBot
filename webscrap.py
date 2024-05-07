from bs4 import BeautifulSoup
import requests

# Define the URL of the page to scrape
url = 'https://www.vlr.gg/314647/nrg-esports-vs-evil-geniuses-champions-tour-2024-americas-stage-1-w4'

# Fetch the content from the URL
response = requests.get(url)
response.raise_for_status()  # Raises an HTTPError for bad responses

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the container
stats_game = soup.find('div', {'class': 'vm-stats-game mod-active', 'data-game-id': 'all'})

if stats_game:
    # Extract player data
    players = stats_game.find_all('tr')

    for player in players:
        name_tag = player.find('td', class_='mod-player')
        kills_tag = player.find('td', class_='mod-vlr-kills')

        if name_tag and kills_tag:
            # Clean the name to only include the first word (assumes first word is the player name)
            name = ' '.join(name_tag.text.strip().split())  # Clean up name to remove extra spaces
            player_name = name.split()[0]  # Assuming the first word is the player's name without org
            kills = ' '.join(kills_tag.text.strip().split()).split()[0]  # Clean up and take the top kill count
            print(f"{player_name}: {kills} kills")
else:
    print("Stats section not found on the page.")
