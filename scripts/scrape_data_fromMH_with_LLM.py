import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive'
}

def scrape_data_fromMH_with_LLM(newspage_url, pdf_paths, therapy_area_df, df, indications):
    # Request for HTML of the given URL
    news_response = requests.get(newspage_url, headers=headers)
    news_response.encoding = 'utf-8'
    news_soup = BeautifulSoup(news_response.text, 'html.parser')

    # Find all sections
    items = news_soup.find_all('div', class_='item')

    # Prepare a list to store extracted data
    product_data_list = []
    current_recommendation = None

    for item in items:
        try:
            # Check if this item is a recommendation heading
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
                    current_recommendation = None  # Ignore other sections
                continue

            # Skip items if the current recommendation is not positive
            if current_recommendation != 'Positive':
                continue

            # Extract the product name
            product_name_tag = item.find('h3', class_='mb-4')
            if product_name_tag:
                product_name = product_name_tag.get_text(strip=True).lower()  # Convert to lowercase
                product_name = product_name.replace(' ', '-')  # Replace spaces with hyphens
            else:
                product_name = 'N/A'

            # Construct the EPAR URL using the product name
            epar_url = f"https://www.ema.europa.eu/en/medicines/human/EPAR/{product_name}"
            #variation_url = f"https://www.ema.europa.eu/en/medicines/human/variation/{product_name}"

            matching_variation_urls = [url for url in variation_urls if url.split('/')[-1].startswith(product_name)]
            if not matching_variation_urls:
                matching_variation_urls = [f"https://www.ema.europa.eu/en/medicines/human/variation/{product_name}"]

            # Initialize a dictionary for this product
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

            # Extract additional data from the EPAR page
            try:
                product_data = scrape_data_fromEPAR(epar_url, product_data, therapy_area_df)
            except Exception as e:
                print(f"Error scraping data from EPAR for {product_name}: {e}")

            # Match the EPAR URL with the indication dictionary
            if epar_url in indications:
                product_data['Full indication'] = indications[epar_url]
            else:
                product_data['Full indication'] = 'N/A'

            # Match the variation URL with the new indication dictionary
            product_data['New indication HTML'] = ', '.join(
                [new_indications_html.get(url, 'N/A') for url in matching_variation_urls]
            )

            #if matching_variation_urls in new_indications_html:
            #    product_data['New indication HTML'] = new_indications_html[matching_variation_urls]
            #else:
            #    product_data['New indication HTML'] = 'N/A'

            product_data['Removed indication HTML'] = ', '.join(
                [removed_indications_html.get(url, 'N/A') for url in matching_variation_urls]
            )

            # Match the variation URL with the removed indication dictionary
            #if matching_variation_urls in removed_indications_html:
            #    product_data['Removed indication HTML'] = removed_indications_html[matching_variation_urls]
            #else:
            #    product_data['Removed indication HTML'] = 'N/A'

            # Extract the INN or Common name
            inn_tag = item.find('dt', string=re.compile(r'International non-proprietary name \(INN\)|INN'))
            common_name_tag = item.find('dt', string=re.compile(r'Common name'))
            if inn_tag:
                product_data['INN'] = inn_tag.find_next('dd').get_text(strip=True)
                inn_name = product_data['INN']
                # Construct the NICE URL using the medicine name
                nice_url = f'https://www.nice.org.uk/search?q={inn_name}'
                try:
                    product_data = scrape_data_fromNICE(nice_url, product_data)
                except Exception as e:
                    print(f"Error scraping data from NICE for {inn_name}: {e}")

            elif common_name_tag:
                product_data['INN'] = common_name_tag.find_next('dd').get_text(strip=True)
                common_name = product_data['INN']
                # Construct the NICE URL using the medicine name
                nice_url = f'https://www.nice.org.uk/search?q={common_name}'
                try:
                    product_data = scrape_data_fromNICE(nice_url, product_data)
                except Exception as e:
                    print(f"Error scraping data from NICE for {common_name}: {e}")

            else:
                product_data['INN'] = 'N/A'

            # Extract the Marketing-authorisation applicant
            applicant_tag = item.find('dt', string=re.compile(r'Marketing-authorisation applicant'))
            holder_tag = item.find('dt', string=re.compile(r'Marketing-authorisation holder'))
            if applicant_tag:
                product_data['Marketing authorisation holder'] = applicant_tag.find_next('dd').get_text(strip=True)
            elif holder_tag:
                product_data['Marketing authorisation holder'] = holder_tag.find_next('dd').get_text(strip=True)
            else:
                product_data['Marketing authorisation holder'] = 'N/A'

            # Match with the data from the dataframe
            dataframe_columns = ['Orphan medicine', 'European Commission decision date']
            try:
                dataframe_data = scrape_data_fromSHEET(product_name, df, dataframe_columns)
                if dataframe_data:
                    product_data.update(dataframe_data)
            except Exception as e:
                print(f"Error matching data from sheet for {product_name}: {e}")

            # Find the PDF corresponding to this product
            matching_pdf = next((pdf for pdf in pdf_paths if product_name in pdf.lower()), None)
            if matching_pdf:
                print(f"Processing PDF: {matching_pdf} for product: {product_name}")
                try:
                    pdf_text = extract_text_from_pdf(matching_pdf)
                    # Query the model for EMA date from the PDF
                    ema_date = query_model_for_ema_date(pdf_text)

                    # If the product is an extension, update 'EMA date'
                    if product_data['Initial Approval'] == 'Extension':
                        product_data['Date for extension'] = ema_date
                    else:
                        product_data['Date for extension'] = 'N/A'

                    new_indication_pdf = query_model_for_new_indication_pdf(pdf_text)

                    # If the product is an extension, update 'New indication PDF'
                    if product_data['Initial Approval'] == 'Extension':
                        product_data['New indication PDF'] = new_indication_pdf
                    else:
                        product_data['New indication PDF'] = 'N/A'

                except Exception as e:
                    print(f"Error processing PDF {matching_pdf} for {product_name}: {e}")

            # Add the product data to the list
            product_data_list.append(product_data)

        except Exception as e:
            print(f"Error processing item: {e}")

    return product_data_list