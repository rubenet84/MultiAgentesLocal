from crewai import Agent
from langchain_ollama import ChatOllama
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

def get_escritor_agent():
    """
    Configura y devuelve el agente Escritor Técnico.
    """
    
    # Inicializamos el LLM usando ChatOllama para Ollama local
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    return Agent(
        role='Escritor Técnico',
        goal='Redactar artículos y documentación clara basada en código técnico.',
        backstory=(
            'Eres un redactor experto capaz de explicar conceptos complejos '
            'de forma sencilla para cualquier público.'
        ),
        llm=llm,
        allow_delegation=False,
        verbose=True,
        memory=False
    )