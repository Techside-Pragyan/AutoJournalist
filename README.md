# AutoJournalist 🤖📰

An **Autonomous News Researcher** system that takes a query, fetches relevant news articles, reads them, and uses AI agents to summarize and extract key insights. 

Built with **FastAPI** (Backend) and **React** (Frontend), featuring a multi-agent architecture.

## 🌟 Features
- **Agent-Based Architecture**: Separation of concerns using Search, Extraction, Summarization, and Insight Agents.
- **Multi-Language Support**: Choose which language you want your insights and summaries in.
- **Voice Input**: Speak your query directly into the dashboard (uses Web Speech API).
- **Beautiful Dashboard**: Sleek, modern, responsive UI with glassmorphism effects.
- **Sentiment & Trends Analysis**: Automatically determines the overall sentiment and overarching trend from multiple sources.

## 🏗️ Architecture
1. **Search Agent** (`search_agent.py`): Uses Google News RSS to find the latest headlines and links.
2. **Extractor Agent** (`extractor_agent.py`): Uses BeautifulSoup to cleanly extract main article text from URLs, filtering out ads and navbars.
3. **Summarizer Agent** (`summarizer_agent.py`): Uses OpenAI (`gpt-4o-mini`) to generate concise, bulleted summaries of long articles.
4. **Insight Agent** (`insight_agent.py`): Aggregates all summaries and outputs a JSON containing the overall trend, key takeaways, and sentiment.

## 🚀 Quick Start

### 1. Setup Backend
```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory and add your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

Run the FastAPI Server:
```bash
uvicorn main:app --reload
```
The API will be running at `http://localhost:8000`.

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```
The React frontend will be running at `http://localhost:5173`.

## 📁 Project Structure
```
AutoJournalist/
├── backend/
│   ├── agents/
│   │   ├── search_agent.py      # Fetches URLs
│   │   ├── extractor_agent.py   # Scrapes text
│   │   ├── summarizer_agent.py  # Summarizes text
│   │   ├── insight_agent.py     # Generates overall trends
│   │   └── manager.py           # Orchestrates workflow
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Environment configurations
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main React Dashboard
│   │   ├── App.css              # Custom UI Styling
│   │   └── index.css            # Global UI theme and variables
│   └── package.json
└── README.md
```

## ⚙️ Deployment
- **Backend (Render / Railway)**: Deploy the `backend` folder as a standard Python/FastAPI web service. Ensure `OPENAI_API_KEY` is set in the environment variables.
- **Frontend (Vercel)**: Deploy the `frontend` folder. Make sure to update the API endpoint URL in `App.tsx` from `localhost:8000` to your deployed backend URL.

## 💡 How It Works
1. You type "Latest AI Trends" in the search bar.
2. The UI shows "Researching...".
3. **Backend Manager** kicks off the **Search Agent** to grab 5 articles.
4. For each article, the **Extractor Agent** visits the site and parses the text.
5. The **Summarizer Agent** reads the text and condenses it.
6. The **Insight Agent** takes all 5 summaries and synthesizes them into Key Takeaways and Overall Sentiment.
7. The payload is returned to the frontend, which beautifully renders the cards, badges, and text.