from crewai import Agent
from langchain_ollama import ChatOllama

def get_programador_agent():
    # Configuración del modelo local
    llm = ChatOllama(
        model="qwen2.5-coder:latest", 
        base_url="http://localhost:11434"
    )
    
    return Agent(
        role='Programador Senior de Python',
        goal='Escribir código eficiente, limpio y documentado en Python.',
        backstory='Eres un experto en desarrollo de software con 10 años de experiencia. '
                'Te especializas en crear scripts robustos y automatizaciones inteligentes.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )