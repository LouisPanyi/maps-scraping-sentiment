"""
Script 2: Visualize ratings and generate a word cloud
Input: maps.xlsx
Output: grafik_rating.png, wordcloud_review.png
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# ────────────── Load scraped reviews ──────────────
df = pd.read_excel("maps.xlsx")

# ────────────── 1. Rating Distribution ──────────────
# Extract numeric rating (e.g. "5 bintang" → 5)
df['Rating'] = df['Rating'].str.extract(r'(\d(?:[.,]\d)?)')[0].str.replace(',', '.').astype(float)
rating_counts = df['Rating'].value_counts().sort_index()

# Plot rating distribution
plt.figure(figsize=(8, 5))
plt.bar(rating_counts.index, rating_counts.values, color='skyblue')
plt.xlabel('Star Rating')
plt.ylabel('Number of Reviews')
plt.title('Distribution of Star Ratings')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("grafik_rating.png")
plt.show()

# ────────────── 2. Word Cloud from Reviews ──────────────
stopwords = set(STOPWORDS)
stopwords.update({'makanan', 'tempat', 'makan', 'aja', 'banget', 'udah',
                  'nya', 'sih', 'di', 'ke', 'yg', 'dan', 'yang', 'dengan'})

text = ' '.join(df['Review'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white',
                      stopwords=stopwords, collocations=False).generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig("wordcloud_review.png")
plt.show()

print("✅ Visualization completed. Results saved:")
print("- Rating chart: grafik_rating.png")
print("- Word cloud: wordcloud_review.png")
