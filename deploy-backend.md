# Backend Deployment Guide

## Option 1: Railway Deployment (Recommended)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Connect your GitHub account

### Step 2: Deploy from GitHub
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `AI-App` repository
4. Railway will automatically detect the Python backend

### Step 3: Configure Environment Variables
Add these environment variables in Railway dashboard:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
PYTHON_VERSION=3.11
```

### Step 4: Deploy
1. Railway will automatically build and deploy
2. Your backend will be available at: `https://your-app-name.railway.app`
3. Test the health endpoint: `https://your-app-name.railway.app/health`

## Option 2: Render Deployment

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: ai-app-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables
Add in Render dashboard:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Option 3: Heroku Deployment

### Step 1: Install Heroku CLI
1. Download from https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Deploy
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set ANTHROPIC_API_KEY=your_key_here
git push heroku main
```

## After Deployment

### Step 1: Update Frontend
Once your backend is deployed, update the frontend to connect:

1. Go to your Netlify dashboard
2. Go to Site Settings → Environment Variables
3. Add: `REACT_APP_API_URL=https://your-backend-url.railway.app/api/v1`

### Step 2: Redeploy Frontend
1. In Netlify, go to Deploys
2. Click "Trigger deploy" → "Deploy site"

### Step 3: Test Full System
Your app will now have:
- ✅ Real RAG document processing
- ✅ CrewAI autonomous agents
- ✅ Lead generation automation
- ✅ Full AI backend functionality

## API Endpoints Available

- `GET /health` - Health check
- `POST /api/v1/chat/message` - AI chat with RAG
- `POST /api/v1/documents/upload` - Document processing
- `POST /api/v1/agents/execute` - Agent task execution
- `GET /api/v1/search` - Knowledge base search
- `POST /api/v1/strategy/chat` - Lead generation strategy
- `GET /api/v1/leads/` - Lead management

## Cost Estimates

- **Railway**: $5/month for hobby plan
- **Render**: Free tier available, $7/month for paid
- **Heroku**: $7/month for basic plan

All options include:
- Automatic deployments
- SSL certificates
- Environment variable management
- Health monitoring
