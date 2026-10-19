# MSA-VLUX V4 · Módulo QUALITY

MSA_VERSION=4.0.0-rc3 · Módulo: QUALITY · Se carga en: todo átomo Full, dimensión 8 de AUDIT, PILOT y PRODUCTION
Depende del núcleo. Amplía —no reemplaza— el Build Gate (§10.1) y el Golden Path Gate (§10.3), que siguen en el módulo DELIVERY con su texto de V3.

---

# 19. INGENIERÍA DE CALIDAD

## 19.1 Regla innegociable

**Si falla el Golden Path crítico, el sistema no puede aprobar producción ni cerrar el átomo, aunque todas las demás pruebas pasen.** Si el Golden Path no pudo ejecutarse, el resultado es `UNKNOWN`, y un `UNKNOWN` crítico no cuenta como `PASS` (§2.7).

## 19.2 Las pruebas protegen invariantes y escenarios reales

Antes de elegir herramientas, el Verifier lista:
1. los invariantes del flujo (§9.5);
2. los escenarios operativos reales (quién hace qué, con qué datos, qué puede fallar);
3. qué prueba protege cada invariante y escenario.

Una prueba que no protege un invariante, un escenario o una regresión conocida no se exige. Un número alto de pruebas no es evidencia de calidad (§10.3).

## 19.3 Matriz de tipos de prueba

Exigencia: **R** requerida · **C** condicional (cuando se cumple el disparador) · **—** no aplica por defecto.

| Tipo | Lite | Full | Release / PRODUCTION | Disparador para C |
|---|---|---|---|---|
| Unitarias del área tocada | R | R | R | — |
| Integración (DB, colas, servicios internos) | — | R si toca persistencia | R | Hay base de datos o servicio interno |
| Contrato (API, webhook, payload externo) | — | C | C | Hay un consumidor o proveedor externo |
| E2E del Golden Path | — | C (átomo crítico) | R | Toca Golden Path, dinero, permisos o datos |
| Seguridad (SAST, secretos, dependencias, authz) | — | C | R | Disparadores de §4.1 en seguridad |
| Concurrencia | — | C | C | Escrituras concurrentes, contadores, folios, inventario |
| Idempotencia | — | C | C | Webhooks, reintentos, colas, mensajería |
| Compatibilidad / migración de datos | — | C | R si hay migración | Esquema o datos legacy |
| Regresión | — | R | R | — |
| Accesibilidad | — | C | C | Hay UI para usuarios |
| Responsive | — | C | C | Hay UI usada en más de un tamaño |
| Rendimiento | — | C | C | Hay umbral acordado o queja medida |
| Recuperación (restaurar respaldo, rollback) | — | — | R | — |
| Integraciones (sandbox o mock con contrato) | — | C | R si hay integración | Sistema externo |
| Fallo parcial (dependencia caída, timeout) | — | C | R | Dependencia externa o de red |

Un **C** que no se ejecuta se registra como `N/A` con razón o como `NOT_RUN` con riesgo. No se omite en silencio (§10.1).

## 19.4 Perfiles por stack

Respeta el stack real (§9.3). Las herramientas son ejemplos; el criterio es la cobertura, no la marca de la herramienta.

| Stack | Unidad / integración | E2E | Datos y migraciones | Notas |
|---|---|---|---|---|
| Next.js + React + TS + Postgres/Prisma | Vitest/Jest; integración contra Postgres desechable (`*_test`) | Playwright (+ axe para accesibilidad) | `prisma migrate deploy` en base aislada; comparar esquema | Server Components: probar límites cliente/servidor |
| Electron + SQL Server | Pruebas del proceso main y del acceso a datos contra una instancia de prueba | Playwright para Electron o pruebas manuales guiadas con evidencia | Scripts de migración probados contra copia anonimizada | Instalador, auto-update y credenciales locales son parte del Golden Path |
| Python / PySide + bases legacy (Pervasive, etc.) | pytest; adaptadores con dobles cuando el motor no se puede levantar | pytest-qt o recorrido manual con capturas | Lectura de solo-lectura sobre copias | No migrar el motor por preferencia; probar el candidato→final (patrón 16) |
| Plataforma configurable | Pruebas de módulos propios sobre base desechable | Recorrido del flujo configurado con datos sintéticos | Exportar/importar configuración; no tocar la base productiva | Distinguir configuración estándar de módulos propios (§20.3) |
| Sitio estático / página de prospección | Validación de HTML y de enlaces | Navegador real a 1280 y 375 px | — | QA de §16.6 |
| Bots / mensajería | Pruebas de idempotencia con concurrencia real (patrón 3) | Conversación simulada contra sandbox del proveedor | Índices únicos verificados en base | Nunca contra el número productivo |

## 19.5 Build Gate ampliado (todo Full)

Además de §10.1:
- Las pruebas se ejecutan **en el SHA que se reporta**; el reporte incluye comando, resultado y SHA.
- Si una prueba es "flaky", se reporta como fallo con evidencia de inestabilidad; no se reintenta hasta que pase para cerrar el átomo.
- Un CI externo o un mensaje que diga "todo pasa" es evidencia de prioridad 7 (§2.2) hasta reproducirlo.
- Toda prueba que escribe en base de datos se niega a correr fuera de una base local o desechable (§9.4).

## 19.6 Golden Path Gate ampliado (átomos críticos y release)

Además de los 7 puntos de §10.3:
- El Golden Path se describe como guion reproducible (pasos, datos, resultado esperado) en `MSA-EVIDENCIAS.md`, para que otra persona o agente lo repita.
- Se registran tiempos, pasos y errores **medidos**; si no se midieron, se dice "no medido".
- El resultado es `PASS`, `FAIL` o `UNKNOWN` (no se pudo ejecutar), con el SHA y el ambiente.

## 19.7 Formato de evidencia de prueba

```text
TEST_RUN_ID=[id]  SHA=[sha]  ENV=[local|test|staging|production]
COMMAND=[comando exacto]
RESULT=[PASS n/m | FAIL n/m | NOT_RUN: razón]
GOLDEN_PATH=[PASS|FAIL|UNKNOWN]
NOTES=[fallos, flakiness, omisiones]
```
