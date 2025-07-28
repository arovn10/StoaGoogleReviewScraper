import time
import json
import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Define properties and URLs
properties = {
    "The Waters at Settlers Trace": "https://www.google.com/maps?sca_esv=63099446d56d4ef8&output=search&q=The+Waters+at+Settlers+Trace&source=lnms&entry=mc",
    "The Waters at Redstone": "https://www.google.com/maps/place/The+Waters+at+Redstone/@30.7362861,-86.5595057,978m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8891731ed5ef4421:0xe82971b01b043e0e!8m2!3d30.7362861!4d-86.5569308",
    "The Waters at Millerville": "https://www.google.com/maps/place/The+Waters+at+Millerville/@30.4397504,-91.0289876,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626bd7f2db7ca89:0x1d15edca3d614c78!8m2!3d30.4397504!4d-91.0264127",
    "The Waters at McGowin": "https://www.google.com/maps/place/The+Waters+at+McGowin/@30.6516886,-88.1154892,979m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a4db406a47bd1:0xa0adc97698cb8809!8m2!3d30.6516886!4d-88.1129143",
    "The Waters at Freeport": "https://www.google.com/maps/place/The+Waters+at+Freeport/@30.486358,-86.1287459,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8893dda15e2f9069:0x3177e609fc299d13!8m2!3d30.486358!4d-86.126171",
    "The Waters at Crestview": "https://www.google.com/maps/place/The+Waters+at+Crestview/@30.7327129,-86.5707133,1957m/data=!3m1!1e3",
    "The Waters at Bluebonnet": "https://www.google.com/maps/place/The+Waters+at+Bluebonnet/@30.4147242,-91.0766963,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626a53bc0c94fbf:0x84b7af1708cc8d8d!8m2!3d30.4147242!4d-91.0741214",
    "The Heights at Picardy": "https://www.google.com/maps/place/The+Heights+at+Picardy/@30.3941704,-91.1028869,982m/data=!3m2!1e3!4b1!4m6!3m5!1s0x8626a56f7f0dc5bf:0xb38345b83bdc892b!8m2!3d30.3941704!4d-91.100312",
    "The Flats at East Bay": "https://www.google.com/maps/place/The+Flats+at+East+Bay/@30.5014556,-87.8652493,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x889a3f60ad1dd52d:0x332da4c4b0b0c51e!8m2!3d30.5014556!4d-87.8626744",
    "The Waters at West Village": "https://www.google.com/maps/place/The+Waters+at+West+Village/@30.2214016,-92.097974,983m/data=!3m2!1e3!4b1!4m6!3m5!1s0x86249fc349920de9:0x7945e14be23642b4!8m2!3d30.2214016!4d-92.0953991",
    "The Waters at Hammond": "https://www.google.com/maps/place/The+Waters+at+Hammond/@30.4877443,-90.465321,981m/data=!3m2!1e3!4b1!4m6!3m5!1s0x862723fbcc2afb85:0x188d3eeca51192d0!8m2!3d30.4877443!4d-90.4627461"
}

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

def accept_gdpr(driver):
    if 'consent.google.com' in driver.current_url:
        driver.execute_script("document.getElementsByTagName('form')[0].submit()")

def wait_for_page(driver):
    while driver.execute_script('return document.readyState') != 'complete':
        time.sleep(1)

def scroll_reviews(driver):
    try:
        scrollable = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "DxyBCb") and contains(@class, "m6QErb")]'))
        )
        for _ in range(8):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable)
            time.sleep(2)
    except Exception as e:
        print(f"Scroll error: {e}")

def extract_reviews(driver):
    reviews = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-review-id]'))
        )
        cards = driver.find_elements(By.XPATH, '//div[@data-review-id]')
        for card in cards:
            try:
                name = card.find_element(By.CLASS_NAME, 'd4r55').text
            except:
                name = "Unknown"
            try:
                rating = card.find_element(By.XPATH, './/span[contains(@aria-label,"stars")]').get_attribute("aria-label").split(" ")[0]
            except:
                rating = "-"
            try:
                text = card.find_element(By.CLASS_NAME, 'wiI7pd').text
            except:
                text = ""
            reviews.append((name, rating, text))
    except Exception as e:
        print(f"Extract error: {e}")
    return reviews


def send_to_domo(property_name, reviews):
    for name, rating, text in reviews:
        payload = {
            "Property": property_name,
            "Reviewer": name,
            "Rating": rating,
            "Comment": text
        }
        try:
            requests.post(domo_webhook, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        except Exception as e:
            print(f"Error sending to Domo: {e}")

def run_scraper():
    print("Starting Google Review Scraper...")
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--lang=en-US")
    options.add_experimental_option("prefs", {"intl.accept_languages": "en,en_US"})

    driver = webdriver.Chrome(options=options)

    for name, url in properties.items():
        print(f"Processing: {name}")
        try:
            driver.get(url)
            wait_for_page(driver)
            accept_gdpr(driver)
            scroll_reviews(driver)
            reviews = extract_reviews(driver)
            send_to_domo(name, reviews)
            print(f"✓ {len(reviews)} reviews sent for {name}")
        except Exception as e:
            print(f"Error scraping {name}: {e}")
        time.sleep(2)

    driver.quit()
    print("Done!")

if __name__ == "__main__":
    run_scraper()
