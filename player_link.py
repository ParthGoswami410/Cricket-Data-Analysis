import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

def get_cricketer_links(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        cricketer_links = set()  # Use a set to store unique links
        for link in soup.find_all('a', href=True):
            href_value = link.get('href')
            if href_value.startswith('/cricketers/'):
                full_url = urljoin(url, href_value)
                cricketer_links.add(full_url)
                
        print(cricketer_links)
        return cricketer_links
    else:
        print(f"Failed to fetch data for URL: {url}. Status code: {response.status_code}")
        return None

def process_json_file(json_file_path, output_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    unique_cricketer_links = set()  # Use a set to store unique cricketer links

    for row in data:
        last_column_value = row['link']  # Assuming the last column contains the URLs
        cricketer_links = get_cricketer_links(last_column_value)

        if cricketer_links:
            for link in cricketer_links:
                if link not in unique_cricketer_links:
                    unique_cricketer_links.add(link)

    # Convert set to a list and write to a JSON file
    unique_links_list = list(unique_cricketer_links)
    with open(output_file_path, 'w') as json_file:
        json.dump(unique_links_list, json_file, indent=2)

# Example usage
json_file_path = 'link_info.json'  # Replace with your JSON file path
output_file_path = 'cricketer_links.json'  # Replace with desired output file path
process_json_file(json_file_path, output_file_path)
