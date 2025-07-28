import json
import time
import logging
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

logging.basicConfig(level=logging.INFO)

DOMO_WEBHOOK = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

properties = [
    "The Waters at Settlers Trace", "The Waters at Redstone", "The Waters at Millerville",
    "The Waters at McGowin", "The Waters at Freeport", "The Waters at Crestview",
    "The Waters at Bluebonnet", "The Heights at Picardy", "The Flats at East Bay",
    "The Waters at West Village", "The Flats at Ransley", "The Waters at Ransley",
    "The Waters at Heritage", "The Waters at Hammond"
]

def get_reviews(prop_name: str, max_reviews: int = 5) -> list[dict]:
    """Scrape reviews from Google Maps for a given property name."""
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options)
    try:
        driver.get("https://www.google.com/maps")

        # Wait for the search box and search for the property
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.clear()
        search_box.send_keys(prop_name)
        search_box.send_keys(Keys.ENTER)

        # Wait for the side panel to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='complementary']"))
        )

        # Try clicking the reviews button
        review_clicked = False
        try:
            review_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(translate(@aria-label,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'review')]")
                )
            )
            review_button.click()
            review_clicked = True
        except Exception:
            try:
                alt_span = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'reviews')]")
                    )
                )
                alt_button = alt_span.find_element(By.XPATH, "ancestor::button")
                alt_button.click()
                review_clicked = True
            except Exception:
                review_clicked = False

        if not review_clicked:
            logging.warning(f"No reviews button found for {prop_name}.")
            return []

        # Scroll reviews container to load more reviews
        try:
            scrollable = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
        except Exception:
            try:
                scrollable = driver.find_element(By.CSS_SELECTOR, "div.m6QErb.DxyBCb")
            except Exception:
                scrollable = None

        if scrollable:
            for _ in range(10):
                if len(driver.find_elements(By.CSS_SELECTOR, "div.jftiEf")) >= max_reviews:
                    break
                driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable
                )
                time.sleep(2)

        # Collect reviews
        reviews = []
        review_cards = driver.find_elements(By.CSS_SELECTOR, "div.jftiEf")
        if not review_cards:
            review_cards = driver.find_elements(By.CSS_SELECTOR, "div.gws-localreviews__google-review")

        for el in review_cards[:max_reviews]:
            try:
                author = el.find_element(By.CSS_SELECTOR, "span.d4r55").text
            except Exception:
                try:
                    author = el.find_element(By.CSS_SELECTOR, "a[href*='maps/contrib']").text
                except Exception:
                    author = "Unknown"
            try:
                rating_attr = el.find_element(By.CSS_SELECTOR, "span.kvMYJc").get_attribute("aria-label")
                rating = float(rating_attr.split(" ")[0]) if rating_attr else 0.0
            except Exception:
                rating = 0.0
            try:
                text = el.find_element(By.CSS_SELECTOR, "span.wiI7pd").text
            except Exception:
                try:
                    text = el.find_element(By.CSS_SELECTOR, "span[jsname='fbQN7e']").text
                except Exception:
                    text = ""
            reviews.append({
                "property": prop_name,
                "author": author,
                "rating": rating,
                "text": text,
            })
        return reviews
    finally:
        try:
            driver.quit()
        except Exception:
            pass


def run_all():
    all_reviews = []
    for prop in properties:
        logging.info(f"Scraping {prop}")
        reviews = get_reviews(prop)
        all_reviews.extend(reviews)

    if all_reviews:
        payload = '\n'.join(json.dumps(r) for r in all_reviews)
        res = requests.post(DOMO_WEBHOOK, data=payload.encode('utf-8'), headers={'Content-Type': 'application/json'})
        logging.info(f"✅ Sent {len(all_reviews)} reviews to Domo | Status: {res.status_code}")
    else:
        logging.error("❌ No reviews found or all failed.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run scraper once")
    args = parser.parse_args()

    if args.once:
        run_all()
