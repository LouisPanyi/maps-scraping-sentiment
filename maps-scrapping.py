"""
Script 1: Scrape Google Maps reviews and save to Excel
Output: maps.xlsx
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from openpyxl import Workbook

# ────────────── Load environment variables ──────────────
# Example .env:
# MAPS_URL=https://maps.google.com
# SEARCH_QUERY=Warung Oyako Jogja
load_dotenv()
maps_url = os.getenv("MAPS_URL")
search_query = os.getenv("SEARCH_QUERY")

driver = webdriver.Chrome()
driver.get(maps_url)
time.sleep(5)

# ────────────── Step 1: Enter query into search box ──────────────
try:
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="searchboxinput"]'))
    )
    search_box.clear()
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)
    print(f"✅ Query '{search_query}' entered successfully")
except Exception as e:
    print("❌ Failed to input search query:", e)
    driver.quit()
    exit()

time.sleep(5)

# ────────────── Step 2: Click the first search result (if available) ──────────────
try:
    first_result = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '(//a[contains(@class, "hfpxzc")])[1]'))
    )
    driver.execute_script("arguments[0].click();", first_result)
    print("✅ First search result clicked")
except Exception:
    # If no list appears, Google Maps may directly open the business page
    print("ℹ️ No result list found, continuing directly to business page")

time.sleep(5)

# ────────────── Step 3: Click the "Reviews" tab ──────────────
try:
    ulasan_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]'))
    )
    ulasan_tab.click()
    print("✅ Reviews tab opened")
except Exception as e:
    print("❌ Failed to open Reviews tab:", e)
    driver.quit()
    exit()

time.sleep(5)

# ────────────── Step 4: Scroll through reviews ──────────────
scrollable_xpath = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
scrollable_div = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, scrollable_xpath))
)

last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
while True:
    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)
    time.sleep(2)
    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
    if new_height == last_height:
        break
    last_height = new_height

# ────────────── Step 5: Extract reviews ──────────────
reviews = scrollable_div.find_elements(By.CLASS_NAME, "jftiEf")
print(f"📌 Total reviews found: {len(reviews)}")

collected_reviews = []
for idx, review in enumerate(reviews):
    try:
        # Expand full text if "More" button exists
        try:
            more_button = review.find_element(By.XPATH, './/button[contains(@aria-label, "Lainnya")]')
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(0.5)
        except NoSuchElementException:
            pass

        # Extract review details
        name = review.find_element(By.CLASS_NAME, 'd4r55').text
        stars = review.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute("aria-label")
        date = review.find_element(By.CLASS_NAME, 'rsqaWe').text
        text = review.find_element(By.XPATH, './/span[@class="wiI7pd"]').text

        collected_reviews.append({
            "Name": name,
            "Rating": stars,
            "Date": date,
            "Review": text
        })
    except Exception as e:
        print(f"⚠️ Error while scraping review #{idx+1}: {e}")

# ────────────── Step 6: Save to Excel ──────────────
wb = Workbook()
ws = wb.active
ws.title = "Google Maps Reviews"
ws.append(["Name", "Rating", "Date", "Review"])

for r in collected_reviews:
    ws.append([r["Name"], r["Rating"], r["Date"], r["Review"]])

wb.save("maps.xlsx")
print("✅ Reviews successfully saved to maps.xlsx")
