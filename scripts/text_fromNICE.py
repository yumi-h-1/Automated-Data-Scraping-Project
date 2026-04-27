import requests
from bs4 import BeautifulSoup
from config import headers


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