import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def scrape_player_info(url, selectors):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        
        player_info = {}
        for key, selector in selectors.items():
            element = soup.select_one(selector)
            value = element.text.strip() if element else 'N/A'
            player_info[key] = value
        
        return player_info
    else:
        print(f"Failed to fetch data for URL: {url}. Status code: {response.status_code}")
        return None

def scrape_from_json_file(json_file_path, selectors):
    with open(json_file_path, 'r') as file:
        urls = json.load(file)

    # Create a list to store player data dictionaries
    player_data_list = []

    for url in urls:
        player_data = scrape_player_info(url['URL'], selectors)

        if player_data:
            # Extract player name from the URL
            player_name = url['Player Name']

            # Append to the list
            player_data_list.append({'Player Name': player_name,
                                     'BATTING_STYLE': player_data['BATTING_STYLE'],
                                     'BOWLING_STYLE': player_data['BOWLING_STYLE'],
                                     'PLAYING_ROLE': player_data['PLAYING_ROLE']})

    # Create the DataFrame from the list
    df = pd.DataFrame(player_data_list)

    return df

# Example usage
json_file_path = 'unique.json'  # Replace with your JSON file path
selectors = {
    'BATTING_STYLE': '#main-container > div.ds-relative > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.ds-pt-4 > div.ds-flex.ds-space-x-5 > div.ds-grow > div:nth-child(2) > div > div > div.ds-grid.lg\:ds-grid-cols-3.ds-grid-cols-2.ds-gap-4.ds-mb-8 > div:nth-child(4) > span',
    'BOWLING_STYLE': '#main-container > div.ds-relative > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.ds-pt-4 > div.ds-flex.ds-space-x-5 > div.ds-grow > div:nth-child(2) > div > div > div.ds-grid.lg\:ds-grid-cols-3.ds-grid-cols-2.ds-gap-4.ds-mb-8 > div:nth-child(5) > span',
    'PLAYING_ROLE': '#main-container > div.ds-relative > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.ds-pt-4 > div.ds-flex.ds-space-x-5 > div.ds-grow > div:nth-child(2) > div > div > div.ds-grid.lg\:ds-grid-cols-3.ds-grid-cols-2.ds-gap-4.ds-mb-8 > div:nth-child(6) > span'
}

df = scrape_from_json_file(json_file_path, selectors)

# Print the DataFrame
print(df)

# Save the DataFrame to a new JSON file
df.to_json('player_info.json', orient='records', indent=2)
