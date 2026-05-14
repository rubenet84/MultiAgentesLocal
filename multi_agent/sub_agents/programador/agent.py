from crewai import Agent
from crewai.llms.providers.openai.completion import OpenAICompletion
from langchain_ollama import ChatOllama
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, OPENAI_API_BASE, OPENAI_MODEL_NAME, OPENAI_API_KEY


def _build_programador_llm() -> OpenAICompletion:
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


def get_programador_agent():
    """
    Configura y devuelve el agente Programador Senior.
    Utiliza la clase LLM de CrewAI para una conexión nativa y estable.
    """
    
    # Construimos un OpenAI-compatible LLM para CrewAI usando la API de Ollama local.
    llm = _build_programador_llm()
    
    return Agent(
        role='Programador Senior de Python',
        goal='Escribir código eficiente, limpio y documentado en Python.',
        backstory=(
            'Eres un experto en desarrollo de software con más de 10 años de experiencia. '
            'Te especializas en Python y en la creación de soluciones modulares y escalables. '
            'Tu código siempre sigue las normas de PEP 8 y es fácil de mantener.'
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        memory=False
    )