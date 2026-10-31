from textblob import TextBlob

def analyze_sentiment(news_headlines):
    """
    Analyzes headlines/telemetry text and returns a sentiment score (0 to 100)
    along with a finely tuned market mood label.
    """
    if not news_headlines:
        return {"score": 50.0, "mood": "Neutral ⚖️"}
        
    scores = []
    for headline in news_headlines:
        analysis = TextBlob(headline)
        polarity = analysis.sentiment.polarity
        scores.append(polarity)
        
    avg_polarity = sum(scores) / len(scores)
    sentiment_score = round(((avg_polarity + 1) / 2) * 100, 2)
    
    # Fine-tuned & more sensitive mood categorization thresholds
    if sentiment_score >= 55:
        mood = "Bullish 🚀"
    elif sentiment_score <= 45:
        mood = "Bearish 📉"
    else:
        mood = "Neutral ⚖️"
        
    return {
        "score": sentiment_score,
        "mood": mood
    }

# Quick test if run directly
if __name__ == "__main__":
    sample_news = ["Strong momentum observed with positive volume."]
    print(analyze_sentiment(sample_news))