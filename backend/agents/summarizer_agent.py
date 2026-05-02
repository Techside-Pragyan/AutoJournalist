import openai
from backend.config import config

class SummarizationAgent:
    """Agent responsible for summarizing extracted article text."""
    
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def summarize(self, text: str, language: str = "English") -> str:
        """Generate a concise summary of the text."""
        if not text:
            return "No content to summarize."
            
        if not self.client:
            # Fallback if no API key is provided
            return text[:200] + "... (Summary unavailable, no OpenAI API key)"
            
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a professional journalist. Summarize the following news article clearly and concisely in {language}. Keep it to 3-4 sentences."},
                    {"role": "user", "content": text}
                ],
                max_tokens=150,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error during summarization: {e}")
            return "Failed to generate summary."
