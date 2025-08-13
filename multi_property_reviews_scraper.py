#!/usr/bin/env python3
"""
Multi-Property Reviews Scraper
A specialized script to scrape reviews for multiple properties from Google Maps.

This script will:
1. Navigate to each property's Google Maps page
2. Click on the reviews section
3. Scroll through all reviews to load them
4. Extract review data including text, ratings, dates, and user names
5. Export to CSV and JSON formats for each property
6. Continue to the next property until all are processed

Usage:
    python multi_property_reviews_scraper.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import json
import csv
import time
import re
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import calendar

class MultiPropertyReviewsScraper:
    def __init__(self, headless: bool = False):
        """
        Initialize the multi-property reviews scraper.
        
        Args:
            headless: Run browser in headless mode (False to see what's happening)
        """
        self.driver = None
        self.headless = headless
        self.setup_driver()
        
        # List of properties to scrape
        self.properties = [
            {
                'name': 'The Waters at Hammond',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Hammond/@30.4877489,-90.465321,17z/data=!4m8!3m7!1s0x862723fbcc2afb85:0x188d3eeca51192d0!8m2!3d30.4877443!4d-90.4627461!9m1!1b1!16s%2Fg%2F11rsqw95lz?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            },
            {
                'name': 'The Flats at East Bay',
                'url': 'https://www.google.com/maps/place/The+Flats+at+East+Bay/@30.5014556,-87.8652493,17z/data=!4m8!3m7!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!8m2!3d30.5014556!4d-87.8626744!9m1!1b1!16s%2Fg%2F11kphm6rdl?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            },
            {
                'name': 'The Heights at Picardy',
                'url': 'https://www.google.com/maps/place/The+Heights+at+Picardy/@30.394175,-91.1028869,17z/data=!4m8!3m7!1s0x8626a56f7f0dc5bf:0xb38345b83bdc892b!8m2!3d30.3941704!4d-91.100312!9m1!1b1!16s%2Fg%2F11wc3yhv50?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            },
            {
                'name': 'The Waters at Bluebonnet',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Bluebonnet/@30.4147288,-91.0766963,17z/data=!4m8!3m7!1s0x8626a53bc0c94fbf:0x84b7af1708cc8d8d!8m2!3d30.4147242!4d-91.0741214!9m1!1b1!16s%2Fg%2F11vhqlgm6w?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            },
            {
                'name': 'The Waters at Crestview',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Crestview/@30.72914,-86.5837232,16z/data=!4m12!1m2!2m1!1sThe+Waters+at+Crestview!3m8!1s0x8891732640bd5b21:0x1f92c28a5bf11ed2!8m2!3d30.72914!4d-86.574196!9m1!1b1!15sChdUaGUgV2F0ZXJzIGF0IENyZXN0dmlld5IBEWFwYXJ0bWVudF9jb21wbGV4qgFPCg0vZy8xMXdqOWIxd19sEAEyHxABIhtz0Zy4AByGfqcuDOZ1uEsX5sFCaoT55uVWfksyGxACIhd0aGUgd2F0ZXJzIGF0IGNyZXN0dmlld-ABAA!16s%2Fg%2F11wj9b1w_l?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            },
            {
                'name': 'The Waters at Millerville',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Millerville/@30.439755,-91.0289876,17z/data=!4m8!3m7!1s0x8626bd7f2db7ca89:0x1d15edca3d614c78!8m2!3d30.4397504!4d-91.0264127!9m1!1b1!16s%2Fg%2F11sdm7v6s3?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            },
            {
                'name': 'The Waters at Redstone',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Redstone/@30.7362907,-86.5595057,17z/data=!4m8!3m7!1s0x8891731ed5ef4421:0xe82971b01b043e0e!8m2!3d30.7362861!4d-86.5569308!9m1!1b1!16s%2Fg%2F11sdm7w83h?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            },
            {
                'name': 'The Waters at Settlers Trace',
                'url': 'https://www.google.com/maps/place/The+Waters+at+Settlers+Trace/@30.162335,-92.0533341,17z/data=!4m8!3m7!1s0x86249d93f2c9161f:0xde2de5332356386d!8m2!3d30.1623304!4d-92.0507592!9m1!1b1!16s%2Fg%2F11vb312kvw?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            },
            {
                'name': 'The Waters at West Village',
                'url': 'https://www.google.com/maps/place/The+Waters+at+West+Village/@30.2221885,-92.0983901,17z/data=!4m8!3m7!1s0x86249fc349920de9:0x7945e14be23642b4!8m2!3d30.2221839!4d-92.0958152!9m1!1b1!16s%2Fg%2F11vdd4crjw?entry=ttu&g_ep=EgoyMDI1MDgxMC4wIKXMDSoASAFQAw%3D%3D'
            }
        ]
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options."""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Add various options for better scraping
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Set user agent
            ua = UserAgent()
            chrome_options.add_argument(f'--user-agent={ua.random}')
            
            # Setup service and driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("✅ WebDriver setup completed successfully")
            
        except Exception as e:
            print(f"❌ Error setting up WebDriver: {str(e)}")
            raise 
    
    def scrape_all_properties(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Scrape reviews for all properties.
        
        Returns:
            Dictionary with property names as keys and lists of reviews as values
        """
        all_property_reviews = {}
        
        print(f"🏢 Starting Multi-Property Reviews Scraping...")
        print(f"🎯 Total properties to scrape: {len(self.properties)}")
        print("=" * 80)
        
        for i, property_info in enumerate(self.properties, 1):
            property_name = property_info['name']
            property_url = property_info['url']
            
            print(f"\n🏢 Property {i}/{len(self.properties)}: {property_name}")
            print(f"🌐 URL: {property_url}")
            print("-" * 60)
            
            try:
                # Scrape reviews for this property
                property_reviews = self._scrape_single_property(property_name, property_url)
                
                if property_reviews:
                    all_property_reviews[property_name] = property_reviews
                    print(f"✅ Successfully scraped {len(property_reviews)} reviews for {property_name}")
                else:
                    print(f"⚠️ No reviews found for {property_name}")
                    all_property_reviews[property_name] = []
                
                # Add a small delay between properties
                if i < len(self.properties):
                    print("⏳ Waiting 3 seconds before next property...")
                    time.sleep(3)
                
            except Exception as e:
                print(f"❌ Error scraping {property_name}: {str(e)}")
                all_property_reviews[property_name] = []
                continue
        
        print(f"\n🎉 Multi-property scraping completed!")
        print(f"📊 Properties processed: {len(all_property_reviews)}")
        
        # Show summary
        for property_name, reviews in all_property_reviews.items():
            print(f"  {property_name}: {len(reviews)} reviews")
        
        return all_property_reviews 
    
    def _scrape_single_property(self, property_name: str, property_url: str) -> List[Dict[str, Any]]:
        """
        Scrape reviews for a single property.
        
        Args:
            property_name: Name of the property
            property_url: Google Maps URL for the property
            
        Returns:
            List of review dictionaries
        """
        try:
            print(f"🏢 Starting {property_name} Reviews Scraping...")
            
            # Navigate to the property's Google Maps page
            print(f"🌐 Navigating to {property_name}...")
            self.driver.get(property_url)
            time.sleep(5)  # Wait for page to load
            
            # Wait for the page to load and find the reviews section
            self._wait_for_reviews_section()
            
            # Check if we're already on a reviews page
            if self._is_reviews_page():
                print("✅ Already on reviews page, proceeding with extraction...")
                
                # Check if this is Google Maps Lite
                if self._is_maps_lite():
                    print("📱 Detected Google Maps Lite - using optimized selectors")
                else:
                    print("🖥️ Standard Google Maps detected")
            else:
                # Click on reviews to open the reviews panel
                self._open_reviews_panel()
            
            # Scroll through all reviews to load them
            all_reviews = self._scroll_and_extract_reviews()
            
            # Add property information to each review
            for review in all_reviews:
                review['Property'] = property_name  # Changed to just "Property"
                review['property_url'] = property_url
            
            print(f"🎉 Successfully extracted {len(all_reviews)} reviews for {property_name}!")
            return all_reviews
            
        except Exception as e:
            print(f"❌ Error during scraping {property_name}: {str(e)}")
            return [] 
    
    def _wait_for_reviews_section(self):
        """Wait for the reviews section to appear on the page."""
        try:
            print("⏳ Waiting for reviews section to load...")
            
            # Wait for either reviews section or business info to appear
            WebDriverWait(self.driver, 30).until(
                lambda driver: len(driver.find_elements(By.CSS_SELECTOR, '[aria-label*="review"]')) > 0 or
                             len(driver.find_elements(By.CSS_SELECTOR, '[aria-label*="rating"]')) > 0 or
                             len(driver.find_elements(By.CSS_SELECTOR, 'h1')) > 0
            )
            
            print("✅ Reviews section loaded")
            
        except TimeoutException:
            print("⚠️ Timeout waiting for reviews section")
    
    def _is_reviews_page(self) -> bool:
        """Check if we're already on a reviews page."""
        try:
            # Look for indicators that we're on a reviews page
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
    
    def _is_maps_lite(self) -> bool:
        """Check if we're on Google Maps Lite."""
        try:
            # Look for indicators of Google Maps Lite
            lite_indicators = [
                'mapslite' in self.driver.page_source.lower(),
                'maps.lite' in self.driver.page_source.lower(),
                len(self.driver.find_elements(By.CSS_SELECTOR, '.hjmQqc')) > 0,
                len(self.driver.find_elements(By.CSS_SELECTOR, '.IaK8zc')) > 0
            ]
            
            is_lite = any(lite_indicators)
            print(f"🔍 Maps Lite check: {is_lite}")
            return is_lite
            
        except Exception as e:
            print(f"⚠️ Error checking if Maps Lite: {str(e)}")
            return False 
    
    def _open_reviews_panel(self):
        """Click on reviews to open the reviews panel."""
        try:
            print("🔍 Looking for reviews section to click...")
            
            # Try multiple selectors for the reviews section
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
                            time.sleep(3)  # Wait for reviews panel to open
                            break
                    if reviews_clicked:
                        break
                except Exception as e:
                    continue
            
            if not reviews_clicked:
                print("⚠️ Could not find reviews section to click, trying alternative approach...")
                # Try to find and click on the reviews count
                try:
                    reviews_count_element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'reviews') or contains(text(), 'Reviews')]")
                    reviews_count_element.click()
                    time.sleep(3)
                    print("✅ Clicked on reviews count element")
                except:
                    print("⚠️ Alternative approach also failed")
            
        except Exception as e:
            print(f"⚠️ Error opening reviews panel: {str(e)}") 
    
    def _scroll_and_extract_reviews(self) -> List[Dict[str, Any]]:
        """
        Extract reviews with manual scrolling - user scrolls manually to load all reviews.
        
        Returns:
            List of review dictionaries
        """
        all_reviews = []
        last_review_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 10  # Increased to ensure we get all reviews
        same_count_streak = 0  # Track consecutive same review counts
        last_current_review_count = 0  # Track the current reviews found count
        max_same_count_streak = 3  # Allow 3 consecutive same counts before giving up
        
        print("📜 Starting manual review extraction...")
        print("🔄 Please manually scroll through the reviews to load them all...")
        print("📱 The scraper will extract reviews as you scroll...")
        print("🎯 Target: Load as many reviews as possible")
        print("⚠️ Auto-advance: Will move to next property after 3 consecutive same review counts")
        print("⚡ Smart detection: If <3 reviews initially, assumes <8 total and moves to next property")
        print()
        
        while scroll_attempts < max_scroll_attempts:
            try:
                # Extract current visible reviews
                current_reviews = self._extract_visible_reviews()
                current_review_count = len(current_reviews)
                
                print(f"📊 Current reviews found: {current_review_count}")
                
                # Smart detection: If very few reviews initially, assume property has few reviews total
                if scroll_attempts == 0 and current_review_count < 3:
                    print("🔍 Smart detection: Found less than 3 reviews initially")
                    print("💡 Assuming property has less than 8 total reviews (initial render limit)")
                    print("🔄 Moving to next property to save time...")
                    
                    # Still extract what we found
                    for review in current_reviews:
                        if not any(existing.get('review_text') == review.get('review_text') for existing in all_reviews):
                            all_reviews.append(review)
                    
                    print(f"📋 Extracted {len(all_reviews)} reviews before moving to next property")
                    break
                
                # Check if we're getting the same number of reviews repeatedly
                if current_review_count == last_current_review_count:
                    same_count_streak += 1
                    print(f"⚠️ Same review count detected: {same_count_streak}/{max_same_count_streak} times")
                    
                    if same_count_streak >= max_same_count_streak:
                        print("🚨 Same review count detected 3 times in a row!")
                        print("🔄 Moving to next property to avoid getting stuck...")
                        break
                else:
                    same_count_streak = 0  # Reset streak if count changes
                
                last_current_review_count = current_review_count
                
                # Add new reviews to the list
                new_reviews_added = 0
                for review in current_reviews:
                    if not any(existing.get('review_text') == review.get('review_text') for existing in all_reviews):
                        all_reviews.append(review)
                        new_reviews_added += 1
                
                print(f"📋 Total reviews so far: {len(all_reviews)} (+{new_reviews_added} new)")
                
                # Check if scrolling is still effective
                if len(all_reviews) == last_review_count:
                    print("⚠️ No new reviews loaded, please scroll down to load more...")
                else:
                    print("✅ New reviews found, continuing...")
                
                last_review_count = len(all_reviews)
                
                # Wait for user to scroll manually
                print(f"📜 Waiting for manual scroll... (Attempt {scroll_attempts + 1}/{max_scroll_attempts})")
                print("🔄 Please scroll down in the reviews panel to load more reviews...")
                
                # Wait for user to scroll
                time.sleep(5)  # Give user time to scroll
                
                scroll_attempts += 1
                
            except Exception as e:
                print(f"⚠️ Error during review extraction: {str(e)}")
                scroll_attempts += 1
                continue
        
        print(f"📋 Total reviews extracted: {len(all_reviews)}")
        
        # Convert relative dates to actual dates
        print("📅 Converting relative dates to actual dates...")
        converted_count = 0
        for i, review in enumerate(all_reviews, 1):
            if review.get('review_date'):
                original_date = review['review_date']
                converted_date = self._convert_relative_date_to_actual_date(original_date)
                review['review_date'] = converted_date
                review['review_date_original'] = original_date  # Keep original for reference
                
                # Add additional date fields for analysis
                try:
                    if converted_date and not converted_date.endswith('(unparseable)'):
                        parsed_date = datetime.strptime(converted_date, '%Y-%m-%d')
                        review['review_year'] = parsed_date.year
                        review['review_month'] = parsed_date.month
                        review['review_month_name'] = calendar.month_name[parsed_date.month]
                        review['review_day_of_week'] = calendar.day_name[parsed_date.weekday()]
                        converted_count += 1
                except Exception as e:
                    print(f"⚠️ Error parsing converted date '{converted_date}': {str(e)}")
                
                # Show progress every 20 reviews
                if i % 20 == 0:
                    print(f"   📅 Processed {i}/{len(all_reviews)} reviews...")
        
        print(f"✅ Date conversion completed: {converted_count} dates converted successfully")
        return all_reviews 
    
    def _extract_visible_reviews(self) -> List[Dict[str, Any]]:
        """
        Extract all currently visible reviews from the page.
        
        Returns:
            List of review dictionaries
        """
        reviews = []
        
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
                        review_data = self._extract_single_review(element, is_maps_lite)
                        if review_data:
                            # Check if this review is already in our list
                            if not any(existing.get('review_text') == review_data.get('review_text') for existing in reviews):
                                reviews.append(review_data)
                                print(f"   ✅ Extracted review {len(reviews)}")
                    except Exception as e:
                        print(f"   ⚠️ Skipped element due to error: {str(e)}")
                        continue
                
                print(f"🎯 Successfully extracted {len(reviews)} reviews with selector '{best_selector}'")
                
                # If we didn't get all elements, try to understand why
                if len(reviews) < max_elements:
                    print(f"⚠️ Found {max_elements} elements but only extracted {len(reviews)} reviews")
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
            if not reviews:
                print("⚠️ No reviews found with specific selectors, trying broader approach...")
                reviews = self._extract_reviews_broad()
                
                # If still no reviews, save page source for debugging
                if not reviews:
                    print("⚠️ Still no reviews found, saving page source for debugging...")
                    self._save_page_source_for_debugging()
            
        except Exception as e:
            print(f"⚠️ Error extracting visible reviews: {str(e)}")
        
        return reviews 
    
    def _extract_single_review(self, review_element, is_maps_lite: bool = False) -> Dict[str, Any]:
        """
        Extract data from a single review element.
        
        Args:
            review_element: Selenium element containing review data
            is_maps_lite: Whether we're on Google Maps Lite (passed from parent method)
            
        Returns:
            Dictionary containing review data
        """
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
    
    def _convert_relative_date_to_actual_date(self, relative_date: str) -> str:
        """Convert relative dates like '2 years ago', '4 months ago' to actual dates."""
        try:
            if not relative_date:
                return relative_date
            
            date_text = relative_date.lower().strip()
            current_date = datetime.now()
            
            if 'year' in date_text:
                match = re.search(r'(\d+)\s*year', date_text)
                if match:
                    years = int(match.group(1))
                    estimated_date = current_date - timedelta(days=years * 365)
                    return estimated_date.strftime('%Y-%m-%d')
            elif 'month' in date_text:
                match = re.search(r'(\d+)\s*month', date_text)
                if match:
                    months = int(match.group(1))
                    estimated_date = current_date - timedelta(days=months * 30)
                    return estimated_date.strftime('%Y-%m-%d')
            elif 'week' in date_text:
                match = re.search(r'(\d+)\s*week', date_text)
                if match:
                    weeks = int(match.group(1))
                    estimated_date = current_date - timedelta(weeks=weeks)
                    return estimated_date.strftime('%Y-%m-%d')
            elif 'day' in date_text:
                match = re.search(r'(\d+)\s*day', date_text)
                if match:
                    days = int(match.group(1))
                    estimated_date = current_date - timedelta(days=days)
                    return estimated_date.strftime('%Y-%m-%d')
            elif 'just now' in date_text or 'today' in date_text:
                return current_date.strftime('%Y-%m-%d')
            
            return f"{relative_date} (unparseable)"
            
        except Exception as e:
            print(f"⚠️ Error converting date '{relative_date}': {str(e)}")
            return relative_date
    
    def export_to_csv(self, all_property_reviews: Dict[str, List[Dict[str, Any]]], filename: str = None) -> str:
        """Export all property reviews to CSV file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"multi_property_reviews_{timestamp}.csv"
        
        all_reviews = []
        for property_name, reviews in all_property_reviews.items():
            all_reviews.extend(reviews)
        
        all_keys = set()
        for record in all_reviews:
            all_keys.update(record.keys())
        
        fieldnames = sorted(list(all_keys))
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in all_reviews:
                row = {key: record.get(key, '') for key in fieldnames}
                writer.writerow(row)
        
        print(f"💾 All property reviews exported to: {filename}")
        return filename
    
    def export_to_json(self, all_property_reviews: Dict[str, List[Dict[str, Any]]], filename: str = None) -> str:
        """Export all property reviews to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"multi_property_reviews_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(all_property_reviews, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"💾 All property reviews exported to: {filename}")
        return filename
    
    def close(self):
        """Close the WebDriver and clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ WebDriver closed successfully")
            except Exception as e:
                print(f"⚠️ Error closing WebDriver: {str(e)}")

def main():
    """Main function to run the multi-property reviews scraper."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Property Reviews Scraper')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode (no browser window)')
    parser.add_argument('--output', choices=['json', 'csv', 'both'], default='json', 
                       help='Output format (default: json)')
    args = parser.parse_args()
    
    scraper = None
    
    try:
        print("🏢 Multi-Property Reviews Scraper")
        print("=" * 50)
        print("This script will extract reviews for multiple properties from Google Maps.")
        print("📱 You will need to manually scroll through the reviews for each property to load them all.")
        print(f"Mode: {'Headless' if args.headless else 'Visible browser'}")
        print(f"Output: {args.output.upper()}")
        print()
        
        scraper = MultiPropertyReviewsScraper(headless=args.headless)
        all_property_reviews = scraper.scrape_all_properties()
        
        if all_property_reviews:
            print(f"\n🎉 Multi-property scraping completed successfully!")
            
            total_reviews = 0
            for property_name, reviews in all_property_reviews.items():
                print(f"📊 {property_name}: {len(reviews)} reviews")
                total_reviews += len(reviews)
            
            print(f"📊 Total reviews across all properties: {total_reviews}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"multi_property_reviews_{timestamp}"
            
            if args.output in ['json', 'both']:
                json_file = scraper.export_to_json(all_property_reviews, f"{base_filename}.json")
                print(f"💾 JSON exported to: {json_file}")
            
            if args.output in ['csv', 'both']:
                csv_file = scraper.export_to_csv(all_property_reviews, f"{base_filename}.csv")
                print(f"💾 CSV exported to: {csv_file}")
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