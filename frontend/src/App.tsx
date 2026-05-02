import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  Search, Mic, Loader2, Sparkles, TrendingUp, 
  BookOpen, ExternalLink, Activity, Clock 
} from 'lucide-react';
import './App.css';

// Types
interface Article {
  title: string;
  link: string;
  source: string;
  published: string;
  summary: string;
}

interface ResearchResult {
  query: string;
  language: string;
  overview: string;
  overall_sentiment: string;
  key_insights: string[];
  articles: Article[];
}

function App() {
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('English');
  const [isSearching, setIsSearching] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [result, setResult] = useState<ResearchResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<string[]>([]);
  
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    // Load history from local storage
    const saved = localStorage.getItem('researchHistory');
    if (saved) {
      setHistory(JSON.parse(saved));
    }

    // Initialize Speech Recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.webkitSpeechRecognition || (window as any).SpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      
      recognitionRef.current.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setQuery(transcript);
        setIsRecording(false);
      };

      recognitionRef.current.onerror = () => {
        setIsRecording(false);
      };

      recognitionRef.current.onend = () => {
        setIsRecording(false);
      };
    }
  }, []);

  const toggleVoice = () => {
    if (isRecording) {
      recognitionRef.current?.stop();
      setIsRecording(false);
    } else {
      if (recognitionRef.current) {
        recognitionRef.current.start();
        setIsRecording(true);
      } else {
        alert("Speech recognition is not supported in this browser.");
      }
    }
  };

  const handleSearch = async (e?: React.FormEvent, searchVal?: string) => {
    if (e) e.preventDefault();
    
    const q = searchVal || query;
    if (!q.trim()) return;

    setIsSearching(true);
    setError(null);
    setResult(null);

    // Save to history
    const newHistory = [q, ...history.filter(h => h !== q)].slice(0, 5);
    setHistory(newHistory);
    localStorage.setItem('researchHistory', JSON.stringify(newHistory));

    try {
      const response = await axios.post('http://localhost:8001/api/research', {
        query: q,
        language: language,
        num_results: 5
      });
      
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to fetch research. Make sure backend is running and API keys are set.");
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="app-container">
      <header className="animate-slide-up">
        <div className="logo-container">
          <Activity className="logo-icon animate-pulse-slow" />
          <h1>AutoJournalist</h1>
        </div>
        <p className="subtitle">Your Autonomous AI News Researcher</p>
      </header>

      <div className="search-container animate-slide-up" style={{ animationDelay: '0.1s' }}>
        <form onSubmit={handleSearch} className="search-input-wrapper">
          <Search className="search-icon" size={20} />
          <input 
            type="text" 
            className="search-input"
            placeholder="What would you like me to research? (e.g., 'Latest AI Trends')"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isSearching}
          />
          
          <div style={{ position: 'absolute', right: '1rem', display: 'flex', gap: '0.5rem' }}>
            <button 
              type="button" 
              className={`voice-btn ${isRecording ? 'recording' : ''}`}
              onClick={toggleVoice}
              disabled={isSearching}
              title="Voice Search"
            >
              <Mic size={18} />
            </button>
            <select 
              className="language-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              disabled={isSearching}
            >
              <option value="English">EN</option>
              <option value="Spanish">ES</option>
              <option value="French">FR</option>
              <option value="German">DE</option>
              <option value="Hindi">HI</option>
            </select>
          </div>
        </form>
        <button 
          onClick={(e) => handleSearch(e)} 
          className="action-btn"
          disabled={isSearching || !query.trim()}
        >
          Research
        </button>
      </div>

      {history.length > 0 && !isSearching && !result && (
        <div className="history-container animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}><Clock size={14} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }}/> Recent:</span>
          {history.map((h, i) => (
            <div key={i} className="history-tag" onClick={() => { setQuery(h); handleSearch(undefined, h); }}>
              {h}
            </div>
          ))}
        </div>
      )}

      {isSearching && (
        <div className="loading-container animate-slide-up">
          <Loader2 className="loader-icon animate-spin-slow" />
          <div className="loading-text">Agents are researching "{query}"...</div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Searching sources, extracting content, and synthesizing insights.</p>
        </div>
      )}

      {error && (
        <div className="glass-panel" style={{ padding: '1rem', color: 'var(--danger-color)', borderLeft: '4px solid var(--danger-color)', marginTop: '2rem' }}>
          {error}
        </div>
      )}

      {result && !isSearching && (
        <main className="dashboard animate-slide-up" style={{ animationDelay: '0.2s' }}>
          
          {/* Main Content Column */}
          <div className="dashboard-main">
            
            <div className="glass-panel overview-card">
              <div className="section-header">
                <Sparkles className="logo-icon" size={24} />
                <h2>Topic Overview</h2>
              </div>
              <p className="overview-text">{result.overview}</p>
            </div>

            <div className="glass-panel dashboard-section">
              <div className="section-header">
                <BookOpen className="logo-icon" size={24} />
                <h2>Sources & Summaries</h2>
              </div>
              
              <div className="articles-list">
                {result.articles.map((article, index) => (
                  <div key={index} className="article-card">
                    <div className="article-header">
                      <a href={article.link} target="_blank" rel="noopener noreferrer" className="article-title">
                        {article.title} <ExternalLink size={14} style={{ display: 'inline', marginLeft: '4px' }}/>
                      </a>
                    </div>
                    <p className="article-summary">{article.summary}</p>
                    <div className="article-meta">
                      <span className="article-source">{article.source}</span>
                      <span>{article.published}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar Column */}
          <div className="dashboard-sidebar">
            <div className="glass-panel dashboard-section" style={{ position: 'sticky', top: '2rem' }}>
              <div className="section-header">
                <TrendingUp className="logo-icon" size={24} />
                <h2>Key Insights</h2>
              </div>
              
              <div style={{ marginBottom: '2rem' }}>
                <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Overall Sentiment</h3>
                <div className={`sentiment-badge sentiment-${result.overall_sentiment}`}>
                  {result.overall_sentiment}
                </div>
              </div>

              <div className="insights-panel">
                <h3 style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '-0.5rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Takeaways</h3>
                {result.key_insights.map((insight, index) => (
                  <div key={index} className="insight-item">
                    <Sparkles className="insight-icon" size={16} />
                    <p className="insight-text">{insight}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
        </main>
      )}
    </div>
  );
}

export default App;
