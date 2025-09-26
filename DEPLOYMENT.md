# 🚀 Deployment Guide (GitHub Pages + optional backend)

## Frontend (GitHub Pages)

The frontend is deployed automatically via GitHub Actions to GitHub Pages.

### Requirements
- Node.js 18+
- GitHub repository with Pages enabled (Source: GitHub Actions)

### How it works
- Workflow: `.github/workflows/deploy.yml`
- Build: `npm ci && npm run build`
- Output: `dist/` (not committed; built in CI)
- Base path: set in `vite.config.js` as `/AI-App/`

### Local development
```bash
npm install
npm run dev
# App opens at http://localhost:3000
```

## Backend (optional)

If you need API features, deploy the FastAPI backend separately using the backend folder. You can use Render, Railway, or your own infrastructure. The frontend `src/config/api.js` points production to the configured backend URL.

### Quick start (local)
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










=======
>>>>>>> Incoming (Background Agent changes)
