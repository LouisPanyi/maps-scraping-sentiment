import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import opinion_lexicon
from nltk.tokenize import word_tokenize
import nltk

# Download resource sekali saja (kalau belum ada)
nltk.download('vader_lexicon')
nltk.download('opinion_lexicon')
nltk.download('punkt')

# Baca file review yang sudah diterjemahkan
df = pd.read_excel("maps_translated.xlsx")

# ────────────── 1. Analisis Sentimen VADER ──────────────
sia = SentimentIntensityAnalyzer()
df['Sentiment_Score_VADER'] = df['Review'].astype(str).apply(lambda x: sia.polarity_scores(x)['compound'])
df['Sentiment_Label_VADER'] = df['Sentiment_Score_VADER'].apply(
    lambda x: 'Positive' if x >= 0.05 else ('Negative' if x <= -0.05 else 'Neutral')
)

# Simpan hasil VADER
df[['Nama', 'Rating', 'Waktu', 'Review', 'Sentiment_Score_VADER', 'Sentiment_Label_VADER']].to_excel("maps_sentimen_vader.xlsx", index=False)

# ────────────── 2. Analisis Sentimen Liu & Hu ──────────────
positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

def liu_hu_sentiment(text):
    words = word_tokenize(text.lower())
    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)

    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"

df['Sentiment_Label_LiuHu'] = df['Review'].astype(str).apply(liu_hu_sentiment)

# Simpan hasil Liu & Hu
df[['Nama', 'Rating', 'Waktu', 'Review', 'Sentiment_Label_LiuHu']].to_excel("maps_sentimen_liuhu.xlsx", index=False)

# ────────────── 3. Visualisasi Distribusi Sentimen (VADER) ──────────────
sentiment_counts = df['Sentiment_Label_VADER'].value_counts()
plt.figure(figsize=(6, 6))
colors = ['lightgreen', 'lightcoral', 'lightgray']
sentiment_counts.plot.pie(autopct='%1.1f%%', colors=colors, startangle=90, ylabel='')
plt.title('Distribusi Sentimen Review (VADER)')
plt.tight_layout()
plt.savefig("sentimen_vader_pie.png")
plt.show()

print("✅ Analisis sentimen selesai. Hasil tersimpan:")
print("- maps_sentimen_vader.xlsx")
print("- maps_sentimen_liuhu.xlsx")
print("- Pie chart: sentimen_vader_pie.png")
