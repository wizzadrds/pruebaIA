# Validación de búsqueda web y revisión semántica — candidata local

**Fecha de registro:** 2026-10-26  
**Repositorio:** [wizzadrds/pruebaIA](https://github.com/wizzadrds/pruebaIA)  
**Estado:** componentes probados de forma aislada; aceptación del ciclo completo pendiente.

## Alcance y seguridad

El trabajo se realizó sobre una candidata local situada en:

`D:\AgenteIA\sandbox\candidato_revision_semantica\ciclo_agente_candidato.py`

No se ejecutaron `main()` ni `ejecutar_ciclo_general()`. El agente original no se modificó. Las pruebas aisladas importaron el módulo candidato y llamaron funciones específicas; no escribieron archivos del agente.

La candidata local **no se ha incorporado a este repositorio** como código. Este documento registra resultados y no implica que la versión local sea idéntica a algún archivo ya versionado aquí.

## Resultados verificados

### Pruebas automatizadas

Se ejecutó la suite local:

- `prueba_integracion_revision_semantica.py`
- `prueba_revision_evidencias.py`
- `prueba_revisor_simulado.py`

Resultado: **23 pruebas superadas (23/23)**. La candidata también pasó la comprobación de sintaxis mediante `ast.parse`.

### Búsqueda web real

Se llamó directamente a `buscar_web("Python official documentation")`. La función devolvió una lista de resultados con título, URL y extracto, incluidos:

- `https://www.python.org/doc/`
- `https://docs.python.org/`
- `https://docs.python.org/3/`

Resultado: búsqueda funcional para esta consulta de prueba.

### Lectura de una página real

Se llamó directamente a `leer_pagina_web("https://www.python.org/doc/")`. La función devolvió un diccionario con URL y texto extraído. El texto incluyó contenido pertinente sobre tutoriales, referencias, guías y descarga de la documentación.

Limitación observada: la página indicó que mostraba contenido alternativo porque los scripts interactivos no se ejecutaron. Por ello, la extracción de texto puede ser incompleta para páginas que dependen de JavaScript.

### Extracción de evidencia

Se comprobaron tres casos aislados:

- Afirmación literal presente en la fuente: encontró un fragmento.
- Afirmación relacionada con el texto: encontró un fragmento candidato para revisión semántica.
- Afirmación sin evidencia textual pertinente: no encontró fragmentos.

Esto comprueba el comportamiento de esos ejemplos, no la exhaustividad de la heurística para todas las fuentes.

### Revisión semántica con Ollama

Pruebas reales aisladas realizadas con el modelo local:

- Tres afirmaciones respaldadas por una fuente breve: resultado `True`.
- Resumen que contenía afirmaciones incorrectas o no respaldadas: resultado `False`.
- Resumen generado a partir de texto de documentación de Python: el revisor devolvió `True`.

Estas pruebas son ejemplos controlados y no garantizan que el modelo detecte todas las falsedades ni que siempre clasifique correctamente una afirmación.

### Decisión del modelo y formato del resumen

Se llamó directamente a `consultar_modelo(tarea, historial, paso)` con un historial de lectura preparado para la prueba. Ollama devolvió la acción `mostrar_resumen` con exactamente tres puntos, coherentes con el texto de entrada.

**Importante:** el historial de esta prueba se construyó explícitamente en el script de prueba. Por tanto, esta prueba valida la decisión del modelo con un historial representativo, pero no valida el ciclo real de orquestación de extremo a extremo.

## Identificación de la candidata y copias de seguridad

SHA-256 informado por PowerShell para la candidata local:

`811791f0d78b50ea81b74b242354ab2ad084068030b8e6cdecb3fc2f9beed6e8`

Backups locales registrados:

| Archivo | SHA-256 |
|---|---|
| `ciclo_agente_candidato.py.bak_revision_semantica` | `a32d7f5e3f56f0bbe36c7dfd0624dfd6bfdf4fd7404e3e3df77f229ab07cb2f6` |
| `ciclo_agente_candidato.py.bak_cierre_integral` | `082b9c76f35788947b73bff26b99b8e30d45974b491df2c324a6fc2f29287b61` |
| `ciclo_agente_candidato.py.bak_evidencia` | `7e73a2f74c90b9fae951123e14932d4ec7155a11d2b331bd02879e15ffe94cee` |

Los backups se encuentran en el entorno local y no se han subido con este documento.

## Pendiente antes de declarar validado el flujo completo

La aceptación de extremo a extremo **todavía no se ha realizado**. Falta una prueba controlada que compruebe la secuencia real de orquestación:

1. buscar en la web;
2. seleccionar una URL devuelta por la búsqueda;
3. leer la página y registrar el contenido real;
4. generar un resumen a partir de esa lectura real;
5. revisar el resumen contra la evidencia;
6. comprobar que el resultado final se gestiona correctamente, incluidos errores o falta de evidencia.

Hasta completar esa prueba, el estado correcto es **“componentes principales probados de forma aislada; ciclo completo pendiente”**.

## Restricciones de seguridad mantenidas

- No ejecutar `main()` ni `ejecutar_ciclo_general()` durante las pruebas aisladas descritas.
- No modificar el agente original.
- No restaurar ni sobrescribir backups automáticamente.
- No tratar una respuesta del modelo como prueba suficiente sin contrastarla con la evidencia.
- No afirmar autonomía prolongada ni fiabilidad general basándose en estas pruebas.
