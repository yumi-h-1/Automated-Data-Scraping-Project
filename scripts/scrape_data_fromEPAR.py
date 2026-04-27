import re
import requests
from bs4 import BeautifulSoup
from config import headers
from scrape_data_fromSHEET import scrape_data_fromSHEET
from scrape_therapy_area import scrape_therapy_area


def scrape_data_fromEPAR(epar_url, product_data, therapy_area_df, df):
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

    therapy_class = 'N/A'
    try:
        atc_code_tag = epar_soup.find('dt', string=re.compile(r'Anatomical therapeutic chemical \(ATC\) code'))
        if atc_code_tag:
            atc_code = atc_code_tag.find_next('dd').get_text(strip=True)
            therapy_class = atc_code[:3]
            product_data['Therapy class'] = therapy_class
        else:
            code_column = ['Pharmacotherapeutic group\n(human)']
            sheet_data = scrape_data_fromSHEET(product_data['Product Name'], df, code_column)
            if sheet_data and sheet_data.get('Pharmacotherapeutic group\n(human)'):
                therapy_class = sheet_data['Pharmacotherapeutic group\n(human)']
                product_data['Therapy class'] = therapy_class
            else:
                product_data['Therapy class'] = 'N/A'
    except Exception as e:
        print(f"Error extracting ATC code or Therapy class for {epar_url}: {e}")
        product_data['Therapy class'] = 'N/A'

    product_data['Cancer'] = 'Yes' if therapy_class in ['L01', 'L02'] else 'No'

    therapy_area = scrape_therapy_area(therapy_class, therapy_area_df, 'Therapy Area')
    product_data['Therapy Area'] = therapy_area if therapy_area else 'N/A'

    return product_data