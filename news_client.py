import requests
import os
from datetime import datetime

class NewsClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/top-headlines"

    def get_top_headlines(self, country="in", category="general"):
        """
        Fetches top headlines for a specific country and category.
        Defaults to India (in) and general category.
        """
        params = {
            "country": country,
            "category": category,
            "apiKey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "ok":
                return data["articles"]
            else:
                print(f"Error fetching news: {data.get('message', 'Unknown error')}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching news: {e}")
            return []

if __name__ == "__main__":
    # Simple test
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("NEWS_API_KEY")
    if api_key:
        client = NewsClient(api_key)
        articles = client.get_top_headlines()
        print(f"Fetched {len(articles)} articles.")
        for i, article in enumerate(articles[:3]):
            print(f"{i+1}. {article['title']}")
    else:
        print("NEWS_API_KEY not found in environment.")
