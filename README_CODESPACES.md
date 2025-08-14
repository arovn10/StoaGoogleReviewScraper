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

### Test Run
```bash
# Run with visible browser (for testing)
python working_auto_scraper.py

# Run in headless mode (for automation)
python working_auto_scraper.py --headless
```

### Scheduled Run (Cron)
```bash
# Edit crontab
crontab -e

# Add this line to run every day at 2 AM
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

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review console output for error messages
3. Ensure all dependencies are properly installed
4. Verify Chrome installation with `google-chrome --version`

---

**Happy Scraping! 🎉** 