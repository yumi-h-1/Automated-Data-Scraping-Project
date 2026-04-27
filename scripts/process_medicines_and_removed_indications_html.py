import requests
from bs4 import BeautifulSoup
from config import headers
from query_model_for_removed_indication_html import query_model_for_removed_indication_html


def process_medicines_and_removed_indications_html(variation_urls):
    removed_indications_dict = {}

    for variation_url in variation_urls:
        try:
            response = requests.get(variation_url, headers=headers, timeout=(3.05, 27))
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            html_content = soup.prettify()

            removed_indications = query_model_for_removed_indication_html(html_content)
            removed_indications_dict[variation_url] = removed_indications

        except Exception as e:
            print(f"Error processing {variation_url}: {e}")
            removed_indications_dict[variation_url] = "Error fetching or processing the page"

    return removed_indications_dict