@echo off
title The Waters at Hammond Reviews Scraper
color 0A

echo.
echo ========================================
echo   THE WATERS AT HAMMOND REVIEWS SCRAPER
echo ========================================
echo.
echo This will scrape all 199 reviews with manual scrolling
echo and automatic date conversion to JSON.
echo.

:menu
echo Choose an option:
echo.
echo 1. Run with visible browser (JSON output)
echo 2. Run headless (JSON output) 
echo 3. Run with visible browser (CSV output)
echo 4. Run with visible browser (Both JSON and CSV)
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto run_visible_json
if "%choice%"=="2" goto run_headless_json
if "%choice%"=="3" goto run_visible_csv
if "%choice%"=="4" goto run_visible_both
if "%choice%"=="5" goto exit
echo Invalid choice. Please try again.
goto menu

:run_visible_json
echo.
echo Starting scraper with visible browser (JSON output)...
echo.
python hammond_reviews_scraper.py
goto end

:run_headless_json
echo.
echo Starting scraper in headless mode (JSON output)...
echo.
python hammond_reviews_scraper.py --headless
goto end

:run_visible_csv
echo.
echo Starting scraper with visible browser (CSV output)...
echo.
python hammond_reviews_scraper.py --output csv
goto end

:run_visible_both
echo.
echo Starting scraper with visible browser (Both JSON and CSV)...
echo.
python hammond_reviews_scraper.py --output both
goto end

:end
echo.
echo Scraping completed! Check the output files above.
echo.
pause
goto menu

:exit
echo.
echo Goodbye!
pause
exit 