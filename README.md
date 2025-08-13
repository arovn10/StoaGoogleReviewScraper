# Google Maps Scraper

A clean, organized project for scraping Google Maps reviews.

## Project Structure

```
google-maps-scraper/
├── multi_property_reviews_scraper.py  # Main scraper script
├── requirements.txt                    # Python dependencies
├── data/                              # All data files
│   ├── json/                          # JSON output files
│   ├── csv/                           # CSV output files
│   └── logs/                          # Log files and debug data
├── scripts/                           # Utility scripts
│   ├── batch/                         # Batch files for running scrapers
│   └── utilities/                     # Helper scripts and tools
├── docs/                              # Documentation
└── screenshots/                       # Screenshots and images
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main scraper:
   ```bash
   python multi_property_reviews_scraper.py
   ```

3. For headless mode:
   ```bash
   python multi_property_reviews_scraper.py --headless
   ```

## Main Scripts

- **`multi_property_reviews_scraper.py`** - Main scraper for multiple properties
- **`scripts/batch/`** - Batch files for easy execution
- **`scripts/utilities/`** - Helper scripts for data processing

## Data Output

- **JSON**: `data/json/` - Structured review data
- **CSV**: `data/csv/` - Tabular review data  
- **Logs**: `data/logs/` - Execution logs and debug info

## Documentation

See `docs/` folder for detailed documentation on each component. 