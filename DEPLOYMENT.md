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
cd backend
pip install -r requirements.txt
python main.py
# API available at http://localhost:8000 (docs at /docs)
```

### Environment variables
Create `.env` for the backend and set required keys as needed by your chosen features (e.g. `OPENAI_API_KEY`). See `env.example` for guidance.

## Troubleshooting
- 404s on GitHub Pages: ensure `base` in `vite.config.js` matches repo name and workflow uploads `./dist`.
- Wrong API URL in production: update `src/config/api.js` `production.backendUrl`.
- Do not commit `dist/`: CI builds artifacts; keep repo clean.









