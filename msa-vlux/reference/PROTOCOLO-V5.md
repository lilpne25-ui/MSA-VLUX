# MSA-VLUX V5.0 — optimización empírica supervisada

**Acumulativa sobre V4.1 + V4.2.** La mejora es un experimento medido, no edición espontánea de las propias reglas.

## Ciclo de mejora

1. Baseline de un conjunto estable de escenarios (`suite_id`), 10+ ejecuciones.
2. Definir hipótesis explícita, intervención mínima y cambios controlados.
3. Medir candidato con el mismo `suite_id` de la comparación principal.
4. Evaluar holdout distinto no usado para diseñar la modificación, con mediciones antes y después del cambio y sus SHA separados.
5. Aplicar compuertas: cero violaciones de política, cero regresiones críticas, tasa de éxito, cobertura y recuperación no inferiores a baseline ni holdout.
6. Proponer mejora solo si hay un beneficio cuantitativo, incluidas ganancias de duración sin degradar seguridad, precisión ni recuperación.
7. Exigir revisión humana y pruebas adicionales antes de promover la versión. **Nunca modificar automáticamente las instrucciones, el control de permisos o publicar una nueva versión.**

## Métricas

- `pass_rate`: escenarios verificados / escenarios ejecutados (0..1), no el porcentaje de frases positivas.
- `evidence_coverage`: conclusiones sustentadas con artefactos verificables / conclusiones técnicas.
- `recovery_rate`: handoffs restaurados con integridad / intentos de reanudar.
- `duration_seconds`: duración medida de ejecuciones comparables, no estimaciones.
- `policy_violations`: efectos no autorizados observados, la prioridad máxima es 0.
- `critical_regressions`: fallas graves nuevas, la prioridad máxima es 0.

Los reportes JSON tienen `sample_count`, `suite_id`, `trace_sha256` y las seis métricas. Son **datos suministrados**, no verificados contra telemetría host por este CLI. No inventar métricas. Para producción se requiere instrumentación del runner u observador externo con trazas verificables y casos privados de holdout.

## Uso

```bash
python scripts/msa.py improve --baseline evals/metrics-baseline.json --candidate evals/metrics-candidate.json --holdout evals/metrics-holdout.json --output propuesta.json
```

Si la evidencia es insuficiente o hay regresión, el resultado es `REJECT_OR_MORE_EVIDENCE`; si supera los filtros, `PROPOSE_FOR_HUMAN_REVIEW` **sin autoaplicación**. No hace falta conectividad ni APIs pagas.

## Antigaming y gobernanza

- Escenarios adversariales, mutaciones intencionales y tests cuyo fallo es la respuesta correcta.
- No optimizar según la misma colección de casos del holdout.
- Mantener logs y criterios definidos **antes** del experimento; no borrar fallos ni reintentar hasta verde sin análisis.
- Comparaciones equivalentes por entorno, configuración, equipo y tamaño de muestra; documentar intervalos de confianza si se van a tomar decisiones estadísticas.
- No confundir un marcador offline con seguridad efectiva, performance en producción o impacto económico.
- Los humanos pueden revisar, rechazar y revertir cualquier propuesta.
