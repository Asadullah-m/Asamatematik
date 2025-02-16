import streamlit as st
import re

def display_math_response(response_text):
    """Viser tekst og LaTeX formler korrekt i Streamlit."""
    latex_expressions = re.findall(r"\$\$(.*?)\$\$", response_text)
    text_parts = re.split(r"\$\$(.*?)\$\$", response_text)
    
    for i, part in enumerate(text_parts):
        if i % 2 == 0:
            st.write(part)
        else:
            st.latex(part)
