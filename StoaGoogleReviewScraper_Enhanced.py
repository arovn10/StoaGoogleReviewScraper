import time
import json
import requests
import pandas as pd
import random
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define properties with multiple URL formats
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

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

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

def wait_for_page_load(driver, timeout=10):
    """Wait for page to load completely"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        time.sleep(2)  # Additional wait for dynamic content
    except TimeoutException:
        print("Page load timeout")

def click_reviews_tab(driver):
    """Click on the reviews tab to open reviews section"""
    try:
        # Try multiple possible selectors for the reviews tab
        review_selectors = [
            "//button[contains(., 'Reviews')]",
            "//a[contains(., 'Reviews')]",
            "//div[contains(., 'Reviews') and @role='tab']",
            "//span[contains(., 'Reviews')]/parent::button",
            "//div[contains(@aria-label, 'Reviews')]",
            "//button[contains(@aria-label, 'Reviews')]",
            "//div[contains(text(), 'Reviews')]",
            "//span[contains(text(), 'Reviews')]/parent::*"
        ]
        
        for selector in review_selectors:
            try:
                review_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"Found reviews tab with selector: {selector}")
                review_tab.click()
                time.sleep(3)
                return True
            except TimeoutException:
                continue
        
        # If no reviews tab found, try to scroll to find it
        print("No reviews tab found, scrolling to find it...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        for selector in review_selectors:
            try:
                review_tab = driver.find_element(By.XPATH, selector)
                print(f"Found reviews tab after scrolling with selector: {selector}")
                review_tab.click()
                time.sleep(3)
                return True
            except NoSuchElementException:
                continue
                
        return False
    except Exception as e:
        print(f"Error clicking reviews tab: {e}")
        return False

def scroll_reviews_section(driver):
    """Scroll through the reviews section to load more reviews"""
    try:
        # Wait for reviews container to appear
        review_container_selectors = [
            "//div[contains(@class, 'm6QErb')]",
            "//div[contains(@class, 'DxyBCb')]",
            "//div[@role='main']//div[contains(@class, 'scrollable')]",
            "//div[contains(@class, 'review-dialog-list')]",
            "//div[contains(@class, 'review-dialog')]",
            "//div[contains(@class, 'reviews')]",
            "//div[@role='main']",
            "//div[contains(@class, 'scrollable')]"
        ]
        
        scrollable_container = None
        for selector in review_container_selectors:
            try:
                scrollable_container = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                print(f"Found scrollable container with selector: {selector}")
                break
            except TimeoutException:
                continue
        
        if not scrollable_container:
            print("Could not find reviews container")
            return False
        
        # Scroll multiple times to load more reviews
        for i in range(10):
            try:
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_container)
                time.sleep(random.uniform(1.5, 2.5))  # Random delay to avoid detection
            except Exception as e:
                print(f"Scroll error on iteration {i}: {e}")
                break
        
        return True
    except Exception as e:
        print(f"Error scrolling reviews: {e}")
        return False

def extract_reviews_data(driver):
    """Extract review data from the page"""
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
            "//div[contains(@class, 'review-item')]"
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
                    ".//div[contains(@class, 'author')]"
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
                    ".//div[contains(@class, 'stars')]//span"
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
                    ".//div[contains(@class, 'snippet')]"
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

def scrape_property(driver, property_name, urls):
    """Try to scrape reviews from a property using multiple URL formats"""
    for i, url in enumerate(urls):
        print(f"  Trying URL format {i+1}/{len(urls)}: {url}")
        
        try:
            # Navigate to the property page
            driver.get(url)
            wait_for_page_load(driver)
            
            # Handle consent popup if present
            handle_consent_popup(driver)
            
            # Try to click on reviews tab (only for first URL format)
            if i == 0:
                if not click_reviews_tab(driver):
                    print(f"    Could not find reviews tab, trying alternative approach...")
                    # Try to navigate directly to reviews URL
                    reviews_url = url.replace("!5e0", "!5e0!3m1!1e1")
                    driver.get(reviews_url)
                    wait_for_page_load(driver)
                    handle_consent_popup(driver)
            
            # Scroll to load more reviews
            scroll_reviews_section(driver)
            
            # Extract reviews
            reviews = extract_reviews_data(driver)
            
            if reviews:
                print(f"    Found {len(reviews)} reviews with URL format {i+1}")
                return reviews
            else:
                print(f"    No reviews found with URL format {i+1}")
                
        except Exception as e:
            print(f"    Error with URL format {i+1}: {e}")
            continue
    
    return []

def run_scraper_enhanced():
    print("Starting Enhanced Google Review Scraper...")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--lang=en-US")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})

    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    total_reviews = 0
    successful_properties = 0

    for name, urls in properties.items():
        print(f"\nProcessing: {name}")
        try:
            reviews = scrape_property(driver, name, urls)
            
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
        time.sleep(random.uniform(3, 5))

    driver.quit()
    print(f"\n=== SCRAPING COMPLETE ===")
    print(f"Successfully scraped {successful_properties}/{len(properties)} properties")
    print(f"Total reviews sent: {total_reviews}")
    print("Done!")

if __name__ == "__main__":
    run_scraper_enhanced() 