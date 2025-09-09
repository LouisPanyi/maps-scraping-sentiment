import nltk

def setup_nltk():
    print("📥 Downloading NLTK resources...")
    nltk.download('vader_lexicon')
    nltk.download('opinion_lexicon')
    nltk.download('punkt')
    print("✅ NLTK setup complete!")

if __name__ == "__main__":
    setup_nltk()
