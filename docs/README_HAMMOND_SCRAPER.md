# 🏢 The Waters at Hammond Reviews Scraper

A specialized Python script that scrapes **all 199 reviews** for "The Waters at Hammond" from Google Maps with **manual scrolling** and **smart date conversion**.

## ✨ **Key Features**

- 🚀 **Manual Scrolling**: You control the scrolling to load all reviews - the scraper extracts data as you scroll
- 📅 **Smart Date Conversion**: Converts relative dates ("2 years ago") to actual dates (2023-08-12)
- 📱 **Google Maps Lite Support**: Optimized for both standard Google Maps and Maps Lite versions
- 🎯 **Target: 199 Reviews**: Designed specifically to capture all available reviews
- 📊 **Multiple Output Formats**: JSON (default), CSV, or both
- 🔍 **Advanced Selectors**: Multiple CSS selector strategies for reliable data extraction

## 🚀 **Quick Start**

### **Basic Usage (JSON Output)**
```bash
python hammond_reviews_scraper.py
```

### **Headless Mode (No Browser Window)**
```bash
python hammond_reviews_scraper.py --headless
```

### **CSV Output Only**
```bash
python hammond_reviews_scraper.py --output csv
```

### **Both JSON and CSV**
```bash
python hammond_reviews_scraper.py --output both
```

## 📋 **What Gets Scraped**

Each review includes:
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

### **1. Navigation**
- Opens Google Maps page for "The Waters at Hammond"
- Automatically detects if it's on a reviews page
- Identifies Google Maps Lite vs. standard version

### **2. Manual Scrolling**
- **User Control**: You manually scroll through the reviews
- **Real-time Extraction**: The scraper extracts reviews as you scroll
- **Progress Tracking**: Shows current review count and progress
- **Smart Detection**: Stops when no new reviews are found

### **3. Data Extraction**
- Uses multiple CSS selectors for reliability
- Extracts review text, ratings, names, and dates
- Handles different Google Maps HTML structures

### **4. Date Processing**
- Converts all relative dates to actual dates
- Adds structured date fields for analysis
- Preserves original relative dates for reference

### **5. Export**
- Primary output: JSON format
- Optional: CSV format
- Automatic filename with timestamp

## 📊 **Output Structure**

### **JSON Format (Default)**
```json
{
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
- All fields in columns
- Sorted alphabetically for consistency
- UTF-8 encoding

## ⚙️ **Command Line Options**

| Option | Description | Default |
|--------|-------------|---------|
| `--headless` | Run without browser window | False |
| `--output` | Output format: json, csv, or both | json |

## 🎯 **Target Achievement**

The scraper is designed to reach the target of **199 reviews** by:
- **Manual scrolling** - you control the pace and direction
- **Real-time extraction** as reviews become visible
- **Smart detection** of when all reviews are loaded
- **Progress tracking** with detailed logging

## 🚨 **Troubleshooting**

### **No Reviews Found**
- Check if the page is loading correctly
- Verify internet connection
- Try running in non-headless mode to see what's happening

### **Scrolling Issues**
- The scraper waits for you to scroll manually
- Make sure to scroll down in the reviews panel
- Check console output for extraction progress

### **Date Conversion Errors**
- Original relative dates are always preserved
- Check `review_date_original` field for unparseable dates
- Conversion errors are logged but don't stop the process

## 📁 **File Outputs**

- **Primary**: `hammond_reviews_YYYYMMDD_HHMMSS.json`
- **Optional**: `hammond_reviews_YYYYMMDD_HHMMSS.csv`
- **Debug**: `debug_page_source_*.html` and `debug_screenshot_*.png` (if issues occur)

## 🔒 **Privacy & Ethics**

- **Respectful Scraping**: Built-in delays between requests
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

- **Target Reached**: "🎯 Target reached! Found 199 reviews"
- **Date Conversion**: "✅ Date conversion completed: X dates converted successfully"
- **Export Complete**: "💾 JSON exported to: filename.json"

---

**Happy Scraping! 🚀** The scraper will extract reviews as you manually scroll through them, delivering a comprehensive JSON file with all 199 reviews and properly converted dates. 