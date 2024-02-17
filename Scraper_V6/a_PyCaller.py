from a_URLS_Reconstruction import reconstruct_urls_and_extract_buttons
from b_URLS_Validation import validate_urls
from c_PoleStudio_Overview_S import scrape_pole_studio
from d_Workshop_List_SW import scrape_workshops
from e_Workshop_Overview_E import scrape_workshop_details
import pandas as pd

validated_urls_df = []
validated_urls = []

def process_urls(urls):
    """
    Processes a list of URLs through various scraping functions.

    Args:
        urls (list): A list of URLs to be processed.

    Returns:
        dict: A dictionary containing DataFrames for different categories.
    """
    global validated_urls_df, validated_urls  # Declare variables as global

    try:
        print("Starting URL reconstruction...")
        reconstructed_urls_list = [reconstruct_urls_and_extract_buttons(url)[1] for url in urls]
        reconstructed_urls = {k: v for d in reconstructed_urls_list for k, v in d.items()}

        print("Converting to DataFrame...")
        reconstructed_urls_df = pd.DataFrame(list(reconstructed_urls.items()), columns=['Category', 'URL'])
        
        print("Validating URLs...")
        validated_urls_df = validate_urls(reconstructed_urls_df["URL"].to_list())
        validated_urls = validated_urls_df["Valid_URL"].tolist()

        # Processing URLs
        results = {'pole_studio_data': pd.DataFrame(), 'workshops_data': pd.DataFrame(), 
                   'workshop_details': pd.DataFrame()}

        for url in validated_urls:
            if "/s/" in url and "/team" not in url and "/videos" not in url and "/preise" not in url:
                print(f"Scraping Pole Studio Data from {url}...")
                pole_studio_data = scrape_pole_studio(url)
                results['pole_studio_data'] = pd.concat([results['pole_studio_data'], pole_studio_data], ignore_index=True)
            elif "/sw/" in url:
                print(f"Scraping Workshops Data from {url}...")
                workshop_data = scrape_workshops(url)
                results['workshops_data'] = pd.concat([results['workshops_data'], workshop_data], ignore_index=True)
                for workshop_url in workshop_data['URL_E']:
                    print(f"Scraping Workshop Details from {workshop_url}...")
                    workshop_detail = scrape_workshop_details(workshop_url)
                    if not workshop_detail.empty:
                        results['workshop_details'] = pd.concat([results['workshop_details'], workshop_detail], ignore_index=True)
            # Skip "/scl/" URLs
            else:
                continue

        print("\nProcessing completed.\n-------------------------------- \n")
        return results
    except Exception as e:
        print(f"An error occurred during processing: {e}\n")
        return None

# # Test code (if needed)
# test_urls = ["https://www.eversports.de/s/poda-studio"]  # Example URL
# test_results = process_urls(test_urls)
# for category, df in test_results.items():
#     print(f"Category: {category}")
#     print(df)
#     print("\n")

# Create DataFrame containing each kind of URL with its corresponding column
urls_mapping = {'URL_S': [], 'URL_SW': [], 'URL_E': []}
for url in validated_urls:
    if "/s/" in url and "/team" not in url and "/videos" not in url and "/preise" not in url:
        urls_mapping['URL_S'].append(url)
    elif "/sw/" in url:
        urls_mapping['URL_SW'].append(url)
    elif "/e/" in url:
        urls_mapping['URL_E'].append(url)

urls_df = pd.DataFrame(urls_mapping)
# print(urls_df)
