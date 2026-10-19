---
name: msa-vlux
description: Metodología Secuencial Atómica MSA-VLUX 6.0.0 para Codex y Claude Code/Cloud; auditoría y entrega controladas por átomos, evidencia, autoevaluación, continuidad y mejora supervisada cuando la versión lo admita.
---

# MSA-VLUX 6.0.0 — Skill genérica y portable

**No se precargan aplicaciones, clientes, contratos, cuentas, repositorios, entornos ni decisiones.** Si no hay proyecto, declara `READY_NO_PROJECT` y no inventes uno. No reutilices información de otros proyectos.

## Inicio breve y carga progresiva

1. Leer `reference/PROTOCOLO-V4.1.md` antes de operar. después `reference/PROTOCOLO-V4.2.md` y `reference/PROTOCOLO-V5.md`, para continuidad y mejora medible.
2. Ejecutar `python scripts/msa.py doctor` si existe Python y permisos para el CLI; si no, declarar incapacidad de ejecutar comprobaciones.
3. Declarar `MSA_VERSION=5.0.0`, `AGENT_RUNTIME` real, `TECHNICAL_GUARDS=not_verified` hasta comprobarlos, `EXTERNAL_WRITE_AUTHORIZED=NO` hasta permiso específico.
4. Leer **solo** los módulos necesarios de `modules/` y las secciones relevantes del núcleo histórico `reference/msa-vlux-master-v4.0.0-rc3.md` antes del átomo; no cargar todo por inercia.
5. Si el proyecto es existente y no hay expediente válido, iniciar `AUDIT-0`. Si hay expediente, verificar baseline SHA y estado antes de continuar. Distinguir B1 código, B2 release, B3 desplegado y UAT real.
6. Formular un único átomo activo con criterio falsable de terminado; ejecutar exclusivamente dentro de permisos.
7. Registrar evidencia, resultado, prueba no ejecutada y limitaciones. **Autoevaluar y pedir revisión independiente cuando el contexto lo amerite**; no confundir lentes de un mismo agente con revisión externa.
8. Cerrar con hechos verificables, pendientes y siguiente átomo, sin GO cuando falten controles críticos.

## Comandos por capacidad

- `doctor`, `verify-package`, `init`, `status`, `set-atom`, `record`, `verify-ledger`, `assess`, `eval`, `gate`: disponibles desde V4.1.
- `handoff`, `verify-handoff`, `import-handoff`, `resume`, `role-packet`, `check-review`: V4.2 y superiores, después de verificar el archivo.
- `improve`: compara baseline/candidato/holdout, solo genera una propuesta, nunca aplica cambios.


## Fuente de metodología

- `reference/msa-vlux-master-v4.0.0-rc3.md`: núcleo histórico completo.
- `modules/`: los **12** módulos originales.
- `reference/PROTOCOLO-V4.1.md`: controles evaluables de 4.1.
- `reference/PROTOCOLO-V4.2.md`: delegación y reanudación.
- `reference/PROTOCOLO-V5.md`: optimización con métricas y holdout.

- `GUIA-AUTOEVALUACION.md`: revisión de personas y agentes, con evidencias.
- `README.md`: instalación y límites de seguridad.

## Seguridad y honestidad

- La skill y sus scripts **NO** son control de acceso del SO ni interceptan acciones externas; `gate` devuelve siempre DENY por diseño. Exigir sandbox, credenciales mínimas y controles externos verificables.
- Push, PR, merge, deploy, eliminación, cambios de datos, email, pagos, acceso a datos personales y cualquier escritura externa requieren permisos específicos. No suponer que un hook autoriza algo.
- Los escáneres de cadenas detectan solo indicios, no garantizan ausencia de secretos; validar paquetes y adjuntos con revisión humana.
- No garantizar persistencia ni autoaprendizaje no instrumentados. Para Cloud efímero, V4.2+ entrega un handoff verificable que el usuario debe guardar en un destino privado.
- `AGENT_RUNTIME=claude-cloud` no significa que pueda extraer ZIP, acceder a disco o ejecutar Python: comprobarlo.

## Capacidades de V6.0.0

- V5.1: `observe`, `metrics`, `calibrate` con registros suministrados y sin verificación automática de procedencia.
- V5.2: `benchmark` matemático sintético (PSO/random) y `paired-experiment` (datos pareados, holdout y revisión humana).
- V6.0: `adaptive-plan` por riesgo; opcional `--experiment` informativo sin promover ni autorizar acciones.
