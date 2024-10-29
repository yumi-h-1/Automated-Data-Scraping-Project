# Function to query the model to find removed indications from HTML
def query_model_for_removed_indication_html(html_content):
    query = f"""Use the HTML code provided below to answer the following question:
    Extract all removed indications for the medicine. The indications are related to the patient group as well.
    The removed indications are identified within <s></s> tags, indicating strikethrough text.

    HTML structure:
    \"\"\"
    {html_content}
    \"\"\"

    Question: What is the removed indication of the medicine? Extract the words exactly as they appear in strikethrough text.
    If there are different text formats between strikethrough text sections, the first strikethrough text is considered the first removed indication, and any strikethrough text that follows the different format will be the second removed indication, and so on.
    Use a comma (',') to separate each strikethrough text section when extracting them in order.
    Write the answer in the format 'Medicine Name: Removed Indication'.
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