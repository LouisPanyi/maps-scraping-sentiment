"""
Script 3: Translate reviews into English using GoogleTranslator
Input: maps.xlsx
Output: maps_translated.xlsx
"""

import pandas as pd
from deep_translator import GoogleTranslator

# ────────────── Step 1: Load scraped reviews ──────────────
df = pd.read_excel("maps.xlsx")

# ────────────── Step 2: Clean Rating column ──────────────
df['Rating'] = df['Rating'].str.replace('bintang', '', case=False).str.strip()

# ────────────── Step 3: Translate each review ──────────────
translated_reviews = []
for review in df['Review']:
    if isinstance(review, str):
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(review)
        except Exception as e:
            print("⚠️ Translation failed:", e)
            translated = review
    else:
        translated = review
    translated_reviews.append(translated)

# ────────────── Step 4: Save translated reviews ──────────────
df['Review_Translated'] = translated_reviews
df.to_excel("maps_translated.xlsx", index=False)

print("✅ Translation completed. Output file: maps_translated.xlsx")
