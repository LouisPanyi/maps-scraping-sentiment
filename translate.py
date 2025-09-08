import pandas as pd
from deep_translator import GoogleTranslator

# 1. Baca file Excel
df = pd.read_excel("maps.xlsx")

# 2. Hapus kata 'bintang' dari kolom Rating
df['Rating'] = df['Rating'].str.replace('bintang', '', case=False).str.strip()

# 3. Terjemahkan kolom Review ke Bahasa Inggris
translated_reviews = []

for review in df['Review']:
    if isinstance(review, str):
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(review)
        except Exception as e:
            print("Terjemahan gagal:", e)
            translated = review
    else:
        translated = review
    translated_reviews.append(translated)

# 4. Tambahkan hasil ke kolom baru
df['Review_Translated'] = translated_reviews

# 5. Simpan ke file baru
df.to_excel("maps_translated.xlsx", index=False)

print("Selesai! File hasil: maps_translated.xlsx")
