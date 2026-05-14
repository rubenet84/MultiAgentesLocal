import os
from uuid import uuid4
from dotenv import load_dotenv
from crewai import Crew, Process, Task
# Asegúrate de que las rutas de importación coincidan con tu estructura de carpetas
from .sub_agents.programador.agent import get_programador_agent
from .sub_agents.escritor.agent import get_escritor_agent

# Cargamos las variables del archivo .env para evitar errores 401
load_dotenv()


def _make_langsmith_task_callback(task, client, root_run_id):
    if client is None or root_run_id is None:
        return None

    def _callback(output):
        if output is None:
            return
        try:
            client.create_run(
                id=uuid4(),
                name=f"Tarea: {task.agent.role if task.agent else 'Sin agente'}",
                inputs={
                    "task_description": task.description,
                    "agent_role": getattr(task.agent, "role", None),
                },
                outputs={"task_output": str(output)},
                run_type="chain",
                project_name=os.getenv("LANGCHAIN_PROJECT"),
                parent_run_id=root_run_id,
                metadata={
                    "task_id": str(task.id),
                    "task_role": getattr(task.agent, "role", None),
                },
            )
        except Exception as e:
            print(
                f"⚠️ LangSmith callback para tarea '{task.agent.role if task.agent else task.id}' falló: {e}"
            )

    return _callback


def run_multi_agent_system(user_prompt, langsmith_client=None, root_run_id=None):
    try:
        # Instanciamos los agentes
        programador = get_programador_agent()
        escritor = get_escritor_agent()

        # Tarea de Programación (Tu versión preferida)
        tarea_programacion = Task(
            description=(
                f"Desarrolla lo siguiente: '{user_prompt}'. "
                "Escribe un código en Python que sea limpio, eficiente y esté documentado con comentarios breves. "
                "Asegúrate de que el código sea autoejecutable."
            ),
            agent=programador,
            expected_output="Código Python funcional con comentarios explicativos internos."
        )

        # Tarea de Redacción (Tu versión preferida)
        tarea_redaccion = Task(
            description=(
                "Toma el código generado por el programador y genera el output siguiendo este orden ESTRICTO: "
                "1. Primero, escribe el código Python completo dentro de un bloque de código Markdown (```python ... ```). "
                "No añadas texto antes del código. "
                "2. Después del código, añade una línea horizontal (---). "
                "3. Debajo de la línea, añade una explicación detallada de qué hace el código. "
                "4. Desglosa las funciones o partes principales. "
                "5. Usa un tono didáctico adaptado a desarrolladores en España. "
                "Importante: El código debe ser lo primero que vea el usuario."
            ),
            agent=escritor,
            expected_output="Un artículo técnico en Markdown que incluye la explicación y el código original.",
            context=[tarea_programacion] 
        )

        tarea_programacion.callback = _make_langsmith_task_callback(
            tarea_programacion, langsmith_client, root_run_id
        )
        tarea_redaccion.callback = _make_langsmith_task_callback(
            tarea_redaccion, langsmith_client, root_run_id
        )

        # Creamos la Crew
        equipo = Crew(
            agents=[programador, escritor],
            tasks=[tarea_programacion, tarea_redaccion],
            process=Process.sequential,  # Ejecución lineal obligatoria
            verbose=True,                # Muestra el proceso en consola
            memory=False,                # Deshabilita la memoria de CrewAI para evitar llamadas a OpenAI
            embedder=None,               # Deshabilita embedder para evitar llamadas a OpenAI
            tracing=True,                # Habilita trazabilidad de CrewAI para LangSmith
        )

        # Ejecutamos el flujo
        resultado = equipo.kickoff()

        # Devolvemos el contenido final en texto plano para la interfaz
        if hasattr(resultado, 'raw'):
            return resultado.raw
        return str(resultado or "")

    except Exception as e:
        # Mensaje de error amigable si falla la API o el proceso
        return f"Vaya, parece que algo ha fallado: {str(e)}. Revisa que tu clave API en el .env sea válida."