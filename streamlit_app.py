import streamlit as st
import os
import sys
import tempfile
import pprint

# Add the parent directory to sys.path to allow relative imports
# This is important if 'utils' and 'article_scout_agent' are not at the same level
# or if you are running Streamlit from a different directory.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import the PDF extractor from the utils folder
# Make sure the 'utils' folder exists and contains 'pdf_extractor.py'
try:
    from utils.pdf_extractor import extract_text_from_pdf
except ImportError:
    st.error("Error: Could not import 'extract_text_from_pdf' from the 'utils' folder.")
    st.info("Please ensure that the 'utils' folder exists and contains the 'pdf_extractor.py' file.")
    st.stop()

# Import the evaluation function from your Article Scout agent
# Make sure 'article_scout_agent.py' is in the same folder or in sys.path
try:
    from article_scout_agent import evaluate_research_paper
except ImportError:
    st.error("Error: Could not import 'evaluate_research_paper' from 'article_scout_agent.py'.")
    st.info("Please ensure that 'article_scout_agent.py' is in the same folder as 'streamlit_app.py'.")
    st.stop()

# Streamlit page configurations
st.set_page_config(page_title="Article Scout - Article Evaluator", layout="centered")

st.title("📚 Article Scout - Research Paper Evaluator for TCC")
st.markdown("""
    Upload a research paper in PDF format and provide your TCC (Final Project) theme.
    **Article Scout** will evaluate the relevance and other criteria of the paper for your work!
""")

# Input for the TCC theme
tcc_theme = st.text_input(
    "Your Article Theme:",
    placeholder="Ex: Applications of Machine Learning in Data Engineering",
    help="Describe the main theme of your Final Project (Article)."
)

# PDF file upload
uploaded_file = st.file_uploader("Upload the research paper in PDF", type="pdf")

# Button to start evaluation
if st.button("Evaluate Paper"):
    if uploaded_file is not None and tcc_theme:
        with st.spinner("Extracting text from PDF and evaluating the paper..."):
            # Save the PDF file temporarily so PyPDF2 can read it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_pdf_path = tmp_file.name

            # Extract text from the PDF
            article_text = extract_text_from_pdf(temp_pdf_path)

            # Remove the temporary file
            os.unlink(temp_pdf_path)

            if article_text:
                # Call the agent to evaluate the paper
                results = evaluate_research_paper(article_text, tcc_theme)

                st.success("Evaluation completed!")

                # Format the results for display with pprint
                formatted_results = {
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
                    },
                }
                
                st.subheader("Evaluation Results:")
                st.json(formatted_results) # Use st.json for formatted and expandable output

                # Optional: Display the extracted text for debugging
                with st.expander("View Full Extracted Text from PDF"):
                    st.text(article_text)

            else:
                st.error("Could not extract text from the PDF. Please check the file.")
    elif uploaded_file is None:
        st.warning("Please upload a PDF file.")
    elif not tcc_theme:
        st.warning("Please enter your TCC theme.")