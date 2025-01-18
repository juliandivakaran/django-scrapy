import requests
from bs4 import BeautifulSoup

def scrape_annual_prices(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Searching for "annual price" or similar phrases
        results = []
        for text in soup.stripped_strings:
            if 'Tea Production' in text.lower() or 'yearly price' in text.lower():
                results.append(text)
        
        return results if results else ["No annual prices found."]
    except requests.exceptions.RequestException as e:
        return [f"Error: Unable to fetch the URL ({e})"]
