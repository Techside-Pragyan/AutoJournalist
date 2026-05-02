import requests
from bs4 import BeautifulSoup
import re

class ExtractorAgent:
    """Agent responsible for scraping and extracting text from news article URLs."""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def extract_content(self, url: str) -> str:
        """Fetch and extract main text content from a given URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove irrelevant tags
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
                element.decompose()
                
            # Get text from paragraphs
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Limit length to avoid massive token costs (roughly 1000-1500 tokens)
            return text[:5000]
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return ""
