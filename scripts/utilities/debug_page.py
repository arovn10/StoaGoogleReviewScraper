#!/usr/bin/env python3
"""
Debug script to see what's actually on the Google Maps page.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def debug_page():
    """Debug what's on the Google Maps page."""
    try:
        print("🔍 Debugging Google Maps page...")
        
        # Setup Chrome in headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            # Navigate to Hammond property
            url = "https://www.google.com/maps/place/The+Waters+at+Hammond/@30.4877489,-90.465321,17z/data=!4m8!3m7!1s0x862723fbcc2afb85:0x188d3eeca51192d0!8m2!3d30.4877443!4d-90.4627461!9m1!1b1!16s%2Fg%2F11rsqw95lz?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D"
            driver.get(url)
            time.sleep(5)
            
            print("📄 Page loaded, analyzing content...")
            
            # Check page title
            print(f"📋 Page title: {driver.title}")
            
            # Look for review-related elements
            review_selectors = [
                '[aria-label*="review"]',
                '[aria-label*="rating"]',
                'button[aria-label*="review"]',
                'div[aria-label*="review"]',
                '[data-value*="review"]',
                '[aria-label*="reviews"]',
                '[aria-label*="Reviews"]'
            ]
            
            print("\n🔍 Looking for review elements...")
            for selector in review_selectors:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"   ✅ {selector}: Found {len(elements)} elements")
                    for i, elem in enumerate(elements[:3]):  # Show first 3
                        try:
                            aria_label = elem.get_attribute('aria-label')
                            text = elem.text
                            print(f"      Element {i+1}: aria-label='{aria_label}', text='{text[:50]}...'")
                        except:
                            print(f"      Element {i+1}: Could not get details")
                else:
                    print(f"   ❌ {selector}: No elements found")
            
            # Look for any text containing "review"
            print("\n🔍 Looking for text containing 'review'...")
            try:
                review_text_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'review') or contains(text(), 'Review') or contains(text(), 'reviews') or contains(text(), 'Reviews')]")
                print(f"   Found {len(review_text_elements)} elements with 'review' text")
                for i, elem in enumerate(review_text_elements[:5]):  # Show first 5
                    try:
                        text = elem.text.strip()
                        if text:
                            print(f"      Element {i+1}: '{text[:100]}...'")
                    except:
                        continue
            except Exception as e:
                print(f"   Error searching for review text: {e}")
            
            # Save page source for manual inspection
            with open("debug_page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("\n💾 Page source saved to debug_page_source.html")
            
            # Take screenshot
            driver.save_screenshot("debug_page_screenshot.png")
            print("📸 Screenshot saved to debug_page_screenshot.png")
            
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    debug_page() 