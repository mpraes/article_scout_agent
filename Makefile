.PHONY: help install test lint format clean build run docker-build docker-run

help: ## Show this help message
	@echo "Article Scout - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

test: ## Run tests
	uv run pytest tests/ -v

lint: ## Run linting
	uv run flake8 src/ tests/
	uv run black --check src/ tests/
	uv run isort --check-only src/ tests/

format: ## Format code
	uv run black src/ tests/
	uv run isort src/ tests/

clean: ## Clean cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build Docker image
	./scripts/build.sh

run: ## Run application locally
	uv run python -m streamlit run src/article_scout/streamlit_app.py

docker-run: ## Run application with Docker
	docker run -p 8501:8501 --env-file .env article-scout:latest

dev: ## Run development script
	./scripts/dev.sh

setup: install ## Setup project (install dependencies)
	@echo "✅ Project setup complete!"
	@echo "📝 Don't forget to:"
	@echo "   1. Copy config/env.example to .env"
	@echo "   2. Set your GROQ_API_KEY in .env"
	@echo "   3. Run 'make run' to start the application"
