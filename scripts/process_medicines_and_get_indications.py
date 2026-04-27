import requests
from bs4 import BeautifulSoup
from config import headers
from query_model_for_indication import query_model_for_indication


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