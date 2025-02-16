import streamlit as st
from src.generator import generate_explanation, generate_exercise, generate_solution, generate_hint
from src.utils import display_math_response

def show_ui():
    """Viser brugergrænsefladen til AI Matematikopgavegeneratoren med én opgave ad gangen."""

    topics = [
        "Brøker", "Geometri", "Areal af trekanter", "Divisor og primtal",
        "Ligninger", "Ligninger og regneudtryk", "Mål og enheder",
        "Hele koordinatsystemet", "Cirkler", "Skitse og tegning",
        "Statistiske undersøgelser", "Spil og simulering", "Indbrud i borgen"
    ]

    st.title("📚🤖 AI Matematikopgavegenerator")
    st.write("💡 Vælg et matematikemne, og lad mig forklare og give dig opgaver!")

    selected_topic = st.selectbox("📌 Vælg et emne:", topics)
    difficulty = st.selectbox("📏 Vælg sværhedsgrad:", ["Let", "Mellem", "Svær"])

    # 📚 Gemmer forklaring i session state
    if "explanation" not in st.session_state:
        st.session_state.explanation = None

    if st.button("📖 Forklar emnet"):
        st.session_state.explanation = generate_explanation(selected_topic)
    
    if st.session_state.explanation:
        st.subheader(f"📚 Forklaring af {selected_topic}")
        display_math_response(st.session_state.explanation)

        if st.button("🆘 Få hjælp til forklaringen"):
            hint = generate_hint(st.session_state.explanation)
            st.write(f"💡 **Alternativ forklaring:** {hint}")

    # 🔄 Session State til opgaveflow
    if "current_exercise" not in st.session_state:
        st.session_state.current_exercise = None
    if "exercise_solution" not in st.session_state:
        st.session_state.exercise_solution = None
    if "exercise_attempt" not in st.session_state:
        st.session_state.exercise_attempt = None

    if st.button("🎲 Giv mig en opgave"):
        st.session_state.current_exercise = generate_exercise(selected_topic, difficulty)
        st.session_state.exercise_solution = generate_solution(selected_topic, st.session_state.current_exercise)
        st.session_state.exercise_attempt = None  # Nulstil svar

    if st.session_state.current_exercise:
        st.subheader("📝 Opgave:")
        display_math_response(st.session_state.current_exercise)

        # Elevens svar
        st.session_state.exercise_attempt = st.text_area("✍️ Skriv din løsning her:")

        if st.button("✅ Tjek mit svar"):
            if st.session_state.exercise_attempt:  # Eleven har skrevet noget
                st.write("### ✅ Løsning:")
                display_math_response(st.session_state.exercise_solution)

                # Spørg eleven om de vil prøve igen
                st.write("Vil du prøve en ny opgave?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Jeg vil prøve igen"):
                        st.session_state.current_exercise = generate_exercise(selected_topic, difficulty)
                        st.session_state.exercise_solution = generate_solution(selected_topic, st.session_state.current_exercise)
                        st.session_state.exercise_attempt = None  # Nulstil svar
                with col2:
                    if st.button("❌ Nej, jeg er færdig"):
                        st.session_state.current_exercirse = None
                        st.session_state.exercise_solution = None
                        st.session_state.exercise_attempt = None
