import argparse
import logging
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

logging.basicConfig(level=logging.INFO)

property_names = [
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
]

def get_google_reviews(property_name):
    logging.info(f"Scraping {property_name}")
    
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        # Navigate to Google
        driver.get("https://www.google.com/")
        time.sleep(1)

        # Accept cookies if prompted
        try:
            agree = driver.find_element(By.XPATH, "//button[.='Accept all']")
            agree.click()
        except:
            pass

        # Search the property name
        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(property_name)
        search_box.send_keys(Keys.RETURN)

        # Click on the review button in the knowledge panel
        try:
            reviews_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, ' reviews')]")
            ))
            reviews_button.click()
        except:
            logging.warning(f"No reviews button found for {property_name}")
            return {"property": property_name, "reviews": []}

        # Wait for reviews section to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jftiEf")))

        # Scroll reviews container
        scrollable_div = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="main"]//div[contains(@class, "m6QErb")]'))
        )

        for _ in range(5):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(2)

        # Collect review text
        reviews = driver.find_elements(By.CLASS_NAME, "wiI7pd")
        review_texts = [r.text for r in reviews if r.text.strip()]

        return {"property": property_name, "reviews": review_texts}

    except Exception as e:
        logging.warning(f"No reviews section found for {property_name}: {e}")
        return {"property": property_name, "reviews": []}

    finally:
        driver.quit()

def scrape_all():
    results = []
    for name in property_names:
        result = get_google_reviews(name)
        results.append(result)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run scraper once immediately")
    args = parser.parse_args()

    if args.once:
        scraped = scrape_all()
        with open("reviews_output.json", "w", encoding="utf-8") as f:
            json.dump(scraped, f, indent=2, ensure_ascii=False)
        print("✅ Scraping complete. Results saved to reviews_output.json")
