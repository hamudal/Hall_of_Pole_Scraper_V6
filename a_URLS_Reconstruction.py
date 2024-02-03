import requests
from bs4 import BeautifulSoup

def get_response_content(url):
    """
    Retrieves the content of a webpage via an HTTP request.

    Args:
        url (str): The URL of the webpage.

    Returns:
        bytes or None: The content of the webpage or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error during HTTP request: {e}")
        return None

def reconstruct_urls_and_extract_buttons(url):
    """
    Reconstructs URLs and extracts buttons for a given URL.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        tuple: A list of link texts and a dictionary of reconstructed URLs.
    """
    content = get_response_content(url)
    if content is None:
        return [], {}

    soup = BeautifulSoup(content, 'html.parser')
    overview_buttons = soup.find_all('div', class_="MuiStack-root css-sgccrm")

    button_url_mapping = {
        'Übersicht': 's',
        'Workshops': 'sw',
        'Preise': 'sp',
        'Team': 's'
    }

    dynamic_part = url.split("/")[-1]
    link_text = []
    reconstructed_urls = {}

    if overview_buttons:
        for item in overview_buttons:
            anchor_elements = item.find_all('a')
            for anchor in anchor_elements:
                text = anchor.text
                if text not in ['Videos', 'Klassen']:  # Skip 'Videos' and 'Klassen'
                    link_text.append(text)
                    try:
                        reconstructed_url = construct_url(url, text, button_url_mapping, dynamic_part)
                    except ValueError as ve:
                        print(f"Error reconstructing URL for '{text}': {ve}")
                        continue
                    reconstructed_urls[text] = reconstructed_url

    return link_text, reconstructed_urls

def construct_url(base_url, button_text, mapping, dynamic_part):
    """
    Constructs a URL based on button text and predefined mapping.

    Args:
        base_url (str): The base URL.
        button_text (str): The button text.
        mapping (dict): The mapping of button text to URL components.
        dynamic_part (str): The dynamic part of the URL.

    Returns:
        str: The reconstructed URL.

    Raises:
        ValueError: If button text is not recognized.
    """
    if button_text in ['Team']:
        return f"{base_url}/{button_text.lower()}"
    elif button_text in mapping:
        return f"https://www.eversports.de/{mapping[button_text]}/{dynamic_part}"
    else:
        raise ValueError(f"Unrecognized text: '{button_text}'")

# # Example call of the function
# url = "https://www.eversports.de/s/poda-studio"
# link_text, reconstructed_urls = reconstruct_urls_and_extract_buttons(url)
# print(link_text, reconstructed_urls)
