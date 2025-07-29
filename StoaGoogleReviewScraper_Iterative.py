#!/usr/bin/env python3
"""
Iterative Google Review Scraper - Stop on failure, find solution, continue until ALL 11 work
"""

import time
import json
import requests
import random
import re

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Start with basic URL formats - we'll expand as needed
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
    "The Waters at Bluebonnet": [
        "https://www.google.com/maps/place/The+Waters+at+Bluebonnet/@30.4147242,-91.0766963,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626a53bc0c94fbf:0x84b7af1708cc8d8d!8m2!3d30.4147242!4d-91.0741214!5e0!3m1!1s0x8626a53bc0c94fbf:0x84b7af1708cc8d8d!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Bluebonnet+reviews"
    ],
    "The Heights at Picardy": [
        "https://www.google.com/maps/place/The+Heights+at+Picardy/@30.3941704,-91.1028869,982m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626a56f7f0dc5bf:0xb38345b83bdc892b!8m2!3d30.3941704!4d-91.100312!5e0!3m1!1s0x8626a56f7f0dc5bf:0xb38345b83bdc892b!2m1!1e1",
        "https://www.google.com/maps/search/The+Heights+at+Picardy+reviews"
    ],
    "The Flats at East Bay": [
        "https://www.google.com/maps/place/The+Flats+at+East+Bay/@30.5014556,-87.8652493,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!8m2!3d30.5014556!4d-87.8626744!5e0!3m1!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!2m1!1e1",
        "https://www.google.com/maps/search/The+Flats+at+East+Bay+reviews"
    ],
    "The Waters at West Village": [
        "https://www.google.com/maps/place/The+Waters+at+West+Village/@30.2214016,-92.097974,983m/data=!3m2!1e3!4b1!4m6!3m5!1s0x86249fc349920de9:0x7945e14be23642b4!8m2!3d30.2214016!4d-92.0953991!5e0!3m1!1s0x86249fc349920de9:0x7945e14be23642b4!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+West+Village+reviews"
    ],
    "The Waters at Hammond": [
        "https://www.google.com/maps/place/The+Waters+at+Hammond/@30.4877443,-90.465321,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x862723fbcc2afb85:0x188d3eeca51192d0!8m2!3d30.4877443!4d-90.4627461!5e0!3m1!1s0x862723fbcc2afb85:0x188d3eeca51192d0!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Hammond+reviews"
    ]
}

# Properties with no reviews online (excluded from scraping)
no_review_properties = ["The Waters at McGowin", "The Waters at Freeport"]

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

def setup_driver():
    """Setup undetected Chrome driver"""
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Don't add excludeSwitches or useAutomationExtension - undetected-chromedriver handles this
        options.add_experimental_option("prefs", {
            "intl.accept_languages": "en,en_US",
            "profile.default_content_setting_values.notifications": 2
        })
        
        driver = uc.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Error setting up undetected driver: {e}")
        # Fallback to regular Chrome
        from selenium import webdriver
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        return driver

def handle_consent_popup(driver):
    """Handle Google consent popup"""
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all') or contains(., 'I agree') or contains(., 'Accept')]"))
        )
        accept_button.click()
        time.sleep(2)
        return True
    except TimeoutException:
        try:
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
        maps_link_selectors = [
            "//a[contains(@href, 'maps.google.com')]",
            "//a[contains(@href, 'google.com/maps')]",
            "//a[contains(text(), 'Maps')]",
            "//a[contains(@aria-label, 'Maps')]"
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

def click_reviews_tab(driver):
    """Click reviews tab"""
    try:
        review_tab_selectors = [
            "//button[contains(., 'Reviews')]",
            "//a[contains(., 'Reviews')]",
            "//span[contains(., 'Reviews')]",
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

def scroll_reviews_section(driver):
    """Scroll reviews section to load ALL reviews"""
    try:
        scroll_selectors = [
            "//div[contains(@class, 'review-dialog-list')]",
            "//div[contains(@class, 'reviews')]",
            "//div[contains(@class, 'review-list')]",
            "//div[@role='main']"
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
            scroll_container = driver
        
        # First, try to click "Show more" buttons if they exist
        show_more_selectors = [
            "//button[contains(., 'Show more')]",
            "//span[contains(., 'Show more')]",
            "//div[contains(., 'Show more')]",
            "//button[contains(., 'More reviews')]",
            "//span[contains(., 'More reviews')]"
        ]
        
        for selector in show_more_selectors:
            try:
                show_more_buttons = driver.find_elements(By.XPATH, selector)
                for button in show_more_buttons:
                    if button.is_displayed() and button.is_enabled():
                        print(f"Clicking 'Show more' button")
                        button.click()
                        time.sleep(3)
            except Exception:
                continue
        
        # Scroll more aggressively to load ALL reviews
        previous_review_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 50  # Increased significantly to load all reviews
        no_change_count = 0
        
        while scroll_attempts < max_scroll_attempts:
            try:
                # Get current review count
                current_review_cards = driver.find_elements(By.XPATH, "//div[@data-review-id]")
                current_review_count = len(current_review_cards)
                
                # Try multiple scrolling methods
                # Method 1: Scroll container to bottom
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
                time.sleep(2)
                
                # Method 2: Scroll page down
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Method 3: Scroll to last review card
                if current_review_cards:
                    last_card = current_review_cards[-1]
                    driver.execute_script("arguments[0].scrollIntoView(true);", last_card)
                    time.sleep(2)
                
                # Get new review count after scroll
                new_review_cards = driver.find_elements(By.XPATH, "//div[@data-review-id]")
                new_review_count = len(new_review_cards)
                
                print(f"Scroll {scroll_attempts + 1}/{max_scroll_attempts} - Reviews: {current_review_count} -> {new_review_count}")
                
                # If no new reviews loaded, try a few more times then stop
                if new_review_count == current_review_count:
                    no_change_count += 1
                    if no_change_count >= 5:  # Try 5 more times after no change
                        print(f"Reached end of reviews after {scroll_attempts + 1} scrolls")
                        break
                else:
                    no_change_count = 0  # Reset counter if we found new reviews
                
                scroll_attempts += 1
                
            except Exception as e:
                print(f"Error scrolling: {e}")
                break
        
        print(f"Completed {scroll_attempts} scroll attempts, loaded {new_review_count} total reviews")
        return True
    except Exception as e:
        print(f"Error scrolling reviews: {e}")
        return False

def expand_all_reviews(driver):
    """Expand all 'More' buttons to get full review text"""
    try:
        # Find all "More" buttons
        more_selectors = [
            "//button[contains(., 'More')]",
            "//span[contains(., 'More')]",
            "//div[contains(., 'More')]",
            "//button[contains(., 'Show more')]",
            "//span[contains(., 'Show more')]"
        ]
        
        expanded_count = 0
        for selector in more_selectors:
            try:
                more_buttons = driver.find_elements(By.XPATH, selector)
                for button in more_buttons:
                    if button.is_displayed() and button.is_enabled():
                        try:
                            driver.execute_script("arguments[0].click();", button)
                            time.sleep(0.5)
                            expanded_count += 1
                        except Exception:
                            continue
            except Exception:
                continue
        
        if expanded_count > 0:
            print(f"  Expanded {expanded_count} reviews to show full text")
        
        return True
    except Exception as e:
        print(f"Error expanding reviews: {e}")
        return False

def extract_reviews_data(driver):
    """Extract ALL review data including dates, removing duplicates"""
    reviews = []
    seen_reviews = set()
    try:
        time.sleep(5)
        
        # First, expand all "More" buttons to get full review text
        expand_all_reviews(driver)
        
        review_card_selectors = [
            "//div[@data-review-id]",
            "//div[contains(@class, 'jftiEf')]",
            "//div[contains(@class, 'g88MCb')]",
            "//div[contains(@class, 'review-dialog-list')]//div[contains(@class, 'g88MCb')]",
            "//div[contains(@class, 'review-dialog-list')]//div[contains(@class, 'jftiEf')]"
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
        
        print(f"Processing ALL {len(review_cards)} review cards")
        
        # Process ALL cards, not just first 20
        for i, card in enumerate(review_cards):
            try:
                name_selectors = [
                    ".//div[contains(@class, 'd4r55')]",
                    ".//div[contains(@class, 'fontTitleSmall')]",
                    ".//div[contains(@class, 'fontBodyMedium')]",
                    ".//span[contains(@class, 'fontTitleSmall')]",
                    ".//span[contains(@class, 'fontBodyMedium')]"
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
                
                rating_selectors = [
                    ".//span[contains(@class, 'kvMYJc')]",
                    ".//span[contains(@class, 'fontDisplayLarge')]",
                    ".//div[contains(@class, 'fontDisplayLarge')]",
                    ".//span[contains(@aria-label, 'stars')]"
                ]
                
                rating = "0"
                for selector in rating_selectors:
                    try:
                        rating_elem = card.find_element(By.XPATH, selector)
                        rating_text = rating_elem.get_attribute('aria-label') or rating_elem.text
                        if rating_text:
                            rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                            if rating_match:
                                rating = rating_match.group(1)
                                break
                    except Exception:
                        continue
                
                text_selectors = [
                    ".//span[contains(@class, 'wiI7pd')]",
                    ".//div[contains(@class, 'wiI7pd')]",
                    ".//span[contains(@class, 'fontBodyMedium')]",
                    ".//div[contains(@class, 'fontBodyMedium')]",
                    ".//span[contains(@class, 'review-text')]",
                    ".//div[contains(@class, 'review-text')]",
                    ".//span[contains(@class, 'review-snippet')]",
                    ".//div[contains(@class, 'review-snippet')]",
                    ".//div[contains(@class, 'review-content')]",
                    ".//span[contains(@class, 'review-content')]",
                    ".//div[contains(@class, 'jftiEf')]//span[contains(@class, 'wiI7pd')]",
                    ".//div[contains(@class, 'jftiEf')]//div[contains(@class, 'wiI7pd')]",
                    ".//div[@data-review-id]//span[contains(@class, 'wiI7pd')]",
                    ".//div[@data-review-id]//div[contains(@class, 'wiI7pd')]"
                ]
                
                text = "No review text available"
                for selector in text_selectors:
                    try:
                        text_elem = card.find_element(By.XPATH, selector)
                        if text_elem.text.strip():
                            extracted_text = text_elem.text.strip()
                            # Check if this looks like actual review text (not just a few words)
                            if len(extracted_text) > 10 and not extracted_text.isdigit():
                                text = extracted_text
                                break
                    except Exception:
                        continue
                
                # If we still don't have text, try to get it from the full review content
                if text == "No review text available":
                    try:
                        # Try to expand the review if there's a "More" button
                        more_buttons = card.find_elements(By.XPATH, ".//button[contains(., 'More')]")
                        for more_btn in more_buttons:
                            if more_btn.is_displayed():
                                more_btn.click()
                                time.sleep(1)
                                break
                        
                        # Try again with expanded content
                        for selector in text_selectors:
                            try:
                                text_elem = card.find_element(By.XPATH, selector)
                                if text_elem.text.strip():
                                    extracted_text = text_elem.text.strip()
                                    if len(extracted_text) > 10 and not extracted_text.isdigit():
                                        text = extracted_text
                                        break
                            except Exception:
                                continue
                    except Exception:
                        pass
                
                # Extract review date
                date_selectors = [
                    ".//span[contains(@class, 'rsqaWe')]",
                    ".//span[contains(@class, 'fontBodySmall')]",
                    ".//div[contains(@class, 'fontBodySmall')]",
                    ".//span[contains(@class, 'review-date')]",
                    ".//div[contains(@class, 'review-date')]",
                    ".//span[contains(text(), 'ago')]",
                    ".//span[contains(text(), 'day')]",
                    ".//span[contains(text(), 'month')]",
                    ".//span[contains(text(), 'year')]"
                ]
                
                date = "Unknown date"
                for selector in date_selectors:
                    try:
                        date_elem = card.find_element(By.XPATH, selector)
                        if date_elem.text.strip():
                            date_text = date_elem.text.strip()
                            # Check if it looks like a date
                            if any(word in date_text.lower() for word in ['ago', 'day', 'month', 'year', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):
                                date = date_text
                                break
                    except Exception:
                        continue
                
                if (name != "Unknown" and 
                    text != "No review text available" and 
                    rating != "0" and
                    not re.match(r'^\d+\.\d+\(\d+\)$', name) and
                    not re.match(r'^\d+\s+days?\s+ago$', name) and
                    not re.match(r'^[A-Z][a-z]+\s+\d+,\s+\d{4}$', name)):
                    
                    # Create unique key for deduplication
                    review_key = f"{name}|{rating}|{text[:100]}"
                    
                    if review_key not in seen_reviews:
                        seen_reviews.add(review_key)
                        reviews.append((name, rating, text, date))
                        if i < 10 or i % 10 == 0:  # Show first 10 and every 10th after
                            print(f"  Extracted review {len(reviews)}: {name} - {rating} stars - {date}")
                    else:
                        print(f"  Skipping duplicate review {i+1}: {name} - {rating} stars")
                
            except Exception as e:
                print(f"Error extracting review from card {i+1}: {e}")
                continue
        
        print(f"✅ Successfully extracted {len(reviews)} unique reviews out of {len(review_cards)} cards")
        return reviews
    except Exception as e:
        print(f"Error extracting reviews: {e}")
        return reviews

def send_to_domo(property_name, reviews):
    """Send reviews to Domo webhook with dates, removing duplicates"""
    success_count = 0
    error_count = 0
    
    # Remove duplicates based on reviewer name, rating, and comment
    unique_reviews = []
    seen_reviews = set()
    
    for review_data in reviews:
        if len(review_data) == 4:
            name, rating, text, date = review_data
        else:
            name, rating, text = review_data
            date = "Unknown date"
        
        # Create a unique key for deduplication
        review_key = f"{name}|{rating}|{text[:100]}"  # First 100 chars of text to avoid memory issues
        
        if review_key not in seen_reviews:
            seen_reviews.add(review_key)
            unique_reviews.append(review_data)
        else:
            print(f"  Skipping duplicate review: {name} - {rating} stars")
    
    print(f"  Sending {len(unique_reviews)} unique reviews (removed {len(reviews) - len(unique_reviews)} duplicates)")
    
    for review_data in unique_reviews:
        if len(review_data) == 4:
            name, rating, text, date = review_data
        else:
            name, rating, text = review_data
            date = "Unknown date"
            
        payload = {
            "Property": property_name,
            "Reviewer": name,
            "Rating": rating,
            "Comment": text,
            "ReviewDate": date
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

def scrape_property(driver, property_name, urls):
    """Try to scrape reviews from a property"""
    for i, url in enumerate(urls):
        print(f"  Trying approach {i+1}/{len(urls)}: {url}")
        
        try:
            driver.get(url)
            wait_for_page_load(driver)
            handle_consent_popup(driver)
            
            if "search" in url and "google.com/search" in url:
                if not find_google_maps_link(driver, property_name):
                    print(f"    Could not find Google Maps link in search results")
                    continue
                handle_consent_popup(driver)
            
            if not click_reviews_tab(driver):
                print(f"    Could not find reviews tab, trying alternative approach...")
                if "place" in url:
                    reviews_url = url.replace("!5e0", "!5e0!3m1!1e1")
                    driver.get(reviews_url)
                    wait_for_page_load(driver)
                    handle_consent_popup(driver)
            
            scroll_reviews_section(driver)
            reviews = extract_reviews_data(driver)
            
            if reviews:
                print(f"    Found {len(reviews)} reviews with approach {i+1}")
                return reviews
            else:
                print(f"    No reviews found with approach {i+1}")
                
        except Exception as e:
            print(f"    Error with approach {i+1}: {e}")
            continue
    
    return []

def add_google_search_urls(property_name):
    """Add Google Search URLs for a property"""
    search_urls = [
        f"https://www.google.com/search?q={property_name.replace(' ', '+')}+apartments+reviews",
        f"https://www.google.com/search?q={property_name.replace(' ', '+')}+Google+reviews"
    ]
    return search_urls

def run_iterative_scraper():
    print("🔄 STARTING FAST SCRAPER - GIVE UP AFTER 2 CHECKS, LOG NO REVIEWS FOR EMPTY PROPERTIES! 🔄")
    
    successful_properties = []
    no_review_properties = []
    total_reviews = 0
    
    # Create driver once
    driver = setup_driver()
    
    try:
        for property_name, urls in properties.items():
            print(f"\n🎯 Processing: {property_name}")
            
            # Try current URLs (first check)
            reviews = scrape_property(driver, property_name, urls)
            
            if reviews:
                success_count, error_count = send_to_domo(property_name, reviews)
                print(f"✅ {success_count} reviews successfully sent for {property_name}")
                total_reviews += success_count
                successful_properties.append(property_name)
            else:
                print(f"❌ No reviews found with first approach for {property_name}")
                
                # Add Google Search URLs and try one more time (second check)
                search_urls = add_google_search_urls(property_name)
                properties[property_name].extend(search_urls)
                print(f"🔍 Adding Google Search URLs and trying one more time...")
                
                reviews = scrape_property(driver, property_name, properties[property_name])
                
                if reviews:
                    success_count, error_count = send_to_domo(property_name, reviews)
                    print(f"✅ {success_count} reviews successfully sent for {property_name}")
                    total_reviews += success_count
                    successful_properties.append(property_name)
                else:
                    print(f"❌ No reviews found after second attempt for {property_name}")
                    no_review_properties.append(property_name)
                    print(f"📝 Logging: {property_name} has no reviews online")
            
            time.sleep(random.uniform(2, 4))
    
    finally:
        driver.quit()
    
    print(f"\n🎉 === SCRAPING COMPLETE ===")
    print(f"✅ Successfully scraped {len(successful_properties)} properties")
    print(f"📊 Total reviews sent: {total_reviews}")
    print(f"📝 Properties with no reviews: {no_review_properties}")
    
    if len(successful_properties) >= 9:
        print("🏆 MISSION ACCOMPLISHED! ALL PROPERTIES WITH REVIEWS SCRAPED! 🏆")
    else:
        print(f"⚠ {len(no_review_properties)} properties have no reviews online")
    
    print("Done!")

if __name__ == "__main__":
    run_iterative_scraper() 