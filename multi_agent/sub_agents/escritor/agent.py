from crewai import Agent
from langchain_ollama import ChatOllama

def get_escritor_agent():
    llm = ChatOllama(model="qwen2.5-coder:latest", base_url="http://localhost:11434")
    
    return Agent(
        role='Escritor Técnico',
        goal='Redactar artículos y documentación clara basada en código técnico.',
        backstory='Eres un redactor experto capaz de explicar conceptos complejos '
                'de forma sencilla para cualquier público.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )