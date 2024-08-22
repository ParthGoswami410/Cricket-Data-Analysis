import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def get_player_name(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract player name from the title tag
        title_tag = soup.find('title')
        if title_tag:
            player_name = title_tag.text.strip().split('-')[0].strip().replace('-', ' ',).replace('Profile','')
            
            # Remove profile postfix if it exists
            profile_postfix = ' Cricbuzz Profile'
            if player_name.endswith(profile_postfix):
                player_name = player_name[:-len(profile_postfix)].strip()
            
            return player_name
        else:
            print(f"No title tag found for URL: {url}")
            return None
    else:
        print(f"Failed to fetch data for URL: {url}. Status code: {response.status_code}")
        return None

# Read URLs from json file into a DataFrame
with open('cricketer_links.json', 'r') as input_file:
    input_data = json.load(input_file)

# Create an empty DataFrame
df = pd.DataFrame(columns=['URL', 'Player Name'])

# Iterate over each URL in the list
for url in input_data:
    # Proceed if URL is available
    if url:
        # Get player name
        player_name = get_player_name(url)
        
        # Concatenate the DataFrame
        df = pd.concat([df, pd.DataFrame({'URL': [url], 'Player Name': [player_name]})], ignore_index=True)

# Drop duplicates based on 'Player Name'
df = df.drop_duplicates(subset=['Player Name'])

# Convert DataFrame to JSON
json_data = df.to_json(orient='records', indent=2)

# Write the JSON data to a file
with open('unique.json', 'w') as json_file:
    json_file.write(json_data)

print("JSON file with unique data created successfully.")
