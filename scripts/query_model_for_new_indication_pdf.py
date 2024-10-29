# Function to query the model to find new indications from PDFs
def query_model_for_new_indication_pdf(pdf_text):
    query = f"""Use the document stored in the variable 'pdf_text' to answer the following question:
    Extract only the most recent added indication for the medicine. The date criteria is 'Commission \nDecision \nIssued2 / \namended'.
    The newly added indication may be stated between 'Extension of indication' and 'Change(s) to therapeutic indication'.

    PDF content: {pdf_text}

    Question: What is the most recent added indication for the medicine in the variable 'pdf_text'?
    Write the answer in the format 'Medicine Name: Newly added Indication'.
    If the answer cannot be found, write 'I don't know.'."""

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