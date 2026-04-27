import re
import requests
from bs4 import BeautifulSoup
from config import headers
from scrape_data_fromEPAR import scrape_data_fromEPAR
from scrape_data_fromNICE import scrape_data_fromNICE
from scrape_data_fromSHEET import scrape_data_fromSHEET
from extract_text_from_pdf import extract_text_from_pdf
from query_model_for_ema_date import query_model_for_ema_date
from query_model_for_new_indication_pdf import query_model_for_new_indication_pdf


def scrape_data_fromMH_with_LLM(newspage_url, pdf_paths, therapy_area_df, df, indications,
                                  variation_urls, new_indications_html, removed_indications_html):
    news_response = requests.get(newspage_url, headers=headers)
    news_response.encoding = 'utf-8'
    news_soup = BeautifulSoup(news_response.text, 'html.parser')

    items = news_soup.find_all('div', class_='item')
    product_data_list = []
    current_recommendation = None

    for item in items:
        try:
            heading_tag = item.find('h2', class_='mb-4 rounded-title')
            if heading_tag:
                heading_text = heading_tag.get_text(strip=True).lower()
                if 'positive recommendations on new medicines' in heading_text:
                    current_recommendation = 'Positive'
                    initial_approval = 'Initial approval'
                elif 'positive recommendations on new therapeutic indications' in heading_text:
                    current_recommendation = 'Positive'
                    initial_approval = 'Extension'
                elif 'positive recommendations on extensions of indications' in heading_text:
                    current_recommendation = 'Positive'
                    initial_approval = 'Extension'
                elif 'positive recommendations on extensions of therapeutic indications' in heading_text:
                    current_recommendation = 'Positive'
                    initial_approval = 'Extension'
                else:
                    current_recommendation = None
                continue

            if current_recommendation != 'Positive':
                continue

            product_name_tag = item.find('h3', class_='mb-4')
            if product_name_tag:
                product_name = product_name_tag.get_text(strip=True).lower().replace(' ', '-')
            else:
                product_name = 'N/A'

            epar_url = f"https://www.ema.europa.eu/en/medicines/human/EPAR/{product_name}"

            matching_variation_urls = [url for url in variation_urls if url.split('/')[-1].startswith(product_name)]
            if not matching_variation_urls:
                matching_variation_urls = [f"https://www.ema.europa.eu/en/medicines/human/variation/{product_name}"]

            product_data = {
                'Product Name': product_name,
                'Recommendation': current_recommendation,
                'Initial Approval': initial_approval,
                'Date for extension': 'N/A',
                'Full indication': 'N/A',
                'New indication HTML': 'N/A',
                'Removed indication HTML': 'N/A',
                'epar_url': epar_url,
                'variation_url': matching_variation_urls
            }

            try:
                product_data = scrape_data_fromEPAR(epar_url, product_data, therapy_area_df, df)
            except Exception as e:
                print(f"Error scraping data from EPAR for {product_name}: {e}")

            product_data['Full indication'] = indications.get(epar_url, 'N/A')

            product_data['New indication HTML'] = ', '.join(
                [new_indications_html.get(url, 'N/A') for url in matching_variation_urls]
            )
            product_data['Removed indication HTML'] = ', '.join(
                [removed_indications_html.get(url, 'N/A') for url in matching_variation_urls]
            )

            inn_tag = item.find('dt', string=re.compile(r'International non-proprietary name \(INN\)|INN'))
            common_name_tag = item.find('dt', string=re.compile(r'Common name'))
            if inn_tag:
                product_data['INN'] = inn_tag.find_next('dd').get_text(strip=True)
                nice_url = f"https://www.nice.org.uk/search?q={product_data['INN']}"
                try:
                    product_data = scrape_data_fromNICE(nice_url, product_data)
                except Exception as e:
                    print(f"Error scraping data from NICE for {product_data['INN']}: {e}")
            elif common_name_tag:
                product_data['INN'] = common_name_tag.find_next('dd').get_text(strip=True)
                nice_url = f"https://www.nice.org.uk/search?q={product_data['INN']}"
                try:
                    product_data = scrape_data_fromNICE(nice_url, product_data)
                except Exception as e:
                    print(f"Error scraping data from NICE for {product_data['INN']}: {e}")
            else:
                product_data['INN'] = 'N/A'

            applicant_tag = item.find('dt', string=re.compile(r'Marketing[- ]authorisation applicant', re.IGNORECASE))
            holder_tag = item.find('dt', string=re.compile(r'Marketing[- ]authorisation holder', re.IGNORECASE))
            if applicant_tag:
                product_data['Marketing authorisation holder'] = applicant_tag.find_next('dd').get_text(strip=True)
            elif holder_tag:
                product_data['Marketing authorisation holder'] = holder_tag.find_next('dd').get_text(strip=True)
            else:
                product_data['Marketing authorisation holder'] = 'N/A'

            dataframe_columns = ['Orphan medicine', 'European Commission decision date']
            try:
                dataframe_data = scrape_data_fromSHEET(product_name, df, dataframe_columns)
                if dataframe_data:
                    product_data.update(dataframe_data)
            except Exception as e:
                print(f"Error matching data from sheet for {product_name}: {e}")

            matching_pdf = next((pdf for pdf in pdf_paths if product_name in pdf.lower()), None)
            if matching_pdf:
                print(f"Processing PDF: {matching_pdf} for product: {product_name}")
                try:
                    pdf_text = extract_text_from_pdf(matching_pdf)
                    ema_date = query_model_for_ema_date(pdf_text)
                    new_indication_pdf = query_model_for_new_indication_pdf(pdf_text)

                    if product_data['Initial Approval'] == 'Extension':
                        product_data['Date for extension'] = ema_date
                        product_data['New indication PDF'] = new_indication_pdf
                    else:
                        product_data['Date for extension'] = 'N/A'
                        product_data['New indication PDF'] = 'N/A'
                except Exception as e:
                    print(f"Error processing PDF {matching_pdf} for {product_name}: {e}")

            product_data_list.append(product_data)

        except Exception as e:
            print(f"Error processing item: {e}")

    return product_data_list