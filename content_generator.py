import google.generativeai as genai
import os

class ContentGenerator:
    def __init__(self, api_key=None):
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    def generate_news_summary(self, articles):
        """
        Generates a structured summary of top 5 news items (Title, Description, Hashtags).
        Prioritizes Technology and AI.
        """
        if not articles:
            return "No articles provided to generate summary."
            
        try:
            if not self.model:
                raise Exception("Gemini API key not configured")

            # Prepare the context from articles
            news_context = ""
            for i, article in enumerate(articles): 
                title = article.get('title', 'No Title')
                description = article.get('description', 'No Description')
                news_context += f"Article {i+1}: {title} - {description}\n"

            prompt = f"""
            You are a tech news curator. 
            From the following list of articles, select the top 5 most relevant and interesting stories, strictly prioritizing Artificial Intelligence (AI) and Technology.

            Input Articles:
            {news_context}

            Output Format:
            Please provide exactly 5 news items in the following format:

            News 1:

            # TITLE
            [Concise and Catchy Title]

            # DESCRIPTION
            [2-3 sentences summarizing the key points]

            # HASHTAGS
            [3-5 relevant hashtags]

            News 2:
            ...
            
            News 5:
            ...
            """

            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating AI summary (likely rate limit or missing key): {e}")
            print("Falling back to simple headline summary...")
            return self.generate_simple_tech_summary(articles)

    def generate_simple_tech_summary(self, articles):
        """
        Fallback method: Generates a simple summary using just headlines when API fails.
        """
        output = "# TOP 5 TECH NEWS (HEADLINES ONLY)\n\n"
        
        # Take up to 5 articles
        count = 0
        for i, article in enumerate(articles):
            if count >= 5:
                break
                
            title = article.get('title', 'No Title')
            description = article.get('description', 'No Description')
            # Some descriptions might be None
            if not description:
                description = "No description available."
            
            output += f"News {count+1}:\n"
            output += f"# TITLE\n{title}\n\n"
            output += f"# DESCRIPTION\n{description}\n\n"
            output += f"# HASHTAGS\n#tech #news #latest\n\n"
            count += 1
            
        return output

    def generate_ai_summary(self, articles):
        """
        Generates a structured summary of top 5 AI news items from Hacker News.
        Uses deterministic formatting instead of AI generation to save quota.
        """
        if not articles:
            return "No AI articles provided."

        # Select top 5 articles
        top_articles = articles[:5]
        
        output = "# 🤖 TOP 5 AI NEWS\n\n"
        
        for i, article in enumerate(top_articles):
            title = article.get('title', 'No Title')
            # For Hacker News, the description we stored is essentially the URL/link or a short text
            link = article.get('description', 'No URL provided')
            
            output += f"News {i+1}:\n"
            output += f"## {title}\n"
            # User asked for "just title, a simple description". 
            # In HN context from news_client.py, 'description' is the URL.
            output += f"{link}\n\n"

        return output

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
        script = generator.generate_news_summary(mock_articles)
        print(script)
    else:
        print("GEMINI_API_KEY not found in environment.")
