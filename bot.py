import requests
import cloudscraper
from bs4 import BeautifulSoup

# Configuration
TOKEN = "8556880350:AAETW_gWc8hWjvX_PT_GNFevOfswzX2xocc"
CHAT_ID = "6672418741"
URL = "https://es.wallapop.com/app/search?keywords=iphone%2012&max_sale_price=500"

def check_site():
    scraper = cloudscraper.create_scraper()
    try:
        response = scraper.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the first item card
        item = soup.select_one('a.ItemCardList__item')
        if item:
            title = item.get('title', 'No title')
            link = item.get('href', '')
            price_element = item.select_one('.ItemCard__price')
            price = price_element.text.strip() if price_element else "N/A"
            
            full_link = f"https://es.wallapop.com{link}" if link.startswith('/') else link
            
            # Construct the message
            message = (
                f"NEW ITEM FOUND!\n\n"
                f"Product: {title}\n"
                f"Price: {price}\n"
                f"Link: {full_link}"
            )
            
            # Send to Telegram
            requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                data={"chat_id": CHAT_ID, "text": message}
            )
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_site()
