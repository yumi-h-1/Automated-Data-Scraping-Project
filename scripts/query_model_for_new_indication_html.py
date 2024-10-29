# Function to query the model to find new indications from HTML
def query_model_for_new_indication_html(html_content):
    query = f"""Use the HTML code provided below to answer the following question:
    Extract all newly added indications for the medicine. The indications are related to the patient group as well.
    The newly added indications are identified within <strong></strong> tags, indicating bold text.

    HTML structure:
    \"\"\"
    {html_content}
    \"\"\"

    Question: What is the newly added indication of the medicine? Extract the words exactly as they appear in bold text.
    If there are different text formats between bold text sections, the first bold text is considered the first newly added indication, and any bold text that follows the different format will be the second newly added indication, and so on.
    Use a comma (',') to separate each bold text section when extracting them in order.
    Write the answer in the format 'Medicine Name: New Indication'.
    If the answer cannot be found, write only 'I don't know.'."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant who extracts complete, exact, and accurate information, especially from text."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error querying the model: {e}")
        return "N/A"