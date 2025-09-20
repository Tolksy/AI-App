#!/bin/bash

# RAG-based AI System Deployment Script

echo "🚀 Deploying RAG-based Agentic AI System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backend/data
mkdir -p backend/logs
mkdir -p data/chroma_db

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your API keys before continuing!"
    echo "   Required: OPENAI_API_KEY or ANTHROPIC_API_KEY"
    read -p "Press Enter to continue after editing .env file..."
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose down
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Test backend health
echo "🏥 Testing backend health..."
curl -f http://localhost:8000/health || echo "❌ Backend health check failed"

# Test frontend
echo "🌐 Testing frontend..."
curl -f http://localhost:3000 || echo "❌ Frontend health check failed"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "📊 Monitor logs with:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services with:"
echo "   docker-compose down"
echo ""
echo "🎉 Your RAG-based AI system is now live!"


