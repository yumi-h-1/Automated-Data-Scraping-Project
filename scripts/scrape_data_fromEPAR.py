# Function to scrape the data from EPAR web pages
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive'
}

def scrape_data_fromEPAR(epar_url, product_data, therapy_area_df):
    try:
        epar_response = requests.get(epar_url, headers=headers)
        epar_response.encoding = 'utf-8'
        epar_soup = BeautifulSoup(epar_response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching or processing the EPAR page: {epar_url}. Error: {e}")
        product_data['Therapy class'] = 'N/A'
        product_data['Cancer'] = 'No'
        product_data['Therapy Area'] = 'N/A'
        return product_data

    # Find the ATC code and Therapy class
    try:
        atc_code_tag = epar_soup.find('dt', string=re.compile(r'Anatomical therapeutic chemical \(ATC\) code'))
        if atc_code_tag:
            atc_code = atc_code_tag.find_next('dd').get_text(strip=True)
            therapy_class = atc_code[:3]  # Only take the first three characters
            product_data['Therapy class'] = therapy_class
        else:
            # If there is no ATC code in the EPAR page, extract the code from the medicine sheet
            code_column = ['Pharmacotherapeutic group\n(human)']
            sheet_data = scrape_data_fromSHEET(product_data['Product Name'], df, code_column)

            if sheet_data and sheet_data.get('Pharmacotherapeutic group\n(human)'):
                therapy_class = sheet_data['Pharmacotherapeutic group\n(human)']
                product_data['Therapy class'] = therapy_class
            else:
                therapy_class = 'N/A'
                product_data['Therapy class'] = therapy_class
    except Exception as e:
        print(f"Error extracting ATC code or Therapy class for {epar_url}: {e}")
        product_data['Therapy class'] = 'N/A'

    # Determine if it's related to cancer
    if therapy_class in ['L01', 'L02']:
        product_data['Cancer'] = 'Yes'
    else:
        product_data['Cancer'] = 'No'

    # Match the Therapy Area using the extracted Therapy Class
    therapy_area = scrape_therapy_area(therapy_class, therapy_area_df, 'Therapy Area')
    if therapy_area:
        product_data['Therapy Area'] = therapy_area
    else:
        product_data['Therapy Area'] = 'N/A'

    return product_data