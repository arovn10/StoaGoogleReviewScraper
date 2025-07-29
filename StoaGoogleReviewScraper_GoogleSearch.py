#!/usr/bin/env python3
"""
Google Search-based Review Scraper for remaining 3 properties
Uses Google Search to find reviews instead of Google Maps directly
"""

import time
import json
import requests
import random
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Focus only on the 3 remaining properties with Google Search approach
properties = {
    "The Waters at McGowin": [
        "https://www.google.com/search?q=The+Waters+at+McGowin+apartments+Mobile+AL+reviews",
        "https://www.google.com/search?q=The+Waters+at+McGowin+Google+reviews",
        "https://www.google.com/search?q=The+Waters+at+McGowin+apartments+reviews+site:google.com",
        "https://www.google.com/search?q=The+Waters+at+McGowin+Mobile+AL+apartment+reviews",
        "https://www.google.com/search?q=The+Waters+at+McGowin+apartments+Mobile+Alabama+reviews"
    ],
    "The Waters at Freeport": [
        "https://www.google.com/search?q=The+Waters+at+Freeport+apartments+Freeport+FL+reviews",
        "https://www.google.com/search?q=The+Waters+at+Freeport+Google+reviews",
        "https://www.google.com/search?q=The+Waters+at+Freeport+apartments+reviews+site:google.com",
        "https://www.google.com/search?q=The+Waters+at+Freeport+Florida+apartment+reviews",
        "https://www.google.com/search?q=The+Waters+at+Freeport+apartments+Freeport+Florida+reviews"
    ],
    "The Waters at Crestview": [
        "https://www.google.com/search?q=The+Waters+at+Crestview+apartments+Crestview+FL+reviews",
        "https://www.google.com/search?q=The+Waters+at+Crestview+Google+reviews",
        "https://www.google.com/search?q=The+Waters+at+Crestview+apartments+reviews+site:google.com",
        "https://www.google.com/search?q=The+Waters+at+Crestview+Florida+apartment+reviews",
        "https://www.google.com/search?q=The+Waters+at+Crestview+apartments+Crestview+Florida+reviews"
    ]
}

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCVRytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

def setup_driver():
    """Setup Chrome driver for Google Search"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--lang=en-US")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
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
    """Handle Google consent popup"""
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

def find_google_maps_link(driver, property_name):
    """Find Google Maps link in search results"""
    try:
        # Look for Google Maps links in search results
        maps_link_selectors = [
            "//a[contains(@href, 'maps.google.com')]",
            "//a[contains(@href, 'google.com/maps')]",
            "//a[contains(text(), 'Maps')]",
            "//a[contains(text(), 'maps')]",
            "//a[contains(@aria-label, 'Maps')]",
            "//a[contains(@aria-label, 'maps')]"
        ]
        
        for selector in maps_link_selectors:
            try:
                links = driver.find_elements(By.XPATH, selector)
                for link in links:
                    href = link.get_attribute('href')
                    if href and ('maps.google.com' in href or 'google.com/maps' in href):
                        print(f"Found Google Maps link: {href}")
                        link.click()
                        time.sleep(5)
                        return True
            except Exception:
                continue
        
        return False
    except Exception as e:
        print(f"Error finding Google Maps link: {e}")
        return False

def click_reviews_tab_from_search(driver):
    """Click reviews tab after navigating from search"""
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
            "//div[contains(@class, 'fontTitleSmall') and contains(text(), 'Reviews')]",
            "//div[contains(@class, 'fontBodyLarge') and contains(text(), 'Reviews')]"
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

def scroll_reviews_section_from_search(driver):
    """Scroll reviews section after navigating from search"""
    try:
        # Try to find scrollable container
        scroll_selectors = [
            "//div[contains(@class, 'review-dialog-list')]",
            "//div[contains(@class, 'reviews')]",
            "//div[contains(@class, 'review-list')]",
            "//div[contains(@class, 'scrollable')]",
            "//div[contains(@class, 'overflow')]",
            "//div[@role='main']",
            "//div[contains(@class, 'content')]",
            "//div[contains(@class, 'review-dialog')]"
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

def extract_reviews_from_search(driver):
    """Extract review data from search results"""
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

def scrape_property_from_search(driver, property_name, urls):
    """Try to scrape reviews from a property using Google Search"""
    for i, url in enumerate(urls):
        print(f"  Trying Google Search approach {i+1}/{len(urls)}: {url}")
        
        try:
            # Navigate to the Google Search URL
            driver.get(url)
            wait_for_page_load(driver)
            
            # Handle consent popup if present
            handle_consent_popup(driver)
            
            # Try to find and click Google Maps link
            if find_google_maps_link(driver, property_name):
                # Handle consent popup again after navigating to Maps
                handle_consent_popup(driver)
                
                # Try to click on reviews tab
                if not click_reviews_tab_from_search(driver):
                    print(f"    Could not find reviews tab, trying alternative approach...")
                    # Try to navigate directly to reviews URL
                    current_url = driver.current_url
                    if "place" in current_url:
                        reviews_url = current_url.replace("!5e0", "!5e0!3m1!1e1")
                        driver.get(reviews_url)
                        wait_for_page_load(driver)
                        handle_consent_popup(driver)
                
                # Scroll to load more reviews
                scroll_reviews_section_from_search(driver)
                
                # Extract reviews
                reviews = extract_reviews_from_search(driver)
                
                if reviews:
                    print(f"    Found {len(reviews)} reviews with Google Search approach {i+1}")
                    return reviews
                else:
                    print(f"    No reviews found with Google Search approach {i+1}")
            else:
                print(f"    Could not find Google Maps link in search results")
                
        except Exception as e:
            print(f"    Error with Google Search approach {i+1}: {e}")
            continue
    
    return []

def run_google_search_scraper():
    print("Starting Google Search-based Review Scraper for remaining 3 properties...")
    driver = setup_driver()
    
    total_reviews = 0
    successful_properties = 0
    
    for name, urls in properties.items():
        print(f"\nProcessing: {name}")
        try:
            reviews = scrape_property_from_search(driver, name, urls)
            
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
    print(f"\n=== GOOGLE SEARCH SCRAPING COMPLETE ===")
    print(f"Successfully scraped {successful_properties}/{len(properties)} properties")
    print(f"Total reviews sent: {total_reviews}")
    print("Done!")

if __name__ == "__main__":
    run_google_search_scraper() 