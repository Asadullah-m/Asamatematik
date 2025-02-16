import openai
import os
from dotenv import load_dotenv

# Indlæs API-nøgle
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.Client(api_key=api_key) if api_key else None

def generate_explanation(topic):
    """Genererer en forklaring af emnet med eksempler."""
    prompt = f"""
    Forklar begrebet {topic} for en 5. klasse elev på en pædagogisk måde.
    - Start med en letforståelig introduktion.
    - Giv mindst ét praktisk eksempel, som elever kan relatere til.
    - Brug venlige og motiverende sætninger.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du er en matematiklærer, der forklarer emner på en pædagogisk måde."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def generate_exercise(topic, difficulty):
    """Genererer en matematikopgave relateret til emnet UDEN at give løsningen."""
    prompt = f"""
    Lav en {difficulty} matematikopgave om {topic} for en 5. klasse elev.
    - Opgaven skal være praktisk og let at forstå.
    - Giv IKKE løsningen eller nogen hints.
    - Stil spørgsmålet klart og tydeligt.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du er en matematiklærer, der laver opgaver til elever uden at give svaret direkte."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def generate_solution(topic, exercise_text):
    """Genererer en forklaring og løsning på en matematikopgave."""
    prompt = f"""
    Giv en trin-for-trin løsning til denne matematikopgave relateret til {topic}:
    {exercise_text}

    Forklar løsningen på en pædagogisk måde, så en 5. klasse elev kan forstå det.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du er en matematiklærer, der forklarer løsninger pædagogisk."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def generate_hint(text):
    """Genererer et hint til en opgave eller forklaring."""
    prompt = f"""
    Eleven har svært ved at forstå følgende: {text}

    Giv et kort hint eller en alternativ forklaring, der hjælper dem uden at afsløre svaret helt.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Du er en hjælpsom matematiklærer, der giver hints til elever."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
