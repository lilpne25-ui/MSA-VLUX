# MSA-VLUX V4 · Módulo AUDIT

MSA_VERSION=4.0.0-rc3 · Módulo: AUDIT · Modo: AUDIT (AUDIT-0 y AUDIT-Δ)
Depende del núcleo. Para las dimensiones 3–4 carga UX (§22); para la 7, SECURITY (§23); para la 8, QUALITY (§19); para la 9, PRODUCTION (§21); para la 10, EVOLUTION (§25). La trazabilidad usa DELIVERY §18.3.

---

# 20. AUDITORÍA 360 DE PROYECTOS EXISTENTES

## 20.1 Ficha del modo AUDIT

| Campo | Contenido |
|---|---|
| Activación | Proyecto existente sin expediente MSA verificable; expediente que contradice el código; o reingreso (§0.4 regla 2) |
| Entradas | Cliente y proyecto; repositorios; documentación; decisiones; acceso a ambientes (lo que haya) |
| Responsabilidades | AUDIT-0 (§20.2–§20.6) o AUDIT-Δ (§20.7): reconstruir el estado real con evidencia y proponer qué ejecutar primero |
| Roles | Verifier (dueño de la línea base) + Architect + Security + Experience + Operations; Commercial sólo para la dimensión 10 |
| Herramientas permitidas | Lectura de repos (`git log/show/diff`, `gh` en lectura), lectura de Drive, ejecución de pruebas y del sistema **en local o en ambientes desechables**, navegador contra ambientes con datos sintéticos, lectura de logs autorizados |
| Herramientas prohibidas | Toda escritura en el proyecto auditado (código, ramas, issues, PRs, Drive), push, merge, deploy, migraciones, reinicios, cambios de configuración, envío de mensajes, pruebas con escritura sobre datos reales |
| Evidencia | Cada afirmación con SHA, archivo, comando o captura y su etiqueta §2.4 |
| Documentos | Reporte de línea base (`MSA-AUDITORIA-[fecha].md`), `MSA-HALLAZGOS.md`, `MSA-TRAZABILIDAD.md`, `MSA-ATOMOS.md` con la propuesta de átomos. Se escriben en una carpeta de trabajo de VLUX o en una rama de documentación **sólo con autorización**; por defecto, fuera del repositorio auditado. Las copias de trabajo (exportaciones de ramas para correr pruebas, clones desechables) viven **dentro de la carpeta de trabajo autorizada**, nunca en carpetas temporales del sistema, y se listan en el reporte |
| Decisiones humanas | Aprobación de la línea base; orden de los átomos; qué hallazgos se aceptan como riesgo |
| Terminado | Línea base aprobada: qué existe, qué funciona, qué falta, qué está roto, qué bloquea UAT y producción, y qué átomos van primero |
| Salidas | DELIVERY (hay contrato vigente), PRODUCTION (la pregunta era readiness), OPERATIONS (sistema ya en uso), PROPOSAL (lo que falta no está contratado) |

AUDIT **no repite el Átomo 0 comercial**: no investiga competencia ni redacta propuesta, salvo que la dimensión 10 lo pida y el usuario lo confirme.

## 20.2 AUDIT-0 · Paso 1: delimitar antes de auditar

Antes de cualquier hallazgo, el Maestro produce este bloque y lo confirma con el usuario si hay huecos:

```text
AUDIT_ID=[proyecto]-AUDIT-0-[fecha]
CLIENT=[cliente]            PROJECT=[proyecto]
REPOS=[repo@rama:sha, ...]  (rama de desarrollo, release y default)
DOC_SOURCES=[rutas/IDs de documentos, con fecha]
APPROVED_REQUIREMENTS_SOURCE=[documento + versión o UNKNOWN]
DECISIONS_SOURCE=[registro D-xx o UNKNOWN]
ENVIRONMENTS=[nombre: url/host · cómo se sabe qué SHA corre · acceso del agente]
DEPLOYED_SHA=[sha · fuente] o UNKNOWN
VERIFIABLE=[lista de lo que se puede comprobar con el acceso actual]
NOT_VERIFIABLE=[lista de lo que no, y quién podría aportarlo]
CONFIDENTIALITY=[repos/datos de otros clientes en el mismo repo u host; datos personales; qué no se copia al reporte]
PERMISSIONS=read-only · external_write: denied · paid_services: denied
```

Reglas:
- Un repositorio que aloja a más de un cliente (ramas o instancias) se declara en `CONFIDENTIALITY`; la auditoría sólo lee las ramas del cliente auditado y no copia al reporte información de los demás (§8.4).
- Si `DEPLOYED_SHA` no se puede establecer, todo lo que dependa de B3 queda `UNKNOWN` y el reporte lo dice en su primera página.

## 20.3 AUDIT-0 · Paso 2: las diez dimensiones

Cada dimensión produce hallazgos con el formato de §20.4 y declara su cobertura: `COVERAGE=FULL | PARTIAL | NONE` con la razón.

| # | Dimensión | Preguntas | Evidencia mínima |
|---|---|---|---|
| 1 | **Requerimientos y trazabilidad** | ¿Qué está aprobado? ¿Qué está en B1/B2/B3? ¿Qué está probado y aceptado? ¿Qué documento contradice al SHA? | Matriz §18.3 completa; contradicciones `C-xx` |
| 2 | **Funcionalidad y Golden Path** | ¿El flujo de punta a punta funciona en el SHA y ambiente observados? ¿Dónde se rompe? | Guion reproducible ejecutado (§19.6); resultado PASS/FAIL/UNKNOWN |
| 3 | **UX/UI y accesibilidad** | ¿Las tareas críticas son eficientes, claras y accesibles? | Recorridos medidos y heurísticas con captura (§22) |
| 4 | **Diseño visual y consistencia** | ¿Hay un sistema visual coherente? ¿Jerarquía, espaciado, componentes, marca? | Inventario de componentes y capturas comparadas (§22) |
| 5 | **Arquitectura y deuda técnica** | ¿Límites, acoplamiento, duplicación de estado, dependencias obsoletas, decisiones sin registrar? | Rutas de archivo, diagramas derivados del código, versiones |
| 6 | **Base de datos e integridad** | ¿Restricciones, índices únicos, migraciones aplicables, datos huérfanos, historia inmutable donde se requiere? | Esquema y migraciones en el SHA; consultas de solo lectura en copias |
| 7 | **Seguridad y privacidad** | Secretos (incluido historial), auth, RBAC, exposición de archivos, webhooks, dependencias, datos personales, aislamiento entre clientes | §23 con evidencia por punto |
| 8 | **Pruebas y calidad** | ¿Qué protegen las pruebas? ¿Pasan en el SHA? ¿Cubren el Golden Path? | Ejecución local con §19.7; mapa invariante → prueba |
| 9 | **Infraestructura y producción** | Ambientes, respaldos y **restauración probada**, logs, alertas, rollback, secretos, responsables | Checklist §21.3 con evidencia o `UNKNOWN` |
| 10 | **Operación y diferenciación** | ¿Cómo lo usan hoy? ¿Qué fricción operativa queda? ¿Qué mejora tendría valor medible? | Métricas de uso medidas o `NOT_MEASURED`; §25 |

**Clasificación de componentes en sistemas de plataforma** (un producto configurable de terceros). En la dimensión 1 y 9, cada pieza se clasifica en exactamente una clase, con evidencia:

| Clase | Qué es | Evidencia que la prueba |
|---|---|---|
| `COMMERCIAL_DEMO` | Experiencia de venta o simulación (ROI, comparadores, maquetas) | Código de la demo; ausencia de conexión a la plataforma |
| `PLATFORM_CONFIG` | Configuración estándar de la plataforma (catálogos, flujos, permisos) | Exportación de configuración o base observada |
| `CUSTOM_MODULE` | Módulo o extensión construida por VLUX | Código del módulo + SHA + pruebas |
| `PENDING_INTEGRATION` | Hardware, pagos, facturación, terceros no conectados | Ausencia verificada o `REQUIRES_INTEGRATION` |
| `RUNTIME` | Instancia corriendo en un host | Host, versión, SHA o imagen observados |

La readiness (§2.8) se evalúa por separado para cada clase. Una demo comercial impecable no aporta readiness a la configuración ni a los módulos.

## 20.4 Formato obligatorio de hallazgo

```text
FINDING_ID=[PROYECTO]-[DIM]-[nnn]
PROJECT=
AREA=[dimensión 1–10 + componente]
DESCRIPTION=[qué pasa, en una o dos frases concretas]
EXPECTED=[comportamiento o criterio esperado, con su fuente]
OBSERVED=[lo que se observó]
EVIDENCE=[pasos de reproducción, comando, archivo:línea, captura, log]
SOURCE_SHA=[sha] o N/A
ENVIRONMENT=[local|test|staging|production|repo-only]
SEVERITY=[CRITICAL|HIGH|MEDIUM|LOW]  BLOCKING=[BLOCKS_PRODUCTION|BLOCKS_PILOT|BLOCKS_UAT|BLOCKS_RELEASE|NON_BLOCKING]
BUSINESS_IMPACT=[a quién afecta y cómo; métricas sólo si se midieron]
TECHNICAL_RISK=[qué puede romperse]
DEPENDENCIES=[D-xx, otros hallazgos, accesos]
ESTIMATED_EFFORT=[S|M|L|XL — estimación de VLUX, no compromiso]
RECOMMENDATION=[cambio verificable + criterio de aceptación]
WORK_TYPE=[§2.6]
STATUS=[OPEN|ACCEPTED_RISK|IN_ATOM n|CLOSED con evidencia]
MEASURED=[qué datos se midieron; "ninguno" si no hubo medición]
```

**Barra de calidad.** Un hallazgo sin `EXPECTED`, `OBSERVED` y `EVIDENCE` reproducible no es un hallazgo: es una sospecha y se lista aparte como `HYPOTHESIS`. Se rechazan frases como "la interfaz puede mejorar" o "la seguridad es débil". Ejemplo aceptable: "Registrar un pago exige 7 pasos y 3 cambios de pantalla; el botón Guardar no muestra estado de carga y un doble clic crea dos pagos. Evidencia: recorrido grabado, consulta que muestra 2 filas, prueba e2e `pay-double-click.spec`."

**Los números se miden, no se inventan.** Tiempos, conteos de pasos, tasas de error o porcentajes llevan su método de medición. Si no se pudo medir, `MEASURED=ninguno` y el impacto se describe cualitativamente.

## 20.5 AUDIT-0 · Paso 3: reporte de línea base

El reporte responde, en este orden, con evidencia o `UNKNOWN`:
1. ¿Qué requerimientos aprobados existen?
2. ¿Cuáles están implementados (B1)?
3. ¿Cuáles funcionan realmente (prueba o recorrido)?
4. ¿Cuáles están en release (B2)?
5. ¿Cuáles están desplegados (B3)?
6. ¿Qué falla en los Golden Paths?
7. ¿Qué mejorar de UX/UI (top 5 de §22.4)?
8. ¿Qué riesgos de seguridad existen?
9. ¿Qué falta para UAT?
10. ¿Qué impide producción (§21)?
11. ¿Qué mejoraría la diferenciación (§25), separado del alcance contratado?
12. ¿Qué átomos ejecutar primero (§20.6)?

Abre con una tabla de cobertura (dimensión → `COVERAGE` → razón) y con la lista `NOT_VERIFIABLE`. **Ninguna auditoría se declara completa para un ambiente que no se observó.**

## 20.6 De hallazgos a átomos

Orden por defecto, salvo decisión humana:
1. `CRITICAL` de seguridad o integridad de datos;
2. Golden Path roto;
3. bloqueadores de UAT;
4. bloqueadores de producción;
5. top 5 UX;
6. deuda técnica que bloquea lo anterior;
7. evolución y diferenciación (fuera del alcance contratado salvo aprobación).

Cada átomo propuesto cita sus `FINDING_ID`, su nivel Lite/Full y su `WORK_TYPE`. La auditoría **propone**; no ejecuta ninguno (§3.4).

## 20.7 AUDIT-Δ (reingreso)

Disparado por la regla 2 de §0.4. Contiene: disparador con evidencia, área afectada, dimensiones que aplican (no las diez por defecto), hallazgos con §20.4, y la salida (modo al que vuelve). No reabre requerimientos cerrados con evidencia salvo que la regresión se pruebe (§10.6). Se cierra cuando la causa está identificada o declarada `ROOT_CAUSE=UNKNOWN` con lo descartado, y existe un átomo o decisión para el remedio.
