import requests
import csv
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

class BookTracker:
    def __init__(self, url, filename="book_data.csv"):
        self.url = url
        self.filename = filename
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def fetch_soup(self): 
        try:
            response = requests.get(self.url, headers=self.headers, timeout=5)
            response.raise_for_status() 
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {e}")
            return None
        
    def get_details(self, soup):
        
        price_element = soup.select_one(".price_color")
        
        title_element = soup.select_one("h1")
        
        price = None
        title = "Unknown Title"

        if price_element:
            raw_price = price_element.get_text()
            price = float(re.sub(r'[^\d.]', '', raw_price))
        
        if title_element:
            title = title_element.get_text().strip()

        return title, price
    
    def log_data(self, title, price): 
        file_exists = os.path.isfile(self.filename)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
           
            if not file_exists:
                writer.writerow(["Timestamp", "Book Title", "Price"])
            
            writer.writerow([timestamp, title, price])

    def run(self, target): 
        print(f"Tracking Product: {self.url}")
        soup = self.fetch_soup()
        if soup:
            title, price = self.get_details(soup)
            
            if price is not None:
                self.log_data(title, price)
                if price <= target:
                    print(f"PRICE DROP {title} is now £{price} (Target: £{target})")
                else:
                    print(f"Logged: {title} - Current Price: £{price}")
            else:
                print("Error: Could not find price on this page. Check the URL/Selector.")

# Find a book on the website
TARGET_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
TARGET_PRICE = 50.00  # Set this slightly below the current price to test logic
DATABASE_FILE = "price_history.csv"

if __name__ == "__main__": 
    tracker = BookTracker(TARGET_URL, DATABASE_FILE)
    
    print("--- Book Price Tracker Starting ---")
    tracker.run(target=TARGET_PRICE)
    print("--- Check completed successfully ---")



