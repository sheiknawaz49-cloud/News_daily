import os
from dotenv import load_dotenv
from news_client import NewsClient
from content_generator import ContentGenerator

def test_tech_news():
    load_dotenv()
    
    news_api_key = os.getenv("NEWS_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not news_api_key or not gemini_api_key:
        print("Error: Missing API keys.")
        return

    print("Fetching TECHNOLOGY news (India)...")
    client = NewsClient(news_api_key)
    # Fetching technology news for India
    articles = client.get_top_headlines(category="technology", country="in")
    
    if not articles:
        print("No articles found for India. Trying US...")
        articles = client.get_top_headlines(category="technology", country="us")

    if not articles:
        print("No articles found for US either. Check API key or quota.")
        # Debug: try fetching without category
        print("Trying without category (India)...")
        articles = client.get_top_headlines(country="in")
        if not articles:
             print("Still no articles. Something is wrong.")
             return

    print(f"Found {len(articles)} articles. Generating script...")
    
    # Generate script for just the top 1 article for a quick test
    generator = ContentGenerator(gemini_api_key)
    # We pass a list containing just the first article to test "one news"
    print("Calling Gemini API...")
    try:
        script = generator.generate_youtube_script(articles[:1])
        print("Gemini API returned.")
    except Exception as e:
        print(f"Gemini API call failed in test script: {e}")
        script = "FAILED"
    
    print("\n--- GENERATED SCRIPT (START) ---\n")
    print(repr(script))
    print("\n--- GENERATED SCRIPT (END) ---\n")
    
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(str(script))
    print("Result written to result.txt")

if __name__ == "__main__":
    test_tech_news()
