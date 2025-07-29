#!/usr/bin/env python3
"""
ULTIMATE Google Review Scraper - Get ALL 11 properties FAST!
Combines all successful approaches and applies them to every property
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

# ALL 11 properties with proven working URL formats
properties = {
    "The Waters at Settlers Trace": [
        # PROVEN WORKING FORMATS (from successful properties)
        "https://www.google.com/maps/place/The+Waters+at+Settlers+Trace/@30.7362861,-86.5595057,978m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8891731ed5ef4421:0xe82971b01b043e0e!8m2!3d30.7362861!4d-86.5569308!5e0!3m1!1s0x8891731ed5ef4421:0xe82971b01b043e0e!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Settlers+Trace+reviews",
        # Google Search variations (proven to work)
        "https://www.google.com/search?q=The+Waters+at+Settlers+Trace+apartments+reviews",
        "https://www.google.com/search?q=The+Waters+at+Settlers+Trace+Google+reviews"
    ],
    "The Waters at Redstone": [
        "https://www.google.com/maps/place/The+Waters+at+Redstone/@30.7362861,-86.5595057,978m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8891731ed5ef4421:0xe82971b01b043e0e!8m2!3d30.7362861!4d-86.5569308!5e0!3m1!1s0x8891731ed5ef4421:0xe82971b01b043e0e!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Redstone+reviews",
        "https://www.google.com/search?q=The+Waters+at+Redstone+apartments+reviews",
        "https://www.google.com/search?q=The+Waters+at+Redstone+Google+reviews"
    ],
    "The Waters at Millerville": [
        "https://www.google.com/maps/place/The+Waters+at+Millerville/@30.4397504,-91.0289876,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626bd7f2db7ca89:0x1d15edca3d614c78!8m2!3d30.4397504!4d-91.0264127!5e0!3m1!1s0x8626bd7f2db7ca89:0x1d15edca3d614c78!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Millerville+reviews",
        "https://www.google.com/search?q=The+Waters+at+Millerville+apartments+reviews",
        "https://www.google.com/search?q=The+Waters+at+Millerville+Google+reviews"
    ],
    "The Waters at McGowin": [
        # PROVEN WORKING FORMATS (from Google Search approach)
        "https://www.google.com/search?q=The+Waters+at+McGowin+apartments+Mobile+AL+reviews",
        "https://www.google.com/search?q=The+Waters+at+McGowin+Google+reviews",
        "https://www.google.com/maps/place/The+Waters+at+McGowin/@30.6516886,-88.1154892,979m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a4db406a47bd1:0xa0adc97698cb8809!8m2!3d30.6516886!4d-88.1129143!5e0!3m1!1s0x889a4db406a47bd1:0xa0adc97698cb8809!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+McGowin+reviews"
    ],
    "The Waters at Freeport": [
        # PROVEN WORKING FORMATS (from Google Search approach)
        "https://www.google.com/search?q=The+Waters+at+Freeport+apartments+Freeport+FL+reviews",
        "https://www.google.com/search?q=The+Waters+at+Freeport+Google+reviews",
        "https://www.google.com/maps/place/The+Waters+at+Freeport/@30.486358,-86.1287459,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8893dda15e2f9069:0x3177e609fc299d13!8m2!3d30.486358!4d-86.126171!5e0!3m1!1s0x8893dda15e2f9069:0x3177e609fc299d13!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Freeport+reviews"
    ],
    "The Waters at Crestview": [
        # PROVEN WORKING FORMATS (from Google Search approach)
        "https://www.google.com/search?q=The+Waters+at+Crestview+apartments+Crestview+FL+reviews",
        "https://www.google.com/search?q=The+Waters+at+Crestview+Google+reviews",
        "https://www.google.com/maps/place/The+Waters+at+Crestview/@30.7327129,-86.5707133,1957m/data=!3m1!1e3!5e0!3m1!1s0x889a4db406a47bd1:0xa0adc97698cb8809!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Crestview+reviews"
    ],
    "The Waters at Bluebonnet": [
        # PROVEN WORKING FORMATS (this one worked!)
        "https://www.google.com/maps/place/The+Waters+at+Bluebonnet/@30.4147242,-91.0766963,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626a53bc0c94fbf:0x84b7af1708cc8d8d!8m2!3d30.4147242!4d-91.0741214!5e0!3m1!1s0x8626a53bc0c94fbf:0x84b7af1708cc8d8d!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Bluebonnet+reviews",
        "https://www.google.com/search?q=The+Waters+at+Bluebonnet+apartments+reviews",
        "https://www.google.com/search?q=The+Waters+at+Bluebonnet+Google+reviews"
    ],
    "The Heights at Picardy": [
        # PROVEN WORKING FORMATS (this one worked!)
        "https://www.google.com/maps/place/The+Heights+at+Picardy/@30.3941704,-91.1028869,982m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626a56f7f0dc5bf:0xb38345b83bdc892b!8m2!3d30.3941704!4d-91.100312!5e0!3m1!1s0x8626a56f7f0dc5bf:0xb38345b83bdc892b!2m1!1e1",
        "https://www.google.com/maps/search/The+Heights+at+Picardy+reviews",
        "https://www.google.com/search?q=The+Heights+at+Picardy+apartments+reviews",
        "https://www.google.com/search?q=The+Heights+at+Picardy+Google+reviews"
    ],
    "The Flats at East Bay": [
        "https://www.google.com/maps/place/The+Flats+at+East+Bay/@30.5014556,-87.8652493,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!8m2!3d30.5014556!4d-87.8626744!5e0!3m1!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!2m1!1e1",
        "https://www.google.com/maps/search/The+Flats+at+East+Bay+reviews",
        "https://www.google.com/search?q=The+Flats+at+East+Bay+apartments+reviews",
        "https://www.google.com/search?q=The+Flats+at+East+Bay+Google+reviews"
    ],
    "The Waters at West Village": [
        # PROVEN WORKING FORMATS (this one worked!)
        "https://www.google.com/maps/place/The+Waters+at+West+Village/@30.2214016,-92.097974,983m/data=!3m2!1e3!4b1!4m6!3m5!1s0x86249fc349920de9:0x7945e14be23642b4!8m2!3d30.2214016!4d-92.0953991!5e0!3m1!1s0x86249fc349920de9:0x7945e14be23642b4!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+West+Village+reviews",
        "https://www.google.com/search?q=The+Waters+at+West+Village+apartments+reviews",
        "https://www.google.com/search?q=The+Waters+at+West+Village+Google+reviews"
    ],
    "The Waters at Hammond": [
        "https://www.google.com/maps/place/The+Waters+at+Hammond/@30.4877443,-90.465321,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x862723fbcc2afb85:0x188d3eeca51192d0!8m2!3d30.4877443!4d-90.4627461!5e0!3m1!1s0x862723fbcc2afb85:0x188d3eeca51192d0!2m1!1e1",
        "https://www.google.com/maps/search/The+Waters+at+Hammond+reviews",
        "https://www.google.com/search?q=The+Waters+at+Hammond+apartments+reviews",
        "https://www.google.com/search?q=The+Waters+at+Hammond+Google+reviews"
    ]
}

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCVRytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

def setup_driver():
    """Setup Chrome driver with optimized settings for speed"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--lang=en-US")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {
        "intl.accept_languages": "en,en_US",
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0
    })
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def handle_consent_popup(driver):
    """Handle Google consent popup - FAST version"""
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
            # Try to find and click "Reject all" button
            reject_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Reject all') or contains(., 'Decline')]"))
            )
            reject_button.click()
            time.sleep(1)
            return True
        except TimeoutException:
            return False

def wait_for_page_load(driver):
    """Wait for page to load - FAST version"""
    try:
        WebDriverWait(driver, 8).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)  # Reduced wait
        return True
    except TimeoutException:
        return False

def find_google_maps_link_fast(driver, property_name):
    """Fast approach to find Google Maps link in search results"""
    try:
        # Quick selectors for Google Maps links
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
                        time.sleep(3)  # Reduced wait
                        return True
            except Exception:
                continue
        
        # Try clicking on property name links
        try:
            property_links = driver.find_elements(By.XPATH, f"//a[contains(text(), '{property_name}')]")
            for link in property_links:
                href = link.get_attribute('href')
                if href:
                    print(f"Found property link: {href}")
                    link.click()
                    time.sleep(3)
                    return True
        except Exception:
            pass
        
        return False
    except Exception as e:
        print(f"Error finding Google Maps link: {e}")
        return False

def click_reviews_tab_fast(driver):
    """Fast approach to click reviews tab - using proven selectors"""
    try:
        # PROVEN WORKING SELECTORS (from successful properties)
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
                time.sleep(2)  # Reduced wait
                print(f"Clicked reviews tab with selector: {selector}")
                return True
            except TimeoutException:
                continue
        
        return False
    except Exception as e:
        print(f"Error clicking reviews tab: {e}")
        return False

def scroll_reviews_section_fast(driver):
    """Fast approach to scroll reviews section"""
    try:
        # Quick scroll selectors
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
        
        # Fast scrolling - fewer attempts
        for i in range(5):  # Reduced scroll attempts
            try:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_container)
                time.sleep(1)  # Faster scrolling
                print(f"Scrolled {i+1}/5 times")
            except Exception as e:
                print(f"Error scrolling: {e}")
                break
        
        return True
    except Exception as e:
        print(f"Error scrolling reviews: {e}")
        return False

def extract_reviews_data_fast(driver):
    """Fast approach to extract review data - using proven selectors"""
    reviews = []
    try:
        # Wait for reviews to load - reduced wait
        time.sleep(3)
        
        # PROVEN WORKING SELECTORS (from successful properties)
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
        
        print(f"Processing {len(review_cards)} review cards")
        
        for card in review_cards:
            try:
                # PROVEN WORKING NAME SELECTORS
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
                
                # PROVEN WORKING RATING SELECTORS
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
                
                # PROVEN WORKING TEXT SELECTORS
                text_selectors = [
                    ".//span[contains(@class, 'wiI7pd')]",
                    ".//div[contains(@class, 'wiI7pd')]",
                    ".//span[contains(@class, 'fontBodyMedium')]",
                    ".//div[contains(@class, 'fontBodyMedium')]",
                    ".//span[contains(@class, 'review-text')]",
                    ".//div[contains(@class, 'review-text')]"
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
                
                # Validate the extracted data
                if (name != "Unknown" and 
                    text != "No review text available" and 
                    rating != "0" and
                    not re.match(r'^\d+\.\d+\(\d+\)$', name) and
                    not re.match(r'^\d+\s+days?\s+ago$', name) and
                    not re.match(r'^[A-Z][a-z]+\s+\d+,\s+\d{4}$', name)):
                    
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
    """Send reviews to Domo webhook - FAST version"""
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
                timeout=15  # Reduced timeout
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

def scrape_property_ultimate(driver, property_name, urls):
    """ULTIMATE approach - combines all successful strategies"""
    for i, url in enumerate(urls):
        print(f"  Trying ultimate approach {i+1}/{len(urls)}: {url}")
        
        try:
            # Navigate to the URL
            driver.get(url)
            wait_for_page_load(driver)
            
            # Handle consent popup if present
            handle_consent_popup(driver)
            
            # If this is a Google Search URL, try to find Google Maps link
            if "search" in url and "google.com/search" in url:
                if not find_google_maps_link_fast(driver, property_name):
                    print(f"    Could not find Google Maps link in search results")
                    continue
                # Handle consent popup again after navigating to Maps
                handle_consent_popup(driver)
            
            # Try to click on reviews tab
            if not click_reviews_tab_fast(driver):
                print(f"    Could not find reviews tab, trying alternative approach...")
                # Try to navigate directly to reviews URL
                if "place" in url:
                    reviews_url = url.replace("!5e0", "!5e0!3m1!1e1")
                    driver.get(reviews_url)
                    wait_for_page_load(driver)
                    handle_consent_popup(driver)
            
            # Scroll to load more reviews
            scroll_reviews_section_fast(driver)
            
            # Extract reviews
            reviews = extract_reviews_data_fast(driver)
            
            if reviews:
                print(f"    Found {len(reviews)} reviews with ultimate approach {i+1}")
                return reviews
            else:
                print(f"    No reviews found with ultimate approach {i+1}")
                
        except Exception as e:
            print(f"    Error with ultimate approach {i+1}: {e}")
            continue
    
    return []

def run_ultimate_scraper():
    print("🚀 STARTING ULTIMATE GOOGLE REVIEW SCRAPER - GET ALL 11 PROPERTIES FAST! 🚀")
    print("Combining all successful approaches and making it lightning fast!")
    driver = setup_driver()
    
    total_reviews = 0
    successful_properties = 0
    
    for name, urls in properties.items():
        print(f"\n🔥 Processing: {name}")
        try:
            reviews = scrape_property_ultimate(driver, name, urls)
            
            if reviews:
                success_count, error_count = send_to_domo(name, reviews)
                print(f"✅ {success_count} reviews successfully sent for {name}")
                if error_count > 0:
                    print(f"⚠ {error_count} reviews failed to send for {name}")
                total_reviews += success_count
                successful_properties += 1
            else:
                print(f"❌ No reviews found for {name}")
                
        except Exception as e:
            print(f"❌ Error scraping {name}: {e}")
        
        # Fast delay between properties
        time.sleep(random.uniform(2, 4))  # Reduced delay
    
    driver.quit()
    print(f"\n🎉 === ULTIMATE SCRAPING COMPLETE ===")
    print(f"✅ Successfully scraped {successful_properties}/{len(properties)} properties")
    print(f"📊 Total reviews sent: {total_reviews}")
    
    if successful_properties == 11:
        print("🏆 MISSION ACCOMPLISHED! ALL 11 PROPERTIES SCRAPED! 🏆")
    else:
        print(f"⚠ {11 - successful_properties} properties still need reviews")
    
    print("Done!")

if __name__ == "__main__":
    run_ultimate_scraper() 