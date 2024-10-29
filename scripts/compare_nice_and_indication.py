# Loop to compare each NICE text with the corresponding indications in a dataframe
def compare_nice_and_indication(nice_text_dict, indication_df):
    similarity_results = []  # List to store the results

    # Iterate over the NICE URLs and corresponding indications
    for url, nice_text in nice_text_dict.items():
        try:
            # Fetch the corresponding indications from the DataFrame
            if url in indication_df['NICE_url'].values:
                indication = indication_df.loc[indication_df['NICE_url'] == url].values[0]

                # Query the model for similarity
                result = query_model_for_NICE_similarity(nice_text, indication)

                # Store the result with URL and result
                similarity_results.append({
                    'NICE_url': url,
                    'Result': result
                })
            else:
                similarity_results.append({
                    'NICE_url': url,
                    'Result': 'No matching indication found in DataFrame'
                })

        except Exception as e:
            print(f"Error processing comparison for {url}: {e}")
            similarity_results.append({
                'NICE_url': url,
                'Result': 'Error'
            })

    return similarity_results