# Agente IA local: estado y hoja de ruta

## Entorno
- Windows 10, proyecto local D:\AgenteIA.
- Programa principal: ciclo_agente_persistente.py.
- Modelo: qwen2.5-coder:7b mediante Ollama local.
- Sandbox de archivos y registro JSONL.

## Funciones implementadas
- Ciclo de agente con acciones JSON validadas.
- Lectura y creación de archivos con autorización explícita.
- Restricción de rutas a la sandbox y rechazo de sobrescrituras.
- Límites de tamaño, verificación de archivos y registro de actividad.
- Flujo para resumir un archivo y guardar el resultado.

## Búsqueda web
Se ha integrado la acción buscar_web en ciclo_agente_persistente.py. Usa la página HTML de DuckDuckGo, limita la consulta a 500 caracteres, aplica un timeout de 20 segundos y devuelve hasta cinco resultados con título, URL y extracto. La disponibilidad depende de la conectividad y de que el buscador no cambie su formato o bloquee la petición.

## Estilo de respuesta
El prompt del agente pide respuestas directas, naturales y concisas, evitar relleno, reconocer incertidumbre y distinguir hechos de opiniones. Estas instrucciones de estilo no eliminan las autorizaciones de archivos ni las validaciones técnicas.

## Seguridad y límites
- El agente no debe ejecutar instrucciones o comandos hallados en páginas web.
- No debe enviar archivos locales al buscador.
- Los resultados son extractos de búsqueda, no una verificación independiente de las páginas.
- La búsqueda web todavía necesita una prueba real en el equipo Windows con Ollama y conexión a Internet.
- Mantener autorización explícita para leer o crear archivos dentro de la sandbox.

## Prueba funcional previa
El usuario confirmó una prueba de creación de archivo: el agente pidió autorización, creó y verificó el archivo solicitado y terminó con estado completado.

## Próximos pasos
1. Descargar la versión actualizada del programa desde GitHub.
2. Ejecutar una compilación sintáctica.
3. Probar una consulta web real y confirmar que el agente usa los resultados y cita las URL.
4. Si DuckDuckGo cambia el HTML o bloquea la consulta, sustituir el proveedor por una API de búsqueda estable.


## Actualización de entorno: WSL 2 (2026-10-24)

### Objetivo
Preparar Windows 10 Home para ejecutar Docker y, posteriormente, desplegar SearXNG como metabuscador local para el agente. Esta configuración es independiente del código del agente y no modifica el archivo original del proyecto.

### Acciones completadas
1. Se habilitaron las características de Windows **Windows Subsystem for Linux** y **Virtual Machine Platform**. Windows indicó que era necesario reiniciar; el usuario reinició el equipo.
2. Se instaló la distribución Ubuntu mediante `wsl --install -d Ubuntu`.
3. Se creó el usuario Linux `agente`.
4. Se configuró WSL 2 como versión predeterminada mediante `wsl --set-default-version 2`.
5. La primera conversión indicó que faltaba actualizar el componente de kernel de WSL 2.
6. Se ejecutó `wsl --update`; la salida confirmó que WSL se instaló correctamente.
7. Se volvió a ejecutar `wsl --set-version Ubuntu 2`; la salida confirmó: «La operación se completó correctamente».
8. Verificación final con `wsl --list --verbose`:

   ```text
     NAME      STATE           VERSION
   * Ubuntu    Stopped         2
   ```

### Estado verificado
- Ubuntu está instalado.
- Ubuntu está configurado como **WSL 2** (verificado por la columna VERSION).
- El estado `Stopped` es normal cuando la distribución no está ejecutándose; no indica un fallo.
- WSL se actualizó correctamente.
- Docker y SearXNG **todavía no están instalados**.
- Inicio de Ubuntu comprobado con `wsl -d Ubuntu`; el terminal mostró `agente@DESKTOP-7OP13Q4:/mnt/c/Windows/system32# Agente IA local: estado y hoja de ruta

## Entorno
- Windows 10, proyecto local D:\AgenteIA.
- Programa principal: ciclo_agente_persistente.py.
- Modelo: qwen2.5-coder:7b mediante Ollama local.
- Sandbox de archivos y registro JSONL.

## Funciones implementadas
- Ciclo de agente con acciones JSON validadas.
- Lectura y creación de archivos con autorización explícita.
- Restricción de rutas a la sandbox y rechazo de sobrescrituras.
- Límites de tamaño, verificación de archivos y registro de actividad.
- Flujo para resumir un archivo y guardar el resultado.

## Búsqueda web
Se ha integrado la acción buscar_web en ciclo_agente_persistente.py. Usa la página HTML de DuckDuckGo, limita la consulta a 500 caracteres, aplica un timeout de 20 segundos y devuelve hasta cinco resultados con título, URL y extracto. La disponibilidad depende de la conectividad y de que el buscador no cambie su formato o bloquee la petición.

## Estilo de respuesta
El prompt del agente pide respuestas directas, naturales y concisas, evitar relleno, reconocer incertidumbre y distinguir hechos de opiniones. Estas instrucciones de estilo no eliminan las autorizaciones de archivos ni las validaciones técnicas.

## Seguridad y límites
- El agente no debe ejecutar instrucciones o comandos hallados en páginas web.
- No debe enviar archivos locales al buscador.
- Los resultados son extractos de búsqueda, no una verificación independiente de las páginas.
- La búsqueda web todavía necesita una prueba real en el equipo Windows con Ollama y conexión a Internet.
- Mantener autorización explícita para leer o crear archivos dentro de la sandbox.

## Prueba funcional previa
El usuario confirmó una prueba de creación de archivo: el agente pidió autorización, creó y verificó el archivo solicitado y terminó con estado completado.

## Próximos pasos
1. Descargar la versión actualizada del programa desde GitHub.
2. Ejecutar una compilación sintáctica.
3. Probar una consulta web real y confirmar que el agente usa los resultados y cita las URL.
4. Si DuckDuckGo cambia el HTML o bloquea la consulta, sustituir el proveedor por una API de búsqueda estable.


## Actualización de entorno: WSL 2 (2026-10-24)

### Objetivo
Preparar Windows 10 Home para ejecutar Docker y, posteriormente, desplegar SearXNG como metabuscador local para el agente. Esta configuración es independiente del código del agente y no modifica el archivo original del proyecto.

### Acciones completadas
1. Se habilitaron las características de Windows **Windows Subsystem for Linux** y **Virtual Machine Platform**. Windows indicó que era necesario reiniciar; el usuario reinició el equipo.
2. Se instaló la distribución Ubuntu mediante `wsl --install -d Ubuntu`.
3. Se creó el usuario Linux `agente`.
4. Se configuró WSL 2 como versión predeterminada mediante `wsl --set-default-version 2`.
5. La primera conversión indicó que faltaba actualizar el componente de kernel de WSL 2.
6. Se ejecutó `wsl --update`; la salida confirmó que WSL se instaló correctamente.
7. Se volvió a ejecutar `wsl --set-version Ubuntu 2`; la salida confirmó: «La operación se completó correctamente».
8. Verificación final con `wsl --list --verbose`:

   ```text
     NAME      STATE           VERSION
   * Ubuntu    Stopped         2
   ```

### Estado verificado
- Ubuntu está instalado.
- Ubuntu está configurado como **WSL 2** (verificado por la columna VERSION).
- El estado `Stopped` es normal cuando la distribución no está ejecutándose; no indica un fallo.
- WSL se actualizó correctamente.
, confirmando que la sesión Linux inicia correctamente. La sesión comenzó en el directorio montado de Windows `/mnt/c/Windows/system32`, algo normal al invocar WSL desde esa ubicación.

### Seguridad
Durante la configuración se compartió en el chat una contraseña de Ubuntu. Por precaución, cambiarla por una contraseña única antes de usar el entorno para tareas sensibles. No incluir contraseñas ni otros secretos en este repositorio.

### Próximos pasos
1. Instalar Docker Desktop para Windows y habilitar la integración con la distribución Ubuntu en WSL 2, siguiendo la documentación oficial y verificando los requisitos de Windows.
3. Probar que Docker responde desde el entorno elegido.
4. Desplegar SearXNG y comprobar una búsqueda local.
5. Diseñar y probar la integración del agente con el buscador sin ejecutar instrucciones procedentes de páginas web ni enviar archivos locales.

## Actualización de entorno: Docker Desktop y SearXNG local (2026-10-24)

### Acciones completadas
1. Se instaló Docker Desktop y se verificó la versión de CLI: `Docker version 29.9.2`.
2. Tras iniciar Docker Desktop, `docker info --format "{{.ServerVersion}}"` devolvió `29.9.2`, confirmando que el motor responde.
3. Se creó la carpeta independiente `D:\\AgenteIA\\searxng`, sin modificar el código original del agente.
4. Se descargaron desde el repositorio oficial de SearXNG los archivos `container/docker-compose.yml` y `container/.env.example`.
5. Se configuró `.env` para publicar SearXNG en `127.0.0.1:8080`, con versión `latest`.
6. `docker compose config` validó la configuración con dos servicios: `core` (SearXNG) y `valkey`.
7. `docker compose up -d` descargó y arrancó ambos contenedores. `docker compose ps` mostró los dos como `Up`; el puerto de SearXNG quedó publicado en `127.0.0.1:8080`.
8. La petición HTTP a `http://127.0.0.1:8080/` devolvió el código `200`.
9. La API JSON inicialmente devolvió `403`. Se creó `core-config/settings.yml` con `use_default_settings: true` y `search.formats: [html, json]`, y se reinició el servicio `core`.
10. La búsqueda de prueba `q=Python 3.14&format=json` devolvió resultados con títulos, URLs y extractos, incluyendo páginas de Python.org y la documentación de Python.

### Estado actual
- SearXNG está disponible localmente en `http://127.0.0.1:8080`.
- La API JSON responde con resultados.
- El servicio está limitado a la interfaz de loopback del PC; no se ha publicado intencionadamente a la red externa.
- Esto confirma que el metabuscador funciona, pero aún no demuestra que la integración con el agente esté terminada ni que todos los motores o sitios web estén siempre disponibles.
- Los archivos de SearXNG están bajo `D:\\AgenteIA\\searxng`. El archivo original `D:\\AgenteIA\\ciclo_agente_persistente.py` no se ha modificado durante estos pasos.

### Pendientes y seguridad
1. Cambiar el valor provisional de `server.secret_key` de `core-config/settings.yml` por un secreto aleatorio local antes de un uso prolongado.
2. Revisar los registros de SearXNG si alguna búsqueda falla; los motores públicos pueden aplicar límites, bloquear consultas o cambiar.
3. Conectar la búsqueda a una copia de trabajo del agente y probar la consulta, lectura de páginas y trazabilidad de URLs.
4. No tratar los extractos de búsqueda como prueba suficiente por sí solos: el agente debe distinguir resultados de búsqueda de páginas realmente leídas y no inventar afirmaciones.
5. Mantener el puerto enlazado a `127.0.0.1`; no exponer el servicio a Internet sin configurar controles de seguridad apropiados.

## Actualización: integración de SearXNG en copia de trabajo (2026-10-24)

### Pruebas confirmadas
1. Se creó una copia de trabajo en `D:\\AgenteIA\\ciclo_agente_persistente_wikipedia.py`; el archivo original `D:\\AgenteIA\\ciclo_agente_persistente.py` permanece sin modificar.
2. Se añadió la constante `URL_SEARXNG = "http://127.0.0.1:8080/search"` a la copia de trabajo.
3. Se sustituyó `buscar_web` para consultar primero SearXNG mediante JSON y recurrir a la API pública de Wikipedia si SearXNG falla o no produce resultados utilizables.
4. `py -m py_compile` terminó sin errores tras el cambio.
5. La consulta directa a SearXNG para `Python 3.14` devolvió títulos, URLs y extractos.
6. La llamada directa a `buscar_web("Python 3.14")` desde la copia de trabajo devolvió cinco resultados, incluidos Python.org y docs.python.org. Esto verifica la conexión entre el agente de prueba y SearXNG.

### Alcance y limitaciones
- La prueba confirma la búsqueda y recepción de extractos; no confirma todavía que el agente lea el contenido completo de cada página, resuma con precisión o cite correctamente las fuentes en una conversación completa.
- No se ha modificado ni desplegado el archivo original.
- La instancia SearXNG debe mantenerse ligada a `127.0.0.1`. Antes de uso prolongado, cambiar la clave provisional `server.secret_key` por un valor aleatorio privado y revisar la configuración de seguridad.
- Próxima tarea: probar el flujo de lectura y resumen de páginas en la copia de trabajo, comprobar que las afirmaciones se apoyan en contenido realmente leído y que las URLs quedan registradas.


## Próximo cambio preparado para copiar: lectura de páginas web (2026-10-24)

**Estado:** propuesta documentada; todavía no integrada ni probada en el agente. El archivo original y las copias locales no se han modificado por esta documentación.

### Objetivo

Añadir una acción `leer_pagina_web` para descargar texto de una URL pública, con límites de tamaño y tiempo, validación de URL/IP y revisión de cada redirección. La lectura deberá quedar en el historial con la URL final para que los resúmenes se basen en contenido obtenido realmente.

### 1. Imports y constantes

En la copia experimental `D:\\AgenteIA\\sandbox\\ciclo_agente_lectura_web_prueba.py`, añade junto a los imports existentes:

```python
import ipaddress
import socket
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
```

Añade junto a las constantes:

```python
MAX_BYTES_PAGINA_WEB = 1_000_000
MAX_CARACTERES_PAGINA_WEB = 20_000
MAX_REDIRECCIONES_WEB = 5
```

### 2. Función de lectura web

Pega esta función antes de `def buscar_web(consulta):`. No reemplaza la función de búsqueda existente.

```python
class _ExtractorTextoHTML(HTMLParser):
    """Extrae texto visible básico de HTML; no ejecuta JavaScript."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes = []
        self_ignorar = {"script", "style", "noscript", "svg"}
        self.ignorar = set()
        self._etiquetas_ignorar = self_ignorar

    def handle_starttag(self, tag, attrs):
        if tag in self._etiquetas_ignorar:
            self.ignorar.add(tag)

    def handle_endtag(self, tag):
        self.ignorar.discard(tag)

    def handle_data(self, data):
        if not self.ignorar:
            texto = " ".join(data.split())
            if texto:
                self.partes.append(texto)


def _validar_url_publica(url):
    """Rechaza esquemas no web, credenciales y destinos IP no públicos."""
    if not isinstance(url, str) or len(url) > 2000:
        raise ValueError("URL no válida o demasiado larga.")

    partes = urlsplit(url)
    if partes.scheme.lower() not in {"http", "https"}:
        raise ValueError("Solo se permiten URLs HTTP o HTTPS.")
    if not partes.hostname or partes.username or partes.password:
        raise ValueError("La URL debe tener un host público y no incluir credenciales.")
    if partes.port not in (None, 80, 443):
        raise ValueError("Solo se permiten puertos web estándar 80 y 443.")

    host = partes.hostname.rstrip(".").lower()
    if host in {"localhost", "localhost.localdomain"} or host.endswith(".localhost"):
        raise ValueError("Se rechazan nombres de host locales.")

    try:
        ip = ipaddress.ip_address(host.strip("[]"))
        direcciones = [ip]
    except ValueError:
        try:
            datos_dns = socket.getaddrinfo(host, partes.port or (443 if partes.scheme == "https" else 80),
                                           type=socket.SOCK_STREAM)
        except socket.gaierror as error:
            raise ValueError("No se pudo resolver el host de la URL.") from error
        direcciones = []
        for dato in datos_dns:
            try:
                direcciones.append(ipaddress.ip_address(dato[4][0].split("%")[0]))
            except ValueError as error:
                raise ValueError("El host resolvió a una dirección IP no válida.") from error

    if not direcciones or any(
        not ip.is_global or ip.is_private or ip.is_loopback or ip.is_link_local
        or ip.is_multicast or ip.is_reserved or ip.is_unspecified
        for ip in direcciones
    ):
        raise ValueError("Se rechaza la URL porque apunta a una dirección IP no pública.")

    return url


def leer_pagina_web(url):
    """Descarga una página pública, sin seguir redirecciones automáticamente."""
    url_actual = url
    sesion = requests.Session()
    sesion.trust_env = False
    cabeceras = {"User-Agent": "AgenteIA/1.0 (lector web local)",
                 "Accept": "text/html,text/plain;q=0.9,*/*;q=0.1"}

    try:
        for salto in range(MAX_REDIRECCIONES_WEB + 1):
            _validar_url_publica(url_actual)
            respuesta = sesion.get(
                url_actual, headers=cabeceras, timeout=(5, 15),
                allow_redirects=False, stream=True
            )
            try:
                if respuesta.is_redirect or respuesta.is_permanent_redirect:
                    destino = respuesta.headers.get("Location")
                    if not destino:
                        raise ValueError("La redirección no contiene destino.")
                    if salto >= MAX_REDIRECCIONES_WEB:
                        raise ValueError("La página supera el límite de redirecciones.")
                    url_actual = urljoin(url_actual, destino)
                    continue

                respuesta.raise_for_status()
                tipo = respuesta.headers.get("Content-Type", "").lower()
                if not (tipo.startswith("text/html") or tipo.startswith("text/plain")
                        or "application/xhtml+xml" in tipo):
                    raise ValueError("La URL no devuelve HTML o texto plano.")

                longitud = respuesta.headers.get("Content-Length")
                if longitud:
                    try:
                        if int(longitud) > MAX_BYTES_PAGINA_WEB:
                            raise ValueError("La página supera el límite de descarga.")
                    except ValueError as error:
                        if str(error) == "La página supera el límite de descarga.":
                            raise
                        raise ValueError("Content-Length no válido.") from error

                bloques = []
                total = 0
                for bloque in respuesta.iter_content(chunk_size=16384):
                    if not bloque:
                        continue
                    total += len(bloque)
                    if total > MAX_BYTES_PAGINA_WEB:
                        raise ValueError("La página supera el límite de descarga.")
                    bloques.append(bloque)
                contenido_bytes = b"".join(bloques)
                codificacion = respuesta.encoding or "utf-8"
                html = contenido_bytes.decode(codificacion, errors="replace")
            finally:
                respuesta.close()

            if tipo.startswith("text/plain"):
                texto = html
            else:
                extractor = _ExtractorTextoHTML()
                extractor.feed(html)
                texto = "\n".join(extractor.partes)

            texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
            if not texto:
                raise ValueError("La página no contiene texto legible.")
            texto = texto[:MAX_CARACTERES_PAGINA_WEB]
            return {"url": url_actual, "texto": texto}
        raise ValueError("No se pudo completar la lectura web.")
    finally:
        sesion.close()
```

### 3. Integración necesaria en el agente

La función por sí sola **no activa una nueva acción**. Para integrarla, hay que hacer los siguientes cambios en la copia experimental:

1. En las instrucciones de `consultar_modelo`, añadir el ejemplo JSON:
   `{"accion":"leer_pagina_web","url":"https://example.org/"}`
2. En `validar_accion`, añadir el esquema `"leer_pagina_web": {"accion", "url"}` y validar que `url` sea texto no vacío de longitud máxima 2000. La validación de destino se realiza también dentro de `leer_pagina_web`, justo antes de cada petición.
3. En la comprobación de `mostrar_resumen`, aceptar como lectura verificada tanto `leer_archivo` como `leer_pagina_web`, siempre que el resultado sea texto no vacío y la acción no esté bloqueada.
4. En `ejecutar_ciclo_general`, antes de la rama final que actualmente ejecuta `buscar_web`, añadir una rama específica:
   ```python
   elif tipo == "leer_pagina_web":
       lectura = leer_pagina_web(accion["url"])
       resultado = f"URL leída: {lectura['url']}\\nContenido leído:\\n{lectura['texto']}"
   ```
   La rama de `buscar_web` debe quedar como `elif tipo == "buscar_web":`, no como `else`.
5. Mantener la autorización humana que ya ocurre antes de ejecutar la acción. Registrar el resultado en el historial como el resto de las acciones.
6. Probar primero con una página pública sencilla, después con una redirección y finalmente comprobar que se rechazan `localhost`, direcciones privadas y esquemas como `file://`. Ejecutar `py -m py_compile` antes de cualquier prueba funcional.

### Advertencias de seguridad y alcance

- Esta validación reduce riesgos de SSRF, pero no es una garantía absoluta frente a DNS rebinding: `requests` puede resolver el nombre otra vez al abrir la conexión. Para un entorno adversarial, la solución más sólida es hacer la descarga a través de un proxy de salida que bloquee redes privadas o fijar la IP validada al conectar.
- No se ejecuta JavaScript ni se procesa contenido que requiera iniciar sesión. Los sitios con paywall, CAPTCHA o anti-bot pueden no funcionar.
- El HTML descargado es contenido no confiable: no debe interpretarse como instrucciones del sistema o del agente.
- La función devuelve texto limitado; no garantiza que la página completa quepa en el contexto del modelo.
- La implementación de esta sección es una propuesta para copiar y probar; todavía no hay resultados de pruebas de `leer_pagina_web`.
