"""
Tests para el sistema de crew (orquestación de agentes).

Pruebas para verificar que el sistema multi-agente funciona correctamente
con la coordinación de tareas secuenciales.
"""

import pytest
from unittest.mock import patch, MagicMock, call
from multi_agent.agent import run_multi_agent_system


class TestMultiAgentSystem:
    """Tests para el sistema multi-agente."""

    @patch('multi_agent.agent.Crew')
    @patch('multi_agent.agent.Task')
    @patch('multi_agent.agent.get_escritor_agent')
    @patch('multi_agent.agent.get_programador_agent')
    def test_run_multi_agent_system_basic(
        self,
        mock_get_programador,
        mock_get_escritor,
        mock_task,
        mock_crew
    ):
        """Verifica que el sistema se ejecuta correctamente."""
        # Configurar mocks
        mock_programador = MagicMock()
        mock_escritor = MagicMock()
        mock_get_programador.return_value = mock_programador
        mock_get_escritor.return_value = mock_escritor

        mock_task1 = MagicMock()
        mock_task2 = MagicMock()
        mock_task.side_effect = [mock_task1, mock_task2]

        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = "Resultado esperado"
        mock_crew.return_value = mock_crew_instance

        # Ejecutar
        user_prompt = "Crea un script para analizar CSVs"
        resultado = run_multi_agent_system(user_prompt)

        # Verificaciones
        assert resultado == "Resultado esperado"
        mock_get_programador.assert_called_once()
        mock_get_escritor.assert_called_once()
        assert mock_task.call_count == 2
        mock_crew_instance.kickoff.assert_called_once()

    @patch('multi_agent.agent.Crew')
    @patch('multi_agent.agent.Task')
    @patch('multi_agent.agent.get_escritor_agent')
    @patch('multi_agent.agent.get_programador_agent')
    def test_run_multi_agent_system_task_sequence(
        self,
        mock_get_programador,
        mock_get_escritor,
        mock_task,
        mock_crew
    ):
        """Verifica que las tareas se ejecutan en secuencia correcta."""
        # Configurar mocks
        mock_programador = MagicMock()
        mock_escritor = MagicMock()
        mock_get_programador.return_value = mock_programador
        mock_get_escritor.return_value = mock_escritor

        mock_task1 = MagicMock()
        mock_task2 = MagicMock()
        mock_task.side_effect = [mock_task1, mock_task2]

        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance

        # Ejecutar
        user_prompt = "Test prompt"
        run_multi_agent_system(user_prompt)

        # Verificar que Task se llamó con los parámetros correctos
        calls = mock_task.call_args_list

        # Primera tarea: programación
        assert calls[0][1]['description'].startswith("Desarrolla lo siguiente:")
        assert calls[0][1]['agent'] == mock_programador
        assert "Código Python" in calls[0][1]['expected_output']

        # Segunda tarea: redacción
        assert "explicación detallada" in calls[1][1]['description'].lower()
        assert calls[1][1]['agent'] == mock_escritor
        assert "Markdown" in calls[1][1]['expected_output']
        # Verificar contexto (tarea anterior)
        assert calls[1][1]['context'] == [mock_task1]

    @patch('multi_agent.agent.Crew')
    @patch('multi_agent.agent.Task')
    @patch('multi_agent.agent.get_escritor_agent')
    @patch('multi_agent.agent.get_programador_agent')
    def test_run_multi_agent_system_crew_configuration(
        self,
        mock_get_programador,
        mock_get_escritor,
        mock_task,
        mock_crew
    ):
        """Verifica que la Crew se configura correctamente."""
        from crewai import Process

        # Configurar mocks
        mock_programador = MagicMock()
        mock_escritor = MagicMock()
        mock_get_programador.return_value = mock_programador
        mock_get_escritor.return_value = mock_escritor

        mock_task1 = MagicMock()
        mock_task2 = MagicMock()
        mock_task.side_effect = [mock_task1, mock_task2]

        mock_crew_instance = MagicMock()
        mock_crew.return_value = mock_crew_instance

        # Ejecutar
        run_multi_agent_system("Test")

        # Verificar configuración de Crew
        crew_call = mock_crew.call_args
        assert crew_call[1]['agents'] == [mock_programador, mock_escritor]
        assert crew_call[1]['tasks'] == [mock_task1, mock_task2]
        assert crew_call[1]['process'] == Process.sequential

    @patch('multi_agent.agent.Crew')
    @patch('multi_agent.agent.Task')
    @patch('multi_agent.agent.get_escritor_agent')
    @patch('multi_agent.agent.get_programador_agent')
    def test_run_multi_agent_system_with_different_prompts(
        self,
        mock_get_programador,
        mock_get_escritor,
        mock_task,
        mock_crew
    ):
        """Verifica que el sistema funciona con diferentes prompts."""
        # Configurar mocks
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

        # Pruebas con diferentes prompts
        prompts = [
            "Crea un script de análisis",
            "Haz un sistema de autenticación",
            "Desarrolla un API REST"
        ]

        for prompt in prompts:
            mock_task.reset_mock()
            mock_task.side_effect = [mock_task1, mock_task2]
            resultado = run_multi_agent_system(prompt)
            assert resultado == "resultado"
            # Verificar que el prompt está en la descripción de la tarea
            assert prompt in mock_task.call_args_list[0][1]['description']
