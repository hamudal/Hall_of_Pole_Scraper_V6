import requests
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_url_valid(url):
    """
    Checks if a URL is valid.

    Args:
        url (str): The URL to be checked.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f"Error while checking URL: {url}\nError: {e}")
        return False

def validate_urls(url_list):
    """
    Validates a list of URLs.

    Args:
        url_list (list): A list of URLs to be validated.

    Returns:
        DataFrame: A Pandas DataFrame with valid URLs.
    """
    valid_urls = []

    for index, url in enumerate(url_list):
        logging.info(f"Processing URL {index + 1}/{len(url_list)}: {url}")
        if is_url_valid(url):
            valid_urls.append(url)
            logging.info(f"URL {url} is valid.")
        else:
            logging.info(f"URL {url} is not valid.")

    valid_urls_df = pd.DataFrame(valid_urls, columns=["Valid_URL"]).drop_duplicates(subset=['Valid_URL'])
    return valid_urls_df

# Example call of the function
# url_list = ["https://www.eversports.de/s/poda-studio"]
# valid_urls_df = validate_urls(url_list)
# print(valid_urls_df)
