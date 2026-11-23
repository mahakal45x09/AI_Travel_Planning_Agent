import { useState, useRef, useEffect } from 'react'
import './index.css'

const API_URL = 'http://localhost:8000'

// Suggestion chips celebrating Indian heritage and global travel
const SUGGESTIONS = [
  "🏰 Plan a 5-day Royal Rajasthan palace & fort trip",
  "🌴 Kerala backwaters & Ayurvedic wellness retreat",
  "🪔 Varanasi spiritual ghats & Ganga Aarti experience",
  "🏖️ Best beaches in Goa & Gokarna under ₹3000/day",
  "🏔️ Himachal Pradesh & Ladakh summer mountain trail",
  "🏛️ UNESCO World Heritage sites in India (Hampi, Ellora, Taj)",
  "🗼 Suggest a 7-day Japan itinerary",
  "🌍 Top 5 European destinations for first-timers",
]

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [activeTab, setActiveTab] = useState('chat')
  const [destinations, setDestinations] = useState({ india: [], world: [] })
  const [stats, setStats] = useState(null)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Load stats and destinations on mount
  useEffect(() => {
    fetchStats()
    fetchDestinations()
  }, [])

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_URL}/api/destinations/stats`)
      if (res.ok) {
        const data = await res.json()
        setStats(data)
      }
    } catch (err) {
      console.log('Stats API not available — backend may not be running')
    }
  }

  const fetchDestinations = async () => {
    try {
      const [indiaRes, worldRes] = await Promise.all([
        fetch(`${API_URL}/api/destinations/india?limit=20`),
        fetch(`${API_URL}/api/destinations/world?limit=20`),
      ])
      if (indiaRes.ok && worldRes.ok) {
        const india = await indiaRes.json()
        const world = await worldRes.json()
        setDestinations({ india: india.results, world: world.results })
      }
    } catch (err) {
      console.log('Destinations API not available')
    }
  }

  const sendMessage = async (text = null) => {
    const messageText = text || input.trim()
    if (!messageText || isLoading) return

    // Add user message
    const userMessage = { role: 'user', content: messageText }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const res = await fetch(`${API_URL}/api/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageText,
          session_id: sessionId,
        }),
      })

      if (res.ok) {
        const data = await res.json()
        setSessionId(data.session_id)
        setMessages(prev => [...prev, { role: 'agent', content: data.reply }])
      } else {
        setMessages(prev => [...prev, {
          role: 'agent',
          content: '❌ Sorry, I encountered an error. Please check that the backend server is running on port 8000 and your API key is configured in .env'
        }])
      }
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'agent',
        content: `❌ Could not connect to the server. Please make sure:\n\n1. Backend is running: \`uvicorn app.main:app --reload --port 8000\`\n2. Your API key is set in \`.env\`\n\nError: ${err.message}`
      }])
    }

    setIsLoading(false)
    inputRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const formatMessage = (content) => {
    // Simple markdown-like formatting
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/^### (.*$)/gm, '<h3>$1</h3>')
      .replace(/^## (.*$)/gm, '<h2>$1</h2>')
      .replace(/^# (.*$)/gm, '<h1>$1</h1>')
      .replace(/^- (.*$)/gm, '<li>$1</li>')
      .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
      .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
      .replace(/^---$/gm, '<hr />')
      .replace(/\n/g, '<br />')
  }

  // Category emoji map
  const categoryEmoji = {
    Heritage: '🏛️', Beach: '🏖️', 'Hill Station': '🏔️', Nature: '🌿',
    Wildlife: '🐅', Adventure: '🧗', Pilgrimage: '🙏', Island: '🏝️',
    Backwater: '🚣', 'Metro City': '🏙️', City: '🏙️', Landmark: '🗼',
    Coastal: '🌊',
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🦚</span>
            <span>TravelBuddy AI</span>
          </div>
          <nav>
            <ul className="nav-links">
              <li>
                <a
                  href="#chat"
                  className={activeTab === 'chat' ? 'active' : ''}
                  onClick={(e) => { e.preventDefault(); setActiveTab('chat') }}
                >
                  💬 Chat
                </a>
              </li>
              <li>
                <a
                  href="#explore"
                  className={activeTab === 'explore' ? 'active' : ''}
                  onClick={(e) => { e.preventDefault(); setActiveTab('explore') }}
                >
                  🗺️ Explore
                </a>
              </li>
              <li>
                <a
                  href="#about"
                  className={activeTab === 'about' ? 'active' : ''}
                  onClick={(e) => { e.preventDefault(); setActiveTab('about') }}
                >
                  ℹ️ About
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* ===== CHAT TAB ===== */}
        {activeTab === 'chat' && (
          <div className="chat-container">
            <div className="chat-header">
              <h1>✈️ AI Travel Planning Agent</h1>
              <p>अतिथि देवो भव • Experience the timeless wonders of Incredible India & the World</p>
            </div>

            <div className="chat-messages">
              {messages.length === 0 && (
                <div className="welcome-screen">
                  <div className="welcome-emoji">🪔</div>
                  <h2>नमस्ते! Where would you like to explore?</h2>
                  <p>
                    From the royal palaces of Rajasthan and holy ghats of Varanasi to the tranquil backwaters of Kerala and global wonders — let's plan your dream itinerary!
                  </p>
                  <div className="features-list">
                    <div className="feature-item">
                      <span className="feature-icon">🇮🇳</span>
                      <div className="feature-text">
                        <strong>71+ Indian Heritage Spots</strong>
                        27 states from Kashmir to Kanyakumari
                      </div>
                    </div>
                    <div className="feature-item">
                      <span className="feature-icon">🕌</span>
                      <div className="feature-text">
                        <strong>Palaces, Forts & Ghats</strong>
                        Deep cultural, historical & culinary depth
                      </div>
                    </div>
                    <div className="feature-item">
                      <span className="feature-icon">💰</span>
                      <div className="feature-text">
                        <strong>Smart Budget Estimator</strong>
                        Cost breakdown in INR (Budget, Mid-range, Royal)
                      </div>
                    </div>
                    <div className="feature-item">
                      <span className="feature-icon">📋</span>
                      <div className="feature-text">
                        <strong>Customized Day-by-Day Plans</strong>
                        Personalized timings, activities, and local tips
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {messages.map((msg, i) => (
                <div key={i} className={`message ${msg.role}`}>
                  <div className="message-label">
                    {msg.role === 'user' ? '👤 You' : '🤖 TravelBuddy'}
                  </div>
                  <div dangerouslySetInnerHTML={{ __html: formatMessage(msg.content) }} />
                </div>
              ))}

              {isLoading && (
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Suggestion Chips */}
            {messages.length === 0 && (
              <div className="suggestions">
                {SUGGESTIONS.map((s, i) => (
                  <button key={i} className="suggestion-chip" onClick={() => sendMessage(s)}>
                    {s}
                  </button>
                ))}
              </div>
            )}

            {/* Input */}
            <div className="chat-input-container">
              <div className="chat-input-wrapper">
                <textarea
                  ref={inputRef}
                  className="chat-input"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about destinations, itineraries, budgets..."
                  rows={1}
                  disabled={isLoading}
                />
                <button
                  className="send-btn"
                  onClick={() => sendMessage()}
                  disabled={!input.trim() || isLoading}
                  title="Send message"
                >
                  ➤
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ===== EXPLORE TAB ===== */}
        {activeTab === 'explore' && (
          <div>
            <div className="chat-header">
              <h1>🗺️ Explore Destinations</h1>
              <p>Browse popular destinations across India and the world</p>
            </div>

            {/* Stats */}
            {stats && (
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon">🇮🇳</div>
                  <div className="stat-value">{stats.india_destinations}</div>
                  <div className="stat-label">India Destinations</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">🌍</div>
                  <div className="stat-value">{stats.world_destinations}</div>
                  <div className="stat-label">World Destinations</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">✈️</div>
                  <div className="stat-value">{stats.airports?.toLocaleString()}</div>
                  <div className="stat-label">Airports</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">🌐</div>
                  <div className="stat-value">{stats.countries}</div>
                  <div className="stat-label">Countries</div>
                </div>
              </div>
            )}

            {/* Tabs */}
            <div className="tabs">
              <button
                className={`tab ${activeTab === 'explore' ? 'active' : ''}`}
                onClick={() => {}}
              >
                🇮🇳 India
              </button>
              <button className="tab" onClick={() => {}}>
                🌍 World
              </button>
            </div>

            {/* India Destinations */}
            <h2 style={{ marginBottom: 'var(--space-md)', fontFamily: 'var(--font-display)' }}>
              🇮🇳 India Destinations
            </h2>
            <div className="destinations-grid">
              {destinations.india.map((d, i) => (
                <div
                  key={i}
                  className="destination-card"
                  onClick={() => {
                    setActiveTab('chat')
                    sendMessage(`Tell me about ${d.place_name}, ${d.state}`)
                  }}
                >
                  <div className="card-image">
                    {categoryEmoji[d.category] || '📍'}
                  </div>
                  <div className="card-body">
                    <h3>{d.place_name}</h3>
                    <div className="card-location">📍 {d.state}, India</div>
                    <p className="card-description">{d.description}</p>
                    <div className="card-meta">
                      <span className="card-badge">{d.category}</span>
                      <span className="card-rating">⭐ {d.rating}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* World Destinations */}
            <h2 style={{ margin: 'var(--space-xl) 0 var(--space-md)', fontFamily: 'var(--font-display)' }}>
              🌍 World Destinations
            </h2>
            <div className="destinations-grid">
              {destinations.world.map((d, i) => (
                <div
                  key={i}
                  className="destination-card"
                  onClick={() => {
                    setActiveTab('chat')
                    sendMessage(`Tell me about ${d.place_name}, ${d.country}`)
                  }}
                >
                  <div className="card-image">
                    {categoryEmoji[d.category] || '📍'}
                  </div>
                  <div className="card-body">
                    <h3>{d.place_name}</h3>
                    <div className="card-location">📍 {d.city}, {d.country}</div>
                    <p className="card-description">{d.description}</p>
                    <div className="card-meta">
                      <span className="card-badge">{d.category}</span>
                      <span className="card-rating">⭐ {d.rating}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* No data fallback */}
            {destinations.india.length === 0 && destinations.world.length === 0 && (
              <div className="welcome-screen">
                <div className="welcome-emoji">🔌</div>
                <h2>Backend Not Connected</h2>
                <p>
                  Start the backend server to load destinations:<br />
                  <code>cd backend && uvicorn app.main:app --reload --port 8000</code>
                </p>
              </div>
            )}
          </div>
        )}

        {/* ===== ABOUT TAB ===== */}
        {activeTab === 'about' && (
          <div className="welcome-screen">
            <div className="welcome-emoji">🌍</div>
            <h2>AI Travel Planning Agent</h2>
            <p>
              An open-source AI-powered travel assistant built with FastAPI, LangChain,
              and React. Plan trips across 190+ countries with deep India coverage.
            </p>
            <div className="features-list">
              <div className="feature-item">
                <span className="feature-icon">🤖</span>
                <div className="feature-text">
                  <strong>LangChain AI Agent</strong>
                  Powered by Gemini/GPT with 7 specialized tools
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">⚡</span>
                <div className="feature-text">
                  <strong>FastAPI Backend</strong>
                  High-performance async API with auto-docs
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">📊</span>
                <div className="feature-text">
                  <strong>Clean Data Pipeline</strong>
                  6 automated cleaning scripts for 7 datasets
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🔓</span>
                <div className="feature-text">
                  <strong>Open Source (MIT)</strong>
                  Contribute destinations, code, or translations
                </div>
              </div>
            </div>
            <div style={{ marginTop: 'var(--space-xl)' }}>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                Built with ❤️ • MIT License •{' '}
                <a href="https://github.com" target="_blank" rel="noopener">
                  GitHub
                </a>
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
