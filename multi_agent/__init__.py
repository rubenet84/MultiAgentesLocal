"""
Paquete principal multi_agent.

Exporta las funciones y clases públicas del sistema de multi-agentes.
"""

from multi_agent.agent import run_multi_agent_system
from multi_agent.sub_agents.programador.agent import get_programador_agent
from multi_agent.sub_agents.escritor.agent import get_escritor_agent

__version__ = "1.0.0"
__author__ = "Tu Nombre"
__all__ = [
    "run_multi_agent_system",
    "get_programador_agent",
    "get_escritor_agent",
]
