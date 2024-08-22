import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_additional_text(url, selector):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element based on the provided selector
        element = soup.select_one(selector)

        if element:
            # Extract text from the element
            text = element.get_text(strip=True)
            return text
        else:
            print(f'Element not found with selector: {selector}')
            return None
    else:
        print(f'Error {response.status_code}: Failed to retrieve the page.')
        return None



def scrape_table_data(url,table_index):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # Find the table element based on your website's structure
        table = soup.find_all('table')[table_index] # Adjust this based on the HTML structure

        if table:
            # Extract data from the table
            table_data = []
            rows = table.find_all('tr')

            for row in rows:
                # Extract data from each cell in the row
                cells = row.find_all(['td', 'th'])
                row_data = [cell.text.strip() for cell in cells]
                table_data.append(row_data)

            # Create a DataFrame from the table data
            df = pd.DataFrame(table_data[1:], columns=table_data[0])

            df.rename(columns={df.columns[0]: 'bowlerName'}, inplace=True)
            df.rename(columns={df.columns[1]: 'Overs'}, inplace=True)
            df.rename(columns={df.columns[2]: 'Maiden'}, inplace=True)
            df.rename(columns={df.columns[3]: 'Runs'}, inplace=True)
            df.rename(columns={df.columns[4]: 'Wickets'}, inplace=True)
            df.rename(columns={df.columns[5]: 'Economy'}, inplace=True)

            return df.dropna()
            
        else:
            print('Table not found on the page.')
            return None
    else:
        print(f'Error {response.status_code}: Failed to retrieve the page.')
        return None
    

def process_urls_from_json(json_filename):
    # Read URLs and match data from the JSON file
    with open(json_filename, 'r') as json_file:
        data = pd.read_json(json_file, orient='records')

    # Process each URL
    output_list = []  # List to store dictionaries for each iteration
    for index, row in data.iterrows():
        url = row['link']
        match_value = row['match']

        selector = "#main-container > div.ds-relative > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child(2) > div > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize"
        additional_text = scrape_additional_text(url, selector)
        result_df = scrape_table_data(url,1)

        # Add a new column named 'match' at the 1st position and populate it with match values
        if result_df is not None:
            result_df.insert(0, 'match', match_value)

            # Add a new column named 'BattingPos' at the 3rd position and insert numbering

            result_df.insert(1, 'teamInnings', additional_text)

            # Convert DataFrame to list of dictionaries
            output_list.extend(result_df.dropna().to_dict(orient='records'))

    # Write the list of dictionaries to a JSON file
    with open('bowling_info.json', 'w') as json_output_file:
        json.dump(output_list, json_output_file, indent=2)
    
    for index, row in data.iterrows():
        url = row['link']
        match_value = row['match']
        selector = "#main-container > div.ds-relative > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child(3) > div > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize"
        additional_text = scrape_additional_text(url, selector)
        result_df = scrape_table_data(url,3)

        # Add a new column named 'match' at the 1st position and populate it with match values
        if result_df is not None:
            result_df.insert(0, 'match', match_value)

            # Add a new column named 'BattingPos' at the 3rd position and insert numbering

            result_df.insert(1, 'teamInnings', additional_text)

            # Convert DataFrame to list of dictionaries
            output_list.extend(result_df.dropna().to_dict(orient='records'))

    # Write the list of dictionaries to a JSON file
    with open('bowling_info.json', 'w') as json_output_file:
        json.dump(output_list, json_output_file, indent=2)
# Example usage:
json_filename = 'match_info.json'  # Replace with the actual JSON file containing URLs and match data
process_urls_from_json(json_filename)
