#!/usr/bin/env python3
"""
Working Auto-Scroll Multi-Property Reviews Scraper
Based on the working multi_property_reviews_scraper.py logic with auto-scrolling.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import json
import time
import re
import requests
from datetime import datetime
from typing import List, Dict, Any
from selenium.webdriver.common.keys import Keys

class WorkingAutoScraper:
    def __init__(self, headless: bool = False):
        self.driver = None
        self.headless = headless
        
        # Domo webhook configuration
        self.DOMO_WEBHOOK_URL = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"
        
        self.setup_driver()
        
        # Properties with lite=1 parameter
        self.properties = [
            {
                'name': 'The Waters at Hammond',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Hammond/@30.4877489,-90.465321,17z/data=!4m8!3m7!1s0x862723fbcc2afb85:0x188d3eeca51192d0!8m2!3d30.4877443!4d-90.4627461!9m1!1b1!16s%2Fg%2F11rsqw95lz?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            },
            {
                'name': 'The Flats at East Bay',
                'url': 'https://www.google.com/maps/place/The+Flats+at+East+Bay/@30.5014556,-87.8652493,17z/data=!4m8!3m7!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!8m2!3d30.5014556!4d-87.8626744!9m1!1b1!16s%2Fg%2F11kphm6rdl?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            },
            {
                'name': 'The Heights at Picardy',
                'url': 'https://www.google.com/maps/place/The+Heights+at+Picardy/@30.394175,-91.1028869,17z/data=!4m8!3m7!1s0x8626a56f7f0dc5bf:0xb38345b83bdc892b!8m2!3d30.3941704!4d-91.100312!9m1!1b1!16s%2Fg%2F11wc3yhv50?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            },
            {
                'name': 'The Waters at Bluebonnet',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Bluebonnet/@30.4147288,-91.0766963,17z/data=!4m8!3m7!1s0x8626a53bc0c94fbf:0x84b7af1708cc8d8d!8m2!3d30.4147242!4d-91.0741214!9m1!1b1!16s%2Fg%2F11vhqlgm6w?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            },
            {
                'name': 'The Waters at Crestview',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Crestview/@30.72914,-86.5837232,16z/data=!4m12!1m2!2m1!1sThe+Waters+at+Crestview!3m8!1s0x8891732640bd5b21:0x1f92c28a5bf11ed2!8m2!3d30.72914!4d-86.574196!9m1!1b1!15sChdUaGUgV2F0ZXJzIGF0IENyZXN0dmlld5IBEWFwYXJ0bWVudF9jb21wbGV4qgFPCg0vZy8xMXdqOWIxd19sEAEyHxABIhtz0Zy4AByGfqcuDOZ1uEsX5sFCaoT55uVWfksyGxACIhd0aGUgd2F0ZXJzIGF0IGNyZXN0dmlld-ABAA!16s%2Fg%2F11wj9b1w_l?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            },
            {
                'name': 'The Waters at Millerville',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Millerville/@30.439755,-91.0289876,17z/data=!4m8!3m7!1s0x8626bd7f2db7ca89:0x1d15edca3d614c78!8m2!3d30.4397504!4d-91.0264127!9m1!1b1!16s%2Fg%2F11sdm7v6s3?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            },
            {
                'name': 'The Waters at Redstone',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Redstone/@30.7362907,-86.5595057,17z/data=!4m8!3m7!1s0x8891731ed5ef4421:0xe82971b01b043e0e!8m2!3d30.7362861!4d-86.5569308!9m1!1b1!16s%2Fg%2F11sdm7w83h?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            },
            {
                'name': 'The Waters at Settlers Trace',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Settlers+Trace/@30.162335,-92.0533341,17z/data=!4m8!3m7!1s0x86249d93f2c9161f:0xde2de5332356386d!8m2!3d30.1623304!4d-92.0507592!9m1!1b1!16s%2Fg%2F11vb312kvw?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            },
            {
                'name': 'The Waters at West Village',
                'url': 'https://www.google.com/maps/place/The+Waters+at+West+Village/@30.2221885,-92.0983901,17z/data=!4m8!3m7!1s0x86249fc349920de9:0x7945e14be23642b4!8m2!3d30.2221839!4d-92.0958152!9m1!1b1!16s%2Fg%2F11vdd4crjw?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D&lite=1'
            }
        ]
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options for Codespaces."""
        try:
            # Try Chrome first
            if self._try_chrome_setup():
                return
            
            # Fallback to Firefox if Chrome fails
            print("🔄 Chrome setup failed, trying Firefox...")
            if self._try_firefox_setup():
                return
            
            # Last resort: try to install Chrome
            print("🔄 Attempting to install Chrome...")
            self._install_chrome_if_needed()
            if self._try_chrome_setup():
                return
            
            raise Exception("Could not set up any WebDriver (Chrome or Firefox)")
            
        except Exception as e:
            print(f"❌ Error setting up WebDriver: {str(e)}")
            raise
    
    def _try_chrome_setup(self):
        """Try to set up Chrome WebDriver."""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Add various options for better scraping in Codespaces
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Additional options for Codespaces/Linux
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            # Set user agent
            ua = UserAgent()
            chrome_options.add_argument(f'--user-agent={ua.random}')
            
            # Setup service and driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ Chrome WebDriver setup completed successfully")
            return True
            
        except Exception as e:
            print(f"⚠️ Chrome setup failed: {str(e)}")
            return False
    
    def _try_firefox_setup(self):
        """Try to set up Firefox WebDriver as fallback."""
        try:
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager
            
            firefox_options = FirefoxOptions()
            
            if self.headless:
                firefox_options.add_argument("--headless")
            
            # Firefox options for Codespaces
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-dev-shm-usage")
            firefox_options.add_argument("--width=1920")
            firefox_options.add_argument("--height=1080")
            
            # Setup service and driver
            service = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=firefox_options)
            
            print("✅ Firefox WebDriver setup completed successfully")
            return True
            
        except Exception as e:
            print(f"⚠️ Firefox setup failed: {str(e)}")
            return False
    
    def _install_chrome_if_needed(self):
        """Install Chrome in Codespaces if not already installed."""
        try:
            import subprocess
            import os
            
            # Check if Chrome is already installed
            try:
                subprocess.run(['google-chrome', '--version'], capture_output=True, check=True)
                print("✅ Chrome is already installed")
                return
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
            
            print("🔄 Installing Chrome in Codespaces...")
            
            # Update package list
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            
            # Install Chrome dependencies
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'wget', 'gnupg2'], check=True)
            
            # Add Google Chrome repository
            subprocess.run(['wget', '-q', '-O', '-', 'https://dl.google.com/linux/linux_signing_key.pub'], 
                         stdout=subprocess.PIPE, check=True)
            
            # Download and install Chrome
            subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'], check=True)
            subprocess.run(['sudo', 'dpkg', '-i', 'google-chrome-stable_current_amd64.deb'], check=True)
            
            # Fix any dependency issues
            subprocess.run(['sudo', 'apt-get', 'install', '-f', '-y'], check=True)
            
            # Clean up
            subprocess.run(['rm', 'google-chrome-stable_current_amd64.deb'], check=True)
            
            print("✅ Chrome installed successfully")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not install Chrome automatically: {str(e)}")
            print("💡 You may need to install Chrome manually or use a different approach")

    def scrape_all_properties(self) -> Dict[str, List[Dict[str, Any]]]:
        """Scrape reviews for all properties."""
        all_property_reviews = {}
        
        print(f"🏢 Starting Working Auto-Scroll Multi-Property Reviews Scraping...")
        print(f"🎯 Total properties to scrape: {len(self.properties)}")
        print("=" * 80)
        
        for i, property_info in enumerate(self.properties, 1):
            property_name = property_info['name']
            property_url = property_info['url']
            
            print(f"\n🏢 Property {i}/{len(self.properties)}: {property_name}")
            print(f"🌐 URL: {property_url}")
            print("-" * 60)
            
            try:
                property_reviews = self._scrape_single_property(property_name, property_url)
                
                if property_reviews:
                    all_property_reviews[property_name] = property_reviews
                    print(f"✅ Successfully scraped {len(property_reviews)} reviews for {property_name}")
                else:
                    print(f"⚠️ No reviews found for {property_name}")
                    all_property_reviews[property_name] = []
                
                if i < len(self.properties):
                    print("⏳ Waiting 2 seconds before next property...")
                    time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error scraping {property_name}: {str(e)}")
                all_property_reviews[property_name] = []
                continue
        
        print(f"\n🎉 Multi-property scraping completed!")
        print(f"📊 Properties processed: {len(all_property_reviews)}")
        
        for property_name, reviews in all_property_reviews.items():
            print(f"  {property_name}: {len(reviews)} reviews")
        
        return all_property_reviews

    def _scrape_single_property(self, property_name: str, property_url: str) -> List[Dict[str, Any]]:
        """Scrape reviews for a single property."""
        try:
            print(f"🏢 Starting {property_name} Reviews Scraping...")
            
            # Navigate to the property
            print(f"🌐 Navigating to {property_name}...")
            self.driver.get(property_url)
            time.sleep(5)
            
            # Force Maps Lite
            print("🔄 Checking and forcing Maps Lite...")
            if not self._is_maps_lite():
                self._force_maps_lite()
            
            # Wait for page to load
            print("⏳ Waiting for page to load...")
            time.sleep(3)
            
            # Double-check Maps Lite after loading
            if not self._is_maps_lite():
                print("🔄 Still not on Maps Lite, trying one more time...")
                self._force_maps_lite()
                time.sleep(3)
            
            if self._is_maps_lite():
                print("✅ Successfully on Maps Lite")
            else:
                print("⚠️ Still not on Maps Lite, but continuing...")
            
            # Check if we're on reviews page
            if self._is_reviews_page():
                print("✅ Already on reviews page, proceeding with extraction...")
            else:
                print("🔍 Reviews page check: False")
                # Try to open reviews
                self._open_reviews_panel()
                time.sleep(3)
                
                if self._is_reviews_page():
                    print("✅ Successfully opened reviews page")
                else:
                    print("⚠️ Could not open reviews page, trying to continue...")
            
            # Extract reviews
            print("🔍 Extracting reviews...")
            all_reviews = self._extract_all_reviews()
            
            # Add property info
            for review in all_reviews:
                review['Property'] = property_name
                review['property_url'] = property_url
            
            print(f"🎉 Successfully extracted {len(all_reviews)} reviews for {property_name}!")
            return all_reviews
            
        except Exception as e:
            print(f"❌ Error during scraping {property_name}: {str(e)}")
            return []

    def _is_maps_lite(self) -> bool:
        """Check if we're on Google Maps Lite."""
        try:
            lite_indicators = [
                'mapslite' in self.driver.page_source.lower(),
                'maps.lite' in self.driver.page_source.lower(),
                'lite' in self.driver.current_url.lower(),
                len(self.driver.find_elements(By.CSS_SELECTOR, '.hjmQqc')) > 0,
                len(self.driver.find_elements(By.CSS_SELECTOR, '.IaK8zc')) > 0,
                len(self.driver.find_elements(By.CSS_SELECTOR, '.umkQCd')) > 0,
                len(self.driver.find_elements(By.CSS_SELECTOR, '.HeTgld')) > 0,
                # Additional Maps Lite indicators
                len(self.driver.find_elements(By.CSS_SELECTOR, '[data-lite]')) > 0,
                'lite' in self.driver.page_source.lower(),
                len(self.driver.find_elements(By.CSS_SELECTOR, '.nkePVe')) > 0  # Reviews container
            ]
            
            is_lite = any(lite_indicators)
            print(f"🔍 Maps Lite check: {is_lite}")
            return is_lite
                    
        except Exception as e:
            print(f"⚠️ Error checking if Maps Lite: {str(e)}")
            return False

    def _force_maps_lite(self):
        """Force Google Maps Lite."""
        try:
            print("🔄 Aggressively forcing Google Maps Lite...")
            
            current_url = self.driver.current_url
            
            # Try multiple attempts
            for attempt in range(1, 6):
                print(f"🔄 Attempt {attempt}: Trying alternative Maps Lite approach...")
                
                # Try refreshing with Maps Lite parameter
                if 'lite=' in current_url:
                    print(f"🔄 Refreshing with Maps Lite: {current_url}")
                    self.driver.get(current_url)
                    time.sleep(5)
                    
                    if self._is_maps_lite():
                        print("✅ Successfully forced Maps Lite via refresh")
                        return True
                
                # Try alternative Maps Lite URL patterns
                if '/place/' in current_url:
                    place_part = current_url.split('/place/')[1].split('?')[0]
                    alt_lite_url = f"https://www.google.com/maps/place/{place_part}?lite=1"
                    
                    if alt_lite_url != current_url:
                        print(f"🔄 Trying alternative Maps Lite URL: {alt_lite_url}")
                        self.driver.get(alt_lite_url)
                        time.sleep(5)
                        
                        if self._is_maps_lite():
                            print("✅ Successfully forced Maps Lite via alternative URL")
                            return True
                
                # Try with different Maps Lite parameters
                if attempt == 3:
                    enhanced_lite_url = f"https://www.google.com/maps/place/{place_part}?lite=1&hl=en"
                    print(f"🔄 Trying enhanced Maps Lite URL: {enhanced_lite_url}")
                    self.driver.get(enhanced_lite_url)
                    time.sleep(5)
                    
                    if self._is_maps_lite():
                        print("✅ Successfully forced Maps Lite via enhanced URL")
                        return True
                
                # Try with mobile user agent (sometimes helps with Maps Lite)
                if attempt == 4:
                    mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
                    self.driver.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{get: () => '{mobile_ua}'}})")
                    
                    print(f"🔄 Trying with mobile user agent...")
                    self.driver.get(current_url)
                    time.sleep(5)
                    
                    if self._is_maps_lite():
                        print("✅ Successfully forced Maps Lite via mobile user agent")
                        return True
            
            print("⚠️ Could not force Maps Lite, continuing with current interface")
            return False
                
        except Exception as e:
            print(f"⚠️ Error forcing Maps Lite: {str(e)}")
            return False

    def _is_reviews_page(self) -> bool:
        """Check if we're on a reviews page."""
        try:
            reviews_indicators = [
                'reviews' in self.driver.current_url.lower(),
                len(self.driver.find_elements(By.CSS_SELECTOR, '[data-review-id]')) > 0,
                len(self.driver.find_elements(By.CSS_SELECTOR, '.jJc9Ad')) > 0,
                len(self.driver.find_elements(By.CSS_SELECTOR, '.g88MCb')) > 0,
                'review' in self.driver.page_source.lower()
            ]
            
            is_reviews_page = any(reviews_indicators)
            print(f"🔍 Reviews page check: {is_reviews_page}")
            return is_reviews_page
            
        except Exception as e:
            print(f"⚠️ Error checking if on reviews page: {str(e)}")
            return False

    def _open_reviews_panel(self):
        """Open the reviews panel."""
        try:
            print("🔍 Looking for reviews section to click...")
            
            review_selectors = [
                '[aria-label*="review"]',
                '[aria-label*="rating"]',
                'button[aria-label*="review"]',
                'div[aria-label*="review"]',
                '[data-value*="review"]'
            ]
            
            reviews_clicked = False
            for selector in review_selectors:
                try:
                    review_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in review_elements:
                        if element.is_displayed() and element.is_enabled():
                            print(f"📝 Clicking on reviews element: {element.get_attribute('aria-label')}")
                            element.click()
                            reviews_clicked = True
                            time.sleep(3)
                            break
                    if reviews_clicked:
                        break
                except Exception as e:
                    continue
            
            if not reviews_clicked:
                print("⚠️ Could not find reviews section to click")
                
        except Exception as e:
            print(f"⚠️ Error opening reviews panel: {str(e)}")

    def _extract_all_reviews(self) -> List[Dict[str, Any]]:
        """Extract all reviews from the page using two-phase approach."""
        try:
            print("🔄 Phase 1: Auto-scrolling to the bottom to load all reviews...")
            
            # First, just scroll to the bottom without tracking reviews
            self._auto_scroll_to_bottom()
            
            print("✅ Phase 1 complete: Reached the bottom of reviews")
            print("🔄 Phase 2: Now extracting all reviews using comprehensive logic...")
            
            # Now use the EXACT logic from multi_property_reviews_scraper.py
            all_reviews = self._extract_all_reviews_comprehensive()
            
            print(f"📋 Phase 2 complete: Extracted {len(all_reviews)} reviews")
            return all_reviews
            
        except Exception as e:
            print(f"⚠️ Error in two-phase review extraction: {str(e)}")
            return []

    def _extract_all_reviews_comprehensive(self) -> List[Dict[str, Any]]:
        """Extract all reviews using the EXACT logic from multi_property_reviews_scraper.py."""
        all_reviews = []
        
        try:
            # Check Maps Lite status once at the beginning
            is_maps_lite = self._is_maps_lite()
            if is_maps_lite:
                print("📱 Using Maps Lite optimized extraction...")
            
            # Look for review containers - updated selectors for Google Maps Lite
            review_selectors = [
                '.hjmQqc',  # Google Maps Lite review container
                '[data-review-id]',
                '[aria-label*="review"]',
                '.review-dialog-review',
                '.g88MCb',
                '[role="article"]',
                '.jftiEf',
                '.jJc9Ad',
                '.g88MCb.S4rAq',
                '[data-review-index]',
                '.review-dialog-review-content',
                '.review-snippet',
                '.review-full-text'
            ]
            
            print("🔍 Searching for reviews with multiple selectors...")
            
            # First, try to find the selector with the most elements
            best_selector = None
            max_elements = 0
            
            for selector in review_selectors:
                try:
                    review_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"   Selector '{selector}': Found {len(review_elements)} elements")
                    
                    if len(review_elements) > max_elements:
                        max_elements = len(review_elements)
                        best_selector = selector
                        
                except NoSuchElementException:
                    continue
            
            # Now extract from the best selector
            if best_selector:
                print(f"🎯 Using best selector '{best_selector}' with {max_elements} elements")
                review_elements = self.driver.find_elements(By.CSS_SELECTOR, best_selector)
                
                for element in review_elements:
                    try:
                        review_data = self._extract_single_review_comprehensive(element, is_maps_lite)
                        if review_data:
                            # Check if this review is already in our list
                            if not any(existing.get('review_text') == review_data.get('review_text') for existing in all_reviews):
                                all_reviews.append(review_data)
                                print(f"   ✅ Extracted review {len(all_reviews)}")
                    except Exception as e:
                        print(f"   ⚠️ Skipped element due to error: {str(e)}")
                        continue
                
                print(f"🎯 Successfully extracted {len(all_reviews)} reviews with selector '{best_selector}'")
                
                # If we didn't get all elements, try to understand why
                if len(all_reviews) < max_elements:
                    print(f"⚠️ Found {max_elements} elements but only extracted {len(all_reviews)} reviews")
                    print(f"💡 This suggests some elements don't contain valid review data")
                    
                    # Analyze a few failed elements to understand why
                    failed_count = 0
                    for i, element in enumerate(review_elements):
                        if failed_count >= 3:  # Only analyze first 3 failures
                            break
                        try:
                            element_text = element.text.strip()
                            if len(element_text) < 10:  # Very short text
                                print(f"   🔍 Failed element {i}: Very short text ({len(element_text)} chars): '{element_text}'")
                                failed_count += 1
                            elif not any(word in element_text.lower() for word in ['review', 'star', 'rating', 'good', 'bad', 'great', 'nice']):
                                print(f"   🔍 Failed element {i}: No review-like content: '{element_text[:100]}...'")
                                failed_count += 1
                        except Exception as e:
                            print(f"   🔍 Failed element {i}: Error analyzing: {str(e)}")
                            failed_count += 1
            
            # If no reviews found with specific selectors, try a broader approach
            if not all_reviews:
                print("⚠️ No reviews found with specific selectors, trying broader approach...")
                all_reviews = self._extract_reviews_broad()
                
                # If still no reviews, save page source for debugging
                if not all_reviews:
                    print("⚠️ Still no reviews found, saving page source for debugging...")
                    self._save_page_source_for_debugging()
            
        except Exception as e:
            print(f"⚠️ Error extracting visible reviews: {str(e)}")
        
        return all_reviews

    def _extract_single_review_comprehensive(self, review_element, is_maps_lite: bool = False) -> Dict[str, Any]:
        """Extract data from a single review element using comprehensive logic from multi_property_reviews_scraper.py."""
        try:
            review_data = {
                'scraped_at': datetime.now().isoformat(),
            }
            
            # Extract review text - updated selectors for Google Maps Lite
            text_selectors = [
                '.umkQCd',  # Google Maps Lite review text container
                '.Inlyae',  # Google Maps Lite review text
                '.wiI7pd',
                '[aria-label*="review"]',
                '.review-full-text',
                '.review-snippet',
                'span[class*="font"]',
                '.jJc9Ad',
                '.review-text',
                '.review-content',
                '[data-review-text]',
                '.fontBodyMedium',
                '.fontBodySmall'
            ]
            
            for selector in text_selectors:
                try:
                    text_element = review_element.find_element(By.CSS_SELECTOR, selector)
                    if text_element.text.strip():
                        review_data['review_text'] = text_element.text.strip()
                        break
                except NoSuchElementException:
                    continue
            
            # Extract rating - updated selectors for Google Maps Lite
            rating_selectors = [
                '.HeTgld',  # Google Maps Lite rating container
                '[aria-label*="stars"]',
                '[aria-label*="rating"]',
                '[data-value]',
                '.lNH4rd'
            ]
            
            for selector in rating_selectors:
                try:
                    rating_element = review_element.find_element(By.CSS_SELECTOR, selector)
                    rating_attr = rating_element.get_attribute('aria-label') or rating_element.text
                    if rating_attr:
                        rating_match = re.search(r'(\d+)', rating_attr)
                        if rating_match:
                            review_data['rating'] = int(rating_match.group(1))
                            break
                except NoSuchElementException:
                    continue
            
            # Extract user name - updated selectors for Google Maps Lite
            name_selectors = [
                '.IaK8zc',  # Google Maps Lite reviewer name
                '.CVo7Bb',  # Google Maps Lite reviewer name
                '.d4r55',
                '.P5Bobd',
                '[aria-label*="review by"]',
                '.reviewer-name'
            ]
            
            for selector in name_selectors:
                try:
                    name_element = review_element.find_element(By.CSS_SELECTOR, selector)
                    if name_element.text.strip():
                        review_data['reviewer_name'] = name_element.text.strip()
                        break
                except NoSuchElementException:
                    continue
            
            # Extract date - updated selectors for Google Maps Lite
            date_selectors = [
                '.bHyEBc',  # Google Maps Lite review date
                '.rsqaWe',
                '.review-date',
                '[aria-label*="reviewed"]',
                '.time-ago'
            ]
            
            for selector in date_selectors:
                try:
                    date_element = review_element.find_element(By.CSS_SELECTOR, selector)
                    if date_element.text.strip():
                        review_data['review_date'] = date_element.text.strip()
                        break
                except NoSuchElementException:
                    continue
            
            # Only return review if we have at least the text
            if review_data.get('review_text'):
                return review_data
            
            # If no text found with standard selectors, try Google Maps Lite specific approach
            if is_maps_lite:
                review_text = self._extract_maps_lite_review_text(review_element)
                if review_text:
                    review_data['review_text'] = review_text
                    review_data['extraction_method'] = 'maps_lite_specific'
                    return review_data
            
            # Try to get any text content from the element as a fallback
            try:
                element_text = review_element.text.strip()
                if element_text and len(element_text) > 10:  # Must have substantial text
                    review_data['review_text'] = element_text
                    review_data['extraction_method'] = 'fallback_text'
                    review_data['debug_info'] = f"Element text length: {len(element_text)}"
                    return review_data
            except Exception as e:
                pass
            
            # Debug: Log what we found in this element
            try:
                element_text = review_element.text.strip()
                element_html = review_element.get_attribute('outerHTML')[:200]  # First 200 chars
                print(f"   🔍 Debug: Element text length: {len(element_text)}, HTML preview: {element_html}")
            except Exception as e:
                print(f"   🔍 Debug: Could not inspect element: {str(e)}")
            
        except Exception as e:
            print(f"   🔍 Debug: Error in review extraction: {str(e)}")
        
        return None

    def _auto_scroll_to_bottom(self):
        """Auto-scroll to the bottom without tracking reviews - just load all content."""
        scroll_attempts = 0
        max_scroll_attempts = 30  # Increased significantly to ensure we get to the bottom
        same_count_streak = 0
        last_review_count = 0
        initial_review_count = 0
        found_reviews = False
        consecutive_no_change = 0
        max_consecutive_no_change = 8  # Allow more consecutive no-change before stopping
        
        print("🚀 Auto-scrolling to the bottom (Phase 1: Loading only, no extraction)...")
        
        while scroll_attempts < max_scroll_attempts:
            try:
                # Just count reviews to see if we're still loading more
                current_reviews = self._count_visible_reviews()
                current_count = current_reviews
                
                print(f"📊 Reviews visible: {current_count}")
                
                # If this is the first time we found reviews, note it
                if current_count > 0 and not found_reviews:
                    found_reviews = True
                    initial_review_count = current_count
                    print(f"🎯 First reviews found! Starting with {current_count} reviews")
                
                # Check if we're getting new reviews
                if current_count > last_review_count:
                    new_reviews = current_count - last_review_count
                    print(f"📈 Found {new_reviews} new reviews, continuing scroll...")
                    same_count_streak = 0
                    consecutive_no_change = 0  # Reset consecutive no-change counter
                else:
                    same_count_streak += 1
                    consecutive_no_change += 1
                    print(f"⚠️ Same review count: {same_count_streak}/8 (stopping when we hit 8)")
                    print(f"📊 Consecutive no-change: {consecutive_no_change}/{max_consecutive_no_change}")
                    
                    # Only stop if we've found reviews AND hit the same count 8 times
                    # AND we've had enough consecutive attempts with no change
                    if same_count_streak >= 8 and found_reviews and consecutive_no_change >= max_consecutive_no_change:
                        print("✅ Same review count detected 8 times with no change - reached the bottom!")
                        break
                    elif same_count_streak >= 8 and not found_reviews:
                        print("⚠️ Still no reviews found after 8 attempts, but continuing...")
                        same_count_streak = 0  # Reset streak and keep trying
                
                last_review_count = current_count
                
                # Perform scroll
                self._scroll_page()
                time.sleep(1)
                
                scroll_attempts += 1
                
            except Exception as e:
                print(f"⚠️ Error during scrolling: {str(e)}")
                scroll_attempts += 1
                continue
        
        print(f"✅ Scrolling complete after {scroll_attempts} attempts - reached the bottom")
        if found_reviews:
            print(f"📊 Started with {initial_review_count} reviews, ended with {last_review_count} reviews")
        return True

    def _count_visible_reviews(self) -> int:
        """Just count visible reviews without extracting them (for Phase 1 scrolling)."""
        try:
            # Use the same selector that the comprehensive extraction will use
            # This ensures Phase 1 and Phase 2 are looking at the same elements
            # Try multiple selectors to find the one that works
            selectors_to_try = ['.hjmQqc', '[data-review-id]', '.jftiEf']
            
            for selector in selectors_to_try:
                try:
                    review_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(review_elements) > 0:
                        print(f"   📊 Phase 1 using selector '{selector}' to count reviews")
                        return len(review_elements)
                except Exception as e:
                    continue
            
            return 0
        except Exception as e:
            print(f"⚠️ Error counting reviews: {str(e)}")
            return 0

    def _scroll_page(self):
        """Scroll the page to load more content."""
        try:
            # Try to find and scroll the reviews container - use the working selector
            reviews_container = self.driver.find_element(By.CSS_SELECTOR, 'div.nkePVe')
            if reviews_container:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", reviews_container)
                time.sleep(0.5)
                return
        except:
            pass
        
        try:
            # Fallback to page scroll
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(0.5)
        except:
            pass
        
        try:
            # Alternative: use Page Down key
            body = self.driver.find_element(By.CSS_SELECTOR, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
        except:
            pass
    
    def _extract_maps_lite_review_text(self, review_element) -> str:
        """Extract review text specifically for Google Maps Lite."""
        try:
            text_selectors = ['.umkQCd', '.Inlyae', '.wiI7pd']
            for selector in text_selectors:
                try:
                    text_element = review_element.find_element(By.CSS_SELECTOR, selector)
                    return text_element.text.strip()
                except NoSuchElementException:
                    continue
            return ""
        except Exception as e:
            return ""
    
    def _extract_reviews_broad(self) -> List[Dict[str, Any]]:
        """Extract reviews using a broader approach when specific selectors fail."""
        reviews = []
        try:
            page_source = self.driver.page_source
            review_patterns = [
                r'<div[^>]*class="[^"]*review[^"]*"[^>]*>([^<]+)</div>',
                r'<span[^>]*class="[^"]*review[^"]*"[^>]*>([^<]+)</span>'
            ]
            for pattern in review_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    if len(match.strip()) > 20:
                        reviews.append({
                            'scraped_at': datetime.now().isoformat(),
                            'review_text': match.strip(),
                            'extraction_method': 'regex_fallback'
                        })
        except Exception as e:
            print(f"⚠️ Error in broad review extraction: {str(e)}")
        return reviews
    
    def _save_page_source_for_debugging(self):
        """Save the current page source for debugging purposes."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"debug_page_source_{timestamp}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            print(f"💾 Debug page source saved to: {filename}")
        except Exception as e:
            print(f"⚠️ Error saving debug files: {str(e)}")

    def export_to_json(self, all_property_reviews: Dict[str, List[Dict[str, Any]]], filename: str = None) -> str:
        """Export to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"working_auto_scraper_{timestamp}.json"
        
        # Flatten the structure
        flattened_reviews = []
        for property_name, reviews in all_property_reviews.items():
            flattened_reviews.extend(reviews)
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(flattened_reviews, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"💾 JSON exported to: {filename} ({len(flattened_reviews)} reviews)")
        return filename

    def save_json_to_folder(self, all_property_reviews: Dict[str, List[Dict[str, Any]]]) -> str:
        """Save review data to JSON file in the organized outputs folder."""
        try:
            # Create outputs directory if it doesn't exist
            import os
            outputs_dir = "data/outputs"
            os.makedirs(outputs_dir, exist_ok=True)
            
            # Generate descriptive filename with timestamp and summary
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            total_properties = len(all_property_reviews)
            total_reviews = sum(len(reviews) for reviews in all_property_reviews.values())
            
            # Create a descriptive filename
            filename = f"google_reviews_{timestamp}_p{total_properties}_r{total_reviews}.json"
            filepath = os.path.join(outputs_dir, filename)
            
            # Prepare data for JSON export (include metadata)
            export_data = {
                "metadata": {
                    "scraper_version": "working_auto_scraper_v1.0",
                    "scraped_at": datetime.now().isoformat(),
                    "total_properties": total_properties,
                    "total_reviews": total_reviews,
                    "properties_processed": list(all_property_reviews.keys())
                },
                "reviews": all_property_reviews
            }
            
            # Save to JSON file
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
            
            print(f"💾 JSON saved to: {filepath}")
            print(f"📊 File contains: {total_properties} properties, {total_reviews} reviews")
            
            # Also create a summary file
            summary_filename = f"summary_{timestamp}_p{total_properties}_r{total_reviews}.json"
            summary_filepath = os.path.join(outputs_dir, summary_filename)
            
            summary_data = {
                "scraping_summary": {
                    "timestamp": datetime.now().isoformat(),
                    "scraper_version": "working_auto_scraper_v1.0",
                    "total_properties": total_properties,
                    "total_reviews": total_reviews,
                    "properties": {}
                }
            }
            
            # Add property summaries
            for property_name, reviews in all_property_reviews.items():
                summary_data["scraping_summary"]["properties"][property_name] = {
                    "review_count": len(reviews),
                    "last_scraped": datetime.now().isoformat(),
                    "sample_reviews": reviews[:3] if reviews else []  # First 3 reviews as sample
                }
            
            with open(summary_filepath, 'w', encoding='utf-8') as summaryfile:
                json.dump(summary_data, summaryfile, indent=2, ensure_ascii=False)
            
            print(f"📋 Summary saved to: {summary_filepath}")
            
            return filepath
            
        except Exception as e:
            print(f"❌ Error saving JSON to folder: {str(e)}")
            return ""

    def push_to_domo(self, all_property_reviews: Dict[str, List[Dict[str, Any]]], max_retries: int = 3):
        """Push review data to Domo webhook with flattened structure - one row per review."""
        try:
            print(f"🔗 Preparing to push flattened review data to Domo webhook...")
            
            # Flatten the data structure - one row per review
            flattened_reviews = []
            
            for property_name, reviews in all_property_reviews.items():
                for review in reviews:
                    # Create a flattened record with all review data
                    flattened_review = {
                        'timestamp': datetime.now().isoformat(),
                        'scraper_version': 'working_auto_scraper_v1.0',
                        'property_name': property_name,
                        'review_text': review.get('review_text', ''),
                        'rating': review.get('rating', ''),
                        'reviewer_name': review.get('reviewer_name', ''),
                        'review_date': review.get('review_date', ''),
                        'review_date_original': review.get('review_date_original', ''),
                        'review_year': review.get('review_year', ''),
                        'review_month': review.get('review_month', ''),
                        'review_month_name': review.get('review_month_name', ''),
                        'review_day_of_week': review.get('review_day_of_week', ''),
                        'scraped_at': review.get('scraped_at', ''),
                        'extraction_method': review.get('extraction_method', ''),
                        'property_url': review.get('property_url', ''),
                        'debug_info': review.get('debug_info', '')
                    }
                    flattened_reviews.append(flattened_review)
            
            print(f"📊 Flattened {len(flattened_reviews)} reviews for Domo")
            
            # Send data in batches to avoid payload size limits
            batch_size = 100
            total_batches = (len(flattened_reviews) + batch_size - 1) // batch_size
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(flattened_reviews))
                batch_data = flattened_reviews[start_idx:end_idx]
                
                # Prepare batch payload
                batch_payload = {
                    'batch_number': batch_num + 1,
                    'total_batches': total_batches,
                    'batch_size': len(batch_data),
                    'total_reviews': len(flattened_reviews),
                    'timestamp': datetime.now().isoformat(),
                    'scraper_version': 'working_auto_scraper_v1.0',
                    'reviews': batch_data
                }
                
                print(f"📦 Sending batch {batch_num + 1}/{total_batches} with {len(batch_data)} reviews...")
                
                # Send batch to Domo
                success = self._send_batch_to_domo(batch_payload, max_retries)
                
                if not success:
                    print(f"❌ Failed to send batch {batch_num + 1} after {max_retries} attempts")
                    return False
                
                # Small delay between batches
                if batch_num < total_batches - 1:
                    time.sleep(1)
            
            print(f"✅ Successfully pushed all {len(flattened_reviews)} reviews to Domo in {total_batches} batches")
            return True
            
        except Exception as e:
            print(f"❌ Error preparing data for Domo: {str(e)}")
            return False
    
    def _send_batch_to_domo(self, batch_payload: Dict[str, Any], max_retries: int = 3) -> bool:
        """Send a single batch of reviews to Domo with retry logic."""
        for attempt in range(max_retries):
            try:
                print(f"   �� Attempt {attempt + 1}/{max_retries}...")
                
                response = requests.post(
                    self.DOMO_WEBHOOK_URL,
                    json=batch_payload,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if response.status_code == 200:
                    print(f"   ✅ Batch sent successfully (Status: {response.status_code})")
                    return True
                else:
                    print(f"   ⚠️ Domo returned status {response.status_code}: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"   ⚠️ Request error (attempt {attempt + 1}): {str(e)}")
                
            except Exception as e:
                print(f"   ⚠️ Unexpected error (attempt {attempt + 1}): {str(e)}")
            
            # Wait before retry (exponential backoff)
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"   ⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
        
        return False

    def close(self):
        """Close the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ WebDriver closed successfully")
            except Exception as e:
                print(f"⚠️ Error closing WebDriver: {str(e)}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Working Auto-Scroll Multi-Property Reviews Scraper')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--no-domo', action='store_true', help='Skip pushing data to Domo')
    args = parser.parse_args()
    
    scraper = None
    
    try:
        print("🏢 Working Auto-Scroll Multi-Property Reviews Scraper")
        print("=" * 60)
        print("This script combines working logic with auto-scrolling!")
        print(f"Mode: {'Headless' if args.headless else 'Visible browser'}")
        print(f"Domo Integration: {'Disabled' if args.no_domo else 'Enabled'}")
        print()
        
        scraper = WorkingAutoScraper(headless=args.headless)
        all_property_reviews = scraper.scrape_all_properties()
        
        if all_property_reviews:
            print(f"\n🎉 Multi-property scraping completed successfully!")
            
            total_reviews = 0
            for property_name, reviews in all_property_reviews.items():
                print(f"📊 {property_name}: {len(reviews)} reviews")
                total_reviews += len(reviews)
            
            print(f"📊 Total reviews across all properties: {total_reviews}")
            
            # Save JSON to organized folder
            print("\n💾 Saving data to organized JSON files...")
            json_filepath = scraper.save_json_to_folder(all_property_reviews)
            
            if json_filepath:
                print(f"✅ JSON data saved successfully to: {json_filepath}")
            else:
                print("⚠️ Failed to save JSON data")
            
            # Push to Domo (unless disabled)
            if not args.no_domo:
                print("\n🔗 Pushing data to Domo...")
                domo_success = scraper.push_to_domo(all_property_reviews)
                if domo_success:
                    print("✅ Data successfully pushed to Domo!")
                else:
                    print("❌ Failed to push data to Domo")
            else:
                print("⏭️ Skipping Domo push (--no-domo flag used)")
            
            print(f"\n🎯 Summary:")
            print(f"   📁 JSON files saved to: data/outputs/")
            print(f"   📊 Total properties: {len(all_property_reviews)}")
            print(f"   📝 Total reviews: {total_reviews}")
            print(f"   🔗 Domo integration: {'Enabled' if not args.no_domo else 'Disabled'}")
        else:
            print("❌ No reviews found for any property.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    finally:
        if scraper:
            if not args.headless:
                input("\nPress Enter to close the browser...")
            scraper.close()

if __name__ == "__main__":
    main() 