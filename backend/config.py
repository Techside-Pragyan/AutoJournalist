import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "") # Optional: if not using Google News RSS
    
config = Config()
