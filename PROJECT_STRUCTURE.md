# Project Structure

## 📁 Core Files (Essential)

### Backend
```
backend/
├── main.py                          # FastAPI application entry point
├── requirements.txt                  # Python dependencies
├── app/
│   ├── core/
│   │   ├── config.py                # Application configuration
│   │   ├── database.py              # Database setup
│   │   └── logging_config.py        # Logging configuration
│   ├── services/
│   │   ├── lead_generation_service.py    # Core lead generation logic
│   │   ├── lead_strategy_ai.py           # Conversational AI expert
│   │   ├── rag_service.py               # RAG and document processing
│   │   ├── agent_service.py             # AI agents and automation
│   │   └── document_service.py          # Document processing
│   └── api/routes/
│       ├── leads.py                      # Lead management API
│       ├── strategy.py                    # Strategy AI API
│       ├── chat.py                        # Chat API
│       ├── documents.py                   # Document API
│       ├── agents.py                      # Agent API
│       └── scheduling.py                 # Scheduling API
```

### Frontend
```
src/
├── App.jsx                          # Main application component
├── main.jsx                         # React entry point
├── components/
│   ├── LeadDashboard.jsx            # Lead management interface
│   ├── StrategyAI.jsx               # Conversational AI interface
│   ├── Calendar.jsx                 # Calendar component
│   ├── TimeBlock.jsx                # Time blocking component
│   ├── AIAssistant.jsx              # AI assistant component
│   └── ScheduleModal.jsx            # Schedule modal component
├── services/
│   └── aiService.js                 # AI service integration
├── utils/
│   └── timeUtils.js                 # Time utility functions
└── index.css                        # Application styles
```

## 🗑️ Files to Remove (Reduce Context)

### Unnecessary Files
```
demo.html                           # Demo file
standalone-server.html              # Standalone server
download-installers.bat            # Windows installer
install-everything.bat             # Windows installer
install-everything.ps1             # PowerShell installer
simple-install.bat                  # Simple installer
start-local.bat                     # Local start script
start-local.sh                      # Local start script
```

### Deployment Files (Keep for Production)
```
deploy.sh                           # Deployment script
docker-compose.yml                  # Docker configuration
Dockerfile                          # Backend Dockerfile
Dockerfile.frontend                 # Frontend Dockerfile
Procfile                            # Heroku configuration
railway.json                        # Railway configuration
render.yaml                         # Render configuration
env.example                         # Environment variables example
```

## 🎯 Essential Commands

### Development
```bash
# Start backend
py backend/main.py

# Start frontend
npm run dev

# Install dependencies
pip install -r backend/requirements.txt
npm install
```

### Production
```bash
# Docker
docker-compose up

# Heroku
git push heroku main

# Railway
railway deploy
```

## 📊 Key Features

1. **Strategy AI**: `/api/v1/strategy/chat` - Conversational lead generation expert
2. **Lead Management**: `/api/v1/leads/` - Full CRUD for leads
3. **Autonomous Generation**: 24/7 background lead sourcing
4. **Multi-Industry**: Expertise across 10+ business niches
5. **Self-Marketing**: Can find leads for the software itself

## 🚀 Quick Access

- **Main App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Strategy AI**: http://localhost:3000 (Strategy AI tab)
- **Lead Dashboard**: http://localhost:3000 (Leads tab)



