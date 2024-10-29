# Function to scrape the therapy area
def scrape_therapy_area(scraped_therapy_class, dataframe, area_column):
    # Search for the name in the dataframe
    matching_row = therapy_area_df[therapy_area_df['Therapy Class'] == scraped_therapy_class]

    if not matching_row.empty:
        # Extract the desired columns from the matching row
        return matching_row[area_column].iloc[0]
    else:
        # Return None or an appropriate message if no match is found
        return None