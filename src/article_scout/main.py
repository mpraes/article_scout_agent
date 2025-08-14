"""
Main entry point for Article Scout application
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import validate_config
from article_scout import evaluate_research_paper, extract_text_from_pdf


def main():
    """Main entry point for the application"""
    try:
        # Validate configuration
        validate_config()
        
        print("🚀 Article Scout - Research Paper Evaluator")
        print("=" * 50)
        print("Configuration validated successfully!")
        print("Use 'uv run streamlit run src/article_scout/streamlit_app.py' to start the web interface")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
