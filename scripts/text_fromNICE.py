# Function to scrape text from each NICE url
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive'
}

def text_fromNICE(Nice_url_list):
    nice_text_dict = {}

    for NICE_url in Nice_url_list:
        try:
            # Send the request and parse the response
            nice_response = requests.get(NICE_url, headers=headers, timeout=(3.05, 27))
            nice_response.encoding = 'utf-8'
            nice_soup = BeautifulSoup(nice_response.text, 'html.parser')

            # Extract the text content from the NICE page
            nice_text = nice_soup.get_text(separator=' ', strip=True)

            # Store the text in the dictionary with the corresponding URL
            nice_text_dict[NICE_url] = nice_text

        except Exception as e:
            print(f"Error processing {NICE_url}: {e}")
            # Store an error message in the dictionary in case of failure
            nice_text_dict[NICE_url] = "Error fetching or processing the page"

    return nice_text_dict