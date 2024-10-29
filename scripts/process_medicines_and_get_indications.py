# Function to find the full indication using the query
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive'
}

def process_medicines_and_get_indications(epar_urls):
    indications_dict = {}  # Dictionary to store indications for each URL

    # Loop over each URL
    for epar_url in epar_urls:
        try:
            response = requests.get(epar_url, headers=headers, timeout=(3.05, 27))
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            html_content = soup.prettify()

            # Query the model with the individual HTML content
            indication = query_model_for_indication(html_content)

            # Store the indication in the dictionary with the URL as its key
            indications_dict[epar_url] = indication

        except Exception as e:
            print(f"Error processing {epar_url}: {e}")
            indications_dict[epar_url] = "Error fetching or processing the page"

    return indications_dict