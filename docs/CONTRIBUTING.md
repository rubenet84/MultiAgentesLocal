# MultiAgentesLocal - Guía de Contribución

## 🤝 Cómo Contribuir

¡Gracias por tu interés en contribuir a MultiAgentesLocal! Esta guía te ayudará a empezar.

### 📋 Requisitos Previos

- Python 3.11+
- Git
- Ollama instalado localmente
- Conocimiento básico de CrewAI y LangChain

### 🚀 Pasos para Contribuir

#### 1. Fork y Clonar

```bash
# Fork el repositorio en GitHub
# Luego clona tu fork
git clone https://github.com/tu-usuario/MultiAgentesLocal.git
cd MultiAgentesLocal
```

#### 2. Crear Rama

```bash
# Crea una rama con un nombre descriptivo
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correcion-de-bug
```

#### 3. Configurar Entorno Local

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # Linux/macOS

# Instalar dependencias
pip install -r requirements.txt

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt  # Si existe
```

#### 4. Hacer Cambios

- Sigue los estándares de código
- Agrega tests para nuevas funcionalidades
- Mantén la documentación actualizada

#### 5. Tests

```bash
# Ejecutar tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=multi_agent --cov-report=html
```

#### 6. Commit y Push

```bash
# Verificar cambios
git status

# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "feat: agregar nueva funcionalidad de X"
# o
git commit -m "fix: corregir bug en Y"
# o
git commit -m "docs: actualizar documentación de Z"

# Push
git push origin feature/nueva-funcionalidad
```

#### 7. Pull Request

- Ve a GitHub
- Crea un PR hacia la rama `main`
- Describe tus cambios en detalle
- Espera revisión

### 📝 Estándares de Código

#### Python Style Guide

Seguimos [PEP 8](https://www.python.org/dev/peps/pep-0008/):

```python
# ✅ Correcto
def get_programador_agent() -> Agent:
    """Obtiene el agente programador.
    
    Returns:
        Agent: Agente configurado.
    """
    llm = ChatOllama(model="qwen2.5-coder:7b")
    return Agent(
        role="Programador",
        goal="Escribir código limpio",
        llm=llm
    )

# ❌ Incorrecto
def get_agent():
    llm=ChatOllama(model="qwen2.5-coder:7b")
    return Agent(role="Programador", goal="Escribir código limpio", llm=llm)
```

#### Docstrings

Usar formato Google:

```python
def example_function(param1: str, param2: int) -> bool:
    """Descripción breve de la función.
    
    Descripción más larga si es necesario. Explica qué hace,
    parámetros especiales, comportamientos importantes.
    
    Args:
        param1: Descripción del parámetro 1.
        param2: Descripción del parámetro 2.
    
    Returns:
        Descripción del valor retornado.
    
    Raises:
        ValueError: Si param1 está vacío.
    """
    if not param1:
        raise ValueError("param1 no puede estar vacío")
    return bool(param2)
```

#### Type Hints

Siempre usar type hints:

```python
from typing import Optional, List, Dict
from crewai import Agent, Task

def create_tasks(agents: List[Agent]) -> Dict[str, Task]:
    """Crear tareas para los agentes."""
    tasks: Dict[str, Task] = {}
    for agent in agents:
        task = Task(description="...", agent=agent)
        tasks[agent.role] = task
    return tasks
```

### 🧪 Testing

#### Escribir Tests

```python
# tests/test_nueva_funcionalidad.py
import pytest
from unittest.mock import patch, MagicMock
from multi_agent.nueva_funcionalidad import nueva_funcion

class TestNuevaFuncionalidad:
    """Tests para nueva funcionalidad."""
    
    def test_caso_basico(self):
        """Prueba caso básico."""
        resultado = nueva_funcion("input")
        assert resultado is not None
    
    @patch('modulo.dependencia_externa')
    def test_con_mock(self, mock_dep):
        """Prueba con dependencias mockeadas."""
        mock_dep.return_value = "resultado"
        resultado = nueva_funcion("input")
        assert resultado == "resultado"
```

#### Cobertura Mínima

- Funciones públicas: 100%
- Funciones privadas: 80%+
- General: 85%+

### 📚 Tipos de Contribuciones

#### 🎨 Mejoras de Interfaz

- Cambios en Streamlit
- Mejoras visuales
- UX improvements

#### 🔧 Bug Fixes

- Correciones de errores
- Optimización de performance
- Refactoring seguro

#### ✨ Nuevas Características

- Nuevos agentes
- Nuevas tareas
- Integración con nuevas herramientas

#### 📖 Documentación

- README updates
- Docstrings mejorados
- Ejemplos de código
- Guías de troubleshooting

### 🔍 Proceso de Revisión

1. **Automated Checks**:
   - Tests deben pasar
   - Cobertura mínima 85%
   - Linting (if configured)

2. **Manual Review**:
   - Al menos 1 mantenedor revisa
   - Feedback constructivo
   - Aprobación antes de merge

3. **Merge**:
   - Squash commits si es necesario
   - Delete rama después de merge

### ❓ Preguntas?

- Abre una [Issue](https://github.com/tu-repo/issues)
- Participa en las [Discussions](https://github.com/tu-repo/discussions)
- Contáctanos en email

---

**¡Gracias por contribuir a MultiAgentesLocal! 🙌**
