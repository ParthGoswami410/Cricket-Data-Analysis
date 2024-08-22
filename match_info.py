import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table_data(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
    
        # Find the table element based on your website's structure
        table = soup.find_all('table')[0] # Adjust this based on the HTML structure

        if table:
            # Extract data from the table
            table_data = []
            rows = table.find_all('tr')

            for row in rows:
                # Extract data from each cell in the row
                cells = row.find_all(['td', 'th'])
                row_data = [cell.text.strip() for cell in cells]
                
                # Extract href from the last column
                last_cell = cells[-1]
                href_value = last_cell.find('a')['href'] if last_cell.find('a') else None
                row_data.append(href_value)
                
                table_data.append(row_data)

            # Create a DataFrame from the table data
            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            df.rename(columns={df.columns[-1]: 'link'}, inplace=True)

            # Concatenate the values from 'Team 1' and 'Team 2' columns with ' vs ' and create a new column 'match'
            df.insert(2, 'match', df['Team 1'] + ' vs ' + df['Team 2'])

            # Concatenate the prefix to the values in the last column
            df['link'] = 'https://www.espncricinfo.com' + df['link']

            return df.dropna()  # Drop rows with None values
        else:
            print('Table not found on the page.')
            return None
    else:
        print(f'Error {response.status_code}: Failed to retrieve the page.')
        return None

# Example usage:
url = 'https://www.espncricinfo.com/records/tournament/team-match-results/icc-cricket-world-cup-2023-24-15338'  # Replace with the actual URL
result_df = scrape_table_data(url)

# Convert the DataFrame to JSON
if result_df is not None:
    result_df.to_json('match_info.json')
    print('match_info successfully created')