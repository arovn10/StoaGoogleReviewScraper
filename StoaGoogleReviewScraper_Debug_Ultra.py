#!/usr/bin/env python3
"""
Debug Ultra-Aggressive Google Review Scraper
Runs in non-headless mode to debug why some properties are failing
"""

import time
import json
import requests
import random
import re
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Focus on the properties that failed in the ultra scraper
properties = {
    "The Waters at Settlers Trace": [
        "https://www.google.com/maps/place/The+Waters+at+Settlers+Trace/@30.7362861,-86.5595057,978m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8891731ed5ef4421:0xe82971b01b043e0e!8m2!3d30.7362861!4d-86.5569308!5e0!3m1!1s0x8891731ed5ef4421:0xe82971b01b043e0e!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Settlers+Trace+reviews"
    ],
    "The Waters at Redstone": [
        "https://www.google.com/maps/place/The+Waters+at+Redstone/@30.7362861,-86.5595057,978m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8891731ed5ef4421:0xe82971b01b043e0e!8m2!3d30.7362861!4d-86.5569308!5e0!3m1!1s0x8891731ed5ef4421:0xe82971b01b043e0e!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Redstone+reviews"
    ],
    "The Waters at Millerville": [
        "https://www.google.com/maps/place/The+Waters+at+Millerville/@30.4397504,-91.0289876,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626bd7f2db7ca89:0x1d15edca3d614c78!8m2!3d30.4397504!4d-91.0264127!5e0!3m1!1s0x8626bd7f2db7ca89:0x1d15edca3d614c78!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Millerville+reviews"
    ],
    "The Waters at McGowin": [
        "https://www.google.com/maps/place/The+Waters+at+McGowin/@30.6516886,-88.1154892,979m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a4db406a47bd1:0xa0adc97698cb8809!8m2!3d30.6516886!4d-88.1129143!5e0!3m1!1s0x889a4db406a47bd1:0xa0adc97698cb8809!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+McGowin+reviews"
    ],
    "The Waters at Freeport": [
        "https://www.google.com/maps/place/The+Waters+at+Freeport/@30.486358,-86.1287459,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8893dda15e2f9069:0x3177e609fc299d13!8m2!3d30.486358!4d-86.126171!5e0!3m1!1s0x8893dda15e2f9069:0x3177e609fc299d13!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Freeport+reviews"
    ],
    "The Waters at Crestview": [
        "https://www.google.com/maps/place/The+Waters+at+Crestview/@30.7327129,-86.5707133,1957m/data=!3m1!1e3!5e0!3m1!1s0x889a4db406a47bd1:0xa0adc97698cb8809!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Crestview+reviews"
    ],
    "The Flats at East Bay": [
        "https://www.google.com/maps/place/The+Flats+at+East+Bay/@30.5014556,-87.8652493,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!8m2!3d30.5014556!4d-87.8626744!5e0!3m1!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!2m1!1e1",
        "https://www.google.com/maps/search/The+Flats+at+East+Bay+reviews"
    ],
    "The Waters at Hammond": [
        "https://www.google.com/maps/place/The+Waters+at+Hammond/@30.4877443,-90.465321,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x862723fbcc2afb85:0x188d3eeca51192d0!8m2!3d30.4877443!4d-90.4627461!5e0!3m1!1s0x862723fbcc2afb85:0x188d3eeca51192d0!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Hammond+reviews"
    ]
}

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

def setup_driver():
    """Setup Chrome driver with anti-detection measures - NON-HEADLESS for debugging"""
    options = Options()
    # options.add_argument("--headless=new")  # COMMENTED OUT FOR DEBUGGING
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    # options.add_argument("--disable-images")  # COMMENTED OUT FOR DEBUGGING
    # options.add_argument("--disable-javascript")  # COMMENTED OUT FOR DEBUGGING
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def handle_consent_popup(driver):
    """Handle various consent popups that may appear"""
    try:
        # Try to find and click "Accept all" button
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all') or contains(., 'I agree') or contains(., 'Accept')]"))
        )
        accept_button.click()
        time.sleep(2)
        return True
    except TimeoutException:
        try:
            # Try to find and click "Reject all" if "Accept all" not found
            reject_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Reject all') or contains(., 'Decline')]"))
            )
            reject_button.click()
            time.sleep(2)
            return True
        except TimeoutException:
            return False

def wait_for_page_load(driver):
    """Wait for page to load"""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)
    except TimeoutException:
        print("Page load timeout")

def click_reviews_tab(driver):
    """Try to click on reviews tab"""
    review_tab_selectors = [
        "//button[contains(., 'Reviews')]",
        "//a[contains(., 'Reviews')]",
        "//div[contains(., 'Reviews')]",
        "//span[contains(., 'Reviews')]",
        "//button[contains(@aria-label, 'Reviews')]"
    ]
    
    for selector in review_tab_selectors:
        try:
            reviews_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            print(f"Found reviews tab with selector: {selector}")
            reviews_tab.click()
            time.sleep(3)
            return True
        except TimeoutException:
            continue
    
    print("No reviews tab found, scrolling to find it...")
    # Scroll down to find reviews section
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)
    
    for selector in review_tab_selectors:
        try:
            reviews_tab = driver.find_element(By.XPATH, selector)
            if reviews_tab.is_displayed():
                print(f"Found reviews tab after scrolling with selector: {selector}")
                reviews_tab.click()
                time.sleep(3)
                return True
        except NoSuchElementException:
            continue
    
    print("    Could not find reviews tab, trying alternative approach...")
    return False

def scroll_reviews_section(driver):
    """Scroll through reviews section to load more reviews"""
    container_selectors = [
        "//div[contains(@class, 'm6QErb')]",
        "//div[contains(@class, 'review-dialog-list')]",
        "//div[contains(@class, 'reviews')]",
        "//div[contains(@class, 'review')]",
        "//div[contains(@class, 'scrollable')]"
    ]
    
    scrollable_container = None
    for selector in container_selectors:
        try:
            container = driver.find_element(By.XPATH, selector)
            if container:
                scrollable_container = container
                print(f"Found scrollable container with selector: {selector}")
                break
        except NoSuchElementException:
            continue
    
    if scrollable_container:
        # Scroll multiple times to load more reviews
        for i in range(5):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_container)
            time.sleep(random.uniform(1, 2))
    else:
        # Fallback: scroll the whole page
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 2))

def extract_reviews_data(driver):
    """Extract review data from the page with enhanced selectors"""
    reviews = []
    try:
        # Wait for reviews to load
        time.sleep(3)
        
        # Multiple possible selectors for review cards
        review_card_selectors = [
            "//div[@data-review-id]",
            "//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'review-dialog-list')]//div[contains(@class, 'g88MCb')]",
            "//div[contains(@class, 'review-dialog-list')]//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'review-dialog')]//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'reviews')]//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'review')]//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'g88MCb')]",
            "//div[contains(@class, 'review-card')]",
            "//div[contains(@class, 'review-item')]",
            "//div[contains(@class, 'review')]",
            "//div[contains(@class, 'comment')]",
            "//div[contains(@class, 'feedback')]"
        ]
        
        review_cards = []
        for selector in review_card_selectors:
            try:
                cards = driver.find_elements(By.XPATH, selector)
                if cards:
                    review_cards = cards
                    print(f"Found {len(cards)} review cards with selector: {selector}")
                    break
            except Exception:
                continue
        
        if not review_cards:
            print("No review cards found")
            return reviews
        
        print(f"Processing {len(review_cards)} review cards")
        
        for card in review_cards:
            try:
                # Extract reviewer name
                name_selectors = [
                    ".//div[contains(@class, 'd4r55')]",
                    ".//div[contains(@class, 'TSUbDb')]",
                    ".//span[contains(@class, 'd4r55')]",
                    ".//div[contains(@class, 'reviewer-name')]",
                    ".//div[contains(@class, 'name')]",
                    ".//span[contains(@class, 'name')]",
                    ".//div[contains(@class, 'author')]",
                    ".//div[contains(@class, 'user')]",
                    ".//span[contains(@class, 'user')]"
                ]
                
                name = "Unknown"
                for selector in name_selectors:
                    try:
                        name_elem = card.find_element(By.XPATH, selector)
                        name = name_elem.text.strip()
                        if name:
                            break
                    except NoSuchElementException:
                        continue
                
                # Extract rating
                rating_selectors = [
                    ".//span[contains(@aria-label, 'stars')]",
                    ".//span[contains(@aria-label, 'star')]",
                    ".//div[contains(@class, 'kvMYJc')]//span",
                    ".//div[contains(@class, 'rating')]//span",
                    ".//span[contains(@class, 'rating')]",
                    ".//div[contains(@class, 'stars')]//span",
                    ".//span[contains(@class, 'star')]",
                    ".//div[contains(@class, 'star')]"
                ]
                
                rating = "-"
                for selector in rating_selectors:
                    try:
                        rating_elem = card.find_element(By.XPATH, selector)
                        aria_label = rating_elem.get_attribute("aria-label")
                        if aria_label:
                            rating = aria_label.split()[0]
                            break
                    except NoSuchElementException:
                        continue
                
                # Extract review text
                text_selectors = [
                    ".//span[contains(@class, 'wiI7pd')]",
                    ".//div[contains(@class, 'wiI7pd')]",
                    ".//div[contains(@class, 'review-snippet')]",
                    ".//span[contains(@class, 'review-text')]",
                    ".//div[contains(@class, 'review-text')]",
                    ".//span[contains(@class, 'snippet')]",
                    ".//div[contains(@class, 'snippet')]",
                    ".//div[contains(@class, 'comment')]",
                    ".//span[contains(@class, 'comment')]",
                    ".//div[contains(@class, 'text')]",
                    ".//span[contains(@class, 'text')]"
                ]
                
                text = ""
                for selector in text_selectors:
                    try:
                        text_elem = card.find_element(By.XPATH, selector)
                        text = text_elem.text.strip()
                        if text:
                            break
                    except NoSuchElementException:
                        continue
                
                if name != "Unknown" or rating != "-" or text:
                    reviews.append((name, rating, text))
                    
            except Exception as e:
                print(f"Error extracting individual review: {e}")
                continue
        
        return reviews
        
    except Exception as e:
        print(f"Error extracting reviews: {e}")
        return reviews

def send_to_domo(property_name, reviews):
    """Send reviews to Domo webhook"""
    success_count = 0
    error_count = 0
    
    for name, rating, text in reviews:
        payload = {
            "Property": property_name,
            "Reviewer": name,
            "Rating": rating,
            "Comment": text
        }
        try:
            response = requests.post(
                domo_webhook, 
                headers={"Content-Type": "application/json"}, 
                data=json.dumps(payload),
                timeout=30
            )
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"HTTP {response.status_code} when sending review for {property_name}")
                error_count += 1
        except requests.exceptions.Timeout:
            print(f"Timeout when sending review for {property_name}")
            error_count += 1
        except Exception as e:
            print(f"Error sending review for {property_name}: {e}")
            error_count += 1
    
    if error_count > 0:
        print(f"⚠ {error_count} reviews failed to send for {property_name}")
    
    return success_count, error_count

def debug_property(driver, property_name, urls):
    """Debug a single property to see what's happening"""
    print(f"\n=== DEBUGGING: {property_name} ===")
    
    for i, url in enumerate(urls, 1):
        print(f"\nTrying URL {i}/{len(urls)}: {url}")
        
        try:
            # Navigate to the URL
            driver.get(url)
            wait_for_page_load(driver)
            
            # Handle consent popup if present
            handle_consent_popup(driver)
            
            # Print page title for debugging
            print(f"Page title: {driver.title}")
            
            # Try to click on reviews tab
            if not click_reviews_tab(driver):
                # If no reviews tab found, try to navigate directly to reviews URL
                if "place" in url:
                    reviews_url = url.replace("!5e0", "!5e0!3m1!1e1")
                    print(f"Trying reviews URL: {reviews_url}")
                    driver.get(reviews_url)
                    wait_for_page_load(driver)
                    handle_consent_popup(driver)
                    print(f"Reviews page title: {driver.title}")
            
            # Scroll to load more reviews
            scroll_reviews_section(driver)
            
            # Extract reviews
            reviews = extract_reviews_data(driver)
            
            if reviews:
                print(f"✅ Found {len(reviews)} reviews!")
                # Show first few reviews
                for j, (name, rating, text) in enumerate(reviews[:3], 1):
                    print(f"  {j}. {name} - {rating} stars: {text[:100]}...")
                
                # Ask user if they want to send to Domo
                response = input(f"\nSend {len(reviews)} reviews to Domo for {property_name}? (y/n): ")
                if response.lower() == 'y':
                    success_count, error_count = send_to_domo(property_name, reviews)
                    print(f"✓ {success_count} reviews successfully sent for {property_name}")
                    if error_count > 0:
                        print(f"⚠ {error_count} reviews failed to send for {property_name}")
                    return True
                else:
                    print("Skipping this property...")
                    return False
            else:
                print("❌ No reviews found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    return False

def run_debug_scraper():
    """Run the debug scraper"""
    print("Starting Debug Ultra-Aggressive Google Review Scraper...")
    print("This will open Chrome in visible mode for debugging")
    print()
    
    driver = setup_driver()
    
    try:
        for property_name, urls in properties.items():
            print(f"\n{'='*60}")
            print(f"DEBUGGING: {property_name}")
            print(f"{'='*60}")
            
            success = debug_property(driver, property_name, urls)
            
            if success:
                print(f"✅ Successfully processed {property_name}")
            else:
                print(f"❌ Failed to process {property_name}")
            
            # Ask user if they want to continue
            response = input(f"\nContinue to next property? (y/n): ")
            if response.lower() != 'y':
                break
    
    except Exception as e:
        print(f"❌ Error in debug scraper: {e}")
    
    finally:
        # Keep browser open for inspection
        input("\nPress Enter to close the browser...")
        driver.quit()
    
    print("\nDebug session complete!")

if __name__ == "__main__":
    run_debug_scraper() 