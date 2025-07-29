#!/usr/bin/env python3
"""
Final Scraper for Remaining 3 Properties
Focuses on The Waters at McGowin, Freeport, and Crestview
"""

import time
import json
import requests
import random
import re
from urllib.parse import quote_plus

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Focus on the 3 remaining properties that need reviews
properties = {
    "The Waters at McGowin": [
        "https://www.google.com/maps/place/The+Waters+at+McGowin/@30.6516886,-88.1154892,979m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a4db406a47bd1:0xa0adc97698cb8809!8m2!3d30.6516886!4d-88.1129143!5e0!3m1!1s0x889a4db406a47bd1:0xa0adc97698cb8809!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+McGowin+reviews",
        "https://www.google.com/maps/search/The+Waters+at+McGowin+apartments+reviews",
        "https://www.google.com/maps/search/The+Waters+at+McGowin+Mobile+reviews",
        "https://www.google.com/maps/search/The+Waters+at+McGowin+apartments+Mobile+AL+reviews",
        "https://www.google.com/maps/search/The+Waters+at+McGowin+apartments+Alabama+reviews"
    ],
    "The Waters at Freeport": [
        "https://www.google.com/maps/place/The+Waters+at+Freeport/@30.486358,-86.1287459,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8893dda15e2f9069:0x3177e609fc299d13!8m2!3d30.486358!4d-86.126171!5e0!3m1!1s0x8893dda15e2f9069:0x3177e609fc299d13!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Freeport+reviews",
        "https://www.google.com/maps/search/The+Waters+at+Freeport+apartments+reviews",
        "https://www.google.com/maps/search/The+Waters+at+Freeport+Florida+reviews",
        "https://www.google.com/maps/search/The+Waters+at+Freeport+apartments+Freeport+FL+reviews",
        "https://www.google.com/maps/search/The+Waters+at+Freeport+apartments+Florida+reviews"
    ],
    "The Waters at Crestview": [
        "https://www.google.com/maps/place/The+Waters+at+Crestview/@30.7327129,-86.5707133,1957m/data=!3m1!1e3!5e0!3m1!1s0x889a4db406a47bd1:0xa0adc97698cb8809!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Crestview+reviews",
        "https://www.google.com/maps/search/The+Waters+at+Crestview+apartments+reviews",
        "https://www.google.com/maps/search/The+Waters+at+Crestview+Florida+reviews",
        "https://www.google.com/maps/search/The+Waters+at+Crestview+apartments+Crestview+FL+reviews",
        "https://www.google.com/maps/search/The+Waters+at+Crestview+apartments+Florida+reviews"
    ]
}

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

def setup_driver():
    """Setup undetected Chrome driver to avoid detection"""
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=VizDisplayCompositor")
    
    driver = uc.Chrome(options=options)
    return driver

def handle_consent_popup(driver):
    """Handle various consent popups that may appear"""
    try:
        # Try to find and click "Accept all" button
        accept_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all') or contains(., 'I agree') or contains(., 'Accept')]"))
        )
        accept_button.click()
        time.sleep(1)
        return True
    except TimeoutException:
        try:
            # Try to find and click "Reject all" if "Accept all" not found
            reject_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Reject all') or contains(., 'Decline')]"))
            )
            reject_button.click()
            time.sleep(1)
            return True
        except TimeoutException:
            return False

def wait_for_page_load(driver):
    """Wait for page to load"""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)  # Give time for JavaScript to load
    except TimeoutException:
        print("Page load timeout")

def click_reviews_tab(driver):
    """Try to click on reviews tab with multiple strategies"""
    review_tab_selectors = [
        "//button[contains(., 'Reviews')]",
        "//a[contains(., 'Reviews')]",
        "//div[contains(., 'Reviews')]",
        "//span[contains(., 'Reviews')]",
        "//button[contains(@aria-label, 'Reviews')]",
        "//button[contains(@class, 'review')]",
        "//div[contains(@class, 'review')]//button"
    ]
    
    for selector in review_tab_selectors:
        try:
            reviews_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            print(f"Found reviews tab with selector: {selector}")
            reviews_tab.click()
            time.sleep(2)
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
                time.sleep(2)
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
            time.sleep(1)
    else:
        # Fallback: scroll the whole page
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

def extract_reviews_data(driver):
    """Extract review data from the page with enhanced selectors"""
    reviews = []
    try:
        # Wait for reviews to load
        time.sleep(2)
        
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
                timeout=10
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

def scrape_property_final(driver, property_name, urls):
    """Try multiple approaches to scrape reviews for a property"""
    all_reviews = []
    
    for i, url in enumerate(urls, 1):
        print(f"  Trying URL format {i}/{len(urls)}: {url}")
        
        try:
            # Navigate to the URL
            driver.get(url)
            wait_for_page_load(driver)
            
            # Handle consent popup if present
            handle_consent_popup(driver)
            
            # Try to click on reviews tab
            if not click_reviews_tab(driver):
                # If no reviews tab found, try to navigate directly to reviews URL
                if "place" in url:
                    reviews_url = url.replace("!5e0", "!5e0!3m1!1e1")
                    driver.get(reviews_url)
                    wait_for_page_load(driver)
                    handle_consent_popup(driver)
            
            # Scroll to load more reviews
            scroll_reviews_section(driver)
            
            # Extract reviews
            reviews = extract_reviews_data(driver)
            
            if reviews:
                print(f"    Found {len(reviews)} reviews with URL format {i}")
                all_reviews.extend(reviews)
                break  # Found reviews, no need to try other URLs
            else:
                print(f"    No reviews found with URL format {i}")
                
        except Exception as e:
            print(f"    Error with URL format {i}: {e}")
            continue
    
    return all_reviews

def run_final_scraper():
    """Run the final scraper to get the remaining 3 properties"""
    print("Starting Final Scraper for Remaining 3 Properties...")
    print("Focusing on: The Waters at McGowin, Freeport, and Crestview")
    print()
    
    total_reviews = 0
    successful_properties = 0
    
    for property_name, urls in properties.items():
        print(f"Processing: {property_name}")
        
        # Create a new driver for each property to avoid session issues
        driver = None
        try:
            driver = setup_driver()
            reviews = scrape_property_final(driver, property_name, urls)
            
            if reviews:
                # Remove duplicates based on reviewer name and text
                unique_reviews = []
                seen = set()
                for review in reviews:
                    key = (review[0], review[2])  # name and text
                    if key not in seen:
                        seen.add(key)
                        unique_reviews.append(review)
                
                if unique_reviews:
                    success_count, error_count = send_to_domo(property_name, unique_reviews)
                    print(f"✓ {success_count} reviews successfully sent for {property_name}")
                    total_reviews += success_count
                    successful_properties += 1
                    if error_count > 0:
                        print(f"⚠ {error_count} reviews failed to send for {property_name}")
                else:
                    print(f"⚠ No unique reviews found for {property_name}")
            else:
                print(f"⚠ No reviews found for {property_name}")
            
        except Exception as e:
            print(f"❌ Error processing {property_name}: {e}")
        
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
        
        # Delay between properties
        time.sleep(random.uniform(3, 5))
    
    print()
    print("=== FINAL SCRAPING COMPLETE ===")
    print(f"Successfully scraped {successful_properties}/3 remaining properties")
    print(f"Total reviews sent: {total_reviews}")
    
    if successful_properties == 3:
        print("🎉 SUCCESS! All 11 properties have been scraped!")
    else:
        print(f"⚠ {3 - successful_properties} properties still need reviews")
    
    print("Done!")

if __name__ == "__main__":
    run_final_scraper() 