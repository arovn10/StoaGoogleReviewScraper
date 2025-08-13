@echo off
title Stoa Properties Reviews Scraper
color 0A

echo.
echo ========================================
echo   STOA PROPERTIES REVIEWS SCRAPER
echo ========================================
echo.
echo This will scrape reviews from ALL 11 Stoa properties
echo with manual scrolling and automatic date conversion.
echo.
echo Properties included:
echo   - The Flats at East Bay
echo   - The Heights at Picardy
echo   - The Waters at Bluebonnet
echo   - The Waters at Crestview
echo   - The Waters at Freeport
echo   - The Waters at McGowin
echo   - The Waters at Millerville
echo   - The Waters at Redstone
echo   - The Waters at Settlers Trace
echo   - The Waters at West Village
echo   - The Waters at Hammond
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
echo This will scrape ALL 11 Stoa properties one by one.
echo You'll need to manually scroll through reviews for each property.
echo.
python stoa_properties_reviews_scraper.py
goto end

:run_headless_json
echo.
echo Starting scraper in headless mode (JSON output)...
echo This will scrape ALL 11 Stoa properties one by one.
echo Note: Manual scrolling won't work in headless mode.
echo.
python stoa_properties_reviews_scraper.py --headless
goto end

:run_visible_csv
echo.
echo Starting scraper with visible browser (CSV output)...
echo This will scrape ALL 11 Stoa properties one by one.
echo You'll need to manually scroll through reviews for each property.
echo.
python stoa_properties_reviews_scraper.py --output csv
goto end

:run_visible_both
echo.
echo Starting scraper with visible browser (Both JSON and CSV)...
echo This will scrape ALL 11 Stoa properties one by one.
echo You'll need to manually scroll through reviews for each property.
echo.
python stoa_properties_reviews_scraper.py --output both
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