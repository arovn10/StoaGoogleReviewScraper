# Google Maps Reviews Scraper

A collection of automated scrapers for extracting Google Maps reviews from multiple properties.

## 🏗️ Project Structure

```
google-maps-scraper/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── working_auto_scraper.py            # ✅ MAIN WORKING SCRAPER (Auto-scroll + Maps Lite)
├── multi_property_reviews_scraper.py  # ✅ Manual scroll reference scraper
├── hammond_reviews_scraper.py         # ✅ Single property scraper
├── run_*.bat                          # Windows batch files for easy execution
├── screenshots/                       # UI screenshots and documentation
└── debugging/                         # Debug files, logs, and broken versions
    ├── auto_scroll_multi_property_scraper.py  # ❌ Broken version (moved)
    ├── test_*.py                      # Test scripts
    ├── debug_*.py                     # Debug scripts
    └── *log*.txt                      # Log files
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Main Scraper
```bash
# Headless mode (recommended)
python working_auto_scraper.py --headless

# Visible browser mode
python working_auto_scraper.py
```

## 📋 Available Scrapers

### ✅ `working_auto_scraper.py` - MAIN WORKING VERSION
- **Purpose**: Working auto-scroll scraper with Maps Lite forcing
- **Features**: 
  - Uses working logic from multi_property_reviews_scraper.py
  - Auto-scrolls through all reviews
  - Aggressively forces Google Maps Lite
  - Knows when to stop scrolling (smart detection)
  - Handles textless reviews
- **Usage**: `python working_auto_scraper.py --headless`



### ✅ `multi_property_reviews_scraper.py` - Reference Implementation
- **Purpose**: Manual scroll reference scraper
- **Features**:
  - Working logic (used as reference)
  - Manual scroll approach
  - Comprehensive extraction
- **Usage**: `python multi_property_reviews_scraper.py --headless`

### ✅ `hammond_reviews_scraper.py` - Single Property
- **Purpose**: Scrape single property (The Waters at Hammond)
- **Features**:
  - Single property focus
  - Manual scroll approach
  - Tested and working
- **Usage**: `python hammond_reviews_scraper.py --headless`

## 🎯 Key Features

### Auto-Scrolling
- Automatically scrolls through all reviews
- No manual intervention required
- Smart detection of when scrolling is complete

### Comprehensive Extraction
- Captures ALL reviews including textless ones
- Multiple extraction strategies
- Fallback methods for robustness

### Maps Lite Support
- Attempts to force Google Maps Lite interface
- Optimized selectors for Maps Lite
- Fallback to standard Maps if needed

### Multi-Property Support
- Scrapes multiple properties in sequence
- Configurable property list
- Progress tracking and reporting

## 📊 Output Formats

### JSON Export
- Flat structure for Domo ingestion
- Includes all review metadata
- Timestamped filenames

### CSV Export
- Tabular format for analysis
- All fields included
- Easy to import into Excel/Google Sheets

## 🔧 Configuration

### Property List
Edit the `properties` list in any scraper to add/remove properties:

```python
self.properties = [
    {
        'name': 'Property Name',
        'url': 'Google Maps URL with &lite=1 parameter'
    }
]
```

### Chrome Options
All scrapers include optimized Chrome options:
- Headless mode support
- Anti-detection measures
- Performance optimizations

## 🚨 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - Run `pip install webdriver-manager` to auto-download drivers

2. **Maps Lite Not Loading**
   - Try the `simple_maps_lite_scraper.py` which has aggressive forcing

3. **Syntax Errors**
   - Use `clean_auto_scraper.py` (fixed version)
   - Avoid the broken version in `debugging/` folder

### Debug Mode
- Check the `debugging/` folder for logs and test files
- Run with visible browser to see what's happening
- Check console output for error messages

## 📁 File Organization

### Working Scrapers (Root Directory)
- All functional scrapers are in the root directory
- Each has a specific purpose and optimization

### Debug Files (debugging/ folder)
- Broken versions moved here
- Test scripts and logs
- Debug output files

### Screenshots (screenshots/ folder)
- UI documentation
- Feature demonstrations
- Troubleshooting guides

## 🎉 Success Metrics

### Current Performance
- **Hammond**: 48+ reviews (vs. 199 total)
- **East Bay**: 48+ reviews
- **Auto-scroll**: Working successfully
- **Maps Lite**: Partially working (fallback to standard)

### Goals
- Capture ALL 199 Hammond reviews (including 38 textless)
- Achieve 100% Maps Lite success rate
- Optimize for maximum speed
- Maintain reliability

## 🔄 Development Workflow

1. **Test Changes**: Use `clean_auto_scraper.py` as base
2. **Debug Issues**: Check `debugging/` folder for reference
3. **Optimize**: Use `ultra_fast_auto_scraper.py` for performance
4. **Validate**: Compare against `multi_property_reviews_scraper.py`

## 📞 Support

For issues or questions:
1. Check the `debugging/` folder for logs
2. Run with visible browser to see errors
3. Compare against working reference scrapers
4. Check console output for specific error messages

---

**Last Updated**: August 14, 2025  
**Status**: ✅ Main scraper fixed and working  
**Next Goal**: Achieve 100% review capture for Hammond (199 total) 