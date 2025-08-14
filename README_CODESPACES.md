# 🚀 Google Maps Scraper - GitHub Codespaces Setup

This guide will help you run the Google Maps Scraper in GitHub Codespaces for automated scheduling.

## 📋 Prerequisites

- GitHub Codespaces environment
- Python 3.8+ (should be pre-installed)
- Git access to this repository

## 🛠️ Quick Setup

### Option 1: Automatic Setup (Recommended)
```bash
# Make the setup script executable
chmod +x setup_codespaces.sh

# Run the setup script
./setup_codespaces.sh
```

### Option 2: Manual Setup
```bash
# Update package list
sudo apt-get update

# Install Chrome dependencies
sudo apt-get install -y wget gnupg2 unzip curl

# Install Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Install Python dependencies
pip install -r requirements.txt
```

## 🚀 Running the Scraper

### Test Domo Webhook First
```bash
# Test the Domo webhook connection before running the scraper
python test_domo_webhook.py
```

### Test Run
```bash
# Run with visible browser (for testing)
python working_auto_scraper.py

# Run in headless mode (for automation)
python working_auto_scraper.py --headless

# Run without pushing to Domo (for testing)
python working_auto_scraper.py --headless --no-domo
```

### Scheduled Run (Cron)
```bash
# Edit crontab
crontab -e

# Add this line to run every day at 2 AM with Domo integration
0 2 * * * cd /workspaces/StoaGoogleScraper && python working_auto_scraper.py --headless

# Or run every 6 hours
0 */6 * * * cd /workspaces/StoaGoogleScraper && python working_auto_scraper.py --headless
```

## 📁 Output Files

The scraper will generate:
- `working_auto_scraper_YYYYMMDD_HHMMSS.json` - Review data
- Console output showing progress

## 🔧 Troubleshooting

### Chrome Not Found
```bash
# Check if Chrome is installed
google-chrome --version

# If not found, reinstall
sudo apt-get remove google-chrome-stable
sudo apt-get install google-chrome-stable
```

### Permission Issues
```bash
# Make sure you have sudo access
sudo whoami

# If no sudo access, contact your Codespaces admin
```

### Python Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

## 📊 Monitoring

### Check Scraper Status
```bash
# View recent cron logs
grep "working_auto_scraper" /var/log/cron

# Check if scraper is running
ps aux | grep python
```

### View Output Files
```bash
# List recent output files
ls -la *.json | head -10

# View latest output
ls -t *.json | head -1 | xargs cat | head -20
```

## 🎯 Features

- ✅ **Auto-scrolling** to capture all reviews (including textless ones)
- ✅ **Maps Lite support** for better performance
- ✅ **Multi-property scraping** (10 properties)
- ✅ **Headless mode** for automation
- ✅ **Comprehensive extraction** using proven logic
- ✅ **JSON output** for easy data processing
- ✅ **Domo webhook integration** for automatic data pushing
- ✅ **Batch processing** for large datasets
- ✅ **Retry logic** with exponential backoff
- ✅ **Error handling** and detailed logging

## 🔗 Domo Integration

The scraper automatically pushes data to your Domo instance via webhook with a **flattened structure**:

### 📊 Data Structure (One Row Per Review)
Each review gets its own row in Domo with these fields:

| Field | Description | Example |
|-------|-------------|---------|
| `timestamp` | When the data was sent to Domo | `2025-01-20T15:30:45.123456` |
| `scraper_version` | Version of the scraper | `working_auto_scraper_v1.0` |
| `property_name` | Name of the property | `The Waters at Hammond` |
| `review_text` | Full review text | `Great place to live!` |
| `rating` | Star rating (1-5) | `5` |
| `reviewer_name` | Name of reviewer | `John Smith` |
| `review_date` | Converted date | `2025-01-18` |
| `review_date_original` | Original relative date | `2 days ago` |
| `review_year` | Year of review | `2025` |
| `review_month` | Month of review | `1` |
| `review_month_name` | Month name | `January` |
| `review_day_of_week` | Day of week | `Saturday` |
| `scraped_at` | When review was scraped | `2025-01-20T15:25:30.123456` |
| `extraction_method` | How review was extracted | `maps_lite_specific` |
| `property_url` | Google Maps URL | `https://maps.google.com/...` |
| `debug_info` | Additional debug info | `Element text length: 45` |

### 🚀 What Gets Pushed:
- **Individual reviews**: Each review becomes a separate row
- **Batch processing**: Reviews sent in batches of 100 for efficiency
- **Complete data**: All review fields including metadata
- **Property identification**: Clear property name for each review

### 📈 Expected Domo Results:
Instead of summary data, you'll now see:
- **Row 1**: Review 1 from The Waters at Hammond
- **Row 2**: Review 2 from The Waters at Hammond  
- **Row 3**: Review 1 from The Flats at East Bay
- **Row 4**: Review 2 from The Flats at East Bay
- And so on...

This makes it easy to:
- Filter by property
- Analyze individual reviews
- Create charts and dashboards
- Export specific review data

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review console output for error messages
3. Ensure all dependencies are properly installed
4. Verify Chrome installation with `google-chrome --version`

---

**Happy Scraping! 🎉** 