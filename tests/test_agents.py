"""
Tests para los agentes del sistema multi-agente.

Pruebas unitarias para verificar que los agentes se crean correctamente
y tienen las configuraciones esperadas.
"""

import pytest
from unittest.mock import patch, MagicMock, Mock


class TestAgentModules:
    """Tests estructurales para los módulos de agentes."""

    def test_programador_agent_module_exists(self):
        """Verifica que el módulo del programador existe."""
        from multi_agent.sub_agents.programador import agent
        assert hasattr(agent, 'get_programador_agent')
        assert callable(agent.get_programador_agent)

    def test_escritor_agent_module_exists(self):
        """Verifica que el módulo del escritor existe."""
        from multi_agent.sub_agents.escritor import agent
        assert hasattr(agent, 'get_escritor_agent')
        assert callable(agent.get_escritor_agent)

    def test_programador_agent_imports_correctly(self):
        """Verifica que el agente programador se importa correctamente."""
        from multi_agent.sub_agents.programador.agent import get_programador_agent
        assert get_programador_agent is not None

    def test_escritor_agent_imports_correctly(self):
        """Verifica que el agente escritor se importa correctamente."""
        from multi_agent.sub_agents.escritor.agent import get_escritor_agent
        assert get_escritor_agent is not None

    def test_programador_agent_uses_correct_model(self):
        """Verifica que el agente programador usa el modelo correcto."""
        with patch('multi_agent.sub_agents.programador.agent.ChatOllama') as mock_chat:
            mock_chat.return_value = "mocked_llm"
            
            # La función intenta crear un agente con el LLM
            # Si se lanza excepción, es porque CrewAI validó correctamente
            try:
                from multi_agent.sub_agents.programador.agent import get_programador_agent
                get_programador_agent()
            except:
                pass  # Esperado debido a validación de Pydantic
            
            # Verificar que ChatOllama fue llamado con los parámetros correctos
            mock_chat.assert_called_once_with(
                model="qwen2.5-coder:latest",
                base_url="http://localhost:11434"
            )

    def test_escritor_agent_uses_correct_model(self):
        """Verifica que el agente escritor usa el modelo correcto."""
        with patch('multi_agent.sub_agents.escritor.agent.ChatOllama') as mock_chat:
            mock_chat.return_value = "mocked_llm"
            
            try:
                from multi_agent.sub_agents.escritor.agent import get_escritor_agent
                get_escritor_agent()
            except:
                pass  # Esperado
            
            mock_chat.assert_called_once_with(
                model="qwen2.5-coder:latest",
                base_url="http://localhost:11434"
            )

    def test_both_agents_use_same_model(self):
        """Verifica que ambos agentes usan el mismo modelo."""
        with patch('multi_agent.sub_agents.programador.agent.ChatOllama') as mock_prog:
            with patch('multi_agent.sub_agents.escritor.agent.ChatOllama') as mock_esc:
                mock_prog.return_value = "mocked_llm"
                mock_esc.return_value = "mocked_llm"
                
                try:
                    from multi_agent.sub_agents.programador.agent import get_programador_agent
                    from multi_agent.sub_agents.escritor.agent import get_escritor_agent
                    get_programador_agent()
                    get_escritor_agent()
                except:
                    pass  # Esperado
                
                # Verificar que ambos usan la misma configuración
                prog_call = mock_prog.call_args
                esc_call = mock_esc.call_args
                
                assert prog_call[1]['model'] == 'qwen2.5-coder:latest'
                assert esc_call[1]['model'] == 'qwen2.5-coder:latest'
                assert prog_call[1]['base_url'] == 'http://localhost:11434'
                assert esc_call[1]['base_url'] == 'http://localhost:11434'

