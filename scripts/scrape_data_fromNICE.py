# Function to scrape data from the NICE web page using INN
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive'
}

def scrape_data_fromNICE(nice_url, product_data):
    nice_response = requests.get(nice_url, headers=headers)
    nice_response.encoding = 'utf-8'
    nice_soup = BeautifulSoup(nice_response.text, 'html.parser')

    # Extract the title of the webpage
    try:
        title_tag = nice_soup.find('title')
        title_text = title_tag.get_text(strip=True) if title_tag else ''
    except Exception as e:
        print(f"Error extracting title from NICE page: {nice_url}. Error: {e}")
        product_data['NICE'] = 'N/A'
        return product_data

    # Check if the title indicates no results
    if "No results" in title_text:
        product_data['NICE'] = 'N/A'
    else:
        try:
            # Extract the medicine name from the title (the part before the first '|')
            inn_common_name = title_text.split('|')[0].strip()

            # Match the extracted name with the original INN from product_data
            if re.search(re.escape(product_data['INN']), inn_common_name, re.IGNORECASE):
                product_data['NICE'] = 'Yes'
            else:
                product_data['NICE'] = 'No'
        except Exception as e:
            print(f"Error processing INN matching for NICE page: {nice_url}. Error: {e}")
            product_data['NICE'] = 'N/A'

    return product_data