# Function to query the model to find the date of the recent new indication from PDFs
def query_model_for_ema_date(pdf_text):
    query = f"""Use the document stored in the variable 'pdf_text' to answer the following question. If the answer cannot be found, write 'N/A'.
    Extract only the most recent added indication for the medicine. The date criteria should be 'Commission \nDecision \nIssued2 / \namended'.
    The newly added indication may be stated as 'Extension of indication' or something similar.

    PDF content: {pdf_text}

    Question: What is the commision decision issued date of the newly added indication for the medicine in the variable 'pdf_text'?
    Answer only the date in DD/MM/YYYY format."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant who extracts complete, exact, and accurate information, especially from text."},
                 {"role": "user", "content": query}]
            )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error querying the model: {e}")
        return "N/A"