"""
Configuración compartida para los tests.

Define fixtures y configuraciones globales para todas las pruebas.
"""

import pytest
import sys
from pathlib import Path

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_ollama_model():
    """Fixture que proporciona un modelo Ollama mockeado."""
    from unittest.mock import MagicMock
    mock_model = MagicMock()
    mock_model.model = "qwen2.5-coder:latest"
    mock_model.base_url = "http://localhost:11434"
    return mock_model


@pytest.fixture
def test_prompt():
    """Fixture que proporciona un prompt de prueba."""
    return "Crea un script Python que lea un archivo CSV"


@pytest.fixture
def expected_code_output():
    """Fixture que proporciona un código de salida esperado."""
    return """import csv
import pandas as pd

def read_csv_file(filepath):
    '''Lee un archivo CSV y retorna un DataFrame'''
    return pd.read_csv(filepath)
"""


@pytest.fixture
def expected_documentation_output():
    """Fixture que proporciona documentación esperada."""
    return """# Análisis de Archivo CSV

Este script permite leer y procesar archivos CSV de manera eficiente...
"""
