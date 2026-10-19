# MSA-VLUX V5.1 — Observabilidad, autoevaluación calibrada y PDCA/DMAIC

**Alcance:** instrumentos locales reproducibles con datos sintéticos o métricas expresamente aportadas. Sin acceso automático a Codex, Claude, servicios, clientes o credenciales.

## PDCA por átomo

1. **Plan** — Identificar hipótesis falsable, resultado esperado y evidencia existente.
2. **Do** — Implementar en entorno autorizado y medir tests, tiempo, costo si es observable y restauración.
3. **Check** — Contrastar contra baseline; no aceptar autoevaluación sin evidencias verificables.
4. **Act** — Proponer ajustar un procedimiento; nueva aprobación y nuevo SHA antes de adopción.

Para incidencias repetidas, aplicar **DMAIC**: definir problema, medir incidencia, analizar causas, mejorar, controlar regresiones.

## Contrato de observación

La plantilla `templates/OBSERVATION.example.json` define el contrato de ingestión. Usar `msa observe --input ...` y `msa metrics`.

- Cada registro debe tener `execution_id` único y SHA de artefacto; procedencia `synthetic`, `manual` o `instrumented-unverified`.
- La declaración `instrumented-attested` no puede importarse directamente: requeriría firma/autenticidad independiente, aún no implementada.
- No importar prompts, respuestas, nombres, correos, resultados de clientes, secretos o código. Nunca aplicar estos datos a evaluación individual de colaboradores.
- Un costo `null` indica **desconocido**, no cero. Una tasa `null` indica denominador cero.
- Las cifras son aportadas por ejecutores; una ejecución sintética no es un benchmark de agentes reales.
- La cadena SHA sirve a integridad, no autenticidad; use almacenamiento privado y control de accesos.

## Calibración de autoevaluación

`msa calibrate` compara pares de calificaciones autoevaluador/revisor para el mismo `task_id`. Es un indicador de calibración, **no autentica que el revisor sea independiente**. Las revisiones sin evidencia externa permanecen no atestadas.

## Métricas de VLUX (sin cifras inventadas)

Exactitud verificada, cobertura de evidencia, tasa de restauración, duración mediana, costo conocido y violaciones de seguridad. Comparar tareas equivalentes; nunca optimizar velocidad a costa de riesgo. No inferir ROI de registros sintéticos.
