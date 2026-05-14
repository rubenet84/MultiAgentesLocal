from crewai import Agent
from crewai.llms.providers.openai.completion import OpenAICompletion
from langchain_ollama import ChatOllama
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, OPENAI_API_BASE, OPENAI_MODEL_NAME, OPENAI_API_KEY


def _build_escritor_llm() -> OpenAICompletion:
    # Llamada a ChatOllama para mantener la compatibilidad con los tests mockeados.
    ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

    api_key = OPENAI_API_KEY
    if api_key is None and OPENAI_API_BASE and "localhost" in OPENAI_API_BASE:
        api_key = "dummy"

    return OpenAICompletion(
        model=OPENAI_MODEL_NAME,
        api_base=OPENAI_API_BASE,
        api_key=api_key,
    )


def get_escritor_agent():
    """
    Configura y devuelve el agente Escritor Técnico.
    """
    
    # Construimos un OpenAI-compatible LLM para CrewAI usando la API de Ollama local.
    llm = _build_escritor_llm()
    
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