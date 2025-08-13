# 🏢 Stoa Properties Reviews Scraper

A comprehensive Python script that scrapes reviews from **ALL 11 Stoa properties** with **manual scrolling** and **smart date conversion**.

## ✨ **Key Features**

- 🚀 **Multi-Property Scraping**: Scrapes all 11 Stoa properties automatically
- 📱 **Manual Scrolling**: You control the scrolling for each property
- 📅 **Smart Date Conversion**: Converts relative dates ("2 years ago") to actual dates (2023-08-12)
- 🏠 **Property Identification**: Each review includes a "Property" field to identify which property it belongs to
- 📱 **Google Maps Lite Support**: Optimized for both standard Google Maps and Maps Lite versions
- 📊 **Multiple Output Formats**: JSON (default), CSV, or both
- 🔍 **Advanced Selectors**: Multiple CSS selector strategies for reliable data extraction

## 🏠 **Properties Included**

1. **The Flats at East Bay**
2. **The Heights at Picardy**
3. **The Waters at Bluebonnet**
4. **The Waters at Crestview**
5. **The Waters at Freeport**
6. **The Waters at McGowin**
7. **The Waters at Millerville**
8. **The Waters at Redstone**
9. **The Waters at Settlers Trace**
10. **The Waters at West Village**
11. **The Waters at Hammond**

## 🚀 **Quick Start**

### **Basic Usage (JSON Output)**
```bash
python stoa_properties_reviews_scraper.py
```

### **Headless Mode (No Browser Window)**
```bash
python stoa_properties_reviews_scraper.py --headless
```

### **CSV Output Only**
```bash
python stoa_properties_reviews_scraper.py --output csv
```

### **Both JSON and CSV**
```bash
python stoa_properties_reviews_scraper.py --output both
```

## 📋 **What Gets Scraped**

Each review includes:
- **Property**: Name of the Stoa property (e.g., "The Waters at Hammond")
- **Review Text**: Full review content
- **Rating**: Star rating (1-5)
- **Reviewer Name**: Name of the person who left the review
- **Review Date**: Converted from relative to actual date
- **Original Date**: Relative date as shown on Google Maps
- **Additional Date Fields**: Year, month, month name, day of week
- **Scraped At**: Timestamp when the review was extracted

## 📅 **Date Conversion Examples**

| Original | Converted | Additional Fields |
|----------|-----------|-------------------|
| "2 years ago" | "2023-08-12" | Year: 2023, Month: August |
| "4 months ago" | "2025-04-12" | Year: 2025, Month: April |
| "3 weeks ago" | "2025-07-22" | Year: 2025, Month: July |
| "2 days ago" | "2025-08-10" | Year: 2025, Month: August |

## 🔧 **How It Works**

### **1. Sequential Property Processing**
- Opens each Stoa property one by one
- Automatically detects if it's on a reviews page
- Identifies Google Maps Lite vs. standard version

### **2. Manual Scrolling for Each Property**
- **User Control**: You manually scroll through the reviews for each property
- **Real-time Extraction**: The scraper extracts reviews as you scroll
- **Progress Tracking**: Shows current review count and progress for each property
- **Smart Detection**: Stops when no new reviews are found

### **3. Data Extraction**
- Uses multiple CSS selectors for reliability
- Extracts review text, ratings, names, and dates
- Handles different Google Maps HTML structures
- Adds "Property" field to each review

### **4. Date Processing**
- Converts all relative dates to actual dates
- Adds structured date fields for analysis
- Preserves original relative dates for reference

### **5. Export**
- Primary output: JSON format with all properties combined
- Optional: CSV format
- Automatic filename with timestamp

## 📊 **Output Structure**

### **JSON Format (Default)**
```json
{
  "property": "The Waters at Hammond",
  "reviewer_name": "John Doe",
  "rating": 5,
  "review_text": "Great place to live! The staff is friendly...",
  "review_date_original": "2 years ago",
  "review_date": "2023-08-12",
  "review_year": 2023,
  "review_month": 8,
  "review_month_name": "August",
  "review_day_of_week": "Saturday",
  "scraped_at": "2025-08-12T16:08:56.123456"
}
```

### **CSV Format**
- All fields in columns including "Property"
- Sorted alphabetically for consistency
- UTF-8 encoding

## ⚙️ **Command Line Options**

| Option | Description | Default |
|--------|-------------|---------|
| `--headless` | Run without browser window | False |
| `--output` | Output format: json, csv, or both | json |

## 🎯 **Workflow**

1. **Start Scraping**: Script begins with first property
2. **Navigate to Property**: Opens Google Maps page for each property
3. **Open Reviews Panel**: Clicks on reviews section
4. **Manual Scrolling**: You scroll through reviews to load them all
5. **Data Extraction**: Scraper extracts reviews as you scroll
6. **Property Completion**: Moves to next property when current one is done
7. **Repeat**: Continues until all 11 properties are processed
8. **Date Conversion**: Converts all relative dates to actual dates
9. **Export**: Saves combined data to JSON/CSV files

## 🚨 **Troubleshooting**

### **No Reviews Found for a Property**
- Check if the page is loading correctly
- Verify internet connection
- Try running in non-headless mode to see what's happening

### **Scrolling Issues**
- The scraper waits for you to scroll manually for each property
- Make sure to scroll down in the reviews panel
- Check console output for extraction progress

### **Date Conversion Errors**
- Original relative dates are always preserved
- Check `review_date_original` field for unparseable dates
- Conversion errors are logged but don't stop the process

## 📁 **File Outputs**

- **Primary**: `stoa_properties_reviews_YYYYMMDD_HHMMSS.json`
- **Optional**: `stoa_properties_reviews_YYYYMMDD_HHMMSS.csv`
- **Debug**: `debug_page_source_*.html` and `debug_screenshot_*.png` (if issues occur)

## 🔒 **Privacy & Ethics**

- **Respectful Scraping**: Built-in delays between properties
- **Public Data Only**: Only scrapes publicly available review information
- **Rate Limiting**: Automatic delays to avoid overwhelming servers
- **Educational Use**: Designed for legitimate business analysis

## 🆘 **Support**

If you encounter issues:
1. Check the console output for error messages
2. Run in non-headless mode to see what's happening
3. Check if Google Maps structure has changed
4. Verify all dependencies are installed

## 📦 **Dependencies**

```bash
pip install selenium webdriver-manager fake-useragent
```

## 🎉 **Success Indicators**

- **Property Progress**: Shows "[1/11] Scraping: Property Name"
- **Reviews Extracted**: "✅ Successfully extracted X reviews from Property Name"
- **Total Progress**: "📊 Total reviews so far: X"
- **Date Conversion**: "✅ Date conversion completed: X dates converted successfully"
- **Export Complete**: "💾 JSON exported to: filename.json"

## 🚀 **Usage Tips**

1. **Start with Visible Browser**: Use option 1 first to see what's happening
2. **Scroll Methodically**: Scroll down slowly to load all reviews for each property
3. **Monitor Progress**: Watch the console for extraction progress
4. **Be Patient**: Each property may take several minutes depending on review count
5. **Check Results**: Verify the output files contain reviews from all properties

---

**Happy Scraping! 🚀** The scraper will systematically go through all 11 Stoa properties, extracting reviews as you manually scroll through each one, delivering a comprehensive JSON file with all reviews properly categorized by property and converted dates. 