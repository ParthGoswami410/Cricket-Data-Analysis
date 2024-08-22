######### match_info csv 

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')[0]

        if table:
            table_data = []
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = [cell.text.strip() for cell in cells]

                last_cell = cells[-1]
                href_value = last_cell.find('a')['href'] if last_cell.find('a') else None
                row_data.append(href_value)

                table_data.append(row_data)

            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            df.rename(columns={df.columns[-1]: 'link'}, inplace=True)
            df.insert(2, 'match', df['Team 1'] + ' vs ' + df['Team 2'])
            df['link'] = 'https://www.espncricinfo.com' + df['link']

            # Save the DataFrame to a CSV file
            df.to_csv('match_info.csv', index=False)

            return df.dropna()
        else:
            print('Table not found on the page.')
            return None
    else:
        print(f'Error {response.status_code}: Failed to retrieve the page.')
        return None

# Example usage:
url = 'https://www.espncricinfo.com/records/tournament/team-match-results/icc-cricket-world-cup-2023-24-15338'
result_df = scrape_table_data(url)

# Check if DataFrame is not None and has data
if result_df is not None and not result_df.empty:
    print('match_info.csv successfully created')
else:
    print('Failed to create match_info.csv')
