import requests
import os
from dotenv import load_dotenv
import json
try:
    import google.generativeai as genai
    print("Imported google.generativeai")
except ImportError:
    print("Could not import google.generativeai")

load_dotenv()

api_key = os.getenv("NEWS_API_KEY")
if not api_key:
    print("Error: NEWS_API_KEY not found in .env")
    exit(1)

print(f"Using API Key: {api_key[:4]}...{api_key[-4:]}")

url = "https://newsapi.org/v2/top-headlines"
combinations = [
    {"country": "in", "category": "technology"},
    {"country": "in", "category": "general"},
    {"country": "us", "category": "technology"},
]

for params in combinations:
    params["apiKey"] = api_key
    print(f"\nTesting: {params['country']} - {params['category']}")
    if params['category'] == 'general' and params['country'] == 'in':
        with open("final_debug_ref.txt", "w", encoding="utf-8") as f:
            f.write(f"URL: {url}?{urllib.parse.urlencode(params)}\n")
            f.write(f"Params: {params}\n")
            f.write(f"API Key: {api_key}\n")

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("status") == "ok":
            articles = data.get("articles", [])
            print(f"Found {data.get('totalResults')} total results")
            print(f"Actual articles returned: {len(articles)}")
            if len(articles) > 0:
                print(f"First article: {articles[0]['title']}")
            else:
                print("WARNING: No articles returned despite totalResults > 0")
        else:
            print(f"Error: {data.get('message')}")
    except Exception as e:
        print(f"Request failed: {e}")
