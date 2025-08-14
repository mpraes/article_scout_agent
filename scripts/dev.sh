#!/bin/bash

# Development script for Article Scout

echo "🚀 Article Scout - Development Script"
echo "====================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env file from template..."
    cp config/env.example .env
    echo "✅ .env file created. Please edit it with your GROQ_API_KEY"
    echo "   Get your API key from: https://console.groq.com/"
    exit 1
fi

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=your_groq_api_key_here" .env; then
    echo "✅ .env file looks good"
else
    echo "⚠️  Please set your GROQ_API_KEY in the .env file"
    echo "   Get your API key from: https://console.groq.com/"
    exit 1
fi

echo ""
echo "Choose an option:"
echo "1. Run with Docker Compose (recommended)"
echo "2. Run with Docker directly"
echo "3. Run locally with uv"
echo "4. Build Docker image only"
echo "5. Run tests"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "🐳 Starting with Docker Compose..."
        docker-compose up --build
        ;;
    2)
        echo "🐳 Starting with Docker..."
        docker build -f docker/Dockerfile -t article-scout:latest .
        docker run -p 8501:8501 --env-file .env article-scout:latest
        ;;
    3)
        echo "🐍 Starting locally with uv..."
        uv run python -m streamlit run src/article_scout/streamlit_app.py
        ;;
    4)
        echo "🔨 Building Docker image..."
        ./docker/build.sh
        ;;
    5)
        echo "🧪 Running tests..."
        uv run pytest tests/ -v
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
