# MSA-VLUX V4 · Módulo EVOLUTION

MSA_VERSION=4.0.0-rc3 · Módulo: EVOLUTION · Modo: EVOLUTION y cierre (Átomo Ω)
Depende del núcleo. §14 es texto de V3.2 sin cambios; §25 es nuevo en V4.

---

# 25. EVOLUCIÓN DEL PRODUCTO Y VALOR DE NEGOCIO

## 25.1 Ficha del modo EVOLUTION

| Campo | Contenido |
|---|---|
| Activación | Producto estable (al menos `PILOT_READY`) y se busca diferenciación o justificar nuevas funcionalidades |
| Entradas | Uso medido, hallazgos de operación y UX, operación del cliente, referentes |
| Responsabilidades | Identificar oportunidades con evidencia, estructurarlas (§25.2), priorizarlas (§25.3) y convertirlas en propuesta |
| Roles | Commercial + Experience + Verifier |
| Herramientas permitidas | Lectura de métricas y del producto; investigación pública; escritura local de propuestas |
| Herramientas prohibidas | Implementar, publicar, contactar al cliente o a terceros, servicios de pago |
| Evidencia | Problema observado o medido; métricas antes con su fuente |
| Documentos | Propuestas de evolución en `MSA-DECISIONES.md` como `CR-xx` o propuesta comercial |
| Decisiones humanas | Qué se propone al cliente; precio; prioridad |
| Terminado | Propuestas entregadas con hipótesis y métricas, o descartadas con razón |
| Salidas | PROPOSAL (requiere aceptación del cliente), DELIVERY (cambio aprobado) |

## 25.2 Estructura de una propuesta de diferenciación

```text
EVO_ID=
USER_PROBLEM=[problema del usuario, en sus términos]
EVIDENCE=[observación, hallazgo, métrica medida — con fuente]
CURRENT_ALTERNATIVE=[cómo lo resuelven hoy]
REFERENCES=[competidores o referentes, sólo información pública]
SOLUTION=[qué se construiría]
EXPECTED_BENEFIT=[en qué dimensión: tiempo, errores, retrabajo, trazabilidad, decisiones, dependencia de personas, visibilidad, adopción]
HYPOTHESIS=[si hacemos X, esperamos Y medido como Z]
METRIC_BEFORE=[valor medido + método] o NOT_MEASURED
METRIC_AFTER_TARGET=[objetivo propuesto, rotulado como hipótesis]
COST=[estimación de VLUX, marcada como propuesta]
RISK=   EFFORT=   DEPENDENCIES=
```

## 25.3 Criterios

- **Diferenciación no es efecto visual.** Una animación o un rediseño sólo cuenta si mejora una métrica de la tarea (§22.4).
- Se priorizan funcionalidades que ahorren tiempo, eviten errores, reduzcan retrabajo, mejoren trazabilidad, aceleren decisiones, reduzcan dependencia de personas, den visibilidad operativa o mejoren adopción.
- Antes de proponer IA aplica la prueba de §8.3.
- **ROI:** sólo con datos medidos o con escenarios expresamente rotulados como hipotéticos, con supuestos visibles y editables (§12.5, §13). Nunca porcentajes inventados ni ahorros presentados como promesa.
- Lo propuesto queda fuera del alcance contratado hasta que el cliente lo acepte (§18.4).

---

# 14. ÁTOMO Ω — CIERRE Y APRENDIZAJE

Cuando el proyecto alcanza una entrega o un hito comercial significativo, crea un cierre de aprendizaje sin reescribir la historia:
- qué hipótesis se confirmó y cuál no;
- qué parte del motor es genérica y reutilizable, y qué pertenece sólo al cliente;
- incidentes que revelaron una regla nueva;
- patrones de UX que funcionaron en UAT o demo;
- métricas del piloto disponibles;
- deuda técnica aceptada;
- oportunidades futuras separadas del alcance entregado;
- handoff operativo: deploy, respaldo, recuperación, cuentas y responsables.

Si se extrae un patrón reusable, documenta **la abstracción**, no copies el proyecto del cliente.

---
