import streamlit as st
from langchain_openai import ChatOpenAI
from openai import APIError

st.set_page_config(page_title="telc B1 Deutsch Tutor", page_icon="🇩🇪")
st.title("🇩🇪 telc B1 Deutsch Tutor")

tab1, tab2, tab3 = st.tabs([
    "Schriftlicher Ausdruck (Writing)",
    "Sprachbausteine (Fill-in-the-blanks)",
    "Mündliche Prüfung (Speaking Simulation)"
])

def get_model():
    openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        st.error("OPENROUTER_API_KEY not found in Streamlit secrets.")
        st.stop()
    return ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=openrouter_api_key,
        temperature=0.3,
        model_name="google/gemma-4-26b-a4b-it"
    )

model = get_model()

with tab1:
    st.subheader("Schriftlicher Ausdruck – Textkorrektur")
    user_text = st.text_area(
        "Füge einen Text ein:",
        height=150,
        key="writing_input"
    )
    if st.button("Korrigieren & Bewerten", key="writing_btn"):
        prompt = (
            "Du bist ein professioneller Deutschlehrer für die Prüfung telc B1. "
            "Korrigiere den Benutzer, wenn er Fehler macht. "
            "Antworte nur auf Deutsch, benutze einfache B1-Vokabeln, erkläre Grammatikfehler auf leicht verständliche Weise und bewerte seine Antworten. "
            "Bitte korrigiere meinen Text und bewerte ihn nach den Kriterien der telc B1 Prüfung. "
            "Achte auf Rechtschreibung, Grammatik, Satzbau und Wortschatz. Zeige mir meine Fehler und verbessere sie."
            f"\nText:\n{user_text}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**Feedback:**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)

with tab2:
    st.subheader("Sprachbausteine – Lückentext")
    grammar_question = st.text_input(
        "Bitte gib einen Grammatikbereich ein:",
        key="grammar_input"
    )
    if st.button("Text generieren & erklären", key="grammar_btn"):
        prompt = (
            "Du bist ein Deutschlehrer auf Niveau B1. "
            "Erstelle einen kurzen Lückentext und zeige die Lösungen an. "
            "Erkläre danach die Grammatikregeln für die Lücken einfach.\n\n"
            f"Übungswunsch: {grammar_question}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**Lückentext & Erklärung:**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)

with tab3:
    st.subheader("Mündliche Prüfung – Rollenspiel")
    speaking_prompt = st.text_input(
        "Gib ein Thema oder eine Prüfungssituation ein:",
        key="spoken_input"
    )
    if st.button("Simulation starten", key="speaking_btn"):
        prompt = (
            "Du bist ein Prüfungspartner in der mündlichen telc B1 Prüfung. "
            "Reagiere als Dialogpartner in einer realistischen Prüfung, antworte nur auf Deutsch, benutze einfaches B1-Deutsch. "
            "Verbessere und bewerte, falls nötig.\n\n"
            f"Situation: {speaking_prompt}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**Prüfungssimulation:**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)
