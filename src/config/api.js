// API Configuration for different environments
const API_CONFIG = {
  development: {
    backendUrl: 'http://localhost:8000',
    frontendUrl: 'http://localhost:3000'
  },
  production: {
    backendUrl: 'https://ai-app-backend.onrender.com', // Render backend URL
    frontendUrl: 'https://superleadman.netlify.app' // Netlify frontend URL
  }
}

// Determine environment
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
const environment = isDevelopment ? 'development' : 'production'

export const API_BASE_URL = API_CONFIG[environment].backendUrl
export const FRONTEND_URL = API_CONFIG[environment].frontendUrl

// Helper function to build API URLs
export const buildApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`
}

export default {
  API_BASE_URL,
  FRONTEND_URL,
  buildApiUrl,
  isDevelopment,
  environment
}
