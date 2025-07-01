# Booking.com Hotel Scraper

A professional web scraping tool for extracting hotel information from Booking.com search results. This project demonstrates advanced web scraping techniques, error handling, and data management practices.

## 🎯 Features

- **Robust Web Scraping**: Extracts hotel data including name, location, reviews, and pricing
- **Error Handling**: Comprehensive exception handling and logging
- **Command Line Interface**: Easy-to-use CLI for different scraping scenarios
- **Professional Logging**: Detailed logging for debugging and monitoring


## 📋 Requirements

```txt
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/booking-hotel-scraper.git
cd booking-hotel-scraper
```



## 💻 Usage

### Basic Usage

```python
from booking_scraper import BookingHotelScraper

# Initialize scraper
scraper = BookingHotelScraper()

# Scrape hotels
url = "https://www.booking.com/searchresults.en-gb.html?ss=Sousse..."
hotels = scraper.scrape_hotels(url)

# Save data
scraper.save_to_csv(hotels)
```

### Command Line Interface

```bash
# Basic scraping
python main.py "https://www.booking.com/searchresults.en-gb.html?ss=Sousse..."

# Custom output filename
python main.py "URL_HERE" --output "sousse_hotels"

# Custom delay between requests
python main.py "URL_HERE" --delay 2.0
```

## 📊 Output Format

### CSV Output
```csv
Hotel Name,Location,Review Score,Number of Reviews,Price
Hotel Example,Sousse Center,8.5,245 reviews,€85
```


## 🔧 Configuration

### Scraper Parameters

- `delay`: Time delay between requests (default: 1.0 seconds)
- `timeout`: Request timeout (default: 10 seconds)
- `output_format`: Data export format (csv)

### Logging

The scraper generates detailed logs in `scraper.log` including:
- Request status and timing
- Data extraction success/failure
- Error messages and debugging information

## ⚠️ Important Notes

### Legal and Ethical Considerations

- **Respect robots.txt**: Always check the website's robots.txt file
- **Rate Limiting**: Built-in delays prevent server overload
- **Terms of Service**: Ensure compliance with Booking.com's terms
- **Personal Use**: This tool is for educational and personal use only

### Technical Limitations

- Class names may change over time (web scraping is fragile)
- Some data might be loaded dynamically via JavaScript
- Large-scale scraping may trigger anti-bot measures

## 🛠️ Advanced Features

### Custom Data Extraction

```python
class CustomScraper(BookingHotelScraper):
    def extract_hotel_data(self, hotel_div):
        # Override method for custom data extraction
        # Add additional fields like amenities, photos, etc.
        pass
```

### Batch Processing

```python
urls = [
    "https://booking.com/search?ss=Paris",
    "https://booking.com/search?ss=London",
    "https://booking.com/search?ss=Rome"
]

for url in urls:
    hotels = scraper.scrape_hotels(url)
    city = extract_city_from_url(url)
    scraper.save_to_csv(hotels, f"{city}_hotels.csv")
```

## 🐛 Troubleshooting

### Common Issues

1. **No data extracted**: Check if class names have changed
2. **Request blocked**: Increase delay between requests
3. **Invalid URL**: Ensure you're using a valid Booking.com search URL

### Error Handling

The scraper includes comprehensive error handling:
- Network timeout errors
- HTML parsing errors
- Data extraction failures
- File I/O errors

## 📈 Performance Tips

- Use appropriate delays (1-2 seconds recommended)
- Process data in batches for large datasets
- Monitor logs for performance bottlenecks
- Consider using proxies for large-scale scraping

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


---

**⭐ If you found this project helpful, please consider giving it a star!**
