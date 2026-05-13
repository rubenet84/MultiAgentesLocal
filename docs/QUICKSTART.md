# 🚀 Guía de Inicio Rápido - MultiAgentesLocal

## ⏱️ 5 Minutos para Empezar

### Paso 1: Instalación (2 min)

```bash
# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Descargar Modelo (1 min)

```bash
# En terminal separada
ollama pull qwen2.5-coder:latest
ollama serve
```

### Paso 3: Ejecutar Aplicación (2 min)

```bash
# Terminal con venv activado
streamlit run interfaz_agentes.py
```

✨ **¡Listo!** Abre `http://localhost:8501`

---

## 🎯 Ejemplo Rápido

### Via Streamlit (Recomendado)

1. Escribe en el área de texto: _"Crea un script que valide emails"_
2. Haz clic en **"Lanzar Equipo"**
3. Espera 2-3 minutos
4. ¡Código + Documentación listos! ✨

### Via Terminal

```python
from multi_agent import run_multi_agent_system

resultado = run_multi_agent_system("Crea un decorador de timing")
print(resultado)
```

---

## 🧪 Verificar que Todo Funciona

```bash
# Ejecutar tests
python run_tests.py

# O manualmente
pytest tests/ -v
```

---

## 🔗 Próximos Pasos

- Lee [README.md](README.md) para documentación completa
- Revisa [CONTRIBUTING.md](CONTRIBUTING.md) para contribuir
- Explora `/tests` para ver ejemplos de testing

---

## ❌ Problemas Comunes

### "Connection refused on localhost:11434"
```bash
# Asegúrate que Ollama esté corriendo
ollama serve  # En terminal separada
```

### "Model not found"
```bash
ollama pull qwen2.5-coder:latest
```

### Puerto 8501 en uso
```bash
streamlit run interfaz_agentes.py --server.port 8502
```

---

**¿Listo? ¡Vamos!** 🚀
