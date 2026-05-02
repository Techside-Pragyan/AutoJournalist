import openai
import json
from config import config
from typing import Dict, List

class InsightAgent:
    """Agent responsible for analyzing overall trends, sentiment, and key insights from a batch of news articles."""
    
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate_insights(self, query: str, articles_data: List[Dict], language: str = "English") -> Dict:
        """Generate trends, overall sentiment, and key insights based on multiple article summaries."""
        if not articles_data or not self.client:
            return {
                "overall_sentiment": "Neutral",
                "key_insights": ["API Key not provided or no data available to generate insights."],
                "trend_summary": "Insufficient data."
            }

        combined_summaries = "\n\n".join([f"Title: {a['title']}\nSummary: {a.get('summary', '')}" for a in articles_data])
        
        prompt = f"""
        You are an expert news analyst. Based on the following news articles about "{query}", 
        provide a JSON output with the following structure:
        {{
            "overall_sentiment": "Positive" | "Negative" | "Neutral",
            "key_insights": ["insight 1", "insight 2", "insight 3"],
            "trend_summary": "A 2-sentence summary of the overall trend or consensus among these articles."
        }}
        
        Ensure the output language is {language}.
        
        Articles:
        {combined_summaries}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a data-driven news insight generator. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" },
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"Error generating insights: {e}")
            return {
                "overall_sentiment": "Neutral",
                "key_insights": ["Error generating insights."],
                "trend_summary": "An error occurred during analysis."
            }
