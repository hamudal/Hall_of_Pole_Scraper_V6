import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_workshop_details(url):
    """
    Scrapes detailed information of a workshop from a given URL.

    Args:
        url (str): The URL of the workshop detail page.

    Returns:
        DataFrame: A DataFrame with detailed information about the workshop.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving the webpage: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, 'html.parser')

    def get_text_or_none(element):
        return element.text.strip() if element else None

    # Extraction of various data points
    workshop_name = get_text_or_none(soup.find('h1', class_='MuiTypography-root MuiTypography-h1 css-gdjtsh'))
    description_div = soup.find('div', class_='css-3awvdx')
    description = ' '.join([p.text for p in description_div.find_all('p')]) if description_div else None
    studio_name = get_text_or_none(soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-z923os'))
    location = get_text_or_none(soup.find_all('p', class_='MuiTypography-root MuiTypography-body1 css-bjhn26')[2])
    level = get_text_or_none(soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-ilcg2f'))
    date = get_text_or_none(soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-16ai5j1'))
    time = get_text_or_none(soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-bjhn26'))

    # Creating the DataFrame
    workshop_df = pd.DataFrame({
        'Workshop Name': [workshop_name],
        'Description': [description],
        'Studio Name': [studio_name],
        'Location': [location],
        'Level': [level],
        'Date': [date],
        'URL_E': [url],
        'Time': [time]
    })

    return workshop_df

# Test the function
# url = "https://www.eversports.de/e/workshop/mT-MZa2"
# workshop_df = scrape_workshop_details(url)
# print(workshop_df)
