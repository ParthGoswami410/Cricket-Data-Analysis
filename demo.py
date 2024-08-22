import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


def scrape_additional_text(url, selector):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.select_one(selector)

        if element:
            text = element.get_text(strip=True)
            return text
        else:
            print(f'Element not found with selector: {selector}')
            return None
    else:
        print(f'Error {response.status_code}: Failed to retrieve the page.')
        return None


def scrape_table_data(url, table_index):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')[table_index]

        if table:
            table_data = []
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = [cell.text.strip() for cell in cells]
                table_data.append(row_data)

            df = pd.DataFrame(table_data[1:], columns=table_data[0])
            df.rename(columns={df.columns[1]: 'bowler'}, inplace=True)

            return df.dropna()

        else:
            print('Table not found on the page.')
            return None
    else:
        print(f'Error {response.status_code}: Failed to retrieve the page.')
        return None


def process_urls_from_json(json_filename):
    with open(json_filename, 'r') as json_file:
        data = pd.read_json(json_file, orient='records')

    output_list = []

    for index, row in data.iterrows():
        url = row['link']
        match_value = row['match']

        selector1 = "#main-container > div.ds-relative > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child(2) > div > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize"
        selector2 = "#main-container > div.ds-relative > div.lg\:ds-container.lg\:ds-mx-auto.lg\:ds-px-5.lg\:ds-pt-4 > div > div.ds-flex.ds-space-x-5 > div.ds-grow > div.ds-mt-3 > div:nth-child(1) > div:nth-child(3) > div > div.ds-flex.ds-px-4.ds-border-b.ds-border-line.ds-py-3.ds-bg-ui-fill-translucent-hover > div > span > span.ds-text-title-xs.ds-font-bold.ds-capitalize"

        selector = selector1 if index % 2 == 0 else selector2
        additional_text = scrape_additional_text(url, selector)

        table_index = 0 if index % 2 == 0 else 2
        result_df = scrape_table_data(url, table_index)

        if result_df is not None:
            result_df.insert(0, 'match', match_value)
            result_df.insert(2, 'BattingPos', range(1, len(result_df) + 1))
            result_df.insert(1, 'teamInnings', additional_text)

            output_list.extend(result_df.dropna().to_dict(orient='records'))

    with open('batting_info.json', 'w') as json_output_file:
        json.dump(output_list, json_output_file, indent=2)


json_filename = 'match_info.json'
process_urls_from_json(json_filename)
