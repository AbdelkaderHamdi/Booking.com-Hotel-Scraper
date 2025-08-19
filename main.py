import requests
from bs4 import BeautifulSoup
import csv
import logging
import argparse
from dataclasses import dataclass




@dataclass
class Hotel:
    """Data class to represent hotel information"""
    name: str
    location: str
    review_score: str
    review_count: str
    price: str

class BookingHotelScraper:
    """Professional web scraper for Booking.com hotel data"""
    
    def __init__(self, delay = 1.0):
        """
        Initialize the scraper with configuration
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
          
    def fetch_page(self, url):
        """
        Fetch and parse a web page with error handling
        """
 
        try:
            logging.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            if response.status_code == 200:
                logging.info(f"Successfully fetched page (Status: {response.status_code})")
                return BeautifulSoup(response.text, 'lxml')
            else:
                logging.warning(f"Unexpected status code: {response.status_code}")
                return None

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return None
    
    def extract_hotel_data(self, hotel_div):
        """
        Extract hotel information from a hotel div element
        """
        try:
            # Extract hotel name
            name_elem = hotel_div.find('div', class_="b87c397a13 a3e0b4ffd1")
            name = name_elem.text.strip() if name_elem else 'N/A'
            
            # Extract location
            location_elem = hotel_div.find('div', class_="d823fbbeed f9b3563dd4")
            location = location_elem.text.strip() if location_elem else 'N/A'
            
            # Extract review score
            review_elem = hotel_div.find('div', class_="f63b14ab7a f546354b44 becbee2f63")
            review_score = review_elem.text.strip() if review_elem else 'N/A'
            
            # Extract number of reviews
            review_count_elem = hotel_div.find('div', class_="fff1944c52 fb14de7f14 eaa8455879")
            review_count = review_count_elem.text.strip() if review_count_elem else 'N/A'
            
            # Extract price
            price_elem = hotel_div.find('span', class_="b87c397a13 f2f358d1de ab607752a2")
            price = price_elem.text.strip() if price_elem else 'N/A'
            
            return Hotel(
                name=name,
                location=location,
                review_score=review_score,
                review_count=review_count,
                price=price
            )
                
   
        except Exception as e:
            logging.warning(f"Failed to extract hotel data: {e}")
            return None

    def scrape_hotels(self, url):
        """
        Scrape hotel data from a Booking.com search results page
        """
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        # Find all hotel listing divs
        hotel_divs = soup.find_all('div', role="listitem")
        logging.info(f"Found {len(hotel_divs)} potential hotel listings")
        
        hotels = []
        for i, hotel_div in enumerate(hotel_divs, 1):
            hotel = self.extract_hotel_data(hotel_div)
            if hotel:
                hotels.append(hotel)
                logging.debug(f"Extracted hotel {i}: {hotel.name}")
            
            
        
        logging.info(f"Successfully extracted {len(hotels)} hotels")
        return hotels
    
    def save_to_csv(self, hotels, filename):
        """
        Save hotel data to CSV file
        """
        if not filename:    
            filename = "booking_hotels.csv"
   
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write header
                writer.writerow(["Hotel Name", "Location", "Review Score", "Number of Reviews", "Price"])
                
                # Write hotel data
                for hotel in hotels:
                    writer.writerow([
                        hotel.name,
                        hotel.location,
                        hotel.review_score,
                        hotel.review_count,
                        hotel.price
                    ])
            
            logging.info(f"Data saved to {filename}")
            return filename
            
        except Exception as e:
            logging.error(f"Failed to save CSV: {e}")
            raise



def main():
    parser = argparse.ArgumentParser(description='Scrape hotel data from Booking.com')
    parser.add_argument('url', help='Booking.com search results URL')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    parser.add_argument('--output', help='Output filename (without extension)')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Output format')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = BookingHotelScraper(delay=args.delay)
    
    try:
        # Scrape hotels
        hotels = scraper.scrape_hotels(args.url)
        
        if not hotels:
            logging.warning("No hotels found or scraped")
            return
        
        # Save data
        if args.format == 'csv':
            csv_file = scraper.save_to_csv(hotels, args.output and f"{args.output}.csv")
            print(f"CSV data saved to: {csv_file}")
        if args.format == 'json':
            json_file = scraper.save_to_json(hotels, args.output and f"{args.output}.json")
            print(f"JSON data saved to: {json_file}")
        
        
        print(f"Successfully scraped {len(hotels)} hotels!")
        

    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        raise


if __name__ == "__main__":
 
    url ="https://www.booking.com/searchresults.en-gb.html?ss=Paris"
    
    scraper = BookingHotelScraper()
    hotels = scraper.scrape_hotels(url)
    scraper.save_to_csv(hotels)
  
