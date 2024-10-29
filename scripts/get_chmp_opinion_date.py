# Function to change the format of date for CHMP opinion date
def get_chmp_opinion_date(date_str, date_format='%d %B %Y'):
    try:
        # Convert date string to datetime object
        date_obj = datetime.strptime(date_str, date_format)

        # Subtract one day to get CHMP Opinion Date
        chmp_opinion_date = date_obj - timedelta(days=1)

        # Convert back to string in the same format
        return chmp_opinion_date.strftime(date_format)
    except ValueError as e:
        # If parsing fails, print the error and return 'N/A'
        print(f"Date parsing error: {e}")
        return 'N/A'