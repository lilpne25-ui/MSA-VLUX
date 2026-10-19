# MSA-VLUX V4 · Módulo OPERATIONS

MSA_VERSION=4.0.0-rc3 · Módulo: OPERATIONS · Modo: OPERATIONS
Depende del núcleo. Para releases de parches carga PRODUCTION; para eventos de seguridad, SECURITY §23.3.

---

# 24. OPERACIÓN Y SOPORTE

## 24.1 Ficha del modo OPERATIONS

| Campo | Contenido |
|---|---|
| Activación | Sistema en uso real (piloto o producción) con `DEPLOYED_SHA` conocido o declarado `UNKNOWN` |
| Entradas | Reporte del usuario o alerta; logs, métricas y estado del ambiente a los que haya acceso; runbook; acuerdos de soporte |
| Responsabilidades | Diagnosticar incidentes, analizar logs, revisar rendimiento y disponibilidad, comprobar respaldos, proponer parches, detectar regresiones, actualizar dependencias, gestionar versiones, reportes de soporte, investigar fricción UX, analizar uso, proponer mejoras |
| Roles | Operations + Verifier; Security si `SECURITY_EVENT`; Experience si la fricción es UX |
| Herramientas permitidas | Lectura de logs, métricas y estado; consultas de solo lectura; reproducción en local o en un ambiente desechable |
| Herramientas prohibidas sin autorización explícita | Reinicios, restauraciones, rollbacks, deploys, migraciones, borrado de datos, cambios de configuración, de DNS o de firewall, mensajes a usuarios del cliente |
| Evidencia | Línea de tiempo con fuentes; SHA y ambiente; logs citados sin datos sensibles |
| Documentos | `MSA-HALLAZGOS.md` (incidentes y problemas), reporte de incidente, reporte de soporte periódico |
| Decisiones humanas | Toda mitigación con efecto en el ambiente; severidad final; comunicación al cliente; aceptación de riesgo |
| Terminado | Incidente cerrado según §24.4, o trabajo de mantenimiento entregado con evidencia |
| Salidas | AUDIT-Δ (SEV1/SEV2, regresión), DELIVERY (corrección aprobada), EVOLUTION (mejora con evidencia) |

## 24.2 Tipos de trabajo operativo

`INCIDENT` (servicio degradado o caído) · `BUG` (comportamiento aprobado roto, sin caída) · `MAINTENANCE` (dependencias, versiones, certificados, respaldos) · `IMPROVEMENT` (mejora dentro del alcance acordado de soporte) · `NEW_FEATURE` (= `NEW_SCOPE`, va a control de cambios §18.4) · `SECURITY_EVENT` (§23.3). Se clasifican antes de actuar (§2.6).

## 24.3 Severidad de incidentes

| Severidad | Criterio (por impacto observado, no por tiempo de respuesta) |
|---|---|
| `SEV1` | Golden Path caído para todos, pérdida o exposición de datos, dinero en riesgo |
| `SEV2` | Golden Path degradado o caído para un grupo; integridad en riesgo; sin alternativa |
| `SEV3` | Función secundaria afectada con alternativa |
| `SEV4` | Molestia menor, cosmético |

**SLA y SLO no se inventan.** Los tiempos de respuesta, resolución y objetivos de disponibilidad se toman de un contrato o decisión aprobada (`SLA_SOURCE=[fuente o NONE]`). Si es `NONE`, el reporte dice "sin SLA acordado" y propone uno como `VLUX_DECISION` pendiente.

Escalamiento: SEV1/SEV2 se notifican de inmediato al responsable humano definido en el runbook; el agente prepara el mensaje pero **no lo envía** sin autorización.

## 24.4 Flujo de incidente

1. **Registrar:** síntoma, ambiente, hora, quién reporta, `DEPLOYED_SHA`.
2. **Proteger:** no ejecutar acciones destructivas ni "a ver si se arregla" (reinicios, borrados, restauraciones, `--force`). Preservar evidencia.
3. **Diagnosticar:** hipótesis ordenadas por evidencia; cada una se confirma o descarta con un dato. Si no se encuentra la causa: `ROOT_CAUSE=UNKNOWN`, lo descartado y qué lo resolvería.
4. **Mitigar:** proponer la mitigación **reversible** de menor impacto (bandera, rollback a imagen anterior, desactivar una integración), con impacto, rollback y riesgo. Se ejecuta sólo con autorización explícita de esa acción.
5. **Corregir:** la corrección definitiva es un átomo (Full si toca los disparadores de §4.1) con Golden Path Gate.
6. **Cerrar:** el síntoma desapareció en el ambiente con evidencia; la causa está identificada o declarada `UNKNOWN`; existe una prueba de regresión o una razón para no tenerla; postmortem sin culpables con acciones `D-xx`/átomos.

## 24.5 Mantenimiento y soporte

- **Respaldos:** comprobar periódicamente que se generan **y** que se restauran (§21.3 punto 7); un respaldo con errores se reporta como `INCIDENT` SEV2 o superior si no hay otro respaldo válido.
- **Dependencias:** actualizar en átomos acotados, con pruebas y Golden Path; las mayores (framework, ORM, motor de base) son Full.
- **Versiones:** cada release con SHA, notas y rollback; el checkpoint se actualiza en el mismo commit (§5.1).
- **Reporte de soporte** (periodicidad acordada): incidentes por severidad, causas, mitigaciones, respaldos verificados, dependencias pendientes, fricción UX observada y propuestas, todo con evidencia.
- **Métricas de uso:** sólo las que existen o se instrumentan con autorización y respetando datos personales (§23.1 punto 7).
