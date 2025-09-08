import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# Baca file hasil scraping
df = pd.read_excel("maps.xlsx")

# ────────────── 1. Analisis Rating ──────────────
df['Rating'] = df['Rating'].str.extract(r'(\d(?:[.,]\d)?)')[0].str.replace(',', '.').astype(float)
rating_counts = df['Rating'].value_counts().sort_index()

# Plot grafik batang distribusi rating
plt.figure(figsize=(8, 5))
plt.bar(rating_counts.index, rating_counts.values, color='skyblue')
plt.xlabel('Rating Bintang')
plt.ylabel('Jumlah Review')
plt.title('Distribusi Rating Review')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("grafik_rating.png")
plt.show()

# ────────────── 2. Word Cloud ──────────────
stopwords = set(STOPWORDS)
stopwords.update({'makanan', 'tempat', 'makan', 'aja', 'banget', 'udah', 'nya', 'sih', 'di', 'ke', 'yg', 'dan', 'yang', 'dengan'})

text = ' '.join(df['Review'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white',
                      stopwords=stopwords, collocations=False).generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
plt.savefig("wordcloud_review.png")
plt.show()

print("✅ Visualisasi selesai. Hasil tersimpan:")
print("- Grafik rating: grafik_rating.png")
print("- Word cloud: wordcloud_review.png")
