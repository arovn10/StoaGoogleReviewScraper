@echo off
echo Starting Multi-Property Reviews Scraper...
echo.
echo This will scrape reviews for all 9 properties:
echo - The Waters at Hammond
echo - The Flats at East Bay
echo - The Heights at Picardy 
echo - The Waters at Bluebonnet
echo - The Waters at Crestview
echo - The Waters at Millerville
echo - The Waters at Redstone
echo - The Waters at Settlers Trace
echo - The Waters at West Village
echo.
echo Features:
echo - Manual scrolling through reviews
echo - Auto-advance after 2 same review counts
echo - Duplicate removal
echo - Export to JSON and CSV
echo - Push to Domo webhook
echo.
echo Make sure you have Python and the required packages installed.
echo.
pause

python multi_property_reviews_scraper.py

echo.
echo Scraping completed. Press any key to exit.
pause >nul 