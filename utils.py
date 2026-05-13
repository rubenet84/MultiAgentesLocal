"""
Módulo de utilidades compartidas.

Funciones y clases auxiliares utilizadas en todo el proyecto.
"""

import logging
from typing import Optional
from config import LOG_LEVEL, LANGCHAIN_TRACING_V2

# Configurar logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def get_logger(name: str) -> logging.Logger:
    """Obtener logger configurado para un módulo.
    
    Args:
        name: Nombre del módulo.
    
    Returns:
        Logger: Logger configurado.
    """
    return logging.getLogger(name)


def validate_input(input_text: str, max_length: int = 5000) -> tuple[bool, Optional[str]]:
    """Validar entrada del usuario.
    
    Args:
        input_text: Texto a validar.
        max_length: Longitud máxima permitida.
    
    Returns:
        Tupla (es_válido, mensaje_error).
    """
    if not input_text or not input_text.strip():
        return False, "El input no puede estar vacío."
    
    if len(input_text) > max_length:
        return False, f"El input excede {max_length} caracteres."
    
    return True, None


def log_agent_execution(agent_name: str, task_description: str) -> None:
    """Log la ejecución de un agente.
    
    Args:
        agent_name: Nombre del agente.
        task_description: Descripción de la tarea.
    """
    logger = get_logger(__name__)
    logger.info(f"Ejecutando agente: {agent_name}")
    logger.debug(f"Tarea: {task_description}")


def print_execution_status(status: str, details: Optional[str] = None) -> None:
    """Imprimir estado de ejecución de forma amigable.
    
    Args:
        status: Estado (processing, completed, error).
        details: Detalles adicionales.
    """
    emojis = {
        "processing": "⏳",
        "completed": "✅",
        "error": "❌",
        "info": "ℹ️",
        "warning": "⚠️"
    }
    
    emoji = emojis.get(status, "•")
    message = f"{emoji} {details}" if details else emoji
    print(message)
