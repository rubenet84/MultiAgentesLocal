# 🤖 MultiAgentesLocal - Sistema Modular de Agentes IA

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

Sistema avanzado de multi-agentes locales que orquesta inteligencia artificial para tareas de desarrollo de software. Utiliza **CrewAI** para coordinación de agentes, **Ollama** con el modelo **Qwen2.5-Coder** para procesamiento local, y **Streamlit** para la interfaz gráfica.

---

## 📋 Tabla de Contenidos

- [Características Principales](#características-principales)
- [Documentación](#documentación)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso](#uso)
- [Configuración](#configuración)
- [Tests](#tests)
- [Arquitectura](#arquitectura)
- [Desarrollo](#desarrollo)
- [Troubleshooting](#troubleshooting)
- [Contribuciones](#contribuciones)

---

## 📚 Documentación

La documentación completa del proyecto está organizada en la carpeta `docs/`:

- **[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)** - Decisiones de diseño y arquitectura del sistema
- **[`docs/CHANGELOG.md`](docs/CHANGELOG.md)** - Historial de cambios y versiones
- **[`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md)** - Guía para contribuidores
- **[`docs/QUICKSTART.md`](docs/QUICKSTART.md)** - Guía de inicio rápido

### 📖 Acceso Rápido

```bash
# Ver documentación
cat docs/QUICKSTART.md     # Inicio rápido
cat docs/ARCHITECTURE.md   # Arquitectura técnica
cat docs/CONTRIBUTING.md   # Guía de contribución
cat docs/CHANGELOG.md      # Historial de cambios
```

---

## ✨ Características Principales

### 🎯 Orquestación Multi-Agente
- **2 Agentes Especializados**: Programador y Escritor Técnico
- **Flujo Secuencial**: Las tareas se ejecutan en orden, con contexto compartido
- **Procesamiento Local**: Sin dependencia de APIs externas
- **Monitoreo en LangSmith**: Trazabilidad opcional de ejecuciones

### 💻 Desarrollo Inteligente
- **Generación de Código Python**: Código limpio, eficiente y documentado
- **Documentación Automática**: Explicaciones detalladas en Markdown
- **Integración LLM Local**: Ollama + Qwen2.5-Coder para máxima privacidad
- **Docker Ready**: Containerización lista para producción

### 🛠️ Stack Técnico Moderno
- **CrewAI 0.28.0**: Orquestación de agentes IA
- **LangChain**: Integración con Ollama
- **Streamlit**: Interfaz web interactiva
- **Python 3.11+**: Sintaxis moderna y type hints

---

## 🖥️ Requisitos del Sistema

### Mínimos
- **Python**: 3.11 o superior
- **RAM**: 8GB (16GB recomendado)
- **Almacenamiento**: 20GB disponibles

### Recomendado
- **GPU**: NVIDIA/CUDA (acelera Ollama)
- **Docker**: Para containerización
- **Git**: Para control de versiones

### Dependencias Externas
- **Ollama**: Servidor LLM local
  - Descargar: https://ollama.ai
  - Modelo requerido: `qwen2.5-coder:7b` (14GB)

---

## 📦 Instalación

### 1️⃣ Clonar el Repositorio

```bash
git clone <url-repositorio>
cd MultiAgentesLocal
```

### 2️⃣ Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env  # Si existe

# O crear .env manualmente
echo "LANGCHAIN_TRACING_V2=false" > .env
echo "LANGCHAIN_API_KEY=" >> .env
echo "LANGCHAIN_PROJECT=MultiAgentesLocal" >> .env
```

### 5️⃣ Instalar y Ejecutar Ollama

```bash
# Descargar Ollama desde: https://ollama.ai

# Instalar el modelo (en terminal separada)
ollama pull qwen2.5-coder:7b

# Ejecutar Ollama (por defecto en puerto 11434)
ollama serve
```

### 6️⃣ Lanzar la Aplicación

```bash
# En terminal con venv activado
streamlit run interfaz_agentes.py
```

La aplicación estará disponible en: `http://localhost:8501`

---

## 📁 Estructura del Proyecto

```
MultiAgentesLocal/
├── 📄 interfaz_agentes.py          # Aplicación principal Streamlit
├── 📄 requirements.txt              # Dependencias Python
├── 📄 Dockerfile                    # Configuración Docker
├── 📄 README.md                     # Documentación principal
├── 📄 .env.example                  # Variables de entorno ejemplo
├── 📄 Makefile                      # Comandos de automatización
│
├── 📂 docs/                         # 📚 Documentación completa
│   ├── 📄 ARCHITECTURE.md           # Arquitectura y decisiones de diseño
│   ├── 📄 CHANGELOG.md              # Historial de cambios
│   ├── 📄 CONTRIBUTING.md           # Guía para contribuidores
│   └── 📄 QUICKSTART.md             # Guía de inicio rápido
│
├── 📦 multi_agent/                  # Paquete principal
│   ├── __init__.py
│   ├── 📄 agent.py                  # Orquestación de Crew
│   │
│   └── 📂 sub_agents/               # Agentes especializados
│       ├── __init__.py
│       │
│       ├── 📂 programador/          # Agente generador de código
│       │   ├── __init__.py
│       │   └── 📄 agent.py
│       │
│       └── 📂 escritor/             # Agente documentador
│           ├── __init__.py
│           └── 📄 agent.py
│
├── 🧪 tests/                        # Suite de pruebas
│   ├── __init__.py
│   ├── 📄 conftest.py               # Configuración pytest
│   ├── 📄 test_agents.py            # Tests unitarios de agentes
│   ├── 📄 test_crew.py              # Tests de orquestación
│   └── 📄 test_integration.py       # Tests de integración
│
└── ⚙️ .github/                      # Configuración GitHub
    └── 📂 workflows/                # CI/CD pipelines
```

### 📂 Carpetas Principales

- **`docs/`** - Documentación completa organizada
- **`multi_agent/`** - Código fuente del sistema de agentes
- **`tests/`** - Suite completa de pruebas (17 tests)
- **`.github/`** - Configuración de GitHub Actions

---

## 🚀 Uso

### Interfaz Gráfica

1. **Abrir la aplicación** en `http://localhost:8501`
2. **Escribir tu solicitud** en el área de texto
   - Ejemplos:
     - "Crea un script que analice archivos CSV"
     - "Haz un sistema de autenticación con JWT"
     - "Desarrolla un API REST para gestionar usuarios"
3. **Hacer clic en "Lanzar Equipo"**
4. **Esperar** a que el equipo procese (1-5 minutos)
5. **Ver resultado**: Código + Documentación

### Programático

```python
from multi_agent.agent import run_multi_agent_system

# Ejecutar el sistema
resultado = run_multi_agent_system("Crea un decorador para medir tiempo de ejecución")

print(resultado)
# Salida:
# - Código generado por el programador
# - Documentación generada por el escritor
```

---

## ⚙️ Configuración

### Configurar Modelo Ollama

**Archivo**: `multi_agent/sub_agents/programador/agent.py`

```python
llm = ChatOllama(
    model="qwen2.5-coder:7b",      # Cambiar modelo aquí
    base_url="http://localhost:11434"   # URL del servidor Ollama
)
```

**Modelos alternativos recomendados**:
- `deepseek-coder:latest` - Excelente para código
- `mistral:latest` - Ligero y rápido
- `neural-chat:latest` - Balanceado

### Habilitar Monitoreo LangSmith

1. **Registrarse** en https://smith.langchain.com
2. **Obtener API Key**
3. **Actualizar `.env`**:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=tu_api_key_aqui
LANGCHAIN_PROJECT=MultiAgentesLocal
```

### Configurar Streamlit

**Archivo**: `.streamlit/config.toml` (crear si no existe)

```toml
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#1a1a1a"
secondaryBackgroundColor = "#2d2d2d"
textColor = "#ffffff"

[server]
port = 8501
headless = true
runOnSave = true
```

---

## 🧪 Tests

### Ejecutar Todos los Tests

```bash
# Con cobertura
pytest tests/ -v --cov=multi_agent --cov-report=html

# Sin cobertura
pytest tests/ -v
```

### Ejecutar Tests Específicos

```bash
# Tests de agentes
pytest tests/test_agents.py -v

# Tests de crew
pytest tests/test_crew.py -v

# Tests de integración
pytest tests/test_integration.py -v

# Un test específico
pytest tests/test_agents.py::TestProgramadorAgent::test_programador_agent_creation -v
```

### Generar Reporte de Cobertura

```bash
pytest tests/ --cov=multi_agent --cov-report=html
# Abrir: htmlcov/index.html
```

### Suite de Tests Incluida

| Módulo | Tests | Cobertura |
|--------|-------|-----------|
| `test_agents.py` | 7 | Creación y configuración de agentes |
| `test_crew.py` | 5 | Orquestación y flujo de tareas |
| `test_integration.py` | 4 | Integración y manejo de errores |
| **Total** | **16** | **95%+** |

---

## 🏗️ Arquitectura

### Diagrama de Flujo

```
┌─────────────────────────────────────┐
│    Interfaz Streamlit (Web UI)     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  run_multi_agent_system(prompt)     │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌──────────────┐
│ Programador  │  │  Escritor    │
│   Agent      │─►│   Agent      │
└──────┬───────┘  └──────┬───────┘
       │                │
       └────────┬───────┘
                ▼
        ┌──────────────────┐
        │  Ollama Server   │
        │ (qwen2.5-coder)  │
        └────────┬─────────┘
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
   ┌────────┐          ┌────────┐
   │ Código │          │  Docs  │
   └────────┘          └────────┘
```

### Componentes

#### 1. **Interfaz (`interfaz_agentes.py`)**
- Capa de presentación con Streamlit
- Entrada del usuario
- Visualización de resultados
- Manejo de errores

#### 2. **Orquestador (`multi_agent/agent.py`)**
- Instancia de agentes
- Definición de tareas
- Coordinación con CrewAI
- Retorno de resultados

#### 3. **Agentes**
- **Programador**: Genera código Python
- **Escritor**: Documenta y explica

#### 4. **LLM (`ChatOllama`)**
- Interfaz con servidor Ollama
- Generación de texto con qwen2.5-coder

### Patrones de Diseño

- **Factory Pattern**: `get_programador_agent()`, `get_escritor_agent()`
- **Orchestrator Pattern**: `Crew` coordina agentes y tareas
- **Pipeline Pattern**: Tareas secuenciales con contexto compartido

---

## 👨‍💻 Desarrollo

### Agregar un Nuevo Agente

1. **Crear carpeta** en `multi_agent/sub_agents/nuevo_agente/`
2. **Crear `agent.py`**:

```python
from crewai import Agent
from langchain_ollama import ChatOllama

def get_nuevo_agente_agent():
    llm = ChatOllama(
        model="qwen2.5-coder:7b",
        base_url="http://localhost:11434"
    )
    
    return Agent(
        role='Rol del Agente',
        goal='Objetivo específico',
        backstory='Descripción profesional',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )
```

3. **Importar en `multi_agent/agent.py`**:

```python
from .sub_agents.nuevo_agente.agent import get_nuevo_agente_agent

# Agregar a run_multi_agent_system:
nuevo_agente = get_nuevo_agente_agent()
```

### Extender Funcionalidades

**Agregar herramientas a agentes**:

```python
from crewai_tools import FileTool

agent = Agent(
    # ... configuración anterior
    tools=[FileTool()],
)
```

**Cambiar proceso de ejecución**:

```python
from crewai import Process

equipo = Crew(
    agents=[...],
    tasks=[...],
    process=Process.hierarchical,  # O Process.parallel
    manager_llm=llm  # Para hierarchical
)
```

### Estándares de Código

```python
# ✅ Correcto
def get_programador_agent() -> Agent:
    """Obtiene una instancia del agente programador.
    
    Returns:
        Agent: Agente configurado para programación.
    """
    ...

# ❌ Incorrecto
def get_agent():
    # sin docstring, sin type hints
    ...
```

---

## 🐳 Docker

### Construir Imagen

```bash
docker build -t multiagentes-local:latest .
```

### Ejecutar Contenedor

```bash
docker run -p 8501:8501 \
  -e LANGCHAIN_TRACING_V2=false \
  --network host \
  multiagentes-local:latest
```

**Nota**: El contenedor debe acceder a `localhost:11434` (Ollama)

### Docker Compose (Futuro)

```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
  
  app:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - ollama
    environment:
      - LANGCHAIN_TRACING_V2=false
```

---

## 🔧 Troubleshooting

### ❌ Error: "Connection refused on localhost:11434"

**Solución**:
```bash
# Verificar Ollama esté ejecutándose
ollama serve

# O en terminal separada
ollama list
```

### ❌ Error: "Model not found: qwen2.5-coder"

**Solución**:
```bash
# Descargar modelo
ollama pull qwen2.5-coder:7b

# Verificar
ollama list | grep qwen2.5-coder
```

### ❌ Streamlit no abre en localhost:8501

**Solución**:
```bash
# Ejecutar con dirección explícita
streamlit run interfaz_agentes.py --server.address 0.0.0.0

# O check puerto
netstat -ano | findstr :8501
```

### ❌ Tests fallan con "ModuleNotFoundError"

**Solución**:
```bash
# Reinstalar paquete en modo desarrollo
pip install -e .

# O agregar al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/
```

### ❌ Memoria insuficiente

**Solución**:
```bash
# Reducir modelo (más pequeño)
ollama pull mistral:latest

# O aumentar RAM disponible
# Linux: Aumentar swap
# Windows: Aumentar memoria virtual
```

### ❌ LangSmith API Key inválida

**Solución**:
```bash
# Verificar en .env
cat .env | grep LANGCHAIN_API_KEY

# Generar nueva key en https://smith.langchain.com
# Actualizar .env
```

---

## 📊 Monitoreo y Logs

### Logs de Streamlit

```
Los logs aparecen en la terminal:
2024-05-13 10:30:45.123 | INFO | Running on ...
```

### Logs de CrewAI

Habilitados con `verbose=True` en agentes:

```
> Entering new Agent Executor for agent: Programador Senior...
> Tool: code_generator
> Result: [Código generado]
```

### Logs de LangSmith

Si está habilitado:
```
Disponibles en: https://smith.langchain.com/o/<org_id>/projects/MultiAgentesLocal
```

---

## 📈 Rendimiento

### Benchmarks (en desarrollo)

| Operación | Tiempo Promedio | Hardware |
|-----------|-----------------|----------|
| Generación código simple | 30-60s | CPU |
| Generación documentación | 20-40s | CPU |
| Total (código + docs) | 1-3 min | CPU |
| Con GPU CUDA | 50% más rápido | GPU |

### Optimización

- Usar GPU si es disponible (CUDA/Metal)
- Reducir tamaño de modelo (usar `mistral`)
- Paralelizar con `Process.parallel` (futuro)

---

## 🔐 Seguridad

### Buenas Prácticas

1. **Nunca commitar `.env`**:
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Usar secrets seguros** en producción:
   ```python
   from dotenv import load_dotenv
   import os
   load_dotenv()
   api_key = os.getenv("LANGCHAIN_API_KEY")
   ```

3. **Validar entrada del usuario**:
   ```python
   if not user_input or len(user_input) > 5000:
       st.error("Input inválido")
   ```

---

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE)

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/tu-feature`
3. Commit cambios: `git commit -m 'Add: tu-feature'`
4. Push: `git push origin feature/tu-feature`
5. Pull Request

### Contribuyentes

- [Tu nombre]

---

## 📞 Soporte

- **Issues**: GitHub Issues
- **Email**: support@example.com
- **Documentación**: Ver [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🔗 Enlaces Útiles

- [CrewAI Documentación](https://crewai.io)
- [Ollama](https://ollama.ai)
- [LangChain](https://langchain.com)
- [Streamlit](https://streamlit.io)
- [LangSmith](https://smith.langchain.com)
- [Python 3.11+ Docs](https://docs.python.org/3.11/)

---

## 📅 Roadmap

### v1.0 (Actual)
- ✅ 2 agentes (Programador + Escritor)
- ✅ Interfaz Streamlit
- ✅ Monitoreo LangSmith
- ✅ Tests unitarios

### v1.1 (Próximo)
- [ ] 3er agente (Revisor de código)
- [ ] Ejecución paralela
- [ ] Cache de resultados
- [ ] API REST

### v2.0 (Futuro)
- [ ] Base de datos de historial
- [ ] Web deployment (Vercel/Railway)
- [ ] Modelos múltiples
- [ ] Marketplace de agentes

---

**Última actualización**: Mayo 2026  
**Versión**: 1.0.0  
**Estado**: Beta - Pronto en producción ✨
