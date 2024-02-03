import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# Basic configuration for repeated requests
session = requests.Session()

def get_soup(url):
    """
    Creates a BeautifulSoup object for a given URL.

    Args:
        url (str): The URL of the webpage.

    Returns:
        BeautifulSoup: A BeautifulSoup object of the webpage, None on errors.
    """
    try:
        response = session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error retrieving the webpage: {e}")
        return None

# Extraction functions
def extract_overview_buttons(soup):
    buttons = soup.find_all('div', class_="MuiStack-root css-sgccrm")
    return [button.text.rstrip() for div in buttons for button in div.find_all('a')]

def extract_pole_studio_name(soup):
    name_element = soup.find('h1', class_='MuiTypography-root MuiTypography-h1 css-l64ylu')
    return name_element.text.rstrip() if name_element else None

def extract_contact_info(soup):
    contact_divs = soup.find_all('div', class_='css-1x2phcg')
    contact_info = {'E-Mail': None, 'Homepage': None, 'Telefon': None}
    for div in contact_divs:
        for a in div.find_all('a', href=True):
            href = a['href']
            if href.startswith('mailto:'):
                contact_info["E-Mail"] = href.replace('mailto:', '').rstrip()
            elif href.startswith('tel:'):
                contact_info["Telefon"] = href.replace('tel:', '').rstrip()
            else:
                contact_info["Homepage"] = href.rstrip()
    return contact_info

def extract_address(soup):
    address_element = soup.find('p', class_='MuiTypography-root MuiTypography-body1 css-1619old')
    if address_element:
        address_text = address_element.text.split(',')
        return address_text, address_text[1].split(" ")[2].rstrip(), address_text[1].split(" ")[1].rstrip(), address_text[0].rstrip()
    return None, None, None, None

def extract_description(soup):
    description_element = soup.find('div', class_="MuiBox-root css-0")
    
    if description_element:
        description_text = description_element.text.rstrip()
        return description_text if len(description_text.split()) > 0 else None
    else:
        return None

def extract_art(soup):
    art_elements = soup.find_all("p", class_="MuiTypography-root MuiTypography-body1 css-6ik050")
    return [art.text.rstrip() for art in art_elements]

def extract_sale(soup):
    sale_element = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-153qxhx")
    return sale_element.text.rstrip() if sale_element else None

# Main function scrape_pole_studio
def scrape_pole_studio(url):
    """
    Scrapes information from a Pole Studio.

    Args:
        url (str): The URL of the Pole Studio.

    Returns:
        DataFrame: A DataFrame with information about the Pole Studio.
    """
    polestudio_soup = get_soup(url)
    if polestudio_soup is None:
        return None

    # Extracting individual information
    overview_buttons = extract_overview_buttons(polestudio_soup)
    pole_studio_name = extract_pole_studio_name(polestudio_soup)
    contact_info = extract_contact_info(polestudio_soup)
    address, town, postal_code, street = extract_address(polestudio_soup)
    description_text = extract_description(polestudio_soup)
    arten = extract_art(polestudio_soup)
    sale = extract_sale(polestudio_soup)

    # Creating the dictionary and returning it as a DataFrame
    pole_studio_overview = {
        'PoleStudio_Name': pole_studio_name,
        'Adresse': address,
        'PLZ': postal_code,
        'Stadt': town,
        'Straße': street,
        'Buttons': overview_buttons,
        'Pole Studio Beschreibung': description_text,
        'E-Mail': contact_info['E-Mail'],
        'Homepage': contact_info['Homepage'],
        'Telefon': contact_info['Telefon'],
        'URL_S': url,
        'Art': arten,
        'Angebot': sale,
    }

    pole_studio_df = pd.DataFrame([pole_studio_overview])
    pole_studio_df['Created Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pole_studio_df['Updated Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return pole_studio_df

# Example call of the main function
# url = "https://www.eversports.de/s/poda-studio"
# pole_studio_df = scrape_pole_studio(url)
# print(pole_studio_df)
