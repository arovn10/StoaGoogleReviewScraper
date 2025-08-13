# Google Maps Scraper - Personal Version

A powerful Python-based Google Maps scraper that extracts comprehensive business information from Google Maps search results. This is your own personal scraper that replicates the functionality of the original Google Maps Scraper project.

## 🚀 Features

- **Comprehensive Data Extraction**: Extracts 40+ data points including:
  - Basic info (name, description, rating, reviews)
  - Contact details (phone, address, website)
  - Business details (categories, hours, status)
  - Social media links (Facebook, Twitter, Instagram, LinkedIn, etc.)
  - Reviews and ratings information
  - Geographic data (coordinates, plus codes)
  - And much more!

- **Multiple Output Formats**: Export data to CSV, JSON, or both
- **Flexible Search**: Search by business type, location, or specific queries
- **Rate Limiting**: Built-in delays to avoid being blocked
- **Error Handling**: Robust error handling and retry mechanisms
- **Two Versions**: Basic (requests-based) and Enhanced (Selenium-based)
- **🎯 Stoa Properties Integration**: Pre-loaded with all Stoa property IDs for automatic scraping

## 📋 Requirements

- Python 3.7 or higher
- Google Chrome browser (for enhanced version)
- Internet connection

## 🛠️ Installation

1. **Clone or download the files** to your local machine

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Chrome installation** (for enhanced version):
   - Make sure Google Chrome is installed on your system
   - The script will automatically download the appropriate ChromeDriver

## 📁 Files Overview

- `google_maps_scraper.py` - Basic version using requests library
- `google_maps_scraper_enhanced.py` - Enhanced version using Selenium WebDriver
- `stoa_properties_scraper.py` - **NEW!** Dedicated script for Stoa properties
- `example_usage.py` - Example script showing programmatic usage
- `requirements.txt` - Required Python packages
- `run_scraper.bat` - Windows batch file launcher
- `README_SCRAPER.md` - This documentation file

## 🎯 Usage

### 🏢 Stoa Properties Scraping (NEW!)

The easiest way to scrape all Stoa properties:

```bash
# Scrape all Stoa properties to CSV
python stoa_properties_scraper.py

# Scrape all Stoa properties to JSON
python stoa_properties_scraper.py --output_format json

# Scrape all Stoa properties to both formats
python stoa_properties_scraper.py --output_format both
```

Or use the enhanced scraper directly:

```bash
python google_maps_scraper_enhanced.py --stoa_properties --output_format csv
```

### Command Line Usage

#### Basic Version
```bash
python google_maps_scraper.py "restaurants in New York" --max_results 50 --output_format csv
```

#### Enhanced Version (Recommended)
```bash
python google_maps_scraper_enhanced.py "coffee shops in San Francisco" --max_results 100 --output_format both
```

### Windows Batch File

Double-click `run_scraper.bat` and choose:
1. **Search Mode**: Search for specific businesses/locations
2. **Stoa Properties Mode**: Automatically scrape all Stoa properties

### Command Line Options

- `query`: Your search query (required for search mode)
- `--stoa_properties`: Scrape all pre-loaded Stoa properties instead of searching
- `--max_results`: Maximum number of results (default: 120, max: 120)
- `--output_format`: Output format - csv, json, or both (default: csv)
- `--output_file`: Custom output filename (without extension)
- `--headless`: Run browser in headless mode (enhanced version only, default: True)
- `--timeout`: Timeout for element waiting in seconds (enhanced version only, default: 30)

### Programmatic Usage

```python
from google_maps_scraper_enhanced import EnhancedGoogleMapsScraper

# Initialize scraper
scraper = EnhancedGoogleMapsScraper(headless=True)

# Option 1: Search for places
places = scraper.search_places("pizza in Chicago", max_results=20)

# Option 2: Scrape all Stoa properties
stoa_data = scraper.scrape_stoa_properties(output_format='both')

# Export data
scraper.export_to_csv(places, "chicago_pizza.csv")
scraper.export_to_json(places, "chicago_pizza.json")

# Always close the scraper
scraper.close()
```

## 🏢 Stoa Properties Included

The scraper comes pre-loaded with all Stoa property IDs:

### Stoa Group Properties
- **Stoa Group**: 5640593249504814493
- **The Flats at East Bay**: 15423722144744456392
- **The Heights at Picardy**: 11603332273223782460

### The Waters Properties
- **The Waters at Bluebonnet**: 16738007922303343196
- **The Waters at Crestview**: 13297649119718305349
- **The Waters at Freeport**: 15766105729835349285
- **The Waters at McGowin**: 1563574346652941468
- **The Waters at Millerville**: 18023488087696788689
- **The Waters at Redstone**: 11477464308785240821

### Greystar Managed Properties
- **The Waters at Hammond**: 8169905190679972139
- **The Waters at Settlers Trace**: 14730649020717053754
- **The Waters at West Village**: 17027270425469346950

## 📊 Data Fields Extracted

The scraper extracts the following data fields (when available):

### Basic Information
- `name` - Business name
- `description` - Business description
- `rating` - Average rating (1-5 stars)
- `reviews` - Number of reviews
- `place_id` - Google Maps place ID
- `property_name` - Stoa property name (for Stoa properties)
- `stoa_place_id` - Stoa property ID (for Stoa properties)

### Contact Information
- `phone` - Phone number
- `website` - Business website
- `address` - Physical address
- `email` - Email address (if available)

### Business Details
- `categories` - Business categories
- `main_category` - Primary business category
- `status` - Open/Closed status
- `workday_timing` - Operating hours
- `price_range` - Price range indicators

### Social Media
- `facebook` - Facebook profile URL
- `twitter` - Twitter profile URL
- `instagram` - Instagram profile URL
- `linkedin` - LinkedIn profile URL
- `youtube` - YouTube channel URL
- And more social platforms...

### Additional Data
- `coordinates` - Latitude and longitude
- `plus_code` - Google Plus Code
- `time_zone` - Business timezone
- `featured_image` - Business image URL
- `review_keywords` - Review-related keywords

## 🔧 Configuration

### Rate Limiting
Adjust the delay between requests in the scraper class:
```python
self.delay_between_requests = 2  # seconds between requests
```

### Browser Options (Enhanced Version)
Modify Chrome options in the `setup_driver` method:
```python
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
```

### Stoa Properties
Add or modify Stoa properties in the `__init__` method:
```python
self.stoa_properties = {
    "Property Name": "google_business_profile_id",
    # Add more properties here
}
```

## ⚠️ Important Notes

### Legal and Ethical Considerations
- **Respect robots.txt**: Always check if scraping is allowed
- **Rate limiting**: Built-in delays to avoid overwhelming servers
- **Terms of service**: Ensure compliance with Google's terms
- **Personal use only**: This tool is for personal, educational, or research purposes

### Technical Limitations
- **Maximum results**: Google Maps typically shows max 120 results per search
- **Dynamic content**: Google Maps uses JavaScript, so the enhanced version is recommended
- **Anti-bot measures**: Google may implement measures to detect automated access
- **IP blocking**: Excessive requests may result in temporary IP blocking

### Best Practices
1. **Start small**: Begin with fewer results to test
2. **Use delays**: Don't remove the built-in delays
3. **Respect limits**: Don't exceed reasonable usage patterns
4. **Monitor output**: Check your results for accuracy
5. **Handle errors**: The script includes error handling, but monitor for issues

## 🚨 Troubleshooting

### Common Issues

#### ChromeDriver Issues
```bash
# Reinstall ChromeDriver
pip uninstall webdriver-manager
pip install webdriver-manager
```

#### Import Errors
```bash
# Install missing packages
pip install -r requirements.txt
```

#### No Results Found
- Check your search query
- Verify internet connection
- Try different search terms
- Check if Google Maps is accessible

#### Browser Crashes
- Reduce the number of results
- Increase timeout values
- Check available system memory
- Update Chrome browser

### Performance Tips

1. **Use headless mode** (default) for better performance
2. **Limit results** to what you actually need
3. **Close browser** properly after use
4. **Monitor memory usage** during long scraping sessions

## 📈 Example Output

### CSV Output
```csv
property_name,stoa_place_id,name,rating,reviews,phone,website,address,categories
The Waters at Bluebonnet,16738007922303343196,The Waters at Bluebonnet,4.5,127,+1-555-1234,https://watersbluebonnet.com,123 Main St,Apartment Building
The Flats at East Bay,15423722144744456392,The Flats at East Bay,4.2,89,+1-555-5678,https://flatseastbay.com,456 Oak Ave,Apartment Building
```

### JSON Output
```json
[
  {
    "property_name": "The Waters at Bluebonnet",
    "stoa_place_id": "16738007922303343196",
    "name": "The Waters at Bluebonnet",
    "rating": 4.5,
    "reviews": 127,
    "phone": "+1-555-1234",
    "website": "https://watersbluebonnet.com",
    "address": "123 Main St",
    "categories": ["Apartment Building"],
    "coordinates": {"latitude": 40.7128, "longitude": -74.0060}
  }
]
```

## 🔄 Updates and Maintenance

- **Regular updates**: Keep dependencies updated
- **Monitor changes**: Google Maps may change their structure
- **Test regularly**: Verify scraping still works
- **Backup data**: Keep backups of important scraped data

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Test with simple queries first
4. Ensure all dependencies are installed

## 📜 License

This project is for personal use only. Please respect:
- Google's Terms of Service
- Website robots.txt files
- Rate limiting and fair use policies
- Local and international laws regarding web scraping

## 🎉 Getting Started

### Quick Start with Stoa Properties
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Run Stoa scraper**: `python stoa_properties_scraper.py`
3. **Check output**: Verify data is extracted correctly

### Quick Start with General Search
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Test with a simple query**: `python google_maps_scraper_enhanced.py "pizza"`
3. **Check the output**: Verify data is extracted correctly
4. **Customize as needed**: Modify the script for your specific requirements

### Windows Users
1. **Double-click** `run_scraper.bat`
2. **Choose mode**: Stoa Properties or Search
3. **Follow prompts** and wait for completion

Happy scraping! 🚀 