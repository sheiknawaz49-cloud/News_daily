import os
from dotenv import load_dotenv
from news_client import NewsClient
from content_generator import ContentGenerator
from datetime import datetime

def main():
    # Load environment variables
    load_dotenv()
    
    news_api_key = os.getenv("NEWS_API_KEY") # Still needed for NewsClient init, though not used for HN
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        print("Error: Missing GEMINI_API_KEY. Please check your .env file or environment variables.")
        return

    # 1. Fetch AI News from Hacker News
    print("Fetching AI news from Hacker News...")
    # Initialize NewsClient (API key is optional for HN but required for the class init)
    news_client = NewsClient(news_api_key if news_api_key else "dummy_key")
    ai_articles = news_client.get_ai_news(limit=10) # Fetch more to let Gemini pick the best 5
    
    if not ai_articles:
        print("No AI news articles found.")
        return

    print(f"Found {len(ai_articles)} AI articles. Generating script...")

    # 2. Generate Content
    generator = ContentGenerator(gemini_api_key)
    content = generator.generate_ai_summary(ai_articles)

    # 3. Save Output
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"daily_ai_script_{date_str}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Success! AI Script saved to {filename}")
    print("-" * 50)
    print(content)

if __name__ == "__main__":
    main()
