@echo off
echo Starting Auto-Scroll Multi-Property Reviews Scraper...
echo.
echo This will automatically scrape reviews for all 9 properties:
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
echo - Automatic scrolling (no manual intervention needed)
echo - Exact same extraction logic as original scraper
echo - Auto-advance after 2 consecutive same review counts
echo - Duplicate removal
echo - Automatic Domo push
echo.
echo Make sure you have Python and the required packages installed.
echo.
pause

python auto_scroll_multi_property_scraper.py

echo.
echo Scraping completed. Press any key to exit.
pause >nul 