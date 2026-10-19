# MSA-VLUX V4 · Módulo PATTERNS

MSA_VERSION=4.0.0-rc3 · Módulo: PATTERNS · Se carga en: revisiones Full del Verifier
Depende del núcleo. §15 es texto de V3.2 sin cambios; §26 agrega patrones observados en la evolución a V4.

---

# 15. PATRONES Y ANTIPATRONES VLUX

## 15.1 Patrones (se aplican cuando el problema los justifica)

1. **Captura → normalización → deduplicación → revisión humana** en leads, formularios y WhatsApp.
2. **Prospecto ≠ cliente; cotización ≠ proyecto.** No colapsar estados comerciales y operativos por conveniencia visual.
3. **Idempotencia antes de IA.** La identidad es el evento del proveedor, la garantía vive en la base de datos (índice único) y se prueba con concurrencia real.
4. **Fuente única de verdad + capa observadora** para la experiencia.
5. **Demo determinista:** reiniciar y reproducir hasta la escena; restaurar al salir.
6. **Revisión humana de decisiones comerciales:** el sistema prepara, una persona aprueba y envía.
7. **Ahora / Piloto / Visión.**
8. **Datos sintéticos por defecto en demo**, con marca visible y discreta.
9. **No-fake-affordances.**
10. **QA de experiencia además de QA técnico:** accesibilidad, responsive, estados, audio, ritmo y navegación.
11. **Respaldo y rollback antes de tocar operación.**
12. **Handoff escrito** que cualquier persona o agente (ChatGPT, Codex, Claude) pueda retomar.
13. **Checkpoint `CLAVE=valor`** con SHA de feature, release y deploy.
14. **Átomo N.1** abierto por revisión independiente antes de aprobar.
15. **Bandera apagada por defecto** como rollback de un cambio de comportamiento.
16. **Candidato → final con gate:** una salida final sólo se publica tras completar todas sus verificaciones; un borrador nunca se promueve por copia o renombre (fail-closed).
17. **Registro de decisiones con identificador**, y cuando conviene, captura dentro del sistema.
18. **Documentación generada** desde el catálogo o manifiesto, marcada "no editar a mano".

## 15.2 Antipatrones (señales de detenerse)

- "Ya que estamos aquí…" y se amplía el alcance.
- Se empieza por dashboard o UI sin mapear el proceso.
- Se presenta una pantalla como evidencia de backend.
- Se agrega IA sin métricas ni confiabilidad del flujo base.
- Se clona un proyecto de otro cliente con sus rastros, o se desarrolla un cliente en ramas del repo de otro sin decisión registrada.
- Se usa un ROI inventado como argumento de venta.
- Se da por terminado porque las pruebas unitarias pasan mientras el Golden Path o el E2E fallan.
- Se hace deploy sin respaldo, rollback ni smoke.
- Se cambia la arquitectura por preferencia del agente.
- Se pregunta algo que ya está documentado y accesible.
- Se borra historia para ocultar contradicciones.
- Se confía en un documento desactualizado frente al SHA real.
- Se gastan créditos de TTS antes de aprobar el guion o antes de validar una muestra corta de voz.
- Un `voiceLabel` o una etiqueta de demo dice algo distinto de lo que realmente ocurre.
- Un agente marca como hecha una revisión humana.
- Se confunde **tool disponible** con **acción autorizada**.
- Se asume que un subagente puede o no puede delegar sin comprobar la disponibilidad real de `Agent` y la profundidad.
- Un subagente con rol de revisión conserva escrituras o conectores mutantes que no necesita.

---

# 26. PATRONES Y ANTIPATRONES AGREGADOS EN V4

**Patrones**
19. **Línea base antes de construir** en proyectos heredados: AUDIT-0 en lugar de repetir la prospección.
20. **Trazabilidad por columnas** (aprobado → B1 → B2 → B3 → probado → UAT) con evidencia por celda.
21. **Clasificación antes de estimar** (`WORK_TYPE`): lo no contratado se registra, no se absorbe.
22. **Restauración probada** como única evidencia de que un respaldo sirve.
23. **Readiness por clase de componente** en plataformas: demo comercial, configuración, módulos e integraciones se evalúan por separado.

**Antipatrones**
- Reiniciar o restaurar "para ver si se arregla" durante un incidente.
- Declarar una auditoría completa sin acceso al ambiente.
- Convertir un hallazgo en corrección dentro de la misma auditoría.
- Presentar como métrica un número que no se midió.
- Inventar SLA, condiciones de pago o hitos sin fuente contractual.
- Tratar la demo comercial de una plataforma como evidencia de la configuración real.
