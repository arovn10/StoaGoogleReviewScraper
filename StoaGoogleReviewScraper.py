"""Stoa Group Google Reviews Scraper

This script scrapes publicly available reviews for a set of Stoa Group
properties from Google Maps and posts them to a Domo webhook.  It uses
Selenium with an undetected Chrome driver in headless mode to avoid API
dependencies.  Reviews are fetched on demand when the script is run, and
the script can optionally enter a loop to perform this process once per
week.  See the accompanying README.md for usage details.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from typing import Dict, List

import requests
from dotenv import load_dotenv
import schedule
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def load_environment() -> None:
    """Load environment variables from a `.env` file if present."""
    if os.path.exists(".env"):
        load_dotenv()

# List of Stoa Group properties to scrape.  Adjust this list as new
# properties are added.
PROPERTIES: List[str] = [
    "The Waters at Settlers Trace",
    "The Waters at Redstone",
    "The Waters at Millerville",
    "The Waters at McGowin",
    "The Waters at Freeport",
    "The Waters at Crestview",
    "The Waters at Bluebonnet",
    "The Heights at Picardy",
    "The Flats at East Bay",
    "The Waters at West Village",
    "The Flats at Ransley",
    "The Waters at Ransley",
    "The Waters at Heritage",
    "The Waters at Hammond",
]

def scrape_property_reviews(property_name: str, max_reviews: int = 5) -> List[Dict[str, object]]:
    """Scrape up to `max_reviews` public reviews for the given property.

    This function automates a headless Chrome browser to search Google Maps,
    open the reviews panel for the specified property and extract reviewer
    names, ratings and text.  It does not require any login or Google API
    key, but it is more fragile than using the official API because Google
    can change their HTML structure at any time.

    Args:
        property_name: The name of the property to search for.
        max_reviews: The maximum number of reviews to return.

    Returns:
        A list of dictionaries containing review data.  If no reviews are
        found, an empty list is returned.
    """
    reviews: List[Dict[str, object]] = []
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    try:
        driver = uc.Chrome(options=options)
    except Exception as exc:
        logging.error("Failed to launch Chrome for %s: %s", property_name, exc)
        return reviews

    try:
        driver.get("https://www.google.com/maps")
        wait = WebDriverWait(driver, 20)
        # Find search box and submit property name
        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
        search_box.clear()
        search_box.send_keys(property_name)
        search_box.submit()

        # Click the first search result to open details panel
        try:
            first_result = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "(//div[@role='article']//a[contains(@href,'/maps/place')])[1]"
                    )
                )
            )
            first_result.click()
        except Exception:
            logging.warning("No search results found for %s", property_name)
            return reviews

        # Wait for the place details header to appear
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
        except Exception:
            logging.warning("Place details did not load for %s", property_name)
            return reviews

        # Click the reviews button
        try:
            reviews_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, ' reviews')]")
                )
            )
            reviews_button.click()
        except Exception:
            logging.warning("No reviews section found for %s", property_name)
            return reviews

        # Wait for review elements to load
        try:
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jftiEf")))
        except Exception:
            logging.warning("Review elements did not load for %s", property_name)
            return reviews

        review_elements = driver.find_elements(By.CLASS_NAME, "jftiEf")[:max_reviews]
        for el in review_elements:
            try:
                author = el.find_element(By.CLASS_NAME, "d4r55").text
                rating: float | None = None
                rating_elem = el.find_element(By.CLASS_NAME, "kvMYJc")
                if rating_elem:
                    rating_str = rating_elem.get_attribute("aria-label")
                    if rating_str:
                        try:
                            rating = float(rating_str.split(" ")[0])
                        except Exception:
                            rating = None
                text_elem = el.find_element(By.CLASS_NAME, "wiI7pd")
                text = text_elem.text if text_elem else ""
                reviews.append(
                    {
                        "property": property_name,
                        "author": author,
                        "rating": rating,
                        "text": text,
                        "timestamp": None,
                    }
                )
            except Exception:
                continue
    finally:
        driver.quit()
    return reviews

def scrape_all(properties: List[str], max_reviews: int = 5) -> List[Dict[str, object]]:
    """Scrape reviews for all properties and return a combined list."""
    all_reviews: List[Dict[str, object]] = []
    for prop in properties:
        logging.info("Scraping %s", prop)
        reviews = scrape_property_reviews(prop, max_reviews)
        all_reviews.extend(reviews)
    return all_reviews

def send_to_domo(payload: List[Dict[str, object]], webhook_url: str) -> None:
    """POST the JSON payload to the configured Domo webhook.

    Args:
        payload: List of review dictionaries.
        webhook_url: The webhook endpoint provided by Domo.
    """
    try:
        headers = {"Content-Type": "application/json"}
        payload_lines = "\n".join(json.dumps(r) for r in payload)
        resp = requests.post(
            webhook_url, data=payload_lines.encode("utf-8"), headers=headers, timeout=30
        )
        resp.raise_for_status()
        logging.info(
            "Sent %d reviews to Domo successfully (status %s)",
            len(payload),
            resp.status_code,
        )
    except Exception as exc:
        logging.error("Failed to send payload to Domo: %s", exc)

def scrape_and_send(properties: List[str], webhook_url: str, max_reviews: int = 5) -> None:
    """Scrape reviews and send them to Domo if any are found."""
    reviews = scrape_all(properties, max_reviews)
    if reviews:
        send_to_domo(reviews, webhook_url)
    else:
        logging.warning("No reviews found for any properties.")

def run_weekly(webhook_url: str) -> None:
    """Schedule the scraping job to run every week."""
    schedule.every(7).days.do(scrape_and_send, PROPERTIES, webhook_url)
    logging.info("Scheduled weekly scraping job.")
    while True:
        schedule.run_pending()
        time.sleep(3600)

def parse_args(argv: List[str]) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Stoa Google Reviews scraper.")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run the scraper once and exit instead of weekly.",
    )
    parser.add_argument(
        "--max-reviews",
        type=int,
        default=5,
        help="Maximum number of reviews to scrape per property.",
    )
    return parser.parse_args(argv)

def main(argv: List[str]) -> None:
    load_environment()
    args = parse_args(argv[1:])
    webhook_url = os.environ.get("DOMO_WEBHOOK_URL")
    if not webhook_url:
        logging.error(
            "Environment variable DOMO_WEBHOOK_URL is not set. Cannot post results."
        )
        sys.exit(1)
    if args.once:
        scrape_and_send(PROPERTIES, webhook_url, args.max_reviews)
    else:
        run_weekly(webhook_url)

if __name__ == "__main__":
    main(sys.argv)
