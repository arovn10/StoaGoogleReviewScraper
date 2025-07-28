# Google Review Scraper Setup Instructions

## Prerequisites

1. **Python 3.8 or higher**
   - Download from: https://python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Google Chrome Browser**
   - Download from: https://www.google.com/chrome/
   - The scraper uses Chrome WebDriver

3. **ChromeDriver**
   - Download from: https://chromedriver.chromium.org/
   - Make sure the version matches your Chrome browser version
   - Add ChromeDriver to your system PATH or place it in the same directory as the script

## Installation Steps

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd StoaGoogleReviewScraper
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import selenium; import requests; import pandas; print('All dependencies installed successfully!')"
   ```

## Running the Scraper

1. **Basic run**
   ```bash
   python StoaGoogleReviewScraper.py
   ```

2. **The scraper will:**
   - Process each Stoa Group property
   - Navigate to Google Maps reviews
   - Extract reviewer names, ratings, and comments
   - Send data to the Domo webhook
   - Display progress and results

## Troubleshooting

### Common Issues:

1. **"Python was not found"**
   - Install Python from https://python.org
   - Make sure to check "Add Python to PATH" during installation
   - Restart your terminal after installation

2. **"ChromeDriver not found"**
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Place it in the same directory as the script or add to PATH

3. **"Module not found" errors**
   - Run: `pip install -r requirements.txt`
   - If that fails, try: `python -m pip install -r requirements.txt`

4. **Chrome crashes or doesn't start**
   - Update Chrome to the latest version
   - Update ChromeDriver to match Chrome version
   - Try running without headless mode (remove `--headless=new` from options)

5. **No reviews found**
   - Google may have changed their page structure
   - The script includes multiple fallback selectors
   - Check if the property URLs are still valid

## Configuration

### Properties List
The properties are defined in the `properties` dictionary in `StoaGoogleReviewScraper.py`. You can:
- Add new properties
- Update URLs if they change
- Remove properties that are no longer needed

### Domo Webhook
The webhook URL is defined in the `domo_webhook` variable. Update it if needed.

## Features

- **Robust error handling**: Continues processing even if one property fails
- **Multiple selectors**: Uses various CSS selectors to handle Google's changing page structure
- **Anti-detection**: Includes measures to avoid being blocked by Google
- **Random delays**: Prevents rate limiting
- **Comprehensive logging**: Shows progress and any issues

## Output

The scraper will output:
- Progress for each property
- Number of reviews found and sent
- Any errors encountered
- Final summary

## Security Notes

- The script runs in headless mode by default
- It includes anti-detection measures
- Random delays prevent rate limiting
- Error handling prevents crashes

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check that Chrome and ChromeDriver versions match
4. Try running without headless mode for debugging 