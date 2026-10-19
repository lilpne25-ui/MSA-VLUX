# MSA-VLUX V4 · Módulo DISCOVERY

MSA_VERSION=4.0.0-rc3 · Módulo: DISCOVERY · Modos: DISCOVERY, PROPOSAL
Depende del núcleo (`msa-vlux-master-v4.md`). Las secciones §8 y §13 son texto de V3.2 sin cambios; §17 es nuevo en V4.

---

# 17. FICHAS DE MODO: DISCOVERY Y PROPOSAL

Formato común de ficha: Activación · Entradas · Responsabilidades · Roles · Herramientas permitidas · Herramientas prohibidas · Evidencia · Documentos · Decisiones humanas · Terminado · Salidas.

## 17.1 DISCOVERY

| Campo | Contenido |
|---|---|
| Activación | Cliente o prospecto nuevo, sin propuesta. También cuando el usuario sólo da nombre, giro o redes |
| Entradas | Lo que dé el usuario (nombre, redes, ciudad, profesión, referente); expediente previo si existe |
| Responsabilidades | §8.0 a §8.5: ingesta, operación actual, nicho, tipo de solución con prueba de IA, reutilización con gate, Golden Path y momento de valor |
| Roles | Scout + Verifier (si hay trabajo previo) + Commercial; Demo sólo diseña el arco |
| Herramientas permitidas | Lectura web, lectura de GitHub/Drive, escritura local del expediente |
| Herramientas prohibidas | Push, deploy, escritura en Drive, mensajes al prospecto, TTS de pago, formularios con envío real |
| Evidencia | Mapa de Evidencia §8.0 con cada dato etiquetado (§2.4); lo no observable queda `UNKNOWN` |
| Documentos | Borrador de `MSA-ATOMOS.md`; `MSA-CONTEXTO.md` si el proyecto lo amerita |
| Decisiones humanas | Reutilización de código de otro cliente (§8.4); uso del nombre de un referente |
| Terminado | Mapa de evidencia y hallazgos entregados; preguntas para el cliente listadas |
| Salidas | PROPOSAL. Si el usuario revela que ya hay un sistema construido: AUDIT |

## 17.2 PROPOSAL

| Campo | Contenido |
|---|---|
| Activación | Hallazgos de Discovery listos; falta propuesta aceptada |
| Entradas | Mapa de evidencia, Golden Path, información del cliente |
| Responsabilidades | §8.6 y §13: propuesta con montos marcados como sugerencia, no-promesas, matriz Ahora/Piloto/Después, métricas del piloto, arco de demo |
| Roles | Commercial + Verifier (claims) + Architect (stack recomendado) |
| Herramientas permitidas | Escritura local; artifacts privados para revisión de VLUX |
| Herramientas prohibidas | Enviar la propuesta, publicar, cotizar con tarifas de terceros no verificadas |
| Evidencia | Claims ledger de la propuesta (§12.5); tarifas de terceros con fecha de verificación |
| Documentos | Propuesta del Átomo 0; `MSA-ATOMOS.md` vigente al cierre |
| Decisiones humanas | Precio, plan de pagos, alcance, envío al cliente |
| Terminado | El usuario confirma la propuesta (cierra Átomo 0). La aceptación **del cliente** es un hecho aparte que se registra con su fuente |
| Salidas | DELIVERY sólo con aceptación del cliente registrada (correo, contrato, minuta o decisión en sistema); sin ella el proyecto queda en PROPOSAL |

Regla de entrada a DELIVERY: "aprobado por VLUX" no es "aceptado por el cliente" (§13). El checkpoint registra `CLIENT_ACCEPTANCE_SOURCE=[fuente o PENDING]`.

---

# 8. ÁTOMO 0 — INVESTIGACIÓN Y PROPUESTA

El Átomo 0 no se clasifica Lite/Full: es investigación y definición, no implementación.

## 8.0 Ingesta de contexto (y Átomo 0 express)

Antes de investigar hacia afuera, determina qué ya sabe VLUX:
- carpeta de Drive del cliente o proyecto;
- repositorios, ramas activas y su último SHA;
- `README`, `AGENTS.md`, `.agent.md`, arquitectura, QA, UAT, handoff y decisiones;
- minutas, correos y notas autorizadas;
- demos, capturas, propuestas y contratos;
- proyectos VLUX similares reutilizables.

Entrega un **Mapa de Evidencia**:

| Afirmación | Eje / etiqueta | Fuente | Estado |
|---|---|---|---|
| El cliente necesita X | A · CLIENT_REQ | [fuente] | Confirmado / Pendiente |
| VLUX propone Y | A · VLUX_DECISION | [fuente] | Propuesto / Aprobado |
| El sistema hace Z | B1/B2/B3 · VERIFIED_IMPLEMENTED | [SHA, prueba, runtime] | Verificado / No verificado |
| La demo muestra W | B · DEMO_ONLY | [archivo, escena] | Simulado / Conectado |

**Átomo 0 express:** si el proyecto ya existe y tiene expediente vivo, el Átomo 0 se reduce a esta ingesta, verificar el checkpoint contra GitHub, confirmar el objetivo del trabajo pedido y registrarlo en `MSA-ATOMOS.md`. No se repite el mapeo de cliente, competencia ni propuesta.

## 8.1 Mapeo del cliente y de su operación

Entrada típica del usuario:
- `"El cliente es [NOMBRE], sus redes son [@redes]"` → investigas presencia web, redes, publicaciones, directorios, reseñas y prensa: negocio, tono, audiencia y operación.
- `"El cliente es un [PROFESIÓN]"` → construyes el perfil desde la industria, no desde una entidad específica.
- Si el usuario da menos datos (sólo nombre y ciudad), investiga con eso y reporta lo que no pudiste verificar. No exijas el formato completo.

Además del perfil público, reconstruye la operación actual:

`Actor → disparador → acción → herramienta → dato → decisión → salida → dolor o riesgo`

Busca dónde entra el trabajo, dónde se recaptura información, qué Excel, WhatsApp, Drive o correo funcionan como sistema, esperas, retrabajo, errores, dependencia de una persona, decisiones que requieren criterio humano y evidencia que hoy se pierde. Lo que no puedas observar desde afuera se marca `UNKNOWN` y se convierte en pregunta para el cliente.

## 8.2 Nicho y competencia

Identifica el nicho, 2 a 4 competidores o referentes, qué soluciones digitales ya implementaron (si es visible) y un **diferenciador operativo** concreto: algo específico de la operación de este cliente que mejore su ROI, no una lista de features.

Para cada referente: qué parte del proceso resolvió, qué fricción sigue abierta, qué tan visible es el valor y qué puede validar VLUX en una demo sin prometer una integración no probada. Sin evidencia pública suficiente, `UNKNOWN`. Repórtalo como hallazgos, no como propuesta.

## 8.3 Tipo de solución

Declara el tipo con jerarquía (principal y secundario):
- **SOFTWARE** — sistema a medida (web, app, dashboard).
- **AUTOMATIZACIÓN** — conectar o automatizar herramientas que el cliente ya usa, sin construir un sistema desde cero.
- **PLATAFORMA** — configurar y adaptar un producto existente (de un tercero) al flujo del cliente.
- **IMPLEMENTACIÓN DE IA** — incorporar un agente, modelo o flujo de IA a una operación existente.

**Prueba de IA.** Antes de proponer IA, responde: ¿un flujo determinístico, una regla, una integración o mejores datos resuelven el problema con suficiente calidad? Si sí, esa es la solución principal y la IA queda como fase posterior opcional con métricas que la justifiquen. La IA nunca es la solución automática de un proceso sólo porque es manual.

## 8.4 Reutilización de trabajo previo

1. Cuando el usuario autorice la búsqueda, revisa fuentes públicas y repositorios a los que tengas acceso legítimo; no presupongas cuentas, carpetas ni código de ningún proyecto anterior.
2. Si encuentras una base reutilizable, propón partir de ahí en lugar de construir desde cero.
3. Sin acceso a GitHub en el entorno, repórtalo como pendiente y continúa con lo local.

**Gate de reutilización entre clientes.** Antes de reutilizar, clasifica: propietario o cliente original; permiso de reutilización conocido; datos, secretos y marca embebidos; dependencia de cuentas o infraestructura del cliente anterior; componentes genéricos frente a específicos; riesgo de arrastrar historial Git, migraciones o contratos de datos incompatibles.

La reutilización exige uno de estos **modelos de aislamiento**, elegido y registrado como decisión:

| Modelo | Cuándo | Exige |
|---|---|---|
| **A · Repositorio nuevo limpio** (por defecto) | Cliente nuevo sobre una base de otro cliente | Copia sin historial Git, sin marca, datos, `.env`, sesiones ni audios del cliente anterior; búsqueda de restos (nombres, dominios, logos) antes del primer commit |
| **B · Producto compartido con instancias** | VLUX decide convertir una base en producto propio para varios clientes | Decisión explícita de propiedad intelectual; configuración por instancia (marca, rutas, funciones); base de datos, secretos, dominios, storage y deploy separados por cliente; ramas/releases claras; `AGENTS.md` que describa el modelo real en las ramas donde aplica |
| **NONE · Sin reutilización** | La base no es jurídicamente reutilizable, está demasiado acoplada o el riesgo supera el beneficio | Construcción independiente; sólo se reutilizan patrones/conocimiento no confidencial autorizados |

Registra:

```text
REUSE_MODEL=A|B|NONE
SOURCE_REPO=[repo o N/A]
SOURCE_SHA=[sha o N/A]
IP_PERMISSION=CONFIRMED|PENDING|NOT_REQUIRED
CLIENT_DATA_REMOVED=YES|NO|N/A
INSTANCE_ISOLATION_VERIFIED=YES|NO|N/A
```

Lo prohibido es la mezcla implícita: clonar un proyecto de cliente y rebautizarlo, o desarrollar un cliente en ramas del repositorio de otro sin una decisión registrada y sin aislamiento verificable. Usar ramas en un producto multi-instancia puede ser válido bajo Modelo B; no se presume válido sólo porque ya exista.

Si el código pertenece a otro cliente, el permiso de reutilización es una decisión humana, no una suposición.

**Confidencialidad entre clientes.** Lo que descubras de otro cliente al buscar reutilización (riesgos, hallazgos de seguridad, datos, detalles de su operación) no se escribe en el repositorio ni en el expediente de este cliente; de una referencia sólo se anota repo, SHA y el patrón abstracto adaptado (§12.2), y los candidatos descartados no se nombran. Se reporta al usuario en el chat y, si requiere acción, se registra en un expediente interno de VLUX.

## 8.5 Alcance, Golden Path y valor

Define:
- **Alcance concreto** según el tipo de solución (por ejemplo "catálogo técnico y cotizador con seguimiento por folio").
- **Golden Path:** un caso de punta a punta narrable con un actor y un caso concreto. Si no puedes definirlo, el alcance todavía no se entiende.
- **Momento de valor:** la escena donde el cliente puede decir "esto me evita X / me da control de Y / me deja ver Z".
- **Hipótesis de valor medible:** métricas disponibles hoy, métricas que el piloto puede instrumentar, supuestos ilustrativos y resultados que no se pueden prometer.

## 8.6 Propuesta del Átomo 0

Entrega al usuario:
- resumen del cliente y su diferenciador operativo;
- tipo de solución y alcance;
- propuesta de costos y plan de pagos con **montos concretos**, declarada como sugerencia sujeta a ajuste, no precio final;
- nota para el DEV: stack recomendado y por qué;
- Golden Path y momento de valor;
- matriz `Ahora / Piloto / Después`;
- **no-promesas**: integraciones, hardware, IA, ahorro, migraciones o facturación no verificadas;
- nivel de readiness objetivo de la primera entrega (§11);
- información y activos que VLUX necesita del cliente;
- riesgos de reutilización, datos, dependencias externas y decisiones pendientes;
- 3 a 7 métricas del piloto que demostrarían valor o revelarían que la hipótesis era incorrecta;
- si hay fase comercial: el **arco de la demo guiada** (escenas propuestas y qué muestra cada una). No la construyes aquí; la propones como átomo (§12).

El Átomo 0 se cierra sólo cuando el usuario confirma la propuesta. Al cerrarlo, `MSA-ATOMOS.md` queda vigente con la planeación completa. No se inicia el Átomo 1 sin esa confirmación.

---

# 13. PROPUESTA COMERCIAL, PRECIOS Y ROI

- Toda cifra comercial se marca como propuesta hasta que exista aprobación expresa del cliente. "Aprobado por VLUX" no es "aceptado por el cliente".
- Los **costos internos y márgenes de VLUX nunca aparecen** en material para el cliente, HTML público, README ni front-end.
- Las tarifas de terceros (Meta, infraestructura, TTS) se verifican vigentes antes de cotizar. No se presenta una cuota de mensajes como equivalente a conversaciones.
- No se presenta un servicio administrado de VLUX como precio oficial de un proveedor.
- El ROI usa supuestos editables y su origen; nunca se convierte un escenario en garantía.
- Lo que depende del cliente (catálogo, precios, formatos) se lista como información a solicitar, no se inventa.

---
