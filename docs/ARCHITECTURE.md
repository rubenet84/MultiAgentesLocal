# 🏗️ Documentación de Arquitectura - MultiAgentesLocal

## Índice

1. [Visión General](#visión-general)
2. [Decisiones Arquitectónicas](#decisiones-arquitectónicas)
3. [Componentes](#componentes)
4. [Flujo de Datos](#flujo-de-datos)
5. [Patrones de Diseño](#patrones-de-diseño)
6. [Escalabilidad](#escalabilidad)

---

## Visión General

**MultiAgentesLocal** es un sistema de orquestación de agentes IA que automatiza tareas de desarrollo de software usando:

- **CrewAI**: Framework para orquestación multi-agente
- **Ollama**: Servidor de LLM local
- **LangChain**: Abstracción para integración con LLM
- **LangSmith**: Monitoreo y trazabilidad de ejecuciones
- **Streamlit**: Interfaz web interactiva

### Objetivos de Diseño

✅ **Privacidad**: Todo procesa localmente, sin enviar datos a APIs externas
✅ **Modularidad**: Fácil agregar nuevos agentes especializados
✅ **Extensibilidad**: Arquitectura preparada para crecimiento
✅ **Testabilidad**: Suite completa de tests unitarios e integración
✅ **Usabilidad**: Interfaz intuitiva sin configuración compleja

---

## Decisiones Arquitectónicas

### 1. Separación de Agentes en Sub-módulos

**Decisión**: Cada agente vive en su propio sub-paquete (`sub_agents/programador/`, `sub_agents/escritor/`)

**Razones**:
- Facilita agregar nuevos agentes sin contaminación de código
- Aislamiento de responsabilidades
- Testing independiente por agente
- Estructura escalable

```
multi_agent/
├── agent.py                 ← Orquestación
└── sub_agents/
    ├── programador/
    │   └── agent.py        ← Implementación
    └── escritor/
        └── agent.py        ← Implementación
```

### 2. Uso de Factory Pattern

**Decisión**: Funciones `get_programador_agent()`, `get_escritor_agent()`

**Ventajas**:
- Facilita testing (mock-friendly)
- Encapsulación de configuración
- Facilita cambiar modelos sin tocar interfaz

```python
def get_programador_agent():
    """Factory que crea y configura el agente."""
    llm = ChatOllama(...)
    return Agent(...)
```

### 3. Configuración Centralizada

**Decisión**: Archivo `config.py` único para todas las constantes

**Beneficios**:
- Un lugar para cambios de configuración
- Fácil encontrar y actualizar parámetros
- Support de variables de entorno (`.env`)

```python
# config.py
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
```

### 4. Flujo Secuencial (Process.sequential)

**Decisión**: Las tareas se ejecutan secuencialmente, no en paralelo

**Justificación**:
- La salida de programador es entrada del escritor
- Asegura consistencia en documentación
- Facilita debugging
- Performance es aceptable para casos de uso actuales

**Futuro**: Migrar a `Process.hierarchical` o `Process.parallel` si se agregan más agentes.

### 5. Testing con Mocks

**Decisión**: Tests unitarios mockean dependencias externas (Ollama, LLM)

**Razones**:
- No requiere Ollama corriendo para tests
- Tests rápidos y determinísticos
- Fácil simular diferentes escenarios

```python
@patch('multi_agent.sub_agents.programador.agent.ChatOllama')
def test_agent_creation(self, mock_chat_ollama):
    mock_chat_ollama.return_value = MagicMock()
    agent = get_programador_agent()
    assert agent is not None
```

---

## Componentes

### Capa de Presentación (Streamlit)

**Archivo**: `interfaz_agentes.py`

**Responsabilidades**:
- Captura input del usuario
- Gestión del estado de la UI
- Visualización de resultados
- Manejo de errores de usuario

**Patrón**: Stateless (Streamlit re-ejecuta completamente en cada interacción)

```python
user_input = st.text_area("¿Qué quieres que construya?")
if st.button("Lanzar Equipo"):
    resultado = run_multi_agent_system(user_input)
    st.write(resultado)
```

### Capa de Orquestación

**Archivo**: `multi_agent/agent.py`

**Responsabilidades**:
- Instancia de agentes
- Definición de tareas
- Coordinación con CrewAI
- Retorno de resultados

**Patrón**: Orchestrator

```python
def run_multi_agent_system(user_prompt):
    programador = get_programador_agent()
    escritor = get_escritor_agent()
    
    tarea_1 = Task(...)
    tarea_2 = Task(...)
    
    equipo = Crew(...)
    return equipo.kickoff()
```

### Capa de Agentes

**Archivos**: `multi_agent/sub_agents/*/agent.py`

**Responsabilidades**:
- Definir rol, objetivo y backstory
- Configurar LLM
- Implementar especialización

**Patrón**: Factory

```python
def get_programador_agent() -> Agent:
    llm = ChatOllama(...)
    return Agent(role="...", goal="...", ...)
```

### Capa de LLM

**Interfaz**: `ChatOllama` (de LangChain)

**Responsabilidades**:
- Comunicación con servidor Ollama
- Ejecución del modelo
- Manejo de timeout/errores

### Capa de Monitoreo

**LangSmith Integration**

**Responsabilidades**:
- Trazabilidad completa de ejecuciones
- Monitoreo de rendimiento por tarea
- Debugging de conversaciones LLM
- Análisis de uso y costos

**Características**:
- Runs raíz para sesiones completas
- Runs hijos para tareas individuales
- Metadata detallada de agentes y prompts
- Dashboard web para visualización

---

## Flujo de Datos

### Ejemplo: Usuario solicita "Crea un validador de emails"

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ENTRADA (Streamlit)                                      │
│    Usuario escribe: "Crea un validador de emails"          │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 2. ORQUESTACIÓN (multi_agent/agent.py)                     │
│    - Crear agentes                                          │
│    - Crear tareas                                          │
│    - Instanciar Crew                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 3. TAREA 1: Programador genera código                       │
│    Prompt: "Desarrolla lo siguiente: ..."                  │
│    Agente: Programador Senior                              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 4. LLM (Ollama + qwen2.5-coder:7b)                            │
│    Genera: Código Python con validador                      │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 5. TAREA 2: Escritor documenta                             │
│    Input: Código anterior (via context)                    │
│    Prompt: "Explica el código..."                          │
│    Agente: Escritor Técnico                                │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 6. LLM (Ollama + qwen2.5-coder:7b)                            │
│    Genera: Documentación Markdown                           │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 7. RETORNO (Streamlit)                                      │
│    Mostrar:                                                 │
│    - Código Python                                         │
│    - Documentación                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Patrones de Diseño

### 1. **Factory Pattern**

Para crear agentes:

```python
# ✅ Correcto (Factory)
agent = get_programador_agent()

# ❌ Incorrecto (Direct instantiation)
agent = Agent(role="...", goal="...")
```

**Beneficios**: Flexibilidad, testabilidad, encapsulación

### 2. **Orchestrator Pattern**

Para coordinar agentes:

```python
# Crew actúa como orchestrator
equipo = Crew(
    agents=[programador, escritor],
    tasks=[tarea_1, tarea_2],
    process=Process.sequential
)
resultado = equipo.kickoff()
```

### 3. **Pipeline Pattern**

Para flujos de tareas:

```python
# Tarea 1 → Tarea 2
tarea_2 = Task(
    ...,
    context=[tarea_1]  # Tarea 2 espera a Tarea 1
)
```

### 4. **Dependency Injection**

Para testing:

```python
def process_task(agent: Agent, task: Task):
    """Función inyecta dependencias (mockeable)"""
    # ...
```

---

## Escalabilidad

### Agregar un Nuevo Agente

```
1. Crear carpeta: multi_agent/sub_agents/revisor/
2. Crear agent.py con get_revisor_agent()
3. Importar en multi_agent/agent.py
4. Agregar tarea en run_multi_agent_system()
5. Agregar tests en tests/
```

### Cambiar a Ejecución Paralela

```python
from crewai import Process

equipo = Crew(
    agents=[...],
    tasks=[...],
    process=Process.parallel,  # Cambiar de sequential
    manager_llm=llm  # Requerido para paralelo
)
```

### Soportar Múltiples Modelos

```python
# config.py
MODELS = {
    "código": "qwen2.5-coder:latest",
    "chat": "mistral:latest",
    "embedding": "nomic-embed-text:latest"
}

# agent.py
def get_programador_agent(model_name: str = "código"):
    llm = ChatOllama(model=MODELS[model_name])
    return Agent(...)
```

---

## Decisiones Futuras

### v1.1

- [ ] Parallelizar ejecución
- [ ] Agregar caché de resultados
- [ ] Implementar API REST
- [ ] Base de datos de historial

### v2.0

- [ ] Multi-modelo support
- [ ] Marketplace de agentes
- [ ] Deploy cloud-ready
- [ ] Webhooks y integración

---

## Conclusión

La arquitectura de **MultiAgentesLocal** prioriza:

- **Claridad**: Código fácil de entender
- **Testabilidad**: Fácil escribir tests
- **Mantenibilidad**: Fácil agregar/cambiar features
- **Escalabilidad**: Preparado para crecer

Cada decisión fue tomada considerando estos principios.
