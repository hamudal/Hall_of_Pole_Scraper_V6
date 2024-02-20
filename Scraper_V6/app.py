import streamlit as st
import pandas as pd
from a_PyCaller import process_urls
from tqdm import tqdm
from datetime import datetime

def process_and_print_results(url, all_pole_studio_data, all_workshops_data, all_workshop_details_data, all_urls_data):
    data = process_urls([url])

    if data:
        for key, df in data.items():
            if df is not None and not df.empty:
                st.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - INFO - Scraping Data from: {url}")
                st.write(f"{key.replace('_', ' ').title()}: {len(df)} entries")

                # Update the appropriate DataFrame
                if key == 'pole_studio_data':
                    all_pole_studio_data = pd.concat([all_pole_studio_data, df], ignore_index=True)
                elif key == 'workshops_data':
                    all_workshops_data = pd.concat([all_workshops_data, df], ignore_index=True)
                elif key == 'workshop_details':
                    all_workshop_details_data = pd.concat([all_workshop_details_data, df], ignore_index=True)

    # Add URLs to DataFrame
    all_urls_data = pd.concat([all_urls_data, pd.DataFrame({'URL': [url]})], ignore_index=True)

    return all_pole_studio_data, all_workshops_data, all_workshop_details_data, all_urls_data

def main():
    # Load initial URLs
    all_found_urls_s = pd.read_csv("your_output_file.csv")
    initial_urls = list(set(all_found_urls_s["0"])) # Delete "[:3]" to scrape all Urls

    # Initialize DataFrames
    all_pole_studio_data = pd.DataFrame()
    all_workshops_data = pd.DataFrame()
    all_workshop_details_data = pd.DataFrame()
    all_urls_data = pd.DataFrame(columns=['URL'])

    # Process each URL with tqdm
    with tqdm(initial_urls, desc="Processing URLs", dynamic_ncols=True) as pbar:
        for url in pbar:
            all_pole_studio_data, all_workshops_data, all_workshop_details_data, all_urls_data = process_and_print_results(
                url, all_pole_studio_data, all_workshops_data, all_workshop_details_data, all_urls_data
            )

    # Export DataFrames to CSV files
    all_pole_studio_data.to_csv("Pole_Studio_Übersicht_S.csv", index=False)
    all_workshops_data.to_csv("Workshop_Liste_SW.csv", index=False)
    all_workshop_details_data.to_csv("Workshop_Übersicht_E.csv", index=False)
    all_urls_data.to_csv("All_URLs.csv", index=False)

    # Return the final DataFrames
    return all_pole_studio_data, all_workshops_data, all_workshop_details_data, all_urls_data

# Streamlit App
def streamlit_app():
    st.title("Web Scraping App")
    st.subheader("Click the button below to start scraping")

    if st.button("Start Scraping"):
        result_pole_studio, result_workshops, result_workshop_details, result_urls = main()

        st.subheader("Pole Studio Data")
        st.write(result_pole_studio)

        st.subheader("Workshops Data")
        st.write(result_workshops)

        st.subheader("Workshop Details Data")
        st.write(result_workshop_details)

        st.subheader("All URLs Data")
        st.write(result_urls)

if __name__ == "__main__":
    streamlit_app()
