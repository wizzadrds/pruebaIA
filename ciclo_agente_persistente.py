import json
import re
import sys
from datetime import datetime
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
SANDBOX = (BASE_DIR / "sandbox").resolve()
API_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"
LOG_FILE = BASE_DIR / "registro.jsonl"
MAX_PASOS = 6
TIMEOUT_SEGUNDOS = 180


def registrar(datos):
    entrada = dict(datos)
    entrada["fecha"] = datetime.now().astimezone().isoformat()
    with LOG_FILE.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(entrada, ensure_ascii=False) + "\n")


def resolver_ruta(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("Nombre de archivo no válido.")
    if nombre in {".", ".."} or Path(nombre).name != nombre:
        raise ValueError("Solo se permiten nombres de archivo simples.")
    if (any(c in nombre for c in '<>:"/\\|?*')
            or nombre.endswith((" ", "."))
            or any(ord(c) < 32 for c in nombre)):
        raise ValueError("El nombre contiene caracteres no permitidos.")
    base = nombre.split(".")[0].upper()
    if re.fullmatch(r"(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])", base):
        raise ValueError("Nombre reservado por Windows.")
    ruta = (SANDBOX / nombre).resolve()
    if not ruta.is_relative_to(SANDBOX) or ruta == SANDBOX:
        raise ValueError("Ruta rechazada: fuera de la sandbox.")
    return ruta


def pedir_autorizacion(descripcion):
    print("\n" + descripcion)
    return input("¿Autorizas esta acción? Escribe SI: ").strip() == "SI"


def leer_archivo(nombre):
    ruta = resolver_ruta(nombre)
    if ruta.is_symlink():
        raise ValueError("No se permite leer enlaces simbólicos.")
    if not ruta.is_file():
        raise FileNotFoundError(f"No existe el archivo: {nombre}")
    return ruta.read_text(encoding="utf-8-sig")


def crear_archivo_nuevo(nombre, contenido):
    ruta = resolver_ruta(nombre)
    if ruta.exists() or ruta.is_symlink():
        raise FileExistsError(
            f"Ya existe {nombre}; no se sobrescribirá. Elige otro nombre."
        )
    with ruta.open("x", encoding="utf-8") as archivo:
        archivo.write(contenido)
    if not ruta.is_file() or ruta.read_text(encoding="utf-8") != contenido:
        raise IOError("No se pudo verificar el archivo creado.")
    return ruta


def llamar_modelo(prompt):
    respuesta = requests.post(
        API_URL,
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        timeout=TIMEOUT_SEGUNDOS,
    )
    respuesta.raise_for_status()
    datos = respuesta.json()
    texto = datos.get("message", {}).get("content")
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError("El modelo no devolvió texto.")
    return texto.strip()


def generar_resumen(tarea, nombre_origen, contenido):
    prompt = f"""
Resume el texto siguiente en una sola frase en español.
Tarea del usuario: {tarea}
Nombre del archivo de origen: {nombre_origen}

CONTENIDO REAL LEÍDO:
--- INICIO ---
{contenido}
--- FIN ---

Requisitos:
- Devuelve solo una frase de resumen.
- Expresa el propósito e instrucciones principales del texto.
- Usa tus propias palabras, no copies el texto completo.
- No digas que el archivo contiene un resumen.
- No inventes información.
"""
    resumen = llamar_modelo(prompt)
    resumen = resumen.strip().strip('"').strip()
    if not resumen:
        raise ValueError("El resumen está vacío.")
    if len(resumen) > 1200:
        raise ValueError("El resumen es demasiado largo; no se guardará.")
    return resumen


def ejecutar_tarea_resumen(tarea):
    # Se esperan nombres .txt explícitos en la tarea: primero origen, último destino.
    nombres = re.findall(r"(?<![\\w.-])([A-Za-z0-9_-]+\.txt)\b", tarea,
                         flags=re.IGNORECASE)
    if len(nombres) < 2:
        print("Para esta modalidad indica el archivo de origen y el de salida,")
        print("por ejemplo: Lee prueba.txt, resume sus ideas y guarda el resultado en resumen_final.txt.")
        return

    nombre_origen = nombres[0]
    nombre_salida = nombres[-1]
    resolver_ruta(nombre_origen)
    resolver_ruta(nombre_salida)

    if nombre_origen.casefold() == nombre_salida.casefold():
        raise ValueError("El archivo de salida no puede ser el archivo de origen.")

    # Comprobación temprana: no pedir permisos ni llamar al modelo si el destino ya existe.
    ruta_salida = resolver_ruta(nombre_salida)
    if ruta_salida.exists() or ruta_salida.is_symlink():
        raise FileExistsError(
            f"Ya existe {nombre_salida}; no se sobrescribirá. Elige otro nombre."
        )

    if not pedir_autorizacion(f"Voy a leer el archivo {nombre_origen}."):
        print("Lectura cancelada.")
        return
    contenido = leer_archivo(nombre_origen)
    registrar({
        "tarea": tarea, "accion": "leer_archivo", "nombre": nombre_origen,
        "resultado": contenido, "estado": "completada",
    })
    print("\nContenido leído:")
    print(contenido)

    print("\nGenerando resumen a partir del contenido real leído...")
    resumen = generar_resumen(tarea, nombre_origen, contenido)
    print("\nResumen propuesto:")
    print(resumen)

    if not pedir_autorizacion(
        f"Voy a crear {nombre_salida} con el resumen mostrado arriba."
    ):
        print("Creación cancelada. No se ha escrito ningún archivo.")
        registrar({
            "tarea": tarea, "accion": "crear_archivo",
            "nombre": nombre_salida, "estado": "cancelada",
        })
        return

    ruta = crear_archivo_nuevo(nombre_salida, resumen + "\n")
    contenido_verificado = ruta.read_text(encoding="utf-8")
    if contenido_verificado.strip() != resumen:
        raise IOError("El contenido guardado no coincide con el resumen aprobado.")

    print(f"\nCorrecto: se creó y verificó {ruta.name}.")
    print("Contenido guardado:")
    print(contenido_verificado)
    registrar({
        "tarea": tarea, "accion": "crear_archivo", "nombre": nombre_salida,
        "resultado": contenido_verificado, "estado": "creado_y_verificado",
    })


def consultar_modelo(tarea, historial, paso):
    prompt = f"""
Eres un agente con herramientas limitadas. Paso {paso}/{MAX_PASOS}.
Devuelve exclusivamente un objeto JSON válido.
Acciones permitidas:
{{"accion":"leer_archivo","nombre":"prueba.txt"}}
{{"accion":"crear_archivo","nombre":"resultado.txt","contenido":"texto"}}
{{"accion":"terminar","mensaje":"explicación final"}}
Usa el historial real. No repitas lecturas correctas. No sobrescribas archivos.
No inventes resultados ni afirmes que una acción se completó sin confirmación.
Si la tarea pide resumir y guardar, usa el contenido leído y crea el archivo solicitado.
TAREA: {tarea}
HISTORIAL REAL: {json.dumps(historial, ensure_ascii=False)}
"""
    texto = llamar_modelo(prompt)
    try:
        accion = json.loads(texto)
    except json.JSONDecodeError as error:
        raise ValueError(f"El modelo no devolvió JSON válido: {error}") from error
    if not isinstance(accion, dict):
        raise ValueError("La respuesta del modelo debe ser un objeto JSON.")
    return accion


def validar_accion(accion):
    if not isinstance(accion, dict):
        raise ValueError("La acción debe ser un objeto JSON.")
    tipo = accion.get("accion")
    esquemas = {
        "leer_archivo": {"accion", "nombre"},
        "crear_archivo": {"accion", "nombre", "contenido"},
        "terminar": {"accion", "mensaje"},
    }
    if tipo not in esquemas or set(accion) != esquemas[tipo]:
        raise ValueError("Acción no permitida o campos incorrectos.")
    if tipo in {"leer_archivo", "crear_archivo"}:
        resolver_ruta(accion["nombre"])
    if tipo == "crear_archivo" and (
        not isinstance(accion["contenido"], str) or not accion["contenido"].strip()
    ):
        raise ValueError("El contenido debe ser texto no vacío.")
    if tipo == "terminar" and not isinstance(accion["mensaje"], str):
        raise ValueError("El mensaje final debe ser texto.")
    return tipo


def ejecutar_ciclo_general(tarea):
    historial = []
    lecturas = set()
    for paso in range(1, MAX_PASOS + 1):
        print(f"\n===== PASO {paso}/{MAX_PASOS} =====")
        accion = consultar_modelo(tarea, historial, paso)
        tipo = validar_accion(accion)

        if tipo == "leer_archivo" and accion["nombre"].casefold() in lecturas:
            print("Lectura repetida bloqueada; se usará el contenido anterior.")
            historial.append({
                "paso": paso, "accion": accion,
                "resultado": "Lectura repetida bloqueada.", "estado": "bloqueada",
            })
            continue

        print("\nAcción propuesta:")
        print(json.dumps(accion, ensure_ascii=False, indent=2))
        if tipo == "terminar":
            print("\nEl agente termina:")
            print(accion["mensaje"])
            registrar({
                "tarea": tarea, "paso": paso, "accion": accion,
                "estado": "terminado",
            })
            return

        if not pedir_autorizacion("¿Autorizas la acción mostrada?"):
            print("Acción cancelada; ciclo detenido.")
            registrar({"tarea": tarea, "paso": paso, "accion": accion,
                       "estado": "cancelada"})
            return

        if tipo == "leer_archivo":
            resultado = leer_archivo(accion["nombre"])
            lecturas.add(accion["nombre"].casefold())
        else:
            ruta = crear_archivo_nuevo(accion["nombre"], accion["contenido"])
            resultado = f"Archivo creado y verificado: {ruta.name}"

        print("\nResultado real:")
        print(resultado)
        historial.append({
            "paso": paso, "accion": accion, "resultado": resultado,
        })
        registrar({
            "tarea": tarea, "paso": paso, "accion": accion,
            "resultado": resultado, "estado": "completada",
        })
    print("\nSe alcanzó el límite de pasos.")
    registrar({"tarea": tarea, "estado": "limite_alcanzado",
               "max_pasos": MAX_PASOS})


def main():
    if not SANDBOX.is_dir():
        raise FileNotFoundError(f"No existe la carpeta sandbox: {SANDBOX}")
    tarea = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else input("¿Qué quieres que haga el agente en la sandbox? ").strip()
    if not tarea:
        print("No se ha indicado ninguna tarea.")
        return

    normalizada = tarea.casefold()
    es_resumen_y_guardado = (
        any(palabra in normalizada for palabra in ("resume", "resumen", "resume"))
        and any(palabra in normalizada for palabra in ("guarda", "guardar", "guarde"))
    )

    try:
        if es_resumen_y_guardado:
            ejecutar_tarea_resumen(tarea)
        else:
            ejecutar_ciclo_general(tarea)
    except (requests.RequestException, ValueError, OSError) as error:
        mensaje = f"{type(error).__name__}: {error}"
        print(f"\nTarea no completada: {mensaje}")
        registrar({"tarea": tarea, "estado": "error", "error": mensaje})


if __name__ == "__main__":
    main()
