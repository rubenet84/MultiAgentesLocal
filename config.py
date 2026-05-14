"""
Archivo de configuración centralizada para el proyecto.

Define todas las constantes y configuraciones globales del sistema.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Eliminar claves OpenAI placeholder que rompen las llamadas si no se usan
def _normalize_api_key(value: str | None) -> str | None:
    if value is None:
        return None
    if value.strip().lower() in {"", "na", "null", "none"}:
        return None
    return value

OPENAI_API_KEY = _normalize_api_key(os.getenv("OPENAI_API_KEY"))
if OPENAI_API_KEY is None:
    os.environ.pop("OPENAI_API_KEY", None)

os.environ.setdefault("CREWAI_TRACING_ENABLED", "true")

# ==================== CONFIGURACIÓN OLLAMA ====================
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")

# ==================== CONFIGURACIÓN LANGSMITH ====================
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# ==================== CONFIGURACIÓN DE AGENTES ====================
PROGRAMADOR_ROLE = "Programador Senior de Python"
PROGRAMADOR_GOAL = "Escribir código eficiente, limpio y documentado en Python."
PROGRAMADOR_BACKSTORY = (
    "Eres un experto en desarrollo de software con 10 años de experiencia. "
    "Te especializas en crear scripts robustos y automatizaciones inteligentes."
)

ESCRITOR_ROLE = "Escritor Técnico"
ESCRITOR_GOAL = "Redactar artículos y documentación clara basada en código técnico."
ESCRITOR_BACKSTORY = (
    "Eres un redactor experto capaz de explicar conceptos complejos "
    "de forma sencilla para cualquier público."
)

# ==================== CONFIGURACIÓN DE STREAMLIT ====================
STREAMLIT_PAGE_TITLE = "Multi-Agente Profesional"
STREAMLIT_LAYOUT = "wide"
STREAMLIT_PAGE_ICON = "🤖"

# ==================== CONFIGURACIÓN DE TAREAS ====================
TASK_EXPECTED_OUTPUT_CODE = "Código Python completo y funcional."
TASK_EXPECTED_OUTPUT_DOCS = "Un artículo en formato Markdown explicando el funcionamiento del código."

# ==================== LOGGING ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
VERBOSE_MODE = os.getenv("VERBOSE_MODE", "true").lower() == "true"
