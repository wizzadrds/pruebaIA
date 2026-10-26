# Proyecto pruebaIA

Documentación central del proyecto de asistente de IA local, automatización y panel de control entre un ordenador de sobremesa y un portátil.

> **Estado:** fase inicial de preparación y validación.  
> **Última actualización:** 2026-10-24.

## Objetivo

Construir progresivamente un agente de IA que se ejecute principalmente en el ordenador de sobremesa, pueda ayudar con programación, Git/GitHub y tareas de creación 3D con Blender, y se pueda supervisar/controlar desde el portátil mediante un panel web dentro de la red local.

El sistema debe priorizar soluciones gratuitas o locales, mantener el control del usuario, ser estable y evitar consumir tantos recursos que interfiera con el estudio o el trabajo diario.

## Principios de trabajo

- Avanzar en pasos pequeños y verificables.
- Registrar decisiones, comandos, resultados, incidencias y próximos pasos.
- No marcar como completada una tarea sin comprobar su resultado.
- No desactivar el cortafuegos ni abrir puertos del router sin una necesidad justificada y una revisión de seguridad.
- Mantener modelos y proyectos en la unidad D: cuando sea práctico, para conservar espacio en C:.
- No ejecutar muchos modelos o contenedores a la vez; medir primero el rendimiento del equipo.
- Separar hechos confirmados, hipótesis y tareas pendientes.

## Arquitectura prevista

- **Sobremesa Windows:** anfitrión de los modelos locales y del agente.
- **Ollama:** ejecución local de modelos de lenguaje.
- **Modelo inicial previsto:** `qwen2.5-coder:7b`; alternativa más ligera: `qwen2.5-coder:3b`.
- **Agente previsto:** OpenHands, pendiente de verificar compatibilidad y requisitos con el modelo local elegido.
- **Herramientas de desarrollo:** Git y GitHub.
- **Creación 3D:** Blender.
- **Portátil:** acceso al panel web de supervisión/control a través de la LAN.
- **Panel de prueba existente:** `C:\Users\ismae\Desktop\PanelIA\panel.py`, servido en el puerto 8765. Es una página de prueba; todavía no está conectada al agente ni ofrece control real de la IA.

## Documentación de seguimiento

- [Estado actual y bitácora](docs/ESTADO_Y_BITACORA.md): inventario del entorno, comprobaciones realizadas, decisiones, incidencias y siguiente acción.
- Cada sesión de trabajo debe actualizar esta documentación con lo que se haya confirmado y los pasos siguientes.

- [Revisión semántica de resúmenes web](docs/REVISION_SEMANTICA_RESUMENES_WEB.md): diseño del parche, hashes, pruebas ejecutadas y validaciones pendientes.
