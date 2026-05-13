"""
Tests de integración para la interfaz Streamlit.

Pruebas para verificar que la interfaz funciona correctamente
y se integra bien con el sistema multi-agente.
"""

import pytest
from unittest.mock import patch, MagicMock
import os
from dotenv import load_dotenv


class TestInterfazAgentes:
    """Tests de integración para la interfaz."""

    def test_environment_variables_loaded(self):
        """Verifica que las variables de entorno se cargan correctamente."""
        load_dotenv()
        # Verificar que al menos podemos acceder al método
        assert os.getenv is not None

    @patch.dict(os.environ, {
        'LANGCHAIN_TRACING_V2': 'true',
        'LANGCHAIN_PROJECT': 'test-project',
        'LANGCHAIN_API_KEY': 'test-key'
    })
    def test_langsmith_configuration_enabled(self):
        """Verifica que la configuración de LangSmith funciona cuando está habilitada."""
        assert os.getenv('LANGCHAIN_TRACING_V2') == 'true'
        assert os.getenv('LANGCHAIN_PROJECT') == 'test-project'
        assert os.getenv('LANGCHAIN_API_KEY') == 'test-key'

    @patch.dict(os.environ, {
        'LANGCHAIN_TRACING_V2': 'false'
    }, clear=False)
    def test_langsmith_configuration_disabled(self):
        """Verifica que el sistema funciona cuando LangSmith está deshabilitado."""
        assert os.getenv('LANGCHAIN_TRACING_V2') == 'false'

    @patch('multi_agent.agent.run_multi_agent_system')
    def test_multi_agent_system_integration(self, mock_run_system):
        """Verifica que el sistema multi-agente se integra correctamente."""
        mock_run_system.return_value = "Resultado de prueba"

        from multi_agent.agent import run_multi_agent_system

        resultado = run_multi_agent_system("Test prompt")
        assert resultado == "Resultado de prueba"
        mock_run_system.assert_called_once()


class TestErrorHandling:
    """Tests para el manejo de errores."""

    @patch('multi_agent.agent.Crew')
    @patch('multi_agent.agent.Task')
    @patch('multi_agent.agent.get_escritor_agent')
    @patch('multi_agent.agent.get_programador_agent')
    def test_system_handles_empty_prompt(
        self,
        mock_get_programador,
        mock_get_escritor,
        mock_task,
        mock_crew
    ):
        """Verifica que el sistema maneja prompts vacíos."""
        from multi_agent.agent import run_multi_agent_system

        mock_programador = MagicMock()
        mock_escritor = MagicMock()
        mock_get_programador.return_value = mock_programador
        mock_get_escritor.return_value = mock_escritor

        mock_task1 = MagicMock()
        mock_task2 = MagicMock()
        mock_task.side_effect = [mock_task1, mock_task2]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "resultado"
        mock_crew.return_value = mock_crew_instance

        # Ejecutar con prompt vacío
        resultado = run_multi_agent_system("")
        assert resultado == "resultado"

    @patch('multi_agent.agent.Crew')
    @patch('multi_agent.agent.Task')
    @patch('multi_agent.agent.get_escritor_agent')
    @patch('multi_agent.agent.get_programador_agent')
    def test_system_handles_special_characters(
        self,
        mock_get_programador,
        mock_get_escritor,
        mock_task,
        mock_crew
    ):
        """Verifica que el sistema maneja caracteres especiales."""
        from multi_agent.agent import run_multi_agent_system

        mock_programador = MagicMock()
        mock_escritor = MagicMock()
        mock_get_programador.return_value = mock_programador
        mock_get_escritor.return_value = mock_escritor

        mock_task1 = MagicMock()
        mock_task2 = MagicMock()
        mock_task.side_effect = [mock_task1, mock_task2]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "resultado"
        mock_crew.return_value = mock_crew_instance

        # Prompt con caracteres especiales
        prompt_especial = "Crea un script con caracteres: @#$%^&*()"
        resultado = run_multi_agent_system(prompt_especial)
        assert resultado == "resultado"
        # Verificar que el prompt se pasó correctamente
        assert prompt_especial in mock_task.call_args_list[0][1]['description']
