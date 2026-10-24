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

