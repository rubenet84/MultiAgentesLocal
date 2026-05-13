from crewai import Crew, Process, Task
from .sub_agents.programador.agent import get_programador_agent
from .sub_agents.escritor.agent import get_escritor_agent

def run_multi_agent_system(user_prompt):
    # Instanciamos los agentes
    programador = get_programador_agent()
    escritor = get_escritor_agent()

    # Definimos las tareas
    tarea_programacion = Task(
        description=f"Desarrolla lo siguiente: {user_prompt}",
        agent=programador,
        expected_output="Código Python completo y funcional."
    )

    tarea_redaccion = Task(
        description="Escribe una explicación detallada del código proporcionado por el programador.",
        agent=escritor,
        expected_output="Un artículo en formato Markdown explicando el funcionamiento del código.",
        context=[tarea_programacion] # Esto asegura que el escritor espere al programador
    )

    # Creamos la Crew (el equipo)
    equipo = Crew(
        agents=[programador, escritor],
        tasks=[tarea_programacion, tarea_redaccion],
        process=Process.sequential # Uno tras otro
    )

    return equipo.kickoff()