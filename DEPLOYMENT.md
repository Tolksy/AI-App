# 🚀 Quick Deployment Guide

## Option 1: Local Development (Fastest)

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed

### Steps
1. **Get API Keys** (Required):
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/ (Alternative)

2. **Run the application**:
   ```bash
   # On Windows
   start-local.bat
   
   # On Mac/Linux
   ./start-local.sh
   ```

3. **Access your app**:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Option 2: Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps
1. **Set up environment**:
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

2. **Deploy**:
   ```bash
   ./deploy.sh
   ```

3. **Access your app**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## Option 3: Cloud Deployment

### Railway (Recommended)
1. Push to GitHub
2. Connect to Railway
3. Add environment variables
4. Deploy automatically

### Render
1. Connect GitHub repository
2. Add environment variables
3. Deploy with render.yaml

### Heroku
1. Install Heroku CLI
2. Create Heroku app
3. Add environment variables
4. Deploy with Procfile

## 🔑 Required Environment Variables

```bash
# At least one API key is required
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Security
SECRET_KEY=your-secret-key-here
```

## 🌐 Live Demo URLs

Once deployed, your RAG-based AI system will be available at:
- **Frontend**: Your deployed URL
- **Backend API**: Your deployed URL + /api/v1
- **API Documentation**: Your deployed URL + /docs

## 🎯 Features Available

✅ **RAG-powered Chat**: Upload documents and chat with AI
✅ **Smart Scheduling**: AI-powered schedule optimization
✅ **Autonomous Agents**: Multi-agent task execution
✅ **Document Management**: Upload and search documents
✅ **Knowledge Base**: Semantic search across documents

## 🆘 Troubleshooting

### Common Issues
1. **API Key Error**: Make sure you have a valid OpenAI or Anthropic API key
2. **Port Conflicts**: Change ports in docker-compose.yml if needed
3. **Memory Issues**: Increase Docker memory allocation
4. **Network Issues**: Check firewall settings

### Support
- Check logs: `docker-compose logs -f`
- Restart services: `docker-compose restart`
- Full reset: `docker-compose down && docker-compose up -d`

## 🎉 Success!

Your RAG-based Agentic AI system is now live and ready to use!




