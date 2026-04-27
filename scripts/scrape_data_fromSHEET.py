def scrape_data_fromSHEET(scraped_medicine_name, dataframe, columns_to_return):
    matching_row = dataframe[dataframe['Name of medicine'] == scraped_medicine_name]

    if not matching_row.empty:
        # Extract the desired columns from the matching row
        return matching_row[columns_to_return].iloc[0].to_dict()
    else:
        return None