import os
import time
import logging
import argparse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(level=logging.INFO)

PROPERTIES = [
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
    "The Waters at Heritage"
]

def scrape_property_reviews(property_name):
    logging.info(f"Scraping {property_name}")
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get("https://www.google.com/maps")

    try:
        # Accept cookies if prompt shows up
        time.sleep(3)
        try:
            accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept all')]")
            accept_button.click()
        except:
            pass

        # Search for the property
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(property_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        # Click the reviews button if it appears
        try:
            reviews_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, ' reviews')]")
            reviews_button.click()
            time.sleep(5)

            # Scroll to load more reviews
            review_scroll_area = driver.find_element(By.CLASS_NAME, "m6QErb.DxyBCb.kA9KIf.dS8AEf")
            for _ in range(5):
                ActionChains(driver).move_to_element(review_scroll_area).click().perform()
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", review_scroll_area)
                time.sleep(2)

            # Collect review text
            reviews = driver.find_elements(By.CLASS_NAME, "wiI7pd")
            review_texts = [r.text for r in reviews]
            logging.info(f"{property_name}: Collected {len(review_texts)} reviews")

            return {
                "property": property_name,
                "reviews": review_texts
            }

        except Exception as e:
            logging.warning(f"No reviews section found for {property_name}: {e}")
            return {
                "property": property_name,
                "reviews": []
            }

    finally:
        driver.quit()

def run_scraper(once=False):
    results = []
    for property_name in PROPERTIES:
        result = scrape_property_reviews(property_name)
        results.append(result)

    output_file = f"reviews_output_{int(time.time())}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in results:
            f.write(f"{entry['property']}:\n")
            for review in entry['reviews']:
                f.write(f"- {review}\n")
            f.write("\n")
    logging.info(f"All reviews written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run one-time scrape and exit")
    args = parser.parse_args()

    run_scraper(once=args.once)
