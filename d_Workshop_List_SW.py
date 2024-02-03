import requests
from bs4 import BeautifulSoup
import pandas as pd

# Global constant for the base URL
BASE_URL = "https://www.eversports.de"

def scrape_workshops(url):
    """
    Scrapes workshop information from a given URL.

    Args:
        url (str): The URL of the workshop page.

    Returns:
        DataFrame: A DataFrame with information about the workshops.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error retrieving the webpage: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Dictionary to store workshop information
    workshop_data = {
        'Workshop Name': [],
        'Workshop Date': [],
        'Workshop Price': [],
        'Workshop Units': [],
        'Workshop Studio': [],
        'Workshop Address': [],
        'URL_E': []
    }

    # Workshop elements
    workshop_elements = soup.find_all('a', class_='marketplace-tile js_marketplace-tile')

    # Iterate through elements and extract information
    for workshop in workshop_elements:
        workshop_data['Workshop Name'].append(workshop.find('h4').text)
        workshop_data['Workshop Date'].append(workshop.find('div', class_='marketplace-tile__date').text)
        workshop_data['Workshop Price'].append(workshop.find('div', class_='marketplace-tile__price').text)
        workshop_data['Workshop Units'].append(workshop.find('small', class_='u-text-bold').text)
        
        workshop_content = workshop.find('div', class_='marketplace-tile__content__bottom').find_all('small')
        workshop_data['Workshop Studio'].append(workshop_content[0].text)
        workshop_data['Workshop Address'].append(workshop_content[1].text)
        
        workshop_data['URL_E'].append(BASE_URL + workshop['href'])

    # Create DataFrame
    workshoplist_df = pd.DataFrame(workshop_data)

    return workshoplist_df

# Example call of the function
# url = "https://www.eversports.de/sw/poda-studio"
# df = scrape_workshops(url)
# df
