# %%
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import re
import pprint
from utils.pdf_extractor import extract_text_from_pdf

MAX_INPUT_CHARS = 5000  # Adjust this value based on your API limits

# %%
# Load environment variables and configure the Groq API key
load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')
if groq_api_key:
    os.environ["GROQ_API_KEY"] = groq_api_key
else:
    print("Warning: GROQ_API_KEY not found in environment variables. Please ensure it is configured in your .env file")
    print("The application will show an error when trying to evaluate papers.")
# %%
class State(TypedDict):
    """
    Represents the state of the research paper evaluation process
    in relation to a TCC theme, including multiple scores and their explanations.
    """
    research_paper: str # The text of the research paper to be evaluated
    article_theme: str      # The theme of the researcher's TCC (Final Project)
    
    relevance_score: float
    relevance_explanation: str

    originality_score: float
    originality_explanation: str

    methodology_quality_score: float
    methodology_quality_explanation: str

    results_discussion_quality_score: float
    results_discussion_quality_explanation: str

    potential_impact_score: float
    potential_impact_explanation: str

    writing_clarity_score: float
    writing_clarity_explanation: str

    references_timeliness_score: float
    references_timeliness_explanation: str

    final_score: float
    truncation_warning: str
# %%
## Groq model initialization
# We use the 'gemma2-9b-it' model with a temperature of 0.3 for more consistent responses.
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
# %%
def extract_score_and_explanation(content: str) -> tuple[float, str]:
    """
    Extracts the numerical score and the explanation from the LLM's response.
    Expects the format 'Score: X.X\nExplanation: YYY'.
    """
    score_match = re.search(r'Score:\s*(\d+(\.\d+)?)', content)
    explanation_match = re.search(r'Explanation:\s*(.*)', content, re.DOTALL) # DOTALL to match across newlines

    score = float(score_match.group(1)) if score_match else 0.0
    explanation = explanation_match.group(1).strip() if explanation_match else "No explanation provided."
    
    if not score_match:
        raise ValueError(f"Could not extract score from: {content}")
        
    return score, explanation
# %%
def check_relevance(state: State) -> State:
    """
    Checks the relevance of a research paper in relation to a TCC theme.
    """
    prompt = ChatPromptTemplate.from_template(
        "Analyze the relevance of the following research paper to the provided TCC theme. "
        "Identify keywords, central concepts, and the research area of both to determine the connection. "
        "Provide a relevance score between 0 and 1, where 1 indicates high relevance. "
        "Your response MUST start with 'Score: ' followed by the numerical score, "
        "then a newline, and then 'Explanation: ' followed by your detailed explanation about the relevance and why the paper is (or is not) useful for the TCC.\n\n"
        "Article Theme: {article_theme}\n\nResearch Paper: {research_paper}"
    )
    
    result = llm.invoke(prompt.format(article_theme=state["article_theme"], research_paper=state["research_paper"]))
    
    try:
        content = result.content if isinstance(result.content, str) else str(result.content)
        score, explanation = extract_score_and_explanation(content)
        state["relevance_score"] = score
        state["relevance_explanation"] = explanation
    except ValueError as e:
        print(f"Error in check_relevance: {e}")
        state["relevance_score"] = 0.0
        state["relevance_explanation"] = f"Error: {e}"
    return state
# %%
def check_originality(state: State) -> State:
    """
    Evaluates the originality/novelty of the work presented in the paper.
    """
    prompt = ChatPromptTemplate.from_template(
        "Evaluate the originality and novelty of the following research paper. "
        "Does it introduce a new idea, methodology, or results that advance the field? "
        "Provide an originality score between 0 and 1. "
        "Your response MUST start with 'Score: ' followed by the numerical score, "
        "then a newline, and then 'Explanation: ' followed by your detailed explanation.\n\nResearch Paper: {research_paper}"
    )
    result = llm.invoke(prompt.format(research_paper=state["research_paper"]))
    try:
        content = result.content if isinstance(result.content, str) else str(result.content)
        score, explanation = extract_score_and_explanation(content)
        state["originality_score"] = score
        state["originality_explanation"] = explanation
    except ValueError as e:
        print(f"Error in check_originality: {e}")
        state["originality_score"] = 0.0
        state["originality_explanation"] = f"Error: {e}"
    return state
# %%
def check_methodology_quality(state: State) -> State:
    """
    Evaluates the quality and robustness of the methodology used in the paper.
    """
    prompt = ChatPromptTemplate.from_template(
        "Evaluate the quality of the methodology presented in the following research paper. "
        "Is the methodology clear, appropriate for the objectives, and robust? "
        "Provide a methodology quality score between 0 and 1. "
        "Your response MUST start with 'Score: ' followed by the numerical score, "
        "then a newline, and then 'Explanation: ' followed by your detailed explanation.\n\nResearch Paper: {research_paper}"
    )
    result = llm.invoke(prompt.format(research_paper=state["research_paper"]))
    try:
        content = result.content if isinstance(result.content, str) else str(result.content)
        score, explanation = extract_score_and_explanation(content)
        state["methodology_quality_score"] = score
        state["methodology_quality_explanation"] = explanation
    except ValueError as e:
        print(f"Error in check_methodology_quality: {e}")
        state["methodology_quality_score"] = 0.0
        state["methodology_quality_explanation"] = f"Error: {e}"
    return state
# %%
def check_results_discussion_quality(state: State) -> State:
    """
    Evaluates the clarity and soundness of the results and discussion in the paper.
    """
    prompt = ChatPromptTemplate.from_template(
        "Evaluate the quality of the results and discussion in the following research paper. "
        "Are the results presented clearly? Does the discussion correctly interpret the results, and are the conclusions well-founded? "
        "Provide a results and discussion quality score between 0 and 1. "
        "Your response MUST start with 'Score: ' followed by the numerical score, "
        "then a newline, and then 'Explanation: ' followed by your detailed explanation.\n\nResearch Paper: {research_paper}"
    )
    result = llm.invoke(prompt.format(research_paper=state["research_paper"]))
    try:
        content = result.content if isinstance(result.content, str) else str(result.content)
        score, explanation = extract_score_and_explanation(content)
        state["results_discussion_quality_score"] = score
        state["results_discussion_quality_explanation"] = explanation
    except ValueError as e:
        print(f"Error in check_results_discussion_quality: {e}")
        state["results_discussion_quality_score"] = 0.0
        state["results_discussion_quality_explanation"] = f"Error: {e}"
    return state
    return state
# %%
def check_potential_impact(state: State) -> State:
    """
    Estimates the potential impact of the paper in the field of study or in practical applications.
    """
    prompt = ChatPromptTemplate.from_template(
        "Estimate the potential impact of the following research paper in its field of study or in practical applications. "
        "Does it open new lines of research, solve a significant problem, or have important implications? "
        "Provide a potential impact score between 0 and 1. "
        "Your response MUST start with 'Score: ' followed by the numerical score, "
        "then a newline, and then 'Explanation: ' followed by your detailed explanation.\n\nResearch Paper: {research_paper}"
    )
    result = llm.invoke(prompt.format(research_paper=state["research_paper"]))
    try:
        content = result.content if isinstance(result.content, str) else str(result.content)
        score, explanation = extract_score_and_explanation(content)
        state["potential_impact_score"] = score
        state["potential_impact_explanation"] = explanation
    except ValueError as e:
        print(f"Error in check_potential_impact: {e}")
        state["potential_impact_score"] = 0.0
        state["potential_impact_explanation"] = f"Error: {e}"
    return state
# %%
def check_writing_clarity(state: State) -> State:
    """
    Evaluates the overall clarity and readability of the technical paper's writing.
    """
    prompt = ChatPromptTemplate.from_template(
        "Evaluate the overall clarity, readability, and flow of the writing in the following technical research paper. "
        "Is the language precise and concise? Are the ideas communicated effectively? "
        "Provide a writing clarity score between 0 and 1. "
        "Your response MUST start with 'Score: ' followed by the numerical score, "
        "then a newline, and then 'Explanation: ' followed by your detailed explanation.\n\nResearch Paper: {research_paper}"
    )
    result = llm.invoke(prompt.format(research_paper=state["research_paper"]))
    try:
        content = result.content if isinstance(result.content, str) else str(result.content)
        score, explanation = extract_score_and_explanation(content)
        state["writing_clarity_score"] = score
        state["writing_clarity_explanation"] = explanation
    except ValueError as e:
        print(f"Error in check_writing_clarity: {e}")
        state["writing_clarity_score"] = 0.0
        state["writing_clarity_explanation"] = f"Error: {e}"
    return state
# %%
def check_references_timeliness(state: State) -> State:
    """
    Checks the timeliness and relevance of the references used in the paper.
    """
    prompt = ChatPromptTemplate.from_template(
        "Evaluate the timeliness and relevance of the references cited in the following research paper. "
        "Does the paper use recent and pertinent sources for the field of study? "
        "Provide a references timeliness score between 0 and 1. "
        "Your response MUST start with 'Score: ' followed by the numerical score, "
        "then a newline, and then 'Explanation: ' followed by your detailed explanation.\n\nResearch Paper: {research_paper}"
    )
    result = llm.invoke(prompt.format(research_paper=state["research_paper"]))
    try:
        content = result.content if isinstance(result.content, str) else str(result.content)
        score, explanation = extract_score_and_explanation(content)
        state["references_timeliness_score"] = score
        state["references_timeliness_explanation"] = explanation
    except ValueError as e:
        print(f"Error in check_references_timeliness: {e}")
        state["references_timeliness_score"] = 0.0
        state["references_timeliness_explanation"] = f"Error: {e}"
    return state
# %%
def calculate_final_score(state: State) -> State:
    """
    Calculates the final score based on all individual scores.
    Weights can be adjusted according to the importance of each criterion.
    """
    total_scores = (
        state["relevance_score"] * 0.20 +
        state["originality_score"] * 0.15 +
        state["methodology_quality_score"] * 0.15 +
        state["results_discussion_quality_score"] * 0.15 +
        state["potential_impact_score"] * 0.15 +
        state["writing_clarity_score"] * 0.10 +
        state["references_timeliness_score"] * 0.10
    )
    state["final_score"] = total_scores
    return state
# %%
# Definition of the workflow/execution of the evaluation process
workflow = StateGraph(State)
# %%
# Adding nodes to the workflow
workflow.add_node("check_relevance", check_relevance)
workflow.add_node("check_originality", check_originality)
workflow.add_node("check_methodology_quality", check_methodology_quality)
workflow.add_node("check_results_discussion_quality", check_results_discussion_quality)
workflow.add_node("check_potential_impact", check_potential_impact)
workflow.add_node("check_writing_clarity", check_writing_clarity)
workflow.add_node("check_references_timeliness", check_references_timeliness)
workflow.add_node("calculate_final_score", calculate_final_score)
# %%
# Define edges for the sequential flow
workflow.add_edge(START, "check_relevance")
workflow.add_edge("check_relevance", "check_originality")
workflow.add_edge("check_originality", "check_methodology_quality")
workflow.add_edge("check_methodology_quality", "check_results_discussion_quality")
workflow.add_edge("check_results_discussion_quality", "check_potential_impact")
workflow.add_edge("check_potential_impact", "check_writing_clarity")
workflow.add_edge("check_writing_clarity", "check_references_timeliness")
workflow.add_edge("check_references_timeliness", "calculate_final_score")
# %%
# Define the exit point of the workflow
workflow.add_edge("calculate_final_score", END)
# %%
# Compile the graph
app = workflow.compile()
# %%
def evaluate_research_paper(research_paper: str, article_theme: str) -> dict:
    """
    Evaluates a research paper for an article theme using the compiled workflow,
    considering multiple criteria. Handles potential input truncation due to API limits.
    """
    original_research_paper_len = len(research_paper)
    truncation_warning = ""

    if original_research_paper_len > MAX_INPUT_CHARS:
        research_paper = research_paper[:MAX_INPUT_CHARS]
        truncation_warning = (
            f"Warning: The research paper was truncated from {original_research_paper_len} "
            f"to {MAX_INPUT_CHARS} characters due to API input limits. "
            "The evaluation might be incomplete or less accurate for the full document."
        )
        # Note: In a production Streamlit app, you might use st.warning() here.
        # For a test script, printing is fine.
        print(truncation_warning) 

    initial_state = State(
        research_paper=research_paper,
        article_theme=article_theme,
        relevance_score=0.0,
        relevance_explanation="",
        originality_score=0.0,
        originality_explanation="",
        methodology_quality_score=0.0,
        methodology_quality_explanation="",
        results_discussion_quality_score=0.0,
        results_discussion_quality_explanation="",
        potential_impact_score=0.0,
        potential_impact_explanation="",
        writing_clarity_score=0.0,
        writing_clarity_explanation="",
        references_timeliness_score=0.0,
        references_timeliness_explanation="",
        final_score=0.0,
        truncation_warning=truncation_warning
    )
    result = app.invoke(initial_state)
    return result
# %%
def format_results_for_display(results: dict) -> dict:
    """
    Formats the raw results dictionary into a more readable format for pprint,
    scaling scores and including explanations.
    """
    formatted = {
        "Final Score": f"{results['final_score'] * 10:.2f}",
        "Relevance to TCC": {
            "Score": f"{results['relevance_score'] * 10:.2f}",
            "Explanation": results['relevance_explanation']
        },
        "Originality": {
            "Score": f"{results['originality_score'] * 10:.2f}",
            "Explanation": results['originality_explanation']
        },
        "Methodology Quality": {
            "Score": f"{results['methodology_quality_score'] * 10:.2f}",
            "Explanation": results['methodology_quality_explanation']
        },
        "Results and Discussion Quality": {
            "Score": f"{results['results_discussion_quality_score'] * 10:.2f}",
            "Explanation": results['results_discussion_quality_explanation']
        },
        "Potential Impact": {
            "Score": f"{results['potential_impact_score'] * 10:.2f}",
            "Explanation": results['potential_impact_explanation']
        },
        "Writing Clarity": {
            "Score": f"{results['writing_clarity_score'] * 10:.2f}",
            "Explanation": results['writing_clarity_explanation']
        },
        "References Timeliness": {
            "Score": f"{results['references_timeliness_score'] * 10:.2f}",
            "Explanation": results['references_timeliness_explanation']
        }
    }
    return formatted
# %%
# Example usage (commented out to avoid undefined variable errors)
# To test the evaluation function, use the test_integration.py file
# 
# Example:
# result = evaluate_research_paper("Your research paper text here", "Your TCC theme here")
# formatted_result = format_results_for_display(result)
# pprint.pprint(formatted_result)
# %%
