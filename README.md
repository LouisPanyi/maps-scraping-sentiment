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
  - Bar chart for rating distribution.  
  - Word cloud of frequently used words.  
- Helps understand review trends and keywords.  

### 3️⃣ `translate.py`
- Translates all reviews into **English**.  
- Cleans the `Rating` column by removing the word *"bintang"* (star).  
- Produces a new file: **`maps_translated.xlsx`**.  

### 4️⃣ `analisis-sentimen.py`
- Performs sentiment analysis on the translated reviews (`maps_translated.xlsx`).  
- Uses **two sentiment analysis methods**:  
  - **VADER** (Valence Aware Dictionary for Sentiment Reasoning).  
  - **LiuHu Opinion Lexicon**.  
- Outputs:  
  - Sentiment distribution summary.  
  - Pie chart visualization of sentiment.  
  - Excel files with sentiment results:  
    - `maps_sentimen_vader.xlsx`  
    - `maps_sentimen_liuhu.xlsx`  

---

## 🛠️ Requirements

Make sure you have Python 3.9+ installed.  

Install dependencies with:

```bash
pip install -r requirements.txt
```bash
pip install -r requirements.txt
