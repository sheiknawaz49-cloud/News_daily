import os
from dotenv import load_dotenv
from news_client import NewsClient
from content_generator import ContentGenerator
from datetime import datetime

def main():
    # Load environment variables
    load_dotenv()
    
    news_api_key = os.getenv("NEWS_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not news_api_key or not gemini_api_key:
        print("Error: Missing API keys. Please check your .env file or environment variables.")
        return

    # 1. Fetch News
    print("Fetching news...")
    news_client = NewsClient(news_api_key)
    articles = news_client.get_top_headlines(country="in") # Defaulting to India as requested (IST context)
    
    if not articles:
        print("No news articles found.")
        return

    print(f"Found {len(articles)} articles. Generating script...")

    # 2. Generate Content
    generator = ContentGenerator(gemini_api_key)
    content = generator.generate_youtube_script(articles)

    # 3. Save Output
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"daily_news_script_{date_str}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Success! Script saved to {filename}")
    print("-" * 50)
    print(content)

if __name__ == "__main__":
    main()
