import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODULO_TAREAS = BASE_DIR / "tareas_persistentes.py"
AGENTE = BASE_DIR / "ciclo_agente_persistente.py"


def ejecutar_comando(*args):
    return subprocess.run(
        [sys.executable, str(MODULO_TAREAS), *args],
        cwd=str(BASE_DIR),
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


def main():
    if not MODULO_TAREAS.is_file() or not AGENTE.is_file():
        print("Error: falta el módulo de tareas o la copia del agente.")
        return

    tarea = input("Describe la nueva tarea: ").strip()
    if not tarea:
        print("No se ha indicado ninguna tarea.")
        return

    creada = ejecutar_comando("nueva", tarea)
    print(creada.stdout, end="")
    if creada.returncode != 0:
        print(creada.stderr)
        print("No se iniciará el agente.")
        return

    # Recuperar el ID generado por el módulo persistente.
    task_id = None
    for linea in creada.stdout.splitlines():
        if linea.startswith("Tarea guardada: "):
            task_id = linea.split(":", 1)[1].strip()
            break

    if not task_id:
        print("No se pudo confirmar el ID. No se iniciará el agente.")
        return

    estado = ejecutar_comando("estado", task_id, "en_curso")
    print(estado.stdout, end="")
    if estado.returncode != 0:
        print(estado.stderr)
        print("No se iniciará el agente.")
        return

    print("\nIniciando el agente. Revisa sus propuestas y autorizaciones.")
    try:
        resultado = subprocess.run(
            [sys.executable, str(AGENTE)],
            cwd=str(BASE_DIR),
            input=tarea + "\n",
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        print("\n--- Salida del agente ---")
        print(resultado.stdout, end="")
        if resultado.stderr:
            print("\n--- Errores del proceso ---")
            print(resultado.stderr, end="")

        salida = resultado.stdout
        cancelada = (
            "Acción cancelada" in salida
            or "Lectura cancelada" in salida
            or "Creación cancelada" in salida
        )
        completada = (
            "Correcto: se creó y verificó" in salida
            or "El agente termina:" in salida
        )

        if resultado.returncode != 0:
            nuevo_estado = "fallida"
        elif cancelada:
            nuevo_estado = "pendiente"
        elif completada:
            nuevo_estado = "completada"
        else:
            nuevo_estado = "fallida"

        actualizacion = ejecutar_comando(
            "estado", task_id, nuevo_estado
        )
        print(actualizacion.stdout, end="")
        if actualizacion.returncode != 0:
            print(actualizacion.stderr)
            print("ATENCIÓN: no se pudo actualizar el estado persistente.")

        print(f"Resultado registrado: {nuevo_estado}")
        if nuevo_estado == "fallida":
            print("Revisa la salida antes de decidir si reintentar.")
    except KeyboardInterrupt:
        print("\nInterrupción detectada. Marcando la tarea como interrumpida.")
        actualizacion = ejecutar_comando(
            "estado", task_id, "interrumpida"
        )
        print(actualizacion.stdout, end="")
        if actualizacion.returncode != 0:
            print(actualizacion.stderr)


if __name__ == "__main__":
    main()
