# digunakan untuk scrapping review google maps dan di jadikan dalam bentuk excel
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
from openpyxl import Workbook

# load variabel dari .env
load_dotenv()

# ambil url dari env
maps_url = os.getenv("MAPS_URL")

driver = webdriver.Chrome()
driver.get(maps_url)
time.sleep(5)

# Klik tab ulasan dengan XPATH yang spesifik
try:
    ulasan_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[3]'))
    )
    ulasan_tab.click()
    print("✅ Tab Ulasan berhasil diklik")
except Exception as e:
    print("❌ Gagal klik tab ulasan:", e)
    driver.quit()
    exit()

time.sleep(5)

# Scroll area ulasan
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

# Ambil semua review
reviews = scrollable_div.find_elements(By.CLASS_NAME, "jftiEf")
print(f"📌 Jumlah review ditemukan: {len(reviews)}")

kumpulan_review = []

for idx, review in enumerate(reviews):
    try:
        # Klik tombol "Lainnya" hanya jika ada untuk expand teks
        try:
            more_button = review.find_element(By.XPATH, './/button[contains(@aria-label, "Lainnya")]')
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(0.5)
        except NoSuchElementException:
            pass

        # Ambil data review
        nama = review.find_element(By.CLASS_NAME, 'd4r55').text
        bintang = review.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute("aria-label")
        waktu = review.find_element(By.CLASS_NAME, 'rsqaWe').text
        isi = review.find_element(By.XPATH, './/span[@class="wiI7pd"]').text

        kumpulan_review.append({
            "Nama": nama,
            "Rating": bintang,
            "Waktu": waktu,
            "Review": isi
        })

    except Exception as e:
        print(f"⚠️ Error saat mengambil review ke-{idx+1}: {e}")

# Simpan ke Excel
wb = Workbook()
ws = wb.active
ws.title = "Ulasan Google Maps"
ws.append(["Nama", "Rating", "Waktu", "Review"])  # Header

for r in kumpulan_review:
    ws.append([r["Nama"], r["Rating"], r["Waktu"], r["Review"]])

wb.save("maps.xlsx")
print("✅ Ulasan berhasil disimpan ke maps.xlsx")
