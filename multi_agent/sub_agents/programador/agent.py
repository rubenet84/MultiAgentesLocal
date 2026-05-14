from crewai import Agent
from langchain_ollama import ChatOllama
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

def get_programador_agent():
    """
    Configura y devuelve el agente Programador Senior.
    Utiliza la clase LLM de CrewAI para una conexión nativa y estable.
    """
    
    # Inicializamos el LLM usando ChatOllama para Ollama local
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
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