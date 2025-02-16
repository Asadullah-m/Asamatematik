import streamlit as st
import openai
import os
import re
from dotenv import load_dotenv

# Indlæs miljøvariabler
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    client = openai.Client(api_key=api_key)
else:
    st.error("🚨 API-nøgle ikke fundet. Sørg for, at .env-filen indeholder OPENAI_API_KEY.")

# Matematiske emner for 5. klasse
topics = [
    "Brøker", "Geometri", "Areal af trekanter", "Divisor og primtal",
    "Ligninger", "Ligninger og regneudtryk", "Mål og enheder",
    "Hele koordinatsystemet", "Cirkler", "Skitse og tegning",
    "Statistiske undersøgelser", "Spil og simulering", "Indbrud i borgen"
]

# Funktion til at vise LaTeX korrekt
def display_math_response(response_text):
    latex_expressions = re.findall(r"\$\$(.*?)\$\$", response_text)
    text_parts = re.split(r"\$\$(.*?)\$\$", response_text)
    for i, part in enumerate(text_parts):
        if i % 2 == 0:
            st.write(part)
        else:
            st.latex(part)

# Opret Streamlit app
st.title("📚🤖 AI Matematikopgavegenerator")
st.write("💡 Vælg et matematikemne, og lad AI’en generere en opgave til dig!")

# Brugeren vælger et emne og sværhedsgrad
selected_topic = st.selectbox("📌 Vælg et emne:", topics)
difficulty = st.selectbox("📏 Vælg sværhedsgrad:", ["Let", "Mellem", "Svær"])
num_exercises = st.slider("🔢 Antal opgaver:", min_value=1, max_value=5, value=1)

# Generér opgave, når knappen trykkes
if st.button("🎲 Generér Opgaver"):
    st.subheader("📖 Dine matematikopgaver:")
    for i in range(num_exercises):
        prompt = f"""
        Lav en {difficulty} matematikopgave om {selected_topic} for 5. klasse på dansk.
        Strukturen skal være:
        - En kort introduktion om emnet.
        - En klart defineret opgave med et praktisk eksempel.
        - En trin-for-trin løsning forklaret pædagogisk.
        - Brug korrekt LaTeX-syntax til formler, fx: $$x + 7 = 12$$.
        - Afslut med en motiverende besked til eleverne.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du er en matematiklærer, der laver pædagogiske opgaver på dansk."},
                    {"role": "user", "content": prompt}
                ]
            )

            st.write(f"### 📝 Opgave {i+1}:")
            display_math_response(response.choices[0].message.content)

        except Exception as e:
            st.error(f"⚠️ Der opstod en fejl: {e}")

# Footer