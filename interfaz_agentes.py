import streamlit as st
import os
from dotenv import load_dotenv
from multi_agent.agent import run_multi_agent_system

load_dotenv()

if os.getenv("LANGCHAIN_TRACING_V2") == "true":
    print(f"🚀 Conectando a LangSmith...")
    print(f"📂 Proyecto: {os.getenv('LANGCHAIN_PROJECT')}")
    if not os.getenv("LANGCHAIN_API_KEY"):
        print("❌ ERROR: No se encuentra la API KEY en el .env")
else:
    print("⚠️ El rastreo (tracing) está desactivado.")

st.set_page_config(page_title="Multi-Agente Profesional", layout="wide")
st.title("🤖 Sistema Modular de Agentes")

user_input = st.text_area("¿Qué quieres que construya hoy?", placeholder="Ej: Haz un script para analizar CSVs...")

if st.button("Lanzar Equipo"):
    if user_input:
        with st.spinner("El equipo está trabajando..."):
            resultado = run_multi_agent_system(user_input)
            st.markdown("### 📝 Resultado Final:")
            st.write(resultado)
    else:
        st.warning("Por favor, escribe algo.")