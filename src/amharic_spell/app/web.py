import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from amharic_spell.core.corrector import SpellCorrector

# Page Config
st.set_page_config(
    page_title="Amharic Spell Checker",
    page_icon="📝",
    layout="wide"
)

# Custom CSS for Amharic Fonts and Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Noto Sans Ethiopic', sans-serif;
    }
    .highlight-error {
        background-color: #ff4b4b4d;
        padding: 2px 4px;
        border-radius: 4px;
        text-decoration: underline;
        text-decoration-style: wavy;
        text-decoration-color: #ff4b4b;
    }
    .suggestion-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📝 Amharic Context-Aware Spell Checker")
st.markdown("Enter Amharic text below to detect and correct spelling errors using our **Interpolated N-gram Model**.")

# Sidebar for controls
st.sidebar.header("Configuration")
dictionary_path = st.sidebar.text_input("Dictionary Path", "data/amharic_dictionary.txt")
model_path = st.sidebar.text_input("Model Path", "models/ngram_model.pkl")

# Initialize Corrector
@st.cache_resource
def load_corrector(dict_path, mod_path):
    try:
        return SpellCorrector(dict_path, model_path=mod_path)
    except Exception as e:
        return None

corrector = load_corrector(dictionary_path, model_path)

if not corrector:
    st.error(f"Could not load model/dictionary. Please check paths and ensure you have trained the model.\n\nRun: `python scripts/train.py data/corpus.txt`")
else:
    st.sidebar.success("Model Loaded Successfully!")

# Main Input
text_input = st.text_area("Input Text", height=200, placeholder="የአማርኛ ጽሑፍ እዚህ ያስገቡ...")

if st.button("Check Spelling 🔍", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
    elif corrector:
        with st.spinner("Analyzing text..."):
            result = corrector.correct(text_input)
            
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Text")
            # Highlight errors
            highlighted_text = result["original_text"]
            for error in result["errors"]:
                word = error["word"]
                highlighted_text = highlighted_text.replace(word, f"<span class='highlight-error'>{word}</span>")
            st.markdown(highlighted_text, unsafe_allow_html=True)
            
        with col2:
            st.subheader("Corrected Text")
            st.success(result["corrected_text"])

        # Detailed Analysis
        if result["errors"]:
            st.divider()
            st.subheader("Detailed Analysis & Suggestions")
            
            for error in result["errors"]:
                word = error["word"]
                suggestions = error["suggestions"]
                context_str = " ".join(error.get("context", []))
                
                with st.expander(f"Error: **{word}**", expanded=True):
                    st.markdown(f"**Context:** ... {context_str} ...")
                    st.markdown("**Suggestions:**")
                    
                    for i, (sugg, score) in enumerate(suggestions):
                        st.markdown(f"{i+1}. **{sugg}** (Confidence: `{score:.4f}`)")
        else:
            st.balloons()
            st.info("No spelling errors found! ✅")

# Footer
st.markdown("---")
st.markdown("*Amharic Spell Checker Project - Built with Python & Streamlit*")
