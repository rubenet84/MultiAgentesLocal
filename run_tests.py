"""
Script para ejecutar los tests del proyecto.

Este script configura el entorno y ejecuta la suite completa de tests.
"""

import subprocess
import sys
from pathlib import Path

# Colores para la terminal
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str) -> None:
    """Imprimir encabezado formateado."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Colors.RESET}\n")


def print_success(text: str) -> None:
    """Imprimir mensaje de éxito."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str) -> None:
    """Imprimir mensaje de error."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text: str) -> None:
    """Imprimir mensaje de advertencia."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def run_command(command: list, description: str) -> bool:
    """Ejecutar comando y retornar éxito/fracaso."""
    print_header(description)
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print_success(description)
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"{description} - Falló con código {e.returncode}")
        return False
    except FileNotFoundError:
        print_error(f"Comando no encontrado: {command[0]}")
        return False


def main():
    """Ejecutar suite completa de tests."""
    project_root = Path(__file__).parent
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  🧪 SUITE DE TESTS - MULTIAGENTESLOCAL                     ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Colors.RESET)
    
    all_passed = True
    
    # 1. Verificar que pytest está instalado
    print("\n📋 Verificando dependencias...")
    try:
        import pytest
        print_success("pytest instalado")
    except ImportError:
        print_error("pytest no instalado. Ejecuta: pip install pytest")
        return 1
    
    # 2. Ejecutar tests unitarios
    if not run_command(
        [sys.executable, "-m", "pytest", "tests/test_agents.py", "-v", "--tb=short"],
        "Tests Unitarios - Agentes"
    ):
        all_passed = False
    
    # 3. Ejecutar tests de crew
    if not run_command(
        [sys.executable, "-m", "pytest", "tests/test_crew.py", "-v", "--tb=short"],
        "Tests - Orquestación (Crew)"
    ):
        all_passed = False
    
    # 4. Ejecutar tests de integración
    if not run_command(
        [sys.executable, "-m", "pytest", "tests/test_integration.py", "-v", "--tb=short"],
        "Tests - Integración"
    ):
        all_passed = False
    
    # 5. Ejecutar todos los tests con cobertura
    try:
        import pytest_cov
        print_header("Todos los Tests con Cobertura")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", 
             "--cov=multi_agent", "--cov-report=term-missing", "--cov-report=html"],
            capture_output=False
        )
        if result.returncode == 0:
            print_success("Cobertura generada en htmlcov/index.html")
        else:
            print_warning("Error generando cobertura")
    except ImportError:
        print_warning("pytest-cov no instalado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest-cov"])
        # Reintentar
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", 
             "--cov=multi_agent", "--cov-report=term-missing"],
            capture_output=False
        )
        if result.returncode != 0:
            all_passed = False
    
    # Resumen final
    print_header("📊 RESUMEN")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print(f"{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}")
        print("❌ ALGUNOS TESTS FALLARON")
        print(f"{Colors.RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
