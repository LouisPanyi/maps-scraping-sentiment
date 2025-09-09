# 📌 Maps Scraping & Sentiment Analysis

This project is designed to **scrape Google Maps reviews** using Selenium, then **visualize**, **translate**, and **analyze sentiments** from the collected data.  

The workflow is divided into four main Python scripts, each handling a specific stage of the process.

---

## 🔧 Project Workflow

### 1️⃣ `maps-scrapping.py`
- Scrapes Google Maps reviews (name, rating, time, and review text).
- Saves the results into an Excel file: **`maps.xlsx`**.

### 2️⃣ `maps-visualisation.py`
- Reads the `maps.xlsx` file.
- Generates:
  - 📊 Bar chart for rating distribution.
  - ☁️ Word cloud of frequently used words.  
- Helps understand review trends and keywords.

### 3️⃣ `translate.py`
- Translates all reviews into **English**.
- Cleans the Rating column by removing the word *"bintang"* (star).
- Produces a new file: **`maps_translated.xlsx`**.

### 4️⃣ `analisis-sentimen.py`
- Performs sentiment analysis on the translated reviews (`maps_translated.xlsx`).
- Uses two sentiment analysis methods:
  - VADER (Valence Aware Dictionary for Sentiment Reasoning).
  - LiuHu Opinion Lexicon.
- Outputs:
  - Sentiment distribution summary.
  - Pie chart visualization of sentiment.
  - Excel files with sentiment results: **`maps_sentimen_vader.xlsx`**, **`maps_sentimen_liuhu.xlsx`**.

---

## 🛠️ Requirements

- Python **3.9+**
- Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📂 File Structure
- maps-scrapping.py          # Script 1: Scrape reviews from Google Maps
- maps-visualisation.py      # Script 2: Visualize ratings & word cloud
- translate.py               # Script 3: Translate reviews to English
- analisis-sentimen.py       # Script 4: Sentiment analysis (VADER & LiuHu)
- maps.xlsx                  # Output of script 1 (raw reviews)
- maps_translated.xlsx       # Output of script 3 (translated reviews)
- requirements.txt           # Python dependencies
- README.md                  # Project documentation

---

## 🚀 How to Run
1. Clone repository (or download project):
```bash
git clone https://github.com/your-username/maps-scraping-sentiment.git
cd maps-scraping-sentiment
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run NLTK Setup
```bash
python setup_nltk.py
```

4. Set environment variables (create .env file):
```bash
MAPS_URL=https://maps.google.com
SEARCH_QUERY=name your place
```

5. Run the workflow step by step:
```bash
# Scrape reviews
python maps-scrapping.py

# Generate visualization
python maps-visualisation.py

# Translate reviews
python translate.py

# Run sentiment analysis
python analisis-sentimen.py
```

---

## 📊 Example Outputs
- maps.xlsx → Raw scraped reviews
- grafik_rating.png → Bar chart of rating distribution
- wordcloud_review.png → Word cloud of keywords in reviews
- maps_translated.xlsx → Reviews translated into English
- maps_sentimen_vader.xlsx, maps_sentimen_liuhu.xlsx → Sentiment analysis results

---

## 📝 Notes
- Selenium requires ChromeDriver installed and compatible with your Chrome version.
- For translation, internet connection is required (Google Translate API).
- Sentiment analysis works best on English text, hence translation step is important.

---

## 📌 Future Improvements
- Add more robust error handling during scraping.
- Extend sentiment analysis with machine learning models (e.g., BERT).
- Build a dashboard to visualize results interactively (e.g., with Streamlit).
