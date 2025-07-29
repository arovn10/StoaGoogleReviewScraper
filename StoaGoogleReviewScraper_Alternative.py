#!/usr/bin/env python3
"""
Alternative Google Review Scraper for remaining 3 properties
Uses different search strategies and URL formats
"""

import time
import json
import requests
import random
import re

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Focus only on the 3 remaining properties with alternative approaches
properties = {
    "The Waters at McGowin": [
        # Alternative search approaches
        "https://www.google.com/maps/search/The+Waters+at+McGowin+apartments+Mobile+AL",
        "https://www.google.com/maps/search/The+Waters+at+McGowin+reviews+Mobile+Alabama",
        "https://www.google.com/maps/place/The+Waters+at+McGowin/@30.6516886,-88.1154892,979m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a4db406a47bd1:0xa0adc97698cb8809!8m2!3d30.6516886!4d-88.1129143!5e0!3m1!1s0x889a4db406a47bd1:0xa0adc97698cb8809!2m1!1e1",
        # Direct business search
        "https://www.google.com/maps/search/The+Waters+at+McGowin+apartment+complex",
        # Location-based search
        "https://www.google.com/maps/search/apartments+near+McGowin+Street+Mobile+AL",
        # Generic search
        "https://www.google.com/maps/search/The+Waters+McGowin"
    ],
    "The Waters at Freeport": [
        # Alternative search approaches
        "https://www.google.com/maps/search/The+Waters+at+Freeport+apartments+Freeport+FL",
        "https://www.google.com/maps/search/The+Waters+at+Freeport+reviews+Florida",
        "https://www.google.com/maps/place/The+Waters+at+Freeport/@30.486358,-86.1287459,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8893dda15e2f9069:0x3177e609fc299d13!8m2!3d30.486358!4d-86.126171!5e0!3m1!1s0x8893dda15e2f9069:0x3177e609fc299d13!2m1!1e1",
        # Direct business search
        "https://www.google.com/maps/search/The+Waters+at+Freeport+apartment+complex",
        # Location-based search
        "https://www.google.com/maps/search/apartments+near+Freeport+Florida",
        # Generic search
        "https://www.google.com/maps/search/The+Waters+Freeport"
    ],
    "The Waters at Crestview": [
        # Alternative search approaches
        "https://www.google.com/maps/search/The+Waters+at+Crestview+apartments+Crestview+FL",
        "https://www.google.com/maps/search/The+Waters+at+Crestview+reviews+Florida",
        "https://www.google.com/maps/place/The+Waters+at+Crestview/@30.7327129,-86.5707133,1957m/data=!3m1!1e3!5e0!3m1!1s0x889a4db406a47bd1:0xa0adc97698cb8809!2m1!1e1",
        # Direct business search
        "https://www.google.com/maps/search/The+Waters+at+Crestview+apartment+complex",
        # Location-based search
        "https://www.google.com/maps/search/apartments+near+Crestview+Florida",
        # Generic search
        "https://www.google.com/maps/search/The+Waters+Crestview"
    ]
}

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCVRytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

def setup_driver():
    """Setup undetected Chrome driver with alternative options"""
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--lang=en-US")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")  # Disable images for faster loading
    options.add_argument("--disable-javascript")  # Disable JavaScript to avoid dynamic content issues
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Additional anti-detection measures - use add_experimental_option for undetected-chromedriver
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {
        "intl.accept_languages": "en,en_US",
        "profile.default_content_setting_values.notifications": 2
    })
    
    try:
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"Error creating undetected Chrome driver: {e}")
        # Fallback to regular Chrome driver
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--lang=en-US")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {
            "intl.accept_languages": "en,en_US",
            "profile.default_content_setting_values.notifications": 2
        })
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
            # Try to find and click "Reject all" button
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
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        time.sleep(3)
        return True
    except TimeoutException:
        return False

def find_property_in_search_results(driver, property_name):
    """Find the specific property in search results"""
    try:
        # Look for the property name in search results
        property_selectors = [
            f"//div[contains(text(), '{property_name}')]",
            f"//a[contains(text(), '{property_name}')]",
            f"//span[contains(text(), '{property_name}')]",
            f"//h3[contains(text(), '{property_name}')]",
            f"//div[contains(@class, 'fontHeadlineSmall') and contains(text(), '{property_name}')]",
            f"//div[contains(@class, 'fontTitleLarge') and contains(text(), '{property_name}')]"
        ]
        
        for selector in property_selectors:
            try:
                elements = driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if property_name.lower() in element.text.lower():
                        print(f"Found property in search results: {element.text}")
                        element.click()
                        time.sleep(3)
                        return True
            except Exception:
                continue
        
        return False
    except Exception as e:
        print(f"Error finding property in search results: {e}")
        return False

def click_reviews_tab_alternative(driver):
    """Alternative method to click reviews tab"""
    try:
        # Multiple selectors for reviews tab
        review_tab_selectors = [
            "//button[contains(., 'Reviews')]",
            "//a[contains(., 'Reviews')]",
            "//div[contains(., 'Reviews') and contains(@class, 'tab')]",
            "//span[contains(., 'Reviews')]",
            "//div[contains(@class, 'review') and contains(@class, 'tab')]",
            "//button[contains(@aria-label, 'Reviews')]",
            "//a[contains(@aria-label, 'Reviews')]",
            "//div[contains(@class, 'fontBodyMedium') and contains(text(), 'Reviews')]",
            "//div[contains(@class, 'fontTitleSmall') and contains(text(), 'Reviews')]"
        ]
        
        for selector in review_tab_selectors:
            try:
                review_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                review_tab.click()
                time.sleep(3)
                print(f"Clicked reviews tab with selector: {selector}")
                return True
            except TimeoutException:
                continue
        
        return False
    except Exception as e:
        print(f"Error clicking reviews tab: {e}")
        return False

def scroll_reviews_section_alternative(driver):
    """Alternative method to scroll reviews section"""
    try:
        # Try to find scrollable container
        scroll_selectors = [
            "//div[contains(@class, 'review-dialog-list')]",
            "//div[contains(@class, 'reviews')]",
            "//div[contains(@class, 'review-list')]",
            "//div[contains(@class, 'scrollable')]",
            "//div[contains(@class, 'overflow')]",
            "//div[@role='main']",
            "//div[contains(@class, 'content')]"
        ]
        
        scroll_container = None
        for selector in scroll_selectors:
            try:
                containers = driver.find_elements(By.XPATH, selector)
                for container in containers:
                    if container.is_displayed():
                        scroll_container = container
                        break
                if scroll_container:
                    break
            except Exception:
                continue
        
        if not scroll_container:
            # Fallback: scroll the entire page
            scroll_container = driver
        
        # Scroll multiple times to load more reviews
        for i in range(5):
            try:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
                time.sleep(2)
                print(f"Scrolled {i+1}/5 times")
            except Exception as e:
                print(f"Error scrolling: {e}")
                break
        
        return True
    except Exception as e:
        print(f"Error scrolling reviews: {e}")
        return False

def extract_reviews_data_alternative(driver):
    """Alternative method to extract review data"""
    reviews = []
    try:
        # Wait for reviews to load
        time.sleep(5)
        
        # Multiple possible selectors for review cards
        review_card_selectors = [
            "//div[@data-review-id]",
            "//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'g88MCb')]",
            "//div[contains(@class, 'review-dialog-list')]//div[contains(@class, 'g88MCb')]",
            "//div[contains(@class, 'review-dialog-list')]//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'review-dialog')]//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'reviews')]//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'review')]//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'review-card')]",
            "//div[contains(@class, 'review-item')]",
            "//div[contains(@class, 'fontBodyMedium')]",
            "//div[contains(@class, 'fontTitleSmall')]",
            "//div[contains(@class, 'content')]//div[contains(@class, 'fontBodyMedium')]"
        ]
        
        review_cards = []
        for selector in review_card_selectors:
            try:
                cards = driver.find_elements(By.XPATH, selector)
                if cards and len(cards) > 0:
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
                # Extract reviewer name with multiple selectors
                name_selectors = [
                    ".//div[contains(@class, 'd4r55')]",
                    ".//div[contains(@class, 'fontTitleSmall')]",
                    ".//div[contains(@class, 'fontBodyMedium')]",
                    ".//span[contains(@class, 'fontTitleSmall')]",
                    ".//span[contains(@class, 'fontBodyMedium')]",
                    ".//div[contains(@class, 'reviewer')]",
                    ".//div[contains(@class, 'author')]"
                ]
                
                name = "Unknown"
                for selector in name_selectors:
                    try:
                        name_elem = card.find_element(By.XPATH, selector)
                        if name_elem.text.strip():
                            name = name_elem.text.strip()
                            break
                    except Exception:
                        continue
                
                # Extract rating with multiple selectors
                rating_selectors = [
                    ".//span[contains(@class, 'kvMYJc')]",
                    ".//span[contains(@class, 'fontDisplayLarge')]",
                    ".//div[contains(@class, 'fontDisplayLarge')]",
                    ".//span[contains(@class, 'rating')]",
                    ".//div[contains(@class, 'rating')]",
                    ".//span[contains(@aria-label, 'stars')]"
                ]
                
                rating = "0"
                for selector in rating_selectors:
                    try:
                        rating_elem = card.find_element(By.XPATH, selector)
                        rating_text = rating_elem.get_attribute('aria-label') or rating_elem.text
                        if rating_text:
                            # Extract number from text like "4 stars" or "4.0"
                            rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                            if rating_match:
                                rating = rating_match.group(1)
                                break
                    except Exception:
                        continue
                
                # Extract review text with multiple selectors
                text_selectors = [
                    ".//span[contains(@class, 'wiI7pd')]",
                    ".//div[contains(@class, 'wiI7pd')]",
                    ".//span[contains(@class, 'fontBodyMedium')]",
                    ".//div[contains(@class, 'fontBodyMedium')]",
                    ".//span[contains(@class, 'review-text')]",
                    ".//div[contains(@class, 'review-text')]",
                    ".//span[contains(@class, 'content')]",
                    ".//div[contains(@class, 'content')]"
                ]
                
                text = "No review text available"
                for selector in text_selectors:
                    try:
                        text_elem = card.find_element(By.XPATH, selector)
                        if text_elem.text.strip():
                            text = text_elem.text.strip()
                            break
                    except Exception:
                        continue
                
                # Only add if we have meaningful data
                if name != "Unknown" or text != "No review text available":
                    reviews.append((name, rating, text))
                    print(f"  Extracted: {name} - {rating} stars")
                
            except Exception as e:
                print(f"Error extracting review from card: {e}")
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

def scrape_property_alternative(driver, property_name, urls):
    """Try to scrape reviews from a property using alternative approaches"""
    for i, url in enumerate(urls):
        print(f"  Trying alternative approach {i+1}/{len(urls)}: {url}")
        
        try:
            # Navigate to the search URL
            driver.get(url)
            wait_for_page_load(driver)
            
            # Handle consent popup if present
            handle_consent_popup(driver)
            
            # If this is a search URL, try to find the specific property
            if "search" in url:
                if not find_property_in_search_results(driver, property_name):
                    print(f"    Could not find {property_name} in search results")
                    continue
            
            # Try to click on reviews tab
            if not click_reviews_tab_alternative(driver):
                print(f"    Could not find reviews tab, trying alternative approach...")
                # Try to navigate directly to reviews URL
                if "place" in url:
                    reviews_url = url.replace("!5e0", "!5e0!3m1!1e1")
                    driver.get(reviews_url)
                    wait_for_page_load(driver)
                    handle_consent_popup(driver)
            
            # Scroll to load more reviews
            scroll_reviews_section_alternative(driver)
            
            # Extract reviews
            reviews = extract_reviews_data_alternative(driver)
            
            if reviews:
                print(f"    Found {len(reviews)} reviews with alternative approach {i+1}")
                return reviews
            else:
                print(f"    No reviews found with alternative approach {i+1}")
                
        except Exception as e:
            print(f"    Error with alternative approach {i+1}: {e}")
            continue
    
    return []

def run_alternative_scraper():
    print("Starting Alternative Google Review Scraper for remaining 3 properties...")
    driver = setup_driver()
    
    total_reviews = 0
    successful_properties = 0
    
    for name, urls in properties.items():
        print(f"\nProcessing: {name}")
        try:
            reviews = scrape_property_alternative(driver, name, urls)
            
            if reviews:
                success_count, error_count = send_to_domo(name, reviews)
                print(f"✓ {success_count} reviews successfully sent for {name}")
                if error_count > 0:
                    print(f"⚠ {error_count} reviews failed to send for {name}")
                total_reviews += success_count
                successful_properties += 1
            else:
                print(f"⚠ No reviews found for {name}")
                
        except Exception as e:
            print(f"❌ Error scraping {name}: {e}")
        
        # Random delay between properties
        time.sleep(random.uniform(5, 8))
    
    driver.quit()
    print(f"\n=== ALTERNATIVE SCRAPING COMPLETE ===")
    print(f"Successfully scraped {successful_properties}/{len(properties)} properties")
    print(f"Total reviews sent: {total_reviews}")
    print("Done!")

if __name__ == "__main__":
    run_alternative_scraper() 