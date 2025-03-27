import requests
from bs4 import BeautifulSoup

# URL of the IRS webpage containing yearly average currency exchange rates
IRS_URL = "https://www.irs.gov/individuals/international-taxpayers/yearly-average-currency-exchange-rates"

# Cache to store exchange rates for previously requested years
CACHE = {}


def get_irs_exchange_rate_israel(year):
    """
    Fetches the average yearly exchange rate for Israel from the IRS website.
    Utilizes caching to avoid redundant network requests for the same year.
    """
    # Check if the exchange rate for the given year is already in the cache
    if year in CACHE:
        return CACHE[year]

    try:
        # Send a GET request to the IRS URL with a timeout of 10 seconds
        response = requests.get(IRS_URL, timeout=10)
        # Raise an exception if the HTTP response contains an error status code
        response.raise_for_status()
    except requests.RequestException as e:
        # Log an error message if the request fails
        print(f"Error fetching IRS exchange rate: {e}")
        return None  # Return None if the IRS website is unavailable

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all tables on the webpage
    tables = soup.find_all("table")

    # If no tables are found, log an error message and return None
    if not tables:
        print("No table found on IRS page.")
        return None

    # Extract the headers (column names) from the first table
    headers = [th.text.strip() for th in tables[0].find_all("th")]
    # Check if the requested year is present in the table headers
    if str(year) not in headers:
        print(f"Year {year} not found in table headers.")
        return None

    # Get the index of the column corresponding to the requested year
    year_index = headers.index(str(year))

    # Iterate through each row in the table
    for row in tables[0].find_all("tr"):
        # Extract all columns (cells) in the current row
        cols = row.find_all("td")
        # Ensure the row contains enough columns to include the year column
        if len(cols) >= year_index + 1:
            # Extract and normalize the text content of all columns in the row
            cols_data = [col.text.strip().lower() for col in cols]

            # Check if the row corresponds to Israel or the New Shekel currency
            if "israel" in cols_data or "new shekel" in cols_data:
                try:
                    # Convert the value in the year column to a float
                    exchange_rate = float(cols[year_index].text.strip())
                    # Store the exchange rate in the cache for future use
                    CACHE[year] = exchange_rate
                    return exchange_rate
                except ValueError:
                    # Log an error message if the value cannot be converted to a float
                    print(f"Could not convert exchange rate: {cols[year_index].text.strip()}")

    # Log a message if no exchange rate is found for the requested year
    print(f"Exchange rate for {year} not found.")
    return None  # Return None if no exchange rate is found


