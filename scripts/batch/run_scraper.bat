@echo off
echo ========================================
echo    Google Maps Scraper - Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
)

echo.
echo Dependencies are ready!
echo.
echo Choose scraping mode:
echo 1. Search for specific businesses/locations
echo 2. Scrape all Stoa properties automatically
echo.
set /p mode_choice=

if "%mode_choice%"=="2" (
    echo.
    echo 🏢 Stoa Properties Mode Selected
    echo.
    echo Choose output format:
    echo 1. CSV only
    echo 2. JSON only  
    echo 3. Both formats
    set /p format_choice=
    
    if "%format_choice%"=="1" (
        set output_format=csv
    ) else if "%format_choice%"=="2" (
        set output_format=json
    ) else if "%format_choice%"=="3" (
        set output_format=both
    ) else (
        set output_format=csv
    )
    
    echo.
    echo Starting Stoa properties scraper with:
    echo Output format: %output_format%
    echo.
    echo Press any key to continue...
    pause >nul
    
    echo.
    echo 🚀 Starting Stoa Properties Scraper...
    echo.
    
    REM Run the enhanced scraper for Stoa properties
    python google_maps_scraper_enhanced.py --stoa_properties --output_format %output_format%
    
    echo.
    echo Stoa properties scraping completed! Check the output files above.
    echo.
    pause
    exit /b 0
)

REM Regular search mode
echo.
echo 🔍 Search Mode Selected
echo.
echo Enter your search query (e.g., "restaurants in New York"):
set /p query=

if "%query%"=="" (
    echo No query entered. Using default example...
    set query=pizza
)

echo.
echo Enter maximum number of results (1-120, default 20):
set /p max_results=

if "%max_results%"=="" (
    set max_results=20
)

echo.
echo Choose output format:
echo 1. CSV only
echo 2. JSON only  
echo 3. Both formats
set /p format_choice=

if "%format_choice%"=="1" (
    set output_format=csv
) else if "%format_choice%"=="2" (
    set output_format=json
) else if "%format_choice%"=="3" (
    set output_format=both
) else (
    set output_format=csv
)

echo.
echo Starting scraper with:
echo Query: %query%
echo Max results: %max_results%
echo Output format: %output_format%
echo.
echo Press any key to continue...
pause >nul

echo.
echo 🚀 Starting Google Maps Scraper...
echo.

REM Run the enhanced scraper
python google_maps_scraper_enhanced.py "%query%" --max_results %max_results% --output_format %output_format%

echo.
echo Scraping completed! Check the output files above.
echo.
pause 