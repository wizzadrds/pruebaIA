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
        return 2

    tarea = input("Describe la nueva tarea: ").strip()
    if not tarea:
        print("No se ha indicado ninguna tarea.")
        return 2

    creada = ejecutar_comando("nueva", tarea)
    print(creada.stdout, end="")
    if creada.returncode != 0:
        print(creada.stderr)
        print("No se iniciará el agente.")
        return 2

    task_id = None
    for linea in creada.stdout.splitlines():
        if linea.startswith("Tarea guardada: "):
            task_id = linea.split(":", 1)[1].strip()
            break
    if not task_id:
        print("No se pudo confirmar el ID. No se iniciará el agente.")
        return 2

    estado = ejecutar_comando("estado", task_id, "en_curso")
    print(estado.stdout, end="")
    if estado.returncode != 0:
        print(estado.stderr)
        print("No se iniciará el agente.")
        return 2

    print("\nIniciando el agente. Responde a sus confirmaciones en esta ventana.")
    print("Para cancelar una acción, responde algo distinto de SI.")
    try:
        # Hereda la consola para que las autorizaciones sigan siendo interactivas.
        resultado = subprocess.run(
            [sys.executable, str(AGENTE), tarea],
            cwd=str(BASE_DIR),
            check=False,
        )
        if resultado.returncode == 0:
            nuevo_estado = "completada"
        elif resultado.returncode == 3:
            nuevo_estado = "pendiente"
        elif resultado.returncode == 2:
            nuevo_estado = "fallida"
        else:
            nuevo_estado = "interrumpida"

        actualizacion = ejecutar_comando("estado", task_id, nuevo_estado)
        print(actualizacion.stdout, end="")
        if actualizacion.returncode != 0:
            print(actualizacion.stderr)
            print("ATENCIÓN: no se pudo actualizar el estado persistente.")
            return 2

        print(f"Resultado registrado: {nuevo_estado}")
        if nuevo_estado in {"fallida", "interrumpida"}:
            print("Revisa el registro antes de decidir si reintentar.")
        return 0 if nuevo_estado in {"completada", "pendiente"} else 2
    except KeyboardInterrupt:
        print("\nInterrupción detectada. Marcando la tarea como interrumpida.")
        actualizacion = ejecutar_comando("estado", task_id, "interrumpida")
        print(actualizacion.stdout, end="")
        if actualizacion.returncode != 0:
            print(actualizacion.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
