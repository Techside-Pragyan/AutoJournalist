from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.manager import ResearchManager

app = FastAPI(title="Autonomous News Researcher API")

# Setup CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

research_manager = ResearchManager()

class ResearchRequest(BaseModel):
    query: str
    language: str = "English"
    num_results: int = 5

@app.get("/")
def read_root():
    return {"message": "Welcome to the Autonomous News Researcher API"}

@app.post("/api/research")
def conduct_research(request: ResearchRequest):
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        results = research_manager.run_research(
            query=request.query,
            language=request.language,
            num_results=request.num_results
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")
