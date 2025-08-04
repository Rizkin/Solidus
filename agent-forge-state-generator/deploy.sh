#!/bin/bash
# Agent Forge State Generator Deployment Script

set -e

echo "🚀 Agent Forge State Generator Deployment"
echo "=========================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Environment setup
echo "🔧 Setting up environment..."

if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual credentials before continuing"
    echo "   Required: SUPABASE_URL, SUPABASE_SERVICE_KEY, ANTHROPIC_API_KEY"
    read -p "Press Enter after updating .env file..."
fi

# Build and deploy
echo "🏗️  Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 30

# Health check
echo "🔍 Performing health check..."
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Agent Forge State Generator is running successfully!"
    echo ""
    echo "📡 Available endpoints:"
    echo "   • API Documentation: http://localhost:8000/docs"
    echo "   • Health Check: http://localhost:8000/api/health"
    echo "   • Block Types: http://localhost:8000/api/block-types"
    echo ""
    echo "🎯 Example API calls:"
    echo "   curl http://localhost:8000/api/health"
    echo "   curl http://localhost:8000/api/block-types"
    echo ""
    echo "🐳 Docker services:"
    docker-compose ps
else
    echo "❌ Health check failed. Checking logs..."
    docker-compose logs agent-forge-generator
    exit 1
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo "📖 Visit http://localhost:8000/docs for API documentation"
