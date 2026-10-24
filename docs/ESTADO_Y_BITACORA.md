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
- [ ] Comprobar si Git está instalado.
- [ ] Comprobar si Blender está instalado.
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
