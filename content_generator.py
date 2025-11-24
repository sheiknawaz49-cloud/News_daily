import google.generativeai as genai
import os

class ContentGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_youtube_script(self, articles):
        """
        Generates a YouTube script, title, description, and hashtags based on news articles.
        """
        if not articles:
            return "No articles provided to generate script."

        # Prepare the context from articles
        news_summary = ""
        for i, article in enumerate(articles[:5]): # Limit to top 5 stories to keep it concise
            title = article.get('title', 'No Title')
            description = article.get('description', 'No Description')
            news_summary += f"{i+1}. {title}: {description}\n"

        prompt = f"""
        You are a professional YouTube content creator. 
        Create a script for a daily news update video based on the following top headlines:

        {news_summary}

        Please provide the output in the following format:

        # TITLE
        [Catchy YouTube Video Title]

        # DESCRIPTION
        [Video Description including a brief summary of the news covered]

        # HASHTAGS
        [5-10 relevant hashtags]

        # SCRIPT
        [Intro]
        ...
        [Body - covering each news item with smooth transitions]
        ...
        [Outro]
        ...
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {e}"

if __name__ == "__main__":
    # Simple test
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        # Mock articles for testing
        mock_articles = [
            {"title": "Tech Giant Releases New AI Model", "description": "A major tech company has unveiled a revolutionary AI model today."},
            {"title": "Global Stock Markets Rally", "description": "Markets hit record highs as inflation data comes in lower than expected."}
        ]
        generator = ContentGenerator(api_key)
        script = generator.generate_youtube_script(mock_articles)
        print(script)
    else:
        print("GEMINI_API_KEY not found in environment.")
