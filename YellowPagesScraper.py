import requests
from bs4 import BeautifulSoup
import csv
import logging
import time
import random
import re
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Configure session with retry mechanism and user agent
session = requests.Session()
retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount('http://', adapter)
session.mount('https://', adapter)
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})

def scrape_yellow_pages(search_terms, zip_code_range, num_pages=1, delay=0, proxy=None):
    search_terms = search_terms.split(",")
    zip_codes = generate_zip_codes(zip_code_range)
    
    results = []
    for search_term in search_terms:
        for zip_code in zip_codes:
            url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={zip_code}"
            
            if proxy:
                proxies = {'http': proxy, 'https': proxy}
            else:
                proxies = None
            
            try:
                response = session.get(url, proxies=proxies)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logging.error(f"An error occurred while making the request for search term '{search_term}' and zip code '{zip_code}': {e}")
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the HTML elements containing the business listings
            listings = soup.find_all('div', {'class': 'v-card'})
            
            for listing in listings:
                name = listing.find('a', {'class': 'business-name'}).text.strip()
                address_element = listing.find('span', {'class': 'street-address'})
                address = address_element.text.strip() if address_element else ''
                phone_element = listing.find('div', {'class': 'phones'})
                phone = phone_element.text.strip() if phone_element else ''
                results.append({'Name': name, 'Address': address, 'Phone': phone, 'Postal Code': zip_code})
            
            if num_pages > 1:
                for page in range(2, num_pages + 1):
                    time.sleep(delay)  # Delay between requests
                    next_url = f"{url}&page={page}"
                    try:
                        response = session.get(next_url, proxies=proxies)
                        response.raise_for_status()
                    except requests.exceptions.RequestException as e:
                        logging.error(f"An error occurred while making the request for page {page} of search term '{search_term}' and zip code '{zip_code}': {e}")
                        continue

                    soup = BeautifulSoup(response.content, 'html.parser')
                    listings = soup.find_all('div', {'class': 'v-card'})
                    
                    for listing in listings:
                        name = listing.find('a', {'class': 'business-name'}).text.strip()
                        address_element = listing.find('span', {'class': 'street-address'})
                        address = address_element.text.strip() if address_element else ''
                        phone_element = listing.find('div', {'class': 'phones'})
                        phone = phone_element.text.strip() if phone_element else ''
                        results.append({'Name': name, 'Address': address, 'Phone': phone, 'Postal Code': zip_code})

            # Write to file after each zip code or search term is attempted
            save_results_to_csv(results, 'yellow_pages_results.csv')

    # Remove duplicates from results
    results = remove_duplicates(results)

    return results

def generate_zip_codes(zip_code_range):
    zip_codes = []
    if '-' in zip_code_range:
        start_zip, end_zip = zip_code_range.split('-')
        start_zip = int(start_zip.strip())
        end_zip = int(end_zip.strip())
        zip_codes = [str(zip_code) for zip_code in range(start_zip, end_zip + 1)]
    else:
        zip_codes = [zip_code_range.strip()]

    return zip_codes

def remove_duplicates(results):
    unique_results = []
    seen = set()
    for result in results:
        result_tuple = (result['Name'], result['Address'], result['Phone'], result['Postal Code'])
        if result_tuple not in seen:
            unique_results.append(result)
            seen.add(result_tuple)

    return unique_results

def save_results_to_csv(results, filename):
    keys = results[0].keys()
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

def search_and_save_results(search_terms, zip_code_range, filename, num_pages=1, delay=0, proxy=None):
    results = scrape_yellow_pages(search_terms, zip_code_range, num_pages, delay, proxy)
    if results:
        save_results_to_csv(results, filename)
        logging.info(f"Results saved to {filename}")
    else:
        logging.warning("No results found.")

# Example usage
search_terms = 'Search Term'
zip_code_range = '10012-10013'
filename = 'yellow_pages_results.csv'
### Only Scrapes For Company Name, Postal Code & Telephone Number to CSV... ###
search_and_save_results(search_terms, zip_code_range, filename, num_pages=1, delay=0, proxy=None)
