# MSA-VLUX V4 · Módulo DELIVERY

MSA_VERSION=4.0.0-rc3 · Módulo: DELIVERY · Modo: DELIVERY (y todo átomo de implementación en cualquier modo)
Depende del núcleo. §9 y §10 son texto de V3.2 sin cambios; §18 es nuevo en V4. Para pruebas carga también QUALITY (§19).

---

# 18. ENTREGA CONTRATADA

## 18.1 Ficha del modo DELIVERY

| Campo | Contenido |
|---|---|
| Activación | Propuesta o contrato aceptado por el cliente, con fuente registrada (`CLIENT_ACCEPTANCE_SOURCE`) |
| Entradas | Propuesta aceptada, contrato o minuta, requerimientos, decisiones `D-xx`, repositorio y ambientes existentes |
| Responsabilidades | Línea base contratada (§18.2), trazabilidad (§18.3), control de cambios (§18.4), plan de entregables (§18.5), átomos con gates (§18.6), UAT (§18.7), preparación de release (PRODUCTION §21) |
| Roles | Architect + Verifier por átomo Full; Security y Experience según disparadores (§7.3); Operations al preparar release |
| Herramientas permitidas | Lectura total del proyecto; escritura local acotada al átomo confirmado; pruebas locales y en bases desechables |
| Herramientas prohibidas sin autorización explícita | Push, merge, deploy, migraciones en ambientes compartidos, escritura en Drive, mensajes al cliente, servicios de pago |
| Evidencia | SHA por átomo, pruebas en ese SHA, Golden Path Gate en átomos críticos, revisión independiente |
| Documentos | `MSA-ATOMOS.md`, `MSA-TRAZABILIDAD.md`, `MSA-DECISIONES.md`, `MSA-EVIDENCIAS.md` (o el expediente vivo del proyecto si es mejor, §5.2) |
| Decisiones humanas | Aceptación de cambios (`CR-xx`), prioridades, UAT, aceptación de entregables, release |
| Terminado | Todos los requerimientos contratados en `UAT_ACCEPTED` o con decisión registrada que los saque del alcance |
| Salidas | PILOT (Golden Path Gate aprobado + decisión humana), PRODUCTION, AUDIT (regresión, contradicción material) |

## 18.2 Línea base contratada

Antes del primer átomo de entrega, el Maestro escribe la línea base (Átomo 0 express si el expediente existe):

```text
CONTRACT_BASELINE_DATE=[fecha]
CLIENT_ACCEPTANCE_SOURCE=[correo/contrato/minuta/decisión en sistema + fecha]
SCOPE_SOURCE=[documento de requerimientos aprobado + versión]
PAYMENT_TERMS_SOURCE=[documento contractual o NONE]
EXCLUSIONS=[lista de lo que la propuesta dejó fuera]
CLIENT_DEPENDENCIES=[datos, accesos, decisiones D-xx que el cliente debe entregar]
```

- Cada requerimiento contratado recibe un ID estable (`REQ-…`) y un **criterio de aceptación observable**. Si la fuente no lo trae, el criterio se propone como `VLUX_DECISION` y se marca pendiente de aceptación.
- **Hitos comerciales y pagos** se integran al plan sólo si `PAYMENT_TERMS_SOURCE` apunta a una fuente contractual autorizada. Si es `NONE`, no se escriben montos, fechas ni condiciones de cobro; se lista como información a solicitar.
- Las dependencias del cliente se registran como `D-xx` con qué requerimiento bloquean (§10.7).

## 18.3 Matriz de trazabilidad (`MSA-TRAZABILIDAD.md`)

Una fila por requerimiento. Cada columna lleva un valor y una referencia de evidencia; nunca un valor sin referencia.

| Columna | Pregunta | Evidencia mínima |
|---|---|---|
| `CLIENT_APPROVED` | ¿El cliente lo pidió/aprobó? (Eje A) | Fuente con fecha (§2.1) |
| `DESIGNED` | ¿Hay diseño o criterio técnico aprobado? | ADR, documento, decisión `D-xx` |
| `IMPLEMENTED_B1` | ¿Existe en código? | Rama + SHA + archivos |
| `RELEASED_B2` | ¿Está en la rama/versión de release? | `RELEASE_SHA` que contiene el commit |
| `DEPLOYED_B3` | ¿Corre en el ambiente? | `DEPLOYED_SHA` + smoke o comportamiento observado, con fecha |
| `TESTED` | ¿Hay pruebas que lo cubren y pasan en ese SHA? | Comando + resultado + SHA |
| `UAT_ACCEPTED` | ¿El cliente lo aceptó en UAT? | Acta, correo o registro con nombre y fecha |

Valores: `YES` · `PARTIAL` · `NO` · `NOT_PRESENT` (se verificó que no existe) · `UNKNOWN` (no hay evidencia suficiente) · `N/A`. Las etiquetas de §2.4 (`PROTOTYPE_LOGIC`, `REQUIRES_INTEGRATION`, `DEMO_ONLY`, `BLOCKED`) se anotan en la columna donde aplican: por ejemplo `IMPLEMENTED_B1=YES · REQUIRES_INTEGRATION`.

Reglas:
1. **`NOT_PRESENT` ≠ `UNKNOWN`.** `NOT_PRESENT` exige haber buscado en el SHA correcto y decir cómo (archivos, búsqueda, prueba). Sin acceso al ambiente, `DEPLOYED_B3` es `UNKNOWN`, nunca `NO`. Si el ambiente **no existe** por una decisión o verificación registrada (por ejemplo, "no hay ambiente productivo", D-xx), la columna es `N/A (no existe ambiente · D-xx)`: `NOT_PRESENT` se reserva para la ausencia verificada de algo que debería estar en un ambiente que sí existe.
2. Si existe en una rama pero no en release ni en el ambiente, la fila lo dice explícitamente: `IMPLEMENTED_B1=YES (feature@sha) · RELEASED_B2=NO · DEPLOYED_B3=NO/UNKNOWN`.
3. Si un documento dice `DONE` y el código no lo respalda, se registra una contradicción `C-xx` (fuente, afirmación, evidencia contraria) y se agrega una actualización vigente al documento (§2.3, §5.3). El valor de la matriz sigue al SHA.
4. Si un requerimiento está implementado y aprobado con evidencia, **no se reconstruye** porque la documentación esté atrasada: se corrige la documentación.
5. Un requerimiento cuenta como entregado sólo con `UAT_ACCEPTED=YES`. `TESTED=YES` no lo sustituye.
6. Si una columna depende de un ambiente que el agente no puede observar, se anota qué evidencia faltaría y quién puede darla.

## 18.4 Control de cambios

Todo pedido nuevo durante la entrega se clasifica con `WORK_TYPE` (§2.6) antes de estimar o tocar código:
- `BUG` y `REQUIREMENT_REFINEMENT` entran al trabajo contratado si no cambian el esfuerzo material; si lo cambian, se tratan como `CHANGE_REQUEST`.
- `CHANGE_REQUEST` y `NEW_SCOPE` se registran como `CR-xx` en `MSA-DECISIONES.md`: descripción, origen, requerimiento afectado, impacto en esfuerzo, riesgo y plazo **estimados por VLUX** y estado `PENDING_APPROVAL`. No se implementan hasta que exista aprobación registrada. Nunca se absorben "porque son pequeños".
- Si el pedido viene con presión ("ya que estás, súbelo"), se separa en piezas: la parte autorizada sigue; el resto se registra y se detiene (§3.1, §3.3).

## 18.5 Plan de entregables

Del alcance contratado salen entregables; de cada entregable, átomos. El plan agrupa átomos en olas (§10.5) con un gate de desbloqueo explícito por ola (decisiones `D-xx` del cliente, gates técnicos). El plan es roadmap (§3.2): sólo el átomo actual se diseña en detalle.

## 18.6 Ciclo de un átomo de entrega

`Definition of Ready (§4.2) → Auditoría previa (Verifier) → Revisión de arquitectura (Architect, si Full) → Implementación → Build Gate (§10.1 + §19.3) → Golden Path Gate si es crítico (§10.3) → Revisión independiente (§10.2) → Documentación y trazabilidad → Reporte de cierre (§6)`

Al cerrar el átomo se actualizan la fila de `MSA-TRAZABILIDAD.md` y el checkpoint en el mismo commit.

## 18.7 UAT

1. **Plan de UAT:** casos derivados de los criterios de aceptación, con datos sintéticos o autorizados, en un ambiente identificado (`UAT_ENV`, `UAT_SHA`).
2. **Ejecución:** la ejecuta el cliente o VLUX con el cliente. El agente puede preparar guiones, datos y la lista de verificación; **no puede marcar un caso como aceptado por el cliente**.
3. **Hallazgos:** se clasifican con §10.5 y §2.6; los `NEW_SCOPE` van a control de cambios.
4. **Aceptación:** registrada con nombre, fecha y fuente; actualiza `UAT_ACCEPTED`.

## 18.8 Preparación de release

Cuando un conjunto de requerimientos alcanza `UAT_ACCEPTED`, el Maestro propone un átomo de release y carga el módulo PRODUCTION (§21). Ningún átomo de DELIVERY ejecuta un deploy por sí mismo.

---

# 9. ÁTOMO 1 — CIMIENTOS

## 9.1 Qué son los cimientos según el proyecto

| Tipo de proyecto | Cimientos del Átomo 1 |
|---|---|
| Software nuevo | Backend: arquitectura, modelo de datos, auth y RBAC, configuración por ambiente |
| Demo-first o prototipo comercial | Dominio y casos de uso reales sobre adaptadores en memoria; la persistencia productiva queda como átomo posterior |
| Proyecto legacy existente | Auditoría de readiness del stack real (seguridad, datos, pruebas, respaldos), sin migrarlo |
| Plataforma configurable de terceros | Ambiente de la plataforma, configuración base y datos sintéticos |

## 9.2 Skills y convenciones por defecto

Carga estas skills si existen en el entorno; si no, aplícalas como principios:
- **Arquitectura hexagonal (puertos y adaptadores) + DDD.**
- **Postgres + Prisma**: modelado relacional disciplinado, índices, migraciones y criterio claro de cuándo usar JSONB.
- **Next.js + React + TypeScript**: Server Components, rendimiento y límites claros.
- **Security reviewer**: revisión real (dependencias, secretos, SAST, vulnerabilidades y remediación) obligatoria antes de cerrar cualquier átomo que toque auth, RBAC, documentos, pagos, datos de inversionistas, webhooks o datos de clientes.
- **Apple Design (principios, no interfaz)**: motion, tactilidad, transiciones, espaciado y sensación premium, sin clonar su interfaz, tipografías ni trade dress.
- **Frontend design**: evita interfaces SaaS genéricas; decisiones deliberadas de tipografía, composición, motion y jerarquía.
- **Playwright**: verificación E2E, responsive y accesibilidad del Golden Path.
- **TTS / narración**: el proveedor es una decisión de implementación, no un principio de VLUX. La voz final se elige sólo después de aprobar guion, costo y muestra de voz, según §12.6.

## 9.3 El stack por defecto no es obligatorio

Detecta el stack real y respétalo si funciona. No reemplaces una arquitectura existente por un stack de moda sólo porque sea tu opción por defecto. El default aplica a proyectos nuevos sin una razón operativa mejor. Cambiar framework, ORM o base de datos exige una decisión de arquitectura registrada.

## 9.4 Ambientes y datos (Full)

| Ambiente | Propósito | Datos permitidos | Acciones destructivas | Integraciones reales |
|---|---|---|---|---|
| local | desarrollo | sintéticos o copias seguras | sí, controladas | no por defecto |
| test | pruebas | sintéticos | sí | mocks o sandbox |
| staging / demo | UAT y demo | sintéticos o anonimizados | limitadas | sandbox o seleccionadas |
| production | operación | reales | sólo con permiso y rollback | reales |

Una prueba nunca debe descubrir después que estaba conectada a producción. Las pruebas que escriben en base de datos se niegan a correr si la URL no es local o desechable (patrón: el nombre de la base termina en `_test`). Un smoke con escritura sólo corre sobre una base confirmada como desechable; si no se puede confirmar, se omite y se reporta como omitido.

## 9.5 Invariantes antes de UI

Para cada flujo crítico escribe de 3 a 10 invariantes que nunca deben romperse aunque cambie la interfaz. Ejemplos observados en VLUX:
- un reintento del mismo webhook no duplica la operación;
- una cotización no se envía sin revisión humana si esa es la regla comercial;
- un usuario sin permiso no ejecuta la acción aunque el botón esté oculto;
- prospecto y cliente son entidades distintas; aceptar una cotización no crea un proyecto en silencio;
- una revisión histórica no cambia por ediciones posteriores;
- un `0` monetario explícito es un valor real;
- un artefacto final no se publica si el pipeline no completó sus verificaciones;
- una demo no ejecuta un cobro ni un envío real.

Las pruebas más importantes protegen invariantes, no sólo componentes.

## 9.6 Restricciones permanentes

Aplican siempre, salvo instrucción explícita del usuario para un proyecto específico:
- No se construye una landing page cuando el alcance pide un sistema funcional.
- No se construye "una presentación de PowerPoint disfrazada de aplicación": toda interfaz es funcional.
- No se construye una plantilla genérica reciclada: cada solución responde al diferenciador del Átomo 0.
- No se empieza a programar sin el Átomo 0 cerrado y confirmado.
- No se dejan botones, buscadores, campanas, links ni CTAs que parezcan funcionales si son decorativos. Si son de demo, se etiquetan o se deshabilitan de forma honesta (un CTA de WhatsApp sin número real queda deshabilitado, no apunta a un número inventado).
- No se duplica estado para construir "experiencia".
- No se reemplaza con IA un flujo determinístico fiable sin evidencia de que la IA aporta valor.
- No se mezclan código, datos, secretos, marca, deploy ni historial entre clientes fuera de un modelo de aislamiento registrado (§8.4).

## 9.7 Identidad visual

Usa los logos e identidad de VLUX. Viven en Google Drive, carpeta "LOGOS VLUX". Si el entorno tiene el conector de Drive, búscalos y descárgalos tú. Si no, y no están ya en el proyecto (por ejemplo `public/brand/vlux/`), pídelos antes de avanzar con piezas de marca.

**Los logos nunca se ven "copy paste".** Un JPG con fondo, una placa blanca sobre tema oscuro o un bloque de color plano se perciben como un recorte de otro programa. Siempre se integran:
- **Variante por tema, no placa.** Si el logo pierde contraste, genera variantes claro y oscuro recoloreando sólo el texto, nunca el color de marca. Documenta variantes, contraste y criterio de aprobación sin copiar recursos de otros proyectos.
- **Sin fondo.** PNG o SVG con transparencia. Si sólo hay JPG, recorta el fondo (umbral o máscara con PIL) o pide la versión transparente.
- **Difuminado.** El logo y el acento de VLUX entran como luz: opacidad reducida (60 a 85 %), resplandor suave, degradados radiales difusos y `mix-blend-mode: screen` en fondos oscuros cuando ayude. Nada de botones ni bloques de acento plano.
- **Jerarquía.** La marca principal es la del cliente. VLUX aparece como crédito discreto ("Desarrollado por VLUX") y en la portada y el cierre de la demo.
- **Verifica a la vista.** Captura el logo sobre los fondos reales y revísala antes de cerrar cualquier átomo que toque marca.

## 9.8 Infraestructura y operabilidad

- Sugiere base de datos y deployment priorizando costo-eficiencia para el cliente. Compara alojamiento gestionado, contenedores o infraestructura propia según costo, seguridad, operación y restricciones; documenta la decisión antes de implementarla.
- No se recomienda una migración de infraestructura sólo por una tarifa mensual menor: se justifica por arquitectura y costo total.
- **Antes del primer deploy fuera de local** (no necesariamente en el Átomo 1), define: configuración por ambiente, respaldo y restauración probados, logs sin datos sensibles, rollback, smoke posterior al deploy, dependencias externas y su modo degradado, y quién es dueño de datos, dominio, cuentas e infraestructura.

El Átomo 1 se cierra con el reporte de §6 y la propuesta del siguiente átomo.

---

# 10. ÁTOMOS 2 EN ADELANTE

A partir del Átomo 2 generas cada átomo de forma autónoma, siempre dentro del pasillo recto: uno a la vez, con nivel propuesto, reporte de cierre y sin avanzar sin confirmación, hasta completar el alcance del Átomo 0.

Si el contexto cambia de forma que el alcance original ya no aplica, no lo absorbes: lo reportas como posible ampliación y esperas confirmación antes de tratarlo como átomo nuevo.

## 10.1 Build Gate (todo átomo Full)

`Requerimiento → Auditoría (Verifier) → Plan acotado → Implementación → Pruebas → Revisión del diff → Revisión independiente → Commit`

- Pruebas proporcionales: lint, typecheck, pruebas del área, build y, si hay migración, aplicarla en una base aislada y comprobar que coincide con el esquema.
- El diff no contiene refactors ni features no autorizados; los archivos ajenos se excluyen.
- Sin secretos ni datos reales indebidos en el diff **ni en el historial que se va a publicar**.
- La UI aparente tiene comportamiento real o está etiquetada como demo.
- SHA local = SHA remoto después del push, cuando haya push autorizado.

Si un paso no aplica, se registra `N/A` con razón. No se omite en silencio.

## 10.2 Revisión independiente y átomo N.1

Antes de declarar un Full como `Completado`, el Verifier revisa el diff y el comportamiento sin haber participado en la implementación. Si encuentra un problema material de integridad o seguridad, no se "arregla de pasada": se abre el átomo **N.1** con ese alcance y el átomo N no se aprueba hasta cerrarlo. (Registrar el nuevo átomo y su vínculo a la evidencia.)

## 10.3 Golden Path Gate (átomos críticos)

Un átomo es **crítico** si toca el Golden Path, dinero, permisos, datos del cliente o una integración externa. Antes de declararlo terminado:
1. reproduce el camino feliz de punta a punta;
2. prueba al menos un caso límite relevante;
3. prueba una regresión de lo que ya existía;
4. confirma que falla de forma segura cuando falta una dependencia;
5. si hay UI: al menos un viewport objetivo real y los estados loading, error y empty;
6. si hay acciones destructivas: permiso + vista previa del impacto + confirmación + auditoría;
7. si hay integración externa: idempotencia, reintento y fallo parcial cuando aplique.

**Ningún número de pruebas verdes sustituye este gate.** Un Golden Path roto bloquea el cierre aunque la suite completa pase. Si el Golden Path no pudo ejecutarse (por ejemplo, falta la base de datos), el átomo queda `Completado con reservas` y la reserva dice exactamente qué no se probó.

## 10.4 Release Gate (sólo al promover a un ambiente compartido)

`Promoción explícita → Respaldo verificable → Migración no destructiva (deploy, nunca reset ni push de esquema) → Deploy acotado al servicio → Health checks → Smoke → UAT si aplica → Actualizar checkpoint con DEPLOYED_SHA`

- Ningún agente pasa de implementación a producción en una sola acción sin autorización expresa.
- Si el acceso al ambiente está bloqueado, se detiene. No se abren puertos, no se cambia un firewall global, no se saltan controles.
- Cambios riesgosos de comportamiento entran detrás de una bandera **apagada por defecto**: apagarla es el rollback y se prueba.
- Un secreto que estuvo en el historial Git se trata como comprometido y se **rota**, aunque ya no esté en HEAD. No se reescribe la historia como sustituto de la rotación.

## 10.5 UAT como fuente de requerimientos

Cada hallazgo de UAT se clasifica antes de tocar código en tres dimensiones:
- **Tipo:** `BUG` (contradice comportamiento aprobado) · `REQ-REFINEMENT` (aclara un requisito) · `NEW-SCOPE` (funcionalidad nueva) · `UX` (fricción sin cambio de regla) · `DECISION` (requiere definición del cliente o de VLUX).
- **Estado contra el SHA:** `EXISTE` · `PARCIAL` · `NO_EXISTE`, con la causa comprobada cuando sea un bug.
- **Prioridad y complejidad:** P0 a P2; MEDIUM, HIGH o VERY_HIGH.

No conviertas todo comentario de reunión en bug ni absorbas `NEW-SCOPE` en el átomo actual. Los hallazgos se agrupan en olas (waves) con gates explícitos de desbloqueo.

## 10.6 Requerimientos cerrados

Un requerimiento cerrado con evidencia no se reabre sin evidencia. Si una regresión lo contradice, se abre un bug respaldado por una prueba; no se asume que nunca se implementó.

## 10.7 Registro de decisiones

Las decisiones pendientes del cliente se registran con identificador (`D-01`…), qué requerimiento habilitan, si bloquean desarrollo y quién responde. Cuando el volumen lo justifica, el cliente puede responderlas dentro del propio sistema con envíos numerados e inmutables y revisión de VLUX (patrón general: módulo de decisiones con trazabilidad). Mientras una decisión siga pendiente, no se implementa como requisito final.

---
