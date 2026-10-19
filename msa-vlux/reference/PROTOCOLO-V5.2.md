# MSA-VLUX V5.2 — Laboratorio experimental

## Dos caminos separados

1. `benchmark`: PSO o muestreo aleatorio sobre las funciones matemáticas sintéticas permitidas `sphere` y `rastrigin`. Semilla explícita; presupuesto acotado; historial de mejores resultados. No ejecuta código arbitrario, proyectos de clientes ni algoritmos en producción.
2. `paired-experiment`: recibe resultados pareados por tarea de estrategias baseline/candidate, con partición de validación `train` y `holdout`. Rechaza regresiones del candidato y violaciones de política. Solo genera propuesta para revisión humana.

## Interpretación correcta

El *benchmark* valida el motor matemático, **no** prueba que PSO mejore MSA o una aplicación. Para comparaciones reales se requieren tareas independientes, métricas instrumentadas y revisión. Un holdout incluido en el mismo archivo es separación lógica solamente, no secreto técnico ni independencia demostrable. Para experimentos de promoción, custodiar el conjunto reservado externamente.

Usar emparejamiento por `task_id`, registrar criterios antes del experimento y garantizar ausencia de filtración entre configuraciones. Si el objetivo es seleccionar entre pocas estrategias discretas, preferir experimento pareado controlado antes de PSO. Optimización bayesiana queda como ruta de investigación, **no implementada**.

## Restricciones

No editar prompts, políticas, permisos, releases ni servicios de forma automática. Cualquier propuesta necesita revisión humana y un nuevo artefacto versionado con ensayos de regresión.
