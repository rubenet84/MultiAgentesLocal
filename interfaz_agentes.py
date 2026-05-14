import os
import sys
import time
from dotenv import load_dotenv

# 1. CARGA DE VARIABLES Y CONFIGURACIÓN DE ENTORNO
load_dotenv()

# Eliminar claves placeholder OpenAI para evitar errores 401
if os.getenv("OPENAI_API_KEY", "").strip().lower() in {"", "na", "null", "none"}:
    os.environ.pop("OPENAI_API_KEY", None)

# Forzamos los endpoints según tu configuración de LangSmith en Europa
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://eu.api.smith.langchain.com"
# Aseguramos que CrewAI trace las ejecuciones si el proyecto lo permite
os.environ.setdefault("CREWAI_TRACING_ENABLED", "true")

# Forzar salida UTF-8 en Windows para evitar errores con emojis
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Importaciones de librerías (después de cargar el entorno)
import streamlit as st
from uuid import uuid4
from langsmith import Client
import langsmith.schemas as schemas
from multi_agent.agent import run_multi_agent_system

# 2. DIAGNÓSTICO ROBUSTO (Sin errores de 'whoami')
print(f"--- COMPROBANDO CONEXIÓN ---")
print(f"📂 Proyecto: {os.getenv('LANGCHAIN_PROJECT')}")
print(f"🌐 Endpoint: {os.getenv('LANGCHAIN_ENDPOINT')}")

client = Client(
    api_url=os.getenv("LANGCHAIN_ENDPOINT"),
    api_key=os.getenv("LANGCHAIN_API_KEY"),
)
try:
    # Usamos list_projects en lugar de whoami para evitar el error de atributo
    client.list_projects()
    print("✅ LangSmith: Conexión establecida con éxito.")
except Exception as e:
    # Si falla, lanzamos un aviso pero permitimos que Streamlit siga adelante
    print(f"⚠️ LangSmith: Aviso de conexión (el tracing intentará funcionar igual).")
    print(f"Detalle: {e}")

# 3. CONFIGURACIÓN DE LA INTERFAZ STREAMLIT
st.set_page_config(page_title="Multi-Agente Profesional", layout="wide")
st.title("🤖 Sistema Modular de Agentes")
st.markdown(f"**Estado del Tracing:** {'Activado ✅' if os.getenv('LANGCHAIN_TRACING_V2') == 'true' else 'Desactivado ❌'}")

# Entrada del usuario
user_input = st.text_area(
    "¿Qué quieres que construya hoy?", 
    placeholder="Ej: Escribe un script en Python para automatizar el envío de correos...",
    height=150
)

# 4. EJECUCIÓN DEL SISTEMA
if st.button("Lanzar Equipo"):
    if user_input:
        with st.spinner("El equipo de agentes está trabajando con Ollama..."):
            root_run_id = None
            try:
                root_run_id = uuid4()
                client.create_run(
                    id=root_run_id,
                    name="Ejecución Multi-Agente",
                    inputs={
                        "user_prompt": user_input,
                    },
                    run_type=schemas.RunTypeEnum.chain,
                    project_name=os.getenv("LANGCHAIN_PROJECT"),
                    metadata={
                        "source": "MultiAgentesLocal",
                        "agents": ["Programador", "Escritor"],
                    },
                )
            except Exception as e:
                print(f"⚠️ No se ha podido crear el run raíz en LangSmith: {e}")
                root_run_id = None

            try:
                # Ejecución del sistema multi-agente
                resultado = run_multi_agent_system(
                    user_input,
                    langsmith_client=client,
                    root_run_id=root_run_id,
                )

                st.divider()
                st.subheader("📝 Resultado Final:")
                st.markdown(resultado or "No se obtuvo ningún resultado.", unsafe_allow_html=False)

                try:
                    client.create_run(
                        id=uuid4(),
                        name="Resultado Final",
                        inputs={
                            "user_prompt": user_input,
                        },
                        outputs={
                            "final_output": resultado,
                        },
                        run_type=schemas.RunTypeEnum.chain,
                        project_name=os.getenv("LANGCHAIN_PROJECT"),
                        parent_run_id=root_run_id,
                        metadata={
                            "phase": "final",
                            "source": "MultiAgentesLocal",
                        },
                    )
                    st.success("¡Tarea completada y registrada en LangSmith con trazas de tareas!")
                except Exception as e:
                    st.warning(f"No se pudo enviar la traza final a LangSmith: {e}")
                    st.success("¡Tarea completada! Revisa tu panel en LangSmith si ya existía conexión.")

            except Exception as e:
                st.error(f"Se produjo un error durante la ejecución: {e}")
                print(f"❌ Error en el sistema: {e}")
    else:
        st.warning("Por favor, introduce una instrucción para los agentes.")