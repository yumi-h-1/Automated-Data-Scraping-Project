import requests
from bs4 import BeautifulSoup
from config import headers
from query_model_for_new_indication_html import query_model_for_new_indication_html


def process_medicines_and_new_indications_html(variation_urls):
    new_indications_dict = {}  # Dictionary to store indications for each URL

    # Loop over each URL
    for variation_url in variation_urls:
        try:
            response = requests.get(variation_url, headers=headers, timeout=(3.05, 27))
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            html_content = soup.prettify()

            # Query the model with the individual HTML content
            new_indication = query_model_for_new_indication_html(html_content)

            # Store the indication in the dictionary with the URL as its key
            new_indications_dict[variation_url] = new_indication

        except Exception as e:
            print(f"Error processing {variation_url}: {e}")
            new_indications_dict[variation_url] = "Error fetching or processing the page"

    return new_indications_dict