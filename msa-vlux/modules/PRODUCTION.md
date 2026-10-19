# MSA-VLUX V4 · Módulo PRODUCTION

MSA_VERSION=4.0.0-rc3 · Módulo: PRODUCTION · Modos: PILOT, PRODUCTION
Depende del núcleo. §11 es texto de V3.2 sin cambios; §21 lo amplía (nunca lo relaja) y agrega LIVE_VERIFIED. El Release Gate (§10.4) está en DELIVERY.

---

# 11. NIVELES DE READINESS

Todo entregable declara su nivel. No se presenta un nivel inferior como uno superior.

| Nivel | Significa | Mínimo exigido |
|---|---|---|
| **DEMO-READY** | Sirve para mostrar y conversar | Gate DEMO-READY (§12.8); datos sintéticos; sin acciones reales |
| **PILOT-READY** | Lo usan usuarios reales del cliente en un ambiente acotado | Golden Path Gate; auth y RBAC reales; respaldos probados; datos del cliente con autorización; rollback; soporte definido |
| **PRODUCTION-READY** | Operación diaria | Lo anterior + Release Gate repetible, monitoreo, runbook de incidentes, secretos rotados, sin bypass de login ni credenciales por defecto |

Una auditoría de readiness honesta puede concluir "listo sólo para demo" (estado válido de readiness) y eso es un resultado válido, no un fracaso que haya que maquillar.

---

---

# 21. PILOTO, PRODUCCIÓN Y READINESS VERIFICABLE

§11 (arriba) es el texto de V3. V4 lo conserva y agrega `LIVE_VERIFIED` y un procedimiento comprobable.

## 21.1 Niveles

| Nivel | Significa | Mínimo exigido |
|---|---|---|
| `DEMO_READY` | Sirve para mostrar y conversar | Gate DEMO-READY (§12.8); datos sintéticos; sin acciones reales |
| `PILOT_READY` | Usuarios reales del cliente en un ambiente acotado | §21.3 con todos los puntos marcados **P** en PASS; Golden Path Gate PASS; aprobación humana del piloto |
| `PRODUCTION_READY` | Preparado para entrar en operación diaria | §21.3 con todos los puntos marcados **P** y **R** en PASS; ningún `CRITICAL`/`HIGH` abierto con bloqueo de producción; aprobación humana |
| `LIVE_VERIFIED` | Desplegado y comprobado en el ambiente | `PRODUCTION_READY` (o `PILOT_READY` para un piloto) + `DEPLOYED_SHA` observado en el ambiente + smoke del Golden Path en ese ambiente + checkpoint actualizado con fecha |

Ninguno se otorga por inferencia, por documentación ni por un reporte de otro agente. `LIVE_VERIFIED` caduca: si el ambiente cambia de SHA, se vuelve a verificar.

## 21.2 Fichas de modo

**PILOT**

| Campo | Contenido |
|---|---|
| Activación | Golden Path Gate PASS y decisión humana de exponer el sistema a usuarios reales acotados |
| Entradas | Línea base, trazabilidad, resultados de pruebas, ambiente de piloto definido |
| Responsabilidades | Evaluar §21.3 (puntos **P**), definir métricas del piloto (§8.5), plan de soporte y de retirada |
| Roles | Verifier + Security + Operations |
| Herramientas permitidas | Lectura del ambiente; pruebas en ambiente de piloto con datos autorizados; escritura local de reportes |
| Herramientas prohibidas sin autorización | Deploy, migraciones, alta de usuarios reales, envío de mensajes, cambios de DNS/Cloudflare/firewall |
| Evidencia | §21.3 con evidencia por punto |
| Documentos | Dictamen de readiness (§21.4), plan de piloto, runbook mínimo |
| Decisiones humanas | Inicio y fin del piloto, usuarios incluidos, datos autorizados |
| Terminado | Piloto ejecutado con métricas y hallazgos, o retirado con razón |
| Salidas | PRODUCTION, DELIVERY (cambios), AUDIT (regresión o incidente) |

**PRODUCTION**

| Campo | Contenido |
|---|---|
| Activación | "¿Podemos poner esto en producción?" o preparación de un release productivo |
| Entradas | Todo lo anterior + UAT aceptado + plan de release |
| Responsabilidades | §21.3 completo, dictamen §21.4, Release Gate §10.4 sólo con autorización explícita |
| Roles | Verifier + Security + Operations |
| Herramientas prohibidas sin autorización | Las mismas de PILOT, más cualquier acción en producción |
| Evidencia | §21.3; para `LIVE_VERIFIED`, SHA observado y smoke en producción |
| Documentos | Dictamen, runbook de incidentes, plan de rollback, responsables |
| Decisiones humanas | **Aprobación de despliegue (siempre)**, ventana, aceptación de riesgos residuales |
| Terminado | Dictamen emitido; si se autorizó y ejecutó el release, `LIVE_VERIFIED` registrado |
| Salidas | OPERATIONS (con `LIVE_VERIFIED`), DELIVERY (bloqueadores) |

## 21.3 Procedimiento: "¿Podemos poner este sistema en producción?"

Cada punto recibe `PASS` · `FAIL` · `UNKNOWN` · `N/A (razón)` y su evidencia. Columna Nivel: **P** exigido desde piloto, **R** exigido para producción.

| # | Área | Pregunta verificable | Nivel |
|---|---|---|---|
| 1 | Requisitos funcionales | ¿Los requerimientos del alcance están `UAT_ACCEPTED` o fuera de alcance por decisión? | P (los del piloto) / R |
| 2 | Golden Path | ¿PASS en el SHA candidato y en un ambiente equivalente? | P |
| 3 | Autenticación | ¿Sin bypass de login, sin credenciales por defecto, sesiones con expiración? | P |
| 4 | Autorización | ¿RBAC verificado en servidor para cada acción sensible (no sólo botones ocultos)? | P |
| 5 | Datos y migraciones | ¿Migraciones no destructivas probadas en copia; plan de migración de datos aprobado? | P |
| 6 | Respaldos | ¿Se generan, con qué frecuencia, dónde (incluido fuera del host)? | P |
| 7 | **Restauración probada** | ¿Se restauró un respaldo reciente en un ambiente aislado y se verificó? Fecha y evidencia | P |
| 8 | Secretos y credenciales | ¿Fuera del repo y del historial, rotados si estuvieron expuestos, con dueño? | P |
| 9 | Dependencias | ¿Sin vulnerabilidades críticas conocidas sin mitigar? | R |
| 10 | Integraciones | ¿Cada integración real probada (sandbox/contrato) y con modo degradado? | P si el piloto la usa / R |
| 11 | Infraestructura | ¿Host/plataforma con capacidad suficiente medida, TLS, redirecciones, dominio con dueño? | P |
| 12 | Logs | ¿Existen, sin datos sensibles, con retención conocida? | P |
| 13 | Alertas | ¿Alguien recibe una alerta cuando el Golden Path o el servicio cae? | R |
| 14 | Monitoreo | ¿Disponibilidad y errores observables? | R |
| 15 | Rendimiento | ¿Medido contra un umbral acordado, o declarado `NOT_MEASURED`? | R si hay umbral |
| 16 | Seguridad | ¿Revisión §23 sin `CRITICAL`/`HIGH` abiertos con bloqueo? | P |
| 17 | Rollback | ¿Probado (bandera apagada, imagen anterior, migración reversible)? | P |
| 18 | Incidentes | ¿Runbook con severidades, contactos y escalamiento? | R |
| 19 | Soporte y responsables | ¿Dueños de datos, dominio, cuentas, infraestructura y soporte nombrados? | P |
| 20 | Capacitación | ¿Usuarios clave capacitados, con material? | R |
| 21 | UAT | ¿Aceptación registrada por el cliente? | R |

Reglas de decisión:
- Un `FAIL` o un `UNKNOWN` en un punto exigido para el nivel impide ese nivel. **Un `UNKNOWN` crítico no equivale a `PASS`.**
- "El respaldo existe" no aprueba el punto 7: sólo una restauración comprobada lo aprueba.
- Un hallazgo `CRITICAL` de seguridad bloquea toda promoción (§2.7).
- La aprobación humana de despliegue es obligatoria aunque todo esté en PASS.

## 21.4 Dictamen de readiness

```text
SYSTEM=[proyecto]  SHA_EVALUATED=[sha]  ENV_OBSERVED=[ambientes]
TARGET_LEVEL=[PILOT_READY|PRODUCTION_READY]
RESULT=[GRANTED | NOT_GRANTED | GRANTED_FOR_LOWER_LEVEL:<nivel>]
PASS=[n]  FAIL=[n]  UNKNOWN=[n]  N/A=[n]
BLOCKERS=[ítems §21.3 y FINDING_ID]
NOT_VERIFIED=[lo que no se pudo observar]
HUMAN_APPROVAL=[PENDING | nombre + fecha]
NEXT_ACTION=[átomo propuesto]
```

Un dictamen honesto puede concluir "listo sólo para demo" (§11). Es un resultado válido, no un fracaso.
