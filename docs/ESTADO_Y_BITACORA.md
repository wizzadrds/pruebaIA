# Estado del proyecto y bitácora

**Proyecto:** pruebaIA  
**Última actualización:** 2026-10-24  
**Estado general:** modelo local Qwen2.5-Coder 7B descargado y primera respuesta en español verificada; conectividad LAN y servidor web de prueba verificados. El agente autónomo aún no está integrado.

## 1. Objetivo y alcance

Crear un agente de IA local en el sobremesa Windows, con acceso desde el portátil a un panel web, orientado a programación, Git/GitHub, ejecución de tareas con supervisión y apoyo a flujos de trabajo de Blender/3D. Se priorizan herramientas gratuitas/locales, pasos seguros y un consumo de recursos compatible con estudiar y trabajar en el equipo.

## 2. Entorno conocido

### Sobremesa (anfitrión previsto)

- Sistema: Windows 10 Home de 64 bits.
- CPU: AMD Ryzen 5 3600, 6 núcleos / 12 hilos.
- RAM: 16 GB (2 × 8 GB Kingston, 2400 MHz).
- GPU: NVIDIA GeForce GTX 1660 SUPER, 6 GB de VRAM dedicada.
- Unidad C:: Kingston SA400S37960G, aproximadamente 80 GB libres según el informe anterior.
- Unidad D:: Kingston SKC3000S1024G, aproximadamente 407 GB libres según el informe anterior.
- Python: `py --version` informó Python 3.14.6; `python --version` informó Python 3.12.0.
- `py -m pip --version` funciona.
- Nombre de equipo registrado: `DESKTOP-7OP13Q4`.
- IP LAN registrada: `192.168.1.131`.

### Portátil (panel/cliente previsto)

- Nombre de equipo registrado: `LAPTOP-V2QSMC01`.
- IP LAN registrada: `192.168.1.138`.
- Wi-Fi: `MIWIFI_T4A3`.
- Sistema y hardware del portátil: pendientes de inventario fiable.

### Red local y seguridad

- Router registrado: Sagemcom F@st 5670/6870.
- Ambos equipos estaban en la misma LAN.
- El perfil Ethernet del sobremesa y el perfil Wi-Fi del portátil se configuraron como privados.
- Se creó en el sobremesa una regla de diagnóstico de entrada para permitir ICMPv4 Echo únicamente en el perfil Private y desde la subred local:
  `New-NetFirewallRule -DisplayName "Diagnostico ICMPv4 red privada" -Direction Inbound -Protocol ICMPv4 -IcmpType 8 -Action Allow -Profile Private -RemoteAddress LocalSubnet`
- Tras crearla, el portátil pudo hacer ping a `192.168.1.131`: 3 de 3 respuestas, aproximadamente 2–4 ms.
- Una prueba TCP al puerto 445 falló; no es necesaria para el panel y no debe interpretarse como un fallo del puerto 8765.
- No se abrieron puertos del router ni se desactivó el cortafuegos.
- Cuando ya no se necesite el diagnóstico ICMP, se puede retirar la regla con:
  `Remove-NetFirewallRule -DisplayName "Diagnostico ICMPv4 red privada"`
  Antes de hacerlo, comprobar si sigue siendo útil para el diagnóstico.

## 3. Trabajo realizado y resultados verificados

### 2026-10-24 — conectividad y panel de prueba

1. Se creó el script `C:\Users\ismae\Desktop\PanelIA\panel.py`.
2. El script se ejecuta con:
   `py "$env:USERPROFILE\Desktop\PanelIA\panel.py"`
3. La consola mostró: `Panel preparado en el puerto 8765. Pulsa Ctrl+C para detenerlo.`
4. El servidor escucha en `0.0.0.0:8765`; se observaron solicitudes desde localhost y desde el portátil.
5. Desde el portátil, `http://192.168.1.131:8765` cargó correctamente y devolvió HTTP 200.
6. **Limitación:** el panel actual es únicamente una página de prueba; aún no controla Ollama ni el agente.
7. Se comprobó que Python y el módulo `http.server` están disponibles.

### 2026-10-24 — Ollama

1. En PowerShell del sobremesa se ejecutó `ollama --version`.
2. Resultado confirmado: `ollama version is 0.40.10`.
3. Esto confirma que el comando Ollama está instalado y responde. Todavía no confirma que se haya descargado o ejecutado un modelo.



### 2026-10-24 — estado del modelo en Ollama

1. Se ejecutó `ollama ps` después de la primera respuesta del modelo.
2. Salida registrada: modelo `qwen2.5-coder:7b`, ID `dae161e27b0e`, tamaño informado `5.2 GB`, procesador `18%/82% CPU/GPU`, contexto `4096`, runner `llamacpp`, descarga prevista por inactividad en 3 minutos.
3. Interpretación: el modelo está cargado y reparte el procesamiento entre CPU y GPU. El contexto actual es de 4096 tokens. Esta salida no mide por sí sola la velocidad ni confirma la capacidad de ejecutar tareas autónomas.
4. Decisión: mantener 7B de momento y no cambiar de modelo sin una prueba que lo justifique.



### 2026-10-24 — comprobación de Git y Blender

1. `git --version` devuelve `git version 2.55.0.windows.5`: Git está instalado y accesible desde PowerShell.
2. `blender --version` devuelve `CommandNotFoundException`: el comando Blender no está disponible en el PATH de esta sesión. Esto no confirma por sí solo que Blender no esté instalado; falta comprobar las ubicaciones habituales y las aplicaciones instaladas.



### 2026-10-24 — Blender confirmado

1. La búsqueda en rutas habituales encontró `C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe`.
2. El registro de aplicaciones confirma Blender `5.2.3`, con ubicación `C:\\Program Files\\Blender Foundation\\Blender 5.2\\`.
3. Conclusión: Blender sí está instalado; `blender` no está disponible como comando en PowerShell porque la carpeta no parece estar en PATH. No es necesario reinstalarlo.



### 2026-10-24 — ejecución de Blender por línea de comandos

1. Se ejecutó `& "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" --version` desde PowerShell.
2. Resultado confirmado: `Blender 5.2.3 LTS`, build para Windows, rama `blender-v5.2-release`.
3. Conclusión: Blender se puede invocar por ruta completa desde PowerShell. La siguiente prueba debe verificar la ejecución de un script en modo background y la creación de un archivo de escena, antes de integrarlo con el agente.



### 2026-10-24 — prueba de Blender en segundo plano

- Se creó `D:\\AgenteIA\\prueba_blender.py` para borrar los objetos de la escena temporal por defecto, añadir un cubo y guardar el proyecto en `D:\\AgenteIA\\prueba.blend`.
- Se ejecutó Blender 5.2.3 LTS con `--background --python` y la consola devolvió `Info: Saved as "prueba.blend"`, `PRUEBA_IA_OK: escena guardada` y `Blender quit`.
- Aparecieron dos advertencias de rutas de recursos de pinceles/materiales de Blender; no impidieron guardar el archivo en esta prueba.
- Conclusión: confirmado que Blender puede ejecutar un script Python sin interfaz gráfica y guardar un proyecto .blend. Falta comprobar la existencia del archivo y, más adelante, abrirlo/validarlo visualmente.



### 2026-10-24 — verificación del archivo de escena

- PowerShell confirmó que existe `D:\\AgenteIA\\prueba.blend`.
- Tamaño informado: 94.614 bytes. Última modificación: 24/10/2026 16:08:02.
- Conclusión: la prueba de automatización de Blender queda confirmada tanto por la salida del programa como por la existencia del archivo en disco.
- Próximo objetivo: empezar la integración de un agente que use el modelo local y ejecute herramientas reales con límites, registro de acciones y posibilidad de detenerlo.



### 2026-10-24 — versión de Ollama

- Comando ejecutado: `ollama --version`.
- Resultado: `ollama version is 0.40.10`.
- Conclusión: CLI de Ollama está instalado y responde. Aún falta verificar que el servicio HTTP local esté activo y que la API responda antes de integrarla con el agente.



### 2026-10-24 — API local de Ollama verificada

- Se ejecutó `Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -Method Get` desde PowerShell.
- La petición HTTP respondió y devolvió la lista de modelos; aparece `qwen2.5-coder:7b`.
- Conclusión: la API HTTP local de Ollama está accesible desde el equipo. Esto permite que un programa cliente se comunique con el modelo sin depender de la interfaz interactiva de la terminal.
- Seguridad: mantener la API en el equipo local; no exponer el puerto 11434 a Internet ni abrirlo en el router.
- Siguiente paso: hacer una petición pequeña a `/api/chat` y verificar una respuesta generada por la API.



### 2026-10-24 — generación de respuesta mediante la API de chat

- Se envió una petición POST a `http://localhost:11434/api/chat` usando PowerShell, el modelo `qwen2.5-coder:7b` y `stream = false`.
- El texto recibido fue exactamente `API_FUNCIONA`, tal como se solicitó.
- Conclusión: la comunicación programática con el modelo funciona de extremo a extremo (petición JSON → inferencia local → respuesta JSON).
- Esto todavía no prueba que exista un agente autónomo: falta implementar la orquestación, ejecución de herramientas, comprobación de resultados, límites de seguridad, registro de acciones y pausa/parada.



### 2026-10-24 — comprobación de biblioteca HTTP de Python

- Comando: `py -m pip show requests`.
- Resultado: `requests 2.34.2` instalado en el entorno Python 3.14.
- Conclusión: podemos hacer llamadas HTTP desde Python a la API local de Ollama sin instalar esta dependencia.
- Próximo paso propuesto: crear un primer cliente pequeño en `D:\\AgenteIA` que envíe una instrucción al modelo y guarde la respuesta en un archivo de registro; todavía no tendrá ejecución arbitraria de comandos.



### 2026-10-24 — primer cliente Python para Ollama

- Se creó `D:\\AgenteIA\\agente.py`, que realiza una petición POST a la API local `/api/chat` usando `requests` y el modelo `qwen2.5-coder:7b`.
- La ejecución devolvió exactamente `PRIMER_CLIENTE_FUNCIONA`.
- Se confirmó la creación del registro `D:\\AgenteIA\\registro.jsonl`, con fecha, modelo, instrucción y respuesta.
- Conclusión: el cliente Python puede comunicarse con el modelo y conservar un registro de actividad. Aún no se han añadido ejecución de herramientas, ciclo autónomo ni recuperación automática de errores.
- Próximo paso: verificar que el registro JSONL se puede leer correctamente y luego diseñar una primera herramienta segura y limitada.



### 2026-10-24 — validación del registro JSONL

- Se leyó `D:\\AgenteIA\\registro.jsonl` desde PowerShell, convirtiendo la línea JSON con `ConvertFrom-Json`.
- Se verificaron los campos `fecha`, `modelo`, `instruccion` y `respuesta`; los valores corresponden a la prueba del cliente Python.
- Conclusión: el registro de ejecución es legible y conserva la información de la petición/respuesta. El cliente se ejecutó otra vez durante esta comprobación, por lo que puede haber más de una entrada en el archivo.
- Próximo paso: añadir una herramienta de prueba con alcance limitado (crear/leer un archivo dentro de `D:\\AgenteIA\\sandbox`), sin ejecutar comandos arbitrarios del sistema.



### 2026-10-24 — carpeta sandbox creada y verificada

- Se creó `D:\\AgenteIA\\sandbox\\prueba.txt` con texto de prueba.
- PowerShell confirmó la ruta, tamaño de 155 bytes y mostró el contenido esperado.
- Conclusión: la carpeta de pruebas está disponible. Antes de permitir que el modelo invoque herramientas, se implementará una capa Python con operaciones explícitas y validación de rutas confinadas a esta carpeta.



### 2026-10-24 — primera herramienta de archivos restringida

- Se creó y ejecutó `D:\\AgenteIA\\herramientas.py`.
- La herramienta leyó `sandbox\\prueba.txt`, escribió `sandbox\\resultado_agente.txt` y bloqueó correctamente la ruta de prueba `../archivo_fuera.txt`.
- La consola mostró el carácter BOM al principio del texto leído desde `prueba.txt` (se creó con PowerShell UTF-8 con BOM). No impidió la lectura; se puede limpiar después usando `utf-8-sig` si resulta molesto.
- Conclusión: las operaciones básicas de lectura/escritura y la comprobación de rutas funcionan en la prueba. Esta validación no constituye un aislamiento fuerte frente a enlaces simbólicos o condiciones de carrera; no se debe tratar como una frontera de seguridad suficiente para ejecutar código no confiable.
- Próximo paso: conectar el modelo con un conjunto cerrado de herramientas mediante llamadas estructuradas, validar rigurosamente cada argumento y pedir confirmación antes de sobrescribir archivos existentes.



### 2026-10-24 — confirmación de archivo escrito por la herramienta

- Se leyó desde PowerShell `D:\\AgenteIA\\sandbox\\resultado_agente.txt`.
- Contenido confirmado: `La herramienta de archivos funciona correctamente.`
- Conclusión: la escritura de la herramienta dejó un archivo persistente y su contenido puede verificarse fuera del propio script.
- Próximo paso: diseñar el primer ciclo de herramienta del agente con un conjunto cerrado de acciones, validación estricta y confirmación antes de modificar archivos existentes.

## 4. Plan técnico previsto

El objetivo final es un agente autónomo local y gratuito que pueda trabajar durante muchas horas: programar, ejecutar y probar código, corregir errores, trabajar con Git/GitHub, consultar Internet mediante herramientas integradas, crear proyectos 3D con Blender y permitir supervisión desde el portátil. No basta con que el modelo responda en un chat; habrá que integrar un ejecutor/agente, herramientas reales, ciclos de comprobación, registro de avances y controles de seguridad. La autonomía y calidad dependerán del rendimiento del modelo y del hardware.

1. **Completado parcialmente:** descargar y probar `qwen2.5-coder:7b` en Ollama. Descarga finalizada (aprox. 4,7 GB) y primera respuesta en español con un ejemplo de Python recibida. Aún no se han probado ejecución de código, corrección iterativa ni tareas autónomas.
2. Si hay errores de memoria o el rendimiento no es adecuado, probar `qwen2.5-coder:3b`.
3. Comprobar respuesta en español y generación de un programa Python sencillo.
4. Evaluar el uso de RAM, VRAM, CPU, velocidad y estabilidad antes de añadir más componentes.
5. Instalar/configurar Git y Blender si no están ya instalados.
6. Revisar los requisitos actuales de OpenHands y confirmar si puede trabajar de forma fiable con el modelo local seleccionado.
7. Diseñar la integración del panel con el backend de IA, con autenticación o controles de acceso adecuados y sin exponerlo a Internet.
8. Añadir funciones de agente de forma gradual, con límites de ejecución, registro de actividad y confirmación del usuario para acciones sensibles.

## 5. Próximo paso inmediato

**Pendiente:** verificar que el modelo puede generar código de forma estructurada y comprobar el estado local del modelo. En la misma sesión de Ollama, se recibió una respuesta en español a la petición de un programa de contabilidad básico. La respuesta demuestra generación de código, no que el código se haya ejecutado ni validado.

Siguiente comprobación, en PowerShell del sobremesa (puede salir del chat de Ollama con `/bye`):

```powershell
ollama ps
```

Copiar la salida. Después comprobaremos Git y Blender antes de instalar un agente adicional, y evaluaremos el camino de integración más compatible con el hardware disponible.

## 6. Pendientes

- [x] Descargar `qwen2.5-coder:7b` y confirmar una primera respuesta en español.
- [ ] Ejecutar y validar código generado por el modelo.
- [ ] Medir consumo de RAM/VRAM y velocidad durante una tarea real.
- [ ] Registrar uso aproximado de RAM/VRAM y velocidad.
- [ ] Inventariar el hardware y sistema del portátil.
- [x] Comprobar Git: instalado y accesible desde PowerShell.
- [x] Blender instalado: versión 5.2.3. El comando no está disponible por PATH; ejecutable localizado.
- [ ] Verificar requisitos y compatibilidad local de OpenHands.
- [ ] Definir cómo el panel solicitará tareas al backend de IA.
- [ ] Añadir controles de acceso, límites y registros antes de permitir operaciones reales desde el portátil.
- [ ] Retirar la regla de ICMP de diagnóstico cuando deje de ser necesaria.

## 7. Registro de decisiones

- Mantener el sobremesa como anfitrión principal y el portátil como panel cliente.
- Priorizar modelos locales/gratuitos.
- Empezar con Qwen2.5-Coder 7B y tener 3B como alternativa.
- Usar la unidad D: para modelos y proyectos cuando sea posible.
- No considerar el panel conectado a la IA hasta que se implemente y se pruebe esa integración.
- La primera respuesta del modelo no equivale a tener un agente autónomo; priorizar la integración de herramientas y ciclos de trabajo verificables.
- No afirmar que una herramienta funciona solo porque esté instalada: comprobar la tarea real.

## 8. Protocolo para futuras sesiones

En cada sesión de trabajo:
1. Leer este documento antes de continuar, si está disponible.
2. Confirmar el último estado y el resultado del último paso pendiente.
3. Trabajar en una tarea pequeña cada vez.
4. Actualizar las secciones de trabajo realizado, pendientes, decisiones e incidencias.
5. Registrar comandos y salidas importantes sin guardar contraseñas, tokens ni secretos.
6. Guardar cambios en GitHub con un mensaje de commit descriptivo.
7. Terminar cada sesión indicando qué quedó confirmado y cuál es el siguiente paso.

**Nota de continuidad:** esta documentación es la referencia persistente del proyecto. No sustituye una comprobación técnica nueva cuando el estado del equipo pueda haber cambiado.
