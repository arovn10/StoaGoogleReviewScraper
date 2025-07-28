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
        time.sleep(2)
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(property_name)
        search_box.submit()
        time.sleep(4)
        try:
            reviews_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, ' reviews')]")
            reviews_button.click()
            time.sleep(3)
        except Exception:
            logging.warning("No reviews section found for %s", property_name)
            return reviews
        review_elements = driver.find_elements(By.CLASS_NAME, "jftiEf")[:max_reviews]
        for el in review_elements:
            try:
                author = el.find_element(By.CLASS_NAME, "d4r55").text
                rating_str = el.find_element(By.CLASS_NAME, "kvMYJc").get_attribute("aria-label")
                rating = None
                if rating_str:
                    try:
                        rating = float(rating_str.split(" ")[0])
                    except Exception:
                        rating = None
                text = el.find_element(By.CLASS_NAME, "wiI7pd").text
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


def send_to_domo(payload: List[Dict[str, object]], webhook_url: str) -> None:
    """POST the JSON payload to the configured Domo webhook.

    Args:
        payload: List of review dictionaries.
        webhook_url: The webhook endpoint provided by Domo.
    """
    try:
        headers = {"Content-Type": "application/json"}
        payload_lines = "\n".join(json.dumps(r) for r in payload)
        resp = requests.post(webhook_url, data=payload_lines.encode("utf-8"), headers=headers, timeout=30)
        resp.raise_for_status()
        logging.info(
            "Sent %d reviews to Domo successfully (status %s)", len(payload), resp.status_code
        )
    except Exception as exc:
        logging.error("Failed to send payload to Domo: %s", exc)


def scrape_all() -> List[Dict[str, object]]:
    """Iterate through all properties and collect their scraped reviews.

    Returns:
        Combined list of reviews for all properties.
    """
    all_reviews: List[Dict[str, object]] = []
    for property_name in PROPERTIES:
        logging.info("Scraping %s", property_name)
        prop_reviews = scrape_property_reviews(property_name, max_reviews=5)
        all_reviews.extend(prop_reviews)
    return all_reviews


def scrape_and_send(webhook_url: str) -> None:
    """Scrape reviews for all properties and send them to Domo."""
    reviews = scrape_all()
    if not reviews:
        logging.warning("No reviews fetched; skipping webhook send")
        return
    send_to_domo(reviews, webhook_url)


def run_weekly(webhook_url: str) -> None:
    """Schedule the scraping job to run every week indefinitely."""
    schedule.every(7).days.do(scrape_and_send, webhook_url=webhook_url)
    logging.info("Scheduled weekly scraping job; awaiting first run")
    while True:
        schedule.run_pending()
        time.sleep(3600)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scrape Google reviews for Stoa Group properties.")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run the scraper once and exit instead of scheduling weekly.",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    load_environment()
    args = parse_args(argv)
    webhook_url = os.environ.get("DOMO_WEBHOOK_URL")
    if not webhook_url:
        logging.error("Environment variable DOMO_WEBHOOK_URL is not set; exiting.")
        sys.exit(1)
    if args.once:
        scrape_and_send(webhook_url)
    else:
        run_weekly(webhook_url)


if __name__ == "__main__":
    main(sys.argv[1:])