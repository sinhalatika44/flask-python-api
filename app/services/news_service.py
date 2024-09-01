import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

class NewsService:
    def __init__(self):
        self.base_url = "https://newsapi.org/v2/top-headlines"
        self.api_key = "YOUR_NEWS_API_KEY"  # Replace with your actual API key

    def get_news(self, category=None):
        params = {
            "apiKey": self.api_key,
            "country": "in",  # Assuming Indian news
        }
        if category:
            params["category"] = category

        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            news_data = response.json()
            summarized_news = [self._summarize_article(article) for article in news_data["articles"][:5]]
            return summarized_news
        else:
            return {"error": "Failed to fetch news"}

    def _summarize_article(self, article):
        text = article["description"] or article["title"]
        summary = self._generate_summary(text)
        return {
            "title": article["title"],
            "summary": summary,
            "url": article["url"],
        }

    def _generate_summary(self, text, max_words=60):
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        word_frequencies = {}

        for word in words:
            if word not in stop_words:
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    if len(sentence.split()) < 30:
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = word_frequencies[word]
                        else:
                            sentence_scores[sentence] += word_frequencies[word]

        summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
        summary = ' '.join(summary_sentences[:2])
        
        words = summary.split()
        if len(words) > max_words:
            summary = ' '.join(words[:max_words]) + '...'

        return summary