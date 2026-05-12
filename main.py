import streamlit as st
from langchain_openai import ChatOpenAI
from openai import APIError

st.set_page_config(page_title="DELE B1 Español Tutor", page_icon="🇪🇸")
st.title("🇪🇸 DELE B1 Español Tutor")

tab1, tab2, tab3 = st.tabs([
    "Expresión Escrita (Writing)",
    "Gramática (Fill-in-the-blanks)",
    "Expresión Oral (Speaking Simulation)"
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

# --- Tab 1: Writing correction ---
with tab1:
    st.subheader("Expresión Escrita – Corrección de Texto")
    user_text = st.text_area(
        "Escribe tu texto (p.ej. una carta formal, un correo electrónico, una queja):",
        height=150,
        key="writing_input"
    )
    if st.button("Corregir & Evaluar", key="writing_btn"):
        prompt = (
            "Eres un profesor profesional de español para el examen DELE B1. "
            "Corrige al usuario cuando comete errores. "
            "Responde solo en español, usa vocabulario sencillo de nivel B1, "
            "explica los errores gramaticales de forma clara y evalúa sus respuestas. "
            "Por favor, corrige mi texto y evalúalo según los criterios del examen DELE B1. "
            "Presta atención a la ortografía, gramática, estructura de las oraciones y vocabulario. "
            "Muéstrame mis errores y corrígelos."
            f"\nTexto:\n{user_text}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**Feedback:**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)

# --- Tab 2: Grammar fill-in-the-blanks ---
with tab2:
    st.subheader("Gramática – Ejercicio de Huecos")
    st.write("Pide un ejercicio de rellenar huecos o explicaciones gramaticales (p.ej. ser/estar, subjuntivo, por/para).")
    grammar_question = st.text_input(
        "Introduce un tema gramatical o pide un texto de práctica:",
        key="grammar_input"
    )
    if st.button("Generar ejercicio", key="grammar_btn"):
        prompt = (
            "Eres un profesor de español de nivel B1. "
            "Crea un texto corto con huecos para rellenar y muestra las soluciones. "
            "Explica después las reglas gramaticales de los huecos de forma sencilla.\n\n"
            f"Tema de práctica: {grammar_question}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**Ejercicio & Explicación:**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)

# --- Tab 3: Speaking simulation ---
with tab3:
    st.subheader("Expresión Oral – Simulación de Examen")
    st.write("Simula una conversación del examen DELE B1. Escribe tu respuesta como si estuvieras hablando.")
    speaking_prompt = st.text_input(
        "Introduce un tema o situación (p.ej. planificar unas vacaciones con un amigo):",
        key="spoken_input"
    )
    if st.button("Iniciar simulación", key="speaking_btn"):
        prompt = (
            "Eres un compañero de examen en la prueba oral del DELE B1. "
            "Reacciona como interlocutor en un examen realista, responde solo en español, "
            "usa español sencillo de nivel B1. "
            "Corrige y evalúa si es necesario.\n\n"
            f"Situación: {speaking_prompt}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**Simulación del Examen:**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)
