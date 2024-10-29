# Function to query the model for full indications from HTML
from openai import OpenAI

def query_model_for_indication(html_content):
    query = f"""Use the HTML code provided below to answer the following question:
    Extract the full or therapeutic indication of the medicine. It may be located under the 'Overview' section or the 'Therapeutic Indication' section.

    HTML structure:
    \"\"\"
    {html_content}
    \"\"\"

    Question: What is the full or therapeutic indication of the medicine? Write the answer in the format 'Medicine Name: Full Indication'.
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