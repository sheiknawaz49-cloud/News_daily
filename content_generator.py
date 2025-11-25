import google.generativeai as genai
import os

class ContentGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_news_summary(self, articles):
        """
        Generates a structured summary of top 5 news items (Title, Description, Hashtags).
        Prioritizes Technology and AI.
        """
        if not articles:
            return "No articles provided to generate summary."

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
        script = generator.generate_news_summary(mock_articles)
        print(script)
    else:
        print("GEMINI_API_KEY not found in environment.")
