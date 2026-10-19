# Adaptación MSA-VLUX 4.0.0-rc3 al runtime Codex

## Qué se preserva y qué cambia

Preservado del paquete original: núcleo de metodología MSA-VLUX V4.0.0-rc3, 12 módulos de ciclo de vida, evidencia B1/B2/B3, AUDIT-0, átomos Lite/Full, roles, revisión, decisiones humanas, control de cambios, trazabilidad y criterios de preparación de piloto/producción.

Adaptado: rutas de carga, activación de skill, terminología de subagentes y eliminación de ejemplos que mencionaban sistemas, clientes o repositorios concretos. No se importa información de ninguna aplicación. **No se declara equivalencia binaria con la distribución original para otro runtime.**

## Rutas

- Raíz de habilidad: el directorio que contiene `SKILL.md`.
- Núcleo: `reference/msa-vlux-master-v4.0.0-rc3.md`.
- Módulos: `modules/<NOMBRE>.md`.
- Si el núcleo sugiere rutas para otro runtime, ignóralas y usa estas rutas reales.
- En Codex local puedes instalar la carpeta en `${CODEX_HOME:-~/.codex}/skills/msa-vlux/` o en `<REPO>/.agents/skills/msa-vlux/`.
- `AGENTS.md` de un repositorio solo se incorpora cuando el propietario lo decide. No editar uno existente sin consentimiento ni sobrescribir reglas.

## Preflight: distinguir capacidad de permiso

- La existencia de shell, GitHub, Git, herramientas de edición, browser, subagentes o conectores no concede autorización para usarlos con efectos.
- `EXTERNAL_WRITE_AUTHORIZED=NO` y `PAID_SERVICE_AUTHORIZED=NO` hasta aprobar una acción concreta.
- Para la fase AUDIT, usar el modo solo lectura/sandbox si existe. No afirmes que los prompts impiden escrituras.
- Git local no siempre es inocuo: hooks, filtros y herramientas externas pueden ejecutar procesos. Verifica el entorno antes de confiar en código no inspeccionado.
- Un modelo puede usar subagentes solo si el runtime actual los ofrece. Subagente instruido a ser read-only != barrera verificada.
- No uses comandos que accedan a secretos, sistemas productivos o redes sin necesidad autorizada.

## Contexto independiente

El paquete no incluye código, repositorios, URLs, contratos, datos personales, credenciales, decisiones, clientes ni configuraciones de ninguna app. El contexto lo proporciona el usuario *en cada trabajo*, mediante archivos y conexiones autorizadas. Nunca infieras datos de otros chats o apps que no estén dentro del alcance.

## Roles (lentes cuando no existan subagentes)

- Scout: fuentes, requisitos y restricciones.
- Architect: diseño, integridad y alternativa mínima.
- Verifier: pruebas y reconciliación de hallazgos.
- Security: amenazas, privacidad y mínimos privilegios.
- Experience: UX, accesibilidad, claridad de recorridos.
- Operations: ambientes, observabilidad, backups, despliegue.
- Commercial: resultados medibles, alcance y ROI sin inventar métricas.
- Demo: narración, interacción y etiquetas de simulación.

Si actúas tú solo con varios lentes, descríbelo como *revisión propia*, no como auditoría independiente.

## Estado de esta distribución

Portabilidad documental y estructura de la skill verificables sin ejecutar Codex. No se han instalado ni validado protecciones técnicas del entorno objetivo. `TECHNICAL_GUARDS=not_verified` hasta que se compruebe lo contrario. La metodología V4.0.0-rc3 histórica contenía advertencias de riesgos residuales del agente en su runtime original; este paquete no garantiza haber resuelto esos riesgos por traducir instrucciones.
