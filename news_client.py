import http.client
import json
import urllib.parse
import os

class NewsClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.host = "newsapi.org"

    def get_top_headlines(self, country="us", category="technology"):
        """
        Fetches top headlines for a specific country and category.
        Defaults to US technology news (India news currently returns 0 results).
        """
        try:
            conn = http.client.HTTPSConnection(self.host)
            params = urllib.parse.urlencode({
                "country": country,
                "category": category,
                "apiKey": self.api_key
            })
            headers = {
                "User-Agent": "Python-News-Bot/1.0"
            }
            url = f"/v2/top-headlines?{params}"
            
            conn.request("GET", url, headers=headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            
            if response.status != 200:
                print(f"Error: HTTP {response.status}")
                print(f"Body: {data}")
                return []

            json_data = json.loads(data)
            
            if json_data.get("status") == "ok":
                articles = json_data.get("articles", [])
                return articles
            else:
                print(f"Error from API: {json_data.get('message')}")
                return []

        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def get_ai_news(self, limit=5):
        """
        Fetches the latest 5 AI-related stories from Hacker News using Algolia API.
        """
        try:
            conn = http.client.HTTPSConnection("hn.algolia.com")
            # Search for "AI" in the last 24 hours (approx), sorted by date
            # Using a simple query "AI" and tags="story"
            params = urllib.parse.urlencode({
                "query": "AI",
                "tags": "story",
                "hitsPerPage": limit
            })
            url = f"/api/v1/search_by_date?{params}"
            
            conn.request("GET", url)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            
            if response.status != 200:
                print(f"Error fetching AI news: HTTP {response.status}")
                return []

            json_data = json.loads(data)
            hits = json_data.get("hits", [])
            
            ai_articles = []
            for hit in hits:
                ai_articles.append({
                    "title": hit.get("title"),
                    "description": hit.get("url", "No URL provided"), # HN stories often just have a URL
                    "source": "Hacker News"
                })
            
            return ai_articles

        except Exception as e:
            print(f"Error fetching AI news: {e}")
            return []

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("NEWS_API_KEY")
    if api_key:
        client = NewsClient(api_key)
        articles = client.get_top_headlines()
        print(f"Fetched {len(articles)} articles.")
