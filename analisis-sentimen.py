"""
Script 4: Analyze sentiment of translated reviews
Input: maps_translated.xlsx
Output: sentiment_results.csv, sentiment_distribution.png
"""

import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import opinion_lexicon
from nltk.tokenize import word_tokenize
import nltk

# ────────────── 0. Download NLTK resources (only needed once) ──────────────
# 'vader_lexicon' → for VADER sentiment analysis
# 'opinion_lexicon' → for Liu & Hu sentiment analysis
# 'punkt' → tokenizer for breaking sentences into words
nltk.download('vader_lexicon')
nltk.download('opinion_lexicon')
nltk.download('punkt')

# ────────────── Load translated reviews ──────────────
# Make sure the file "maps_translated.xlsx" exists and contains the column 'Review'
df = pd.read_excel("maps_translated.xlsx")

# ────────────── 1. Sentiment Analysis using VADER ──────────────
# VADER (Valence Aware Dictionary and sEntiment Reasoner) is good for social media & reviews
sia = SentimentIntensityAnalyzer()

# Compute compound sentiment score (-1 very negative, +1 very positive)
df['Sentiment_Score_VADER'] = df['Review'].astype(str).apply(lambda x: sia.polarity_scores(x)['compound'])

# Assign sentiment label based on threshold:
# ≥ 0.05 = Positive, ≤ -0.05 = Negative, otherwise Neutral
df['Sentiment_Label_VADER'] = df['Sentiment_Score_VADER'].apply(
    lambda x: 'Positive' if x >= 0.05 else ('Negative' if x <= -0.05 else 'Neutral')
)

# Save results with VADER analysis
df[['Nama', 'Rating', 'Waktu', 'Review', 'Sentiment_Score_VADER', 'Sentiment_Label_VADER']].to_excel("maps_sentimen_vader.xlsx", index=False)

# ────────────── 2. Sentiment Analysis using Liu & Hu Lexicon ──────────────
# Liu & Hu uses a predefined positive/negative word dictionary
positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

def liu_hu_sentiment(text):
    """
    Count how many words in the text are in the positive or negative word list.
    More positives → 'Positive', more negatives → 'Negative', otherwise 'Neutral'
    """
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

# Save results with Liu & Hu analysis
df[['Nama', 'Rating', 'Waktu', 'Review', 'Sentiment_Label_LiuHu']].to_excel("maps_sentimen_liuhu.xlsx", index=False)

# ────────────── 3. Visualization of VADER Sentiment Distribution ──────────────
# Create a pie chart of sentiment distribution (Positive, Negative, Neutral)
sentiment_counts = df['Sentiment_Label_VADER'].value_counts()
plt.figure(figsize=(6, 6))
colors = ['lightgreen', 'lightcoral', 'lightgray']  # positive, negative, neutral
sentiment_counts.plot.pie(autopct='%1.1f%%', colors=colors, startangle=90, ylabel='')
plt.title('Sentiment Distribution of Reviews (VADER)')
plt.tight_layout()
plt.savefig("sentimen_vader_pie.png")
plt.show()

# ────────────── 4. Output summary ──────────────
print("✅ Sentiment analysis completed. Results saved:")
print("- maps_sentimen_vader.xlsx")
print("- maps_sentimen_liuhu.xlsx")
print("- Pie chart: sentimen_vader_pie.png")
