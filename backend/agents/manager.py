from backend.agents.search_agent import SearchAgent
from backend.agents.extractor_agent import ExtractorAgent
from backend.agents.summarizer_agent import SummarizationAgent
from backend.agents.insight_agent import InsightAgent
from typing import Dict

class ResearchManager:
    """Orchestrates the entire research workflow using the other agents."""
    
    def __init__(self):
        self.search_agent = SearchAgent()
        self.extractor_agent = ExtractorAgent()
        self.summarizer_agent = SummarizationAgent()
        self.insight_agent = InsightAgent()

    def run_research(self, query: str, language: str = "English", num_results: int = 5) -> Dict:
        """Executes the full pipeline: search -> extract -> summarize -> insights."""
        print(f"Starting research for query: '{query}' in {language}")
        
        # 1. Search for news
        articles = self.search_agent.search_news(query, num_results=num_results)
        
        # 2. Extract and Summarize each article
        processed_articles = []
        for article in articles:
            print(f"Processing: {article['title']}")
            content = self.extractor_agent.extract_content(article['link'])
            
            # If we couldn't extract content, skip or use title for summary (simplification)
            if not content:
                content = article['title']
                
            summary = self.summarizer_agent.summarize(content, language=language)
            
            processed_articles.append({
                "title": article["title"],
                "link": article["link"],
                "source": article["source"],
                "published": article["published"],
                "summary": summary
            })
            
        # 3. Generate overall insights
        insights = self.insight_agent.generate_insights(query, processed_articles, language=language)
        
        # 4. Construct final output
        result = {
            "query": query,
            "language": language,
            "overview": insights.get("trend_summary", ""),
            "overall_sentiment": insights.get("overall_sentiment", "Neutral"),
            "key_insights": insights.get("key_insights", []),
            "articles": processed_articles
        }
        
        return result
