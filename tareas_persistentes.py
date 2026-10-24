"""Memoria persistente de tareas para el prototipo del agente.

Este módulo SOLO administra una cola JSON local. No ejecuta tareas ni herramientas.
Uso:
  py tareas_persistentes.py nueva "Descripción de la tarea"
  py tareas_persistentes.py listar
  py tareas_persistentes.py ver ID
  py tareas_persistentes.py estado ID pendiente|en_curso|completada|fallida|interrumpida
  py tareas_persistentes.py recuperar
"""
import json
import os
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
QUEUE_FILE = BASE_DIR / "tareas_pendientes.json"
STATUSES = {"pendiente", "en_curso", "completada", "fallida", "interrumpida"}


def now():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_tasks():
    if not QUEUE_FILE.exists():
        return []
    with QUEUE_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("La cola de tareas no contiene una lista JSON.")
    for item in data:
        if not isinstance(item, dict) or not {"id", "tarea", "estado", "creada", "actualizada"} <= set(item):
            raise ValueError("Formato de tarea inválido; no se modificó el archivo.")
        if item["estado"] not in STATUSES:
            raise ValueError("Estado de tarea desconocido; no se modificó el archivo.")
    return data


def save_tasks(tasks):
    # Escribir temporal y reemplazar evita dejar JSON parcialmente escrito.
    fd, temp_name = tempfile.mkstemp(prefix="tareas_", suffix=".tmp", dir=str(BASE_DIR))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_name, QUEUE_FILE)
    finally:
        try:
            if os.path.exists(temp_name):
                os.remove(temp_name)
        except OSError:
            pass


def new_task(description):
    description = description.strip()
    if not description:
        raise ValueError("La descripción no puede estar vacía.")
    tasks = load_tasks()
    task_id = uuid.uuid4().hex[:8]
    stamp = now()
    tasks.append({
        "id": task_id,
        "tarea": description,
        "estado": "pendiente",
        "creada": stamp,
        "actualizada": stamp,
        "nota": "Guardada; todavía no ejecutada.",
    })
    save_tasks(tasks)
    print(f"Tarea guardada: {task_id}")
    print("Estado: pendiente (no se ha ejecutado ninguna acción).")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No hay tareas guardadas.")
        return
    for t in tasks:
        print(f'{t["id"]} | {t["estado"]} | {t["tarea"]}')


def show_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            print(json.dumps(t, ensure_ascii=False, indent=2))
            return
    raise KeyError(f"No existe la tarea {task_id}.")


def change_status(task_id, status):
    if status not in STATUSES:
        raise ValueError("Estado inválido. Opciones: " + ", ".join(sorted(STATUSES)))
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["estado"] = status
            t["actualizada"] = now()
            if status == "interrumpida":
                t["nota"] = "Revisar manualmente; no se reanudará automáticamente."
            save_tasks(tasks)
            print(f'Tarea {task_id}: estado actualizado a {status}.')
            return
    raise KeyError(f"No existe la tarea {task_id}.")


def recover():
    tasks = load_tasks()
    changed = False
    for t in tasks:
        if t["estado"] == "en_curso":
            t["estado"] = "interrumpida"
            t["actualizada"] = now()
            t["nota"] = "Detectada al consultar recuperación. Revisar antes de continuar; no se ejecutará automáticamente."
            changed = True
    if changed:
        save_tasks(tasks)
    print("Tareas que requieren revisión:")
    found = False
    for t in tasks:
        if t["estado"] in {"pendiente", "interrumpida", "fallida"}:
            found = True
            print(f'{t["id"]} | {t["estado"]} | {t["tarea"]}')
    if not found:
        print("No hay tareas pendientes, interrumpidas ni fallidas.")
    print("Seguridad: recuperar solo muestra estado; nunca ejecuta tareas.")


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    command = argv[1].lower()
    try:
        if command == "nueva" and len(argv) >= 3:
            new_task(" ".join(argv[2:]))
        elif command == "listar" and len(argv) == 2:
            list_tasks()
        elif command == "ver" and len(argv) == 3:
            show_task(argv[2])
        elif command == "estado" and len(argv) == 4:
            change_status(argv[2], argv[3].lower())
        elif command == "recuperar" and len(argv) == 2:
            recover()
        else:
            print(__doc__.strip())
            return 2
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Error: {type(exc).__name__}: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
