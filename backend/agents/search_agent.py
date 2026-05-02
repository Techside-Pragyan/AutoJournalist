import feedparser
import urllib.parse
from typing import List, Dict

class SearchAgent:
    """Agent responsible for finding news articles based on a query."""
    
    def __init__(self):
        pass

    def search_news(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search Google News via RSS for the given query."""
        encoded_query = urllib.parse.quote(query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        
        feed = feedparser.parse(rss_url)
        results = []
        
        for entry in feed.entries[:num_results]:
            results.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(entry, 'published', 'Unknown date'),
                "source": entry.source.title if hasattr(entry, 'source') else "Unknown"
            })
            
        return results
