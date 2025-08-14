"""
Article Scout - Research Paper Evaluator for TCC

A tool to evaluate research papers for relevance to TCC (Final Project) themes.
"""

__version__ = "0.1.0"
__author__ = "Article Scout Team"

from .article_scout_agent import evaluate_research_paper
from .utils.pdf_extractor import extract_text_from_pdf

__all__ = [
    "evaluate_research_paper",
    "extract_text_from_pdf",
]
