#!/bin/bash

# CodeInspiration API Deployment Script
set -e

echo "🚀 Deploying CodeInspiration API..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp env.example .env
    echo "📝 Please edit .env file with your API keys before continuing."
    echo "   Required: OPENAI_API_KEY, GITHUB_TOKEN"
    exit 1
fi

# Create necessary directories
mkdir -p logs data

# Build and start the application
echo "🔨 Building Docker image..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for health check
echo "⏳ Waiting for service to be healthy..."
for i in {1..30}; do
    if curl -f http://localhost:8006/health > /dev/null 2>&1; then
        echo "✅ Service is healthy!"
        break
    fi
    echo "⏳ Waiting... ($i/30)"
    sleep 2
done

# Show status
echo "📊 Deployment Status:"
docker-compose ps

echo "🌐 API is running at: http://localhost:8006"
echo "📚 API Documentation: http://localhost:8006/docs"
echo "💚 Health Check: http://localhost:8006/health"

echo "✅ Deployment complete!" 