.PHONY: help install setup test test-cov lint format clean run docs

# Variables
PYTHON := python
PIP := pip
VENV := venv

help:
	@echo "📚 MultiAgentesLocal - Comandos disponibles"
	@echo ""
	@echo "  🔧 Configuración:"
	@echo "    make setup          Crear venv e instalar dependencias"
	@echo "    make install        Instalar dependencias"
	@echo ""
	@echo "  🧪 Testing:"
	@echo "    make test           Ejecutar tests"
	@echo "    make test-cov       Tests con cobertura"
	@echo ""
	@echo "  🚀 Ejecución:"
	@echo "    make run            Lanzar Streamlit"
	@echo "    make dev            Modo desarrollo (con reload)"
	@echo ""
	@echo "  📖 Documentación:"
	@echo "    make docs           Generar documentación"
	@echo ""
	@echo "  🧹 Limpieza:"
	@echo "    make clean          Limpiar archivos temporales"
	@echo "    make clean-all      Limpiar todo incluyendo venv"
	@echo ""

setup:
	@echo "🔧 Configurando entorno..."
	$(PYTHON) -m venv $(VENV)
	@echo "✓ Venv creado"
	$(VENV)/Scripts/pip install --upgrade pip
	$(VENV)/Scripts/pip install -r requirements.txt
	@echo "✓ Dependencias instaladas"
	@echo ""
	@echo "ℹ️  Próximos pasos:"
	@echo "   1. Activar venv: $(VENV)\\Scripts\\activate"
	@echo "   2. Ejecutar: ollama serve (en terminal separada)"
	@echo "   3. Ejecutar: make run"

install:
	@echo "📦 Instalando dependencias..."
	$(PIP) install -r requirements.txt
	@echo "✓ Dependencias instaladas"

test:
	@echo "🧪 Ejecutando tests..."
	$(PYTHON) run_tests.py

test-cov:
	@echo "📊 Tests con cobertura..."
	$(PYTHON) -m pytest tests/ -v --cov=multi_agent --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "✓ Reporte en: htmlcov/index.html"

run:
	@echo "🚀 Lanzando Streamlit..."
	streamlit run interfaz_agentes.py

dev:
	@echo "⚙️  Modo desarrollo..."
	streamlit run interfaz_agentes.py --logger.level=debug

lint:
	@echo "🔍 Verificando código..."
	$(PYTHON) -m pylint multi_agent/ --disable=all --enable=E,F
	@echo "✓ Linting completado"

format:
	@echo "📝 Formateando código..."
	$(PYTHON) -m black multi_agent/ tests/
	@echo "✓ Código formateado"

clean:
	@echo "🧹 Limpiando archivos temporales..."
	del /q __pycache__ 2>nul || true
	del /q .pytest_cache 2>nul || true
	del /q .coverage 2>nul || true
	rmdir /q /s htmlcov 2>nul || true
	rmdir /q /s __pycache__ 2>nul || true
	rmdir /q /s .pytest_cache 2>nul || true
	@echo "✓ Limpieza completada"

clean-all: clean
	@echo "🔥 Limpiando todo..."
	rmdir /q /s $(VENV) 2>nul || true
	@echo "✓ Todo limpiado"

docs:
	@echo "📖 Documentación del proyecto:"
	@echo ""
	@echo "📚 Documentación Principal:"
	@echo "  📄 README.md                    - Documentación principal"
	@echo ""
	@echo "📂 docs/ - Documentación Detallada:"
	@echo "  📄 docs/QUICKSTART.md           - Guía de inicio rápido"
	@echo "  📄 docs/ARCHITECTURE.md         - Arquitectura y diseño"
	@echo "  📄 docs/CONTRIBUTING.md         - Guía para contribuidores"
	@echo "  📄 docs/CHANGELOG.md            - Historial de cambios"
	@echo ""
	@echo "🔗 Acceso rápido:"
	@echo "  make docs                       # Mostrar esta información"
	@echo "  cat docs/QUICKSTART.md          # Ver guía rápida"
	@echo "  cat docs/ARCHITECTURE.md        # Ver arquitectura"
