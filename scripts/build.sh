#!/bin/bash

# Build script for Article Scout Docker image

echo "🐳 Building Article Scout Docker image..."

# Build the image
docker build -f docker/Dockerfile -t article-scout:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the application:"
    echo "docker run -p 8501:8501 -e GROQ_API_KEY=your_api_key_here article-scout:latest"
    echo ""
    echo "Or with a .env file:"
    echo "docker run -p 8501:8501 --env-file .env article-scout:latest"
else
    echo "❌ Docker build failed!"
    exit 1
fi
