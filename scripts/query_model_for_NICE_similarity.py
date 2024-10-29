# Function to query the model for text similarity between NICE text and indication from a dataframe
def query_model_for_NICE_similarity(nice_text, indication):
    query = f"""Compare the following two pieces of text and determine if they mention the same therapeutic indication for the medicine:

    NICE text:
    \"\"\"{nice_text}\"\"\"

    Full Indication:
    \"\"\"{indication}\"\"\"

    Are there any matching therapeutic indications in both texts?
    Answer only 'Yes' or 'No' and provide any matching terms if applicable.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert assistant who specializes in comparing medical texts and identifying therapeutic indications."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error querying the model: {e}")
        return "N/A"