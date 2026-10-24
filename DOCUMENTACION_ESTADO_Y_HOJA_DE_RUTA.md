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
