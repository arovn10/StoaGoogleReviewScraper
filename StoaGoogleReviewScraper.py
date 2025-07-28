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

def get_reviews(prop_name, max_reviews=5):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options)
    driver.get("https://www.google.com/maps")
    time.sleep(2)

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(prop_name)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    try:
        # Wait for the panel to load
        panel = driver.find_element(By.CLASS_NAME, "m6QErb")
        review_buttons = panel.find_elements(By.TAG_NAME, "button")
        for btn in review_buttons:
            if "review" in btn.get_attribute("aria-label").lower():
                btn.click()
                time.sleep(3)
                break
    except Exception as e:
        logging.warning(f"No reviews section found for {prop_name}: {e}")
        driver.quit()
        return []

    reviews = []
    review_cards = driver.find_elements(By.CLASS_NAME, "jftiEf")[:max_reviews]
    for el in review_cards:
        try:
            author = el.find_element(By.CLASS_NAME, "d4r55").text
            rating = float(el.find_element(By.CLASS_NAME, "kvMYJc").get_attribute("aria-label").split(" ")[0])
            text = el.find_element(By.CLASS_NAME, "wiI7pd").text
            reviews.append({
                "property": prop_name,
                "author": author,
                "rating": rating,
                "text": text
            })
        except Exception:
            continue

    
    driver.quit()
    return reviews

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
