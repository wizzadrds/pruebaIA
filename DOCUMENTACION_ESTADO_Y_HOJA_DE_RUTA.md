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
