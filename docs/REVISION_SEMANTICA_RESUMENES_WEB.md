# Revisión semántica de resúmenes web

**Fecha de registro:** 2026-10-26  
**Ámbito:** únicamente la candidata local `D:\\AgenteIA\\sandbox\\candidato_revision_semantica\\ciclo_agente_candidato.py`.  
**Estado:** parche aplicado y comprobaciones de sintaxis/regresión registradas; validación integrada con Ollama real pendiente.

## Objetivo

Evitar que el agente muestre como válido un resumen de una fuente web cuando sus afirmaciones no están respaldadas por el contenido leído. La revisión es una comprobación adicional y falible; no constituye una garantía de verdad ni sustituye la revisión humana.

## Cambio aplicado en la candidata

- Se añadió `_validar_estado_revision(texto)`, que valida una respuesta JSON estricta con la única clave `estado` y los valores permitidos `respaldada`, `contradicha` o `insuficiente`.
- Se añadió `revisar_resumen_contra_fuente(resumen, fuente)`. Divide el resumen en tres puntos numerados, consulta el endpoint local de Ollama usando la configuración existente (`API_URL`, `MODEL`, `TIMEOUT_SEGUNDOS`) y solicita una salida con esquema JSON. El texto de fuente se limita a 12.000 caracteres.
- La revisión solo permite continuar si los tres puntos resultan `respaldada`.
- En el caso `mostrar_resumen` que requiere investigación web, se busca la última lectura web válida del historial y se contrasta el resumen con ese contenido antes de mostrarlo.
- Si no hay fuente válida, falla la llamada, la respuesta no cumple el contrato o algún punto no está respaldado, el resumen queda bloqueado y se registra el evento `revision_semantica_bloqueada`.
- El flujo de resúmenes desde archivo y los resúmenes que no requieren investigación web se mantienen fuera de esta revisión.

## Archivos locales y hashes

Los siguientes valores fueron comprobados en el equipo local y se conservan aquí como registro. No representan hashes de un commit de GitHub.

| Elemento | SHA-256 |
|---|---|
| Candidata original, antes del parche | `A32D7F5E3F56F0BBE36C7DFD0624DFD6BFDF4FD7404E3E3DF77F229AB07CB2F6` |
| Candidata modificada | `082B9C76F35788947B73BFF26B99B8E30D45974B491DF2C324A6FC2F29287B61` |

- Copia de seguridad: `D:\\AgenteIA\\sandbox\\candidato_revision_semantica\\ciclo_agente_candidato.py.bak_revision_semantica`
- `HASH_BACKUP` coincide con el SHA-256 original.
- `BACKUP_ORIGINAL_INTACTO: True`
- `PARCHE_PRESENTE: True`
- `SINTAXIS: OK`
- El revisor `revisar_resumen_contra_fuente` aparece una sola vez en la candidata.

## Pruebas registradas

Comando de regresión:

```powershell
Set-Location "D:\\AgenteIA\\sandbox"
py -B -m unittest -v prueba_revision_evidencias prueba_revisor_simulado
```

Resultado registrado: **19 pruebas pasaron** (13 en `prueba_revision_evidencias.py` y 6 en `prueba_revisor_simulado.py`).

Además, se ejecutaron **6 pruebas aisladas de contrato con revisor simulado**. Estas comprueban el contrato en aislamiento, no demuestran que el flujo integrado funcione con Ollama real.

También se registró que la candidata compila y que las comprobaciones estructurales del parche en seco pasaron antes de aplicarlo.

## Límites y riesgos conocidos

- **No se ha ejecutado el ciclo completo del agente después del parche.**
- **No se ha validado la función integrada contra Ollama real.**
- Las pruebas unitarias existentes y las pruebas simuladas no demuestran por sí solas que todas las afirmaciones factuales se detecten correctamente.
- Un modelo revisor puede aceptar erróneamente una afirmación o rechazar una afirmación correcta. La revisión reduce algunos riesgos, pero no garantiza veracidad.
- La fuente se trunca a 12.000 caracteres; información relevante fuera de ese límite puede no evaluarse.
- La revisión depende de que el historial identifique correctamente la lectura web más reciente y válida.

## Protección de otros agentes

El agente original y el experimental no se modificaron. El parche se aplicó exclusivamente a la candidata. La copia de seguridad conserva el archivo original y su hash fue verificado.

## Próximos pasos seguros

1. Revisar este registro y el diff de la candidata antes de promover el cambio.
2. En una sesión autorizada, probar la función integrada con respuestas simuladas controladas, incluyendo fuente ausente, JSON inválido, timeout, afirmación contradicha y revisión insuficiente.
3. Después de autorización explícita, realizar una única prueba de bajo riesgo contra Ollama local, sin ejecutar el ciclo general ni modificar el agente original/experimental.
4. Registrar salidas y hashes nuevos tras cualquier modificación.
5. No describir la revisión como garantía de verdad ni promover la candidata a producción hasta completar esas comprobaciones.
