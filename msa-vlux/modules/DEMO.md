# MSA-VLUX V4 · Módulo DEMO

MSA_VERSION=4.0.0-rc3 · Módulo: DEMO · Se carga en: cualquier demo guiada
Depende del núcleo. §12 es texto de V3.2 sin cambios. Su claims ledger (§12.5) también lo usan PROPOSAL, EVOLUTION y PROSPECT-PAGE.

---

# 12. DEMO GUIADA CON VOZ

## 12.1 Cuándo aplica

La demo guiada es el entregable por defecto en **prospección y cierre comercial**: un recorrido interactivo, narrado y con subtítulos que el cliente ve sin que nadie explique pantallas. Se construye como átomo propio (`Átomo D — Demo guiada`), con nivel propuesto y confirmación. En mantenimiento o cambios Lite no es obligatoria.

Hay dos clases:

| Clase | Base | Regla de escenas |
|---|---|---|
| **Demo de prospección** | Prototipo con lógica real en memoria o simulación local fiel al alcance del Átomo 0 | Cada escena declara su nivel de honestidad (§12.4) |
| **Demo sobre sistema existente** | El sistema real con datos sintéticos | Sólo se habilitan escenas cuyo comportamiento está verificado; las demás quedan deshabilitadas y no se narran |

## 12.2 Patrones genéricos de referencia (sin sistemas ni clientes precargados)

- Demo con estado determinista: reloj controlado, IDs estables, casos reproducibles y navegación reversible.
- Matriz de honestidad: cada función se etiqueta como implementada, prototipo, simulada, propuesta o pendiente de integración.
- Escenas declarativas: guion, estado inicial, acciones, verificaciones y restauración al terminar.
- Narración opcional: subtítulos sincronizados, audio autorizado y accesibilidad; la demo sigue siendo usable sin sonido.
- Experiencia segura: sin escribir en datos reales, sin envíos comerciales ni cobros; primero fiabilidad y luego efectos visuales.

No se adjuntan repositorios, proyectos, clientes, productos ni recursos ajenos. Al iniciar un proyecto nuevo, las referencias se descubren a partir del contexto proporcionado por el usuario y con las autorizaciones necesarias.

## 12.3 Runtime de la demo

- Si el sistema ya tiene estado o eventos, la experiencia se conecta a ellos.
- Si la demo necesita estado propio, vive dentro de la demo y es **determinista**: ir a la escena *n* reinicia el estado y reproduce los pasos 0..n-1. Ninguna venta, envío o pago se duplica al navegar hacia atrás.
- Al salir se restaura el estado previo; "explorar libre" puede conservarlo de forma explícita.
- Sin audio sigue siendo entendible (subtítulos y temporizador de lectura); con `prefers-reduced-motion` sigue siendo usable.
- Nunca ejecuta mensajería, correo, cobros ni escrituras sobre datos reales.

## 12.4 Escenas y honestidad

Las escenas siguen el Golden Path, no las pantallas bonitas. Tipos útiles: `CONTEXT`, `ACTION`, `HANDOFF`, `CONTROL`, `EVIDENCE`, `VALUE`, `BOUNDARY`, `NEXT_STEP`.

Cada escena declara su nivel, visible en pantalla y dicho en la narración:
- **Funciona** (`VERIFIED_IMPLEMENTED` o `PROTOTYPE_LOGIC`): la lógica real corre.
- **Simulado** (`DEMO_ONLY`): interfaz con datos de demostración.
- **Propuesto** (`PROPOSED`).
- **Requiere integración** (`REQUIRES_INTEGRATION`).

Estructura por escena: `id`, `chapter`, `title` (una idea, máximo 8 palabras), `label` (`01 / VERBO`), `text` (narración de 35 a 60 palabras, 30 a 60 segundos), `takeaway`, `target`, `view`, `level`, `audioFile`, `voiceLabel`. El número de escenas lo dicta el Golden Path; como guía, de 5 a 10 en prospección y un recorrido de 4 a 10 minutos.

Arco narrativo: bienvenida con el nombre del cliente → el problema hoy → el flujo paso a paso con un caso concreto → la vista del dueño → el alcance (qué hace VLUX y qué se valida en el piloto) → el retorno con supuestos editables → el siguiente paso. La voz explica problema, decisión y resultado, no botones.

## 12.5 Claims ledger

Antes de narrar, registra cada afirmación importante:

| Claim | Nivel | Evidencia | Cómo se dice |
|---|---|---|---|
| "La venta aparece en la vista del dueño" | Funciona / Simulado | [fuente] | literal / "en este ejemplo" |
| "Se integra con X" | Propuesto / Requiere integración | [fuente] | "se valida en el piloto" |
| "Ahorra 20 %" | No permitido sin evidencia | — | escenario con supuestos editables |

El ROI es "un escenario para conversar, no una promesa de ahorro", con supuestos visibles y editables y un botón para capturar los números reales del cliente.

## 12.6 Voz: pipeline por etapas

VLUX estandariza **el proceso de aprobación de voz**, no un proveedor concreto. La voz pasa por estas etapas y **no salta ninguna**:

1. **Guion en borrador** en `narration.json` (`id`, `text`, `voice`).
2. **Placeholder etiquetado.** Voz del navegador o un TTS provisional/de bajo costo para ensayar ritmo y sincronía. El `voiceLabel` dice el motor real; no se llama "final".
3. **Aprobación humana del guion** por VLUX, registrada con nombre y fecha. No se gastan créditos de voz final antes de este punto.
4. **Selección de proveedor + presupuesto.** Evalúa calidad en español objetivo, naturalidad, alineación palabra-tiempo, costo/créditos, cuota disponible, privacidad/licencia y reproducibilidad. Compara proveedores o motores locales únicamente cuando la tarea lo requiera y estén disponibles. Si los créditos no alcanzan para todo el guion, se avisa antes de generar.
5. **Prueba corta de voz.** Genera 1–2 escenas representativas con la voz candidata y somételas a escucha humana. La aprobación de esta muestra valida la voz; el gasto del lote final requiere además su estimación de costo y una autorización explícita aparte (§3.3). Si la muestra no convence, cambia voz/proveedor sin desperdiciar todo el presupuesto.
6. **Generación final + QA técnico.** Genera los audios aprobados (`<id>-<voz>.mp3` o formato equivalente); cuando el motor lo permita, guarda alineación para anclar acciones y subtítulos a palabras. Verifica duración, archivos faltantes, reproducción, pausa/reanudación, concurrencia y que no queden audios huérfanos. Genera en tandas razonables según los límites del proveedor.
7. **Revisión auditiva humana final** de pronunciación, ritmo, pausas, naturalidad y coherencia escena a escena, registrada con nombre y fecha.

Reglas:
- La llave de la API vive en una variable de entorno, nunca se imprime ni se versiona. La demo final reproduce assets locales o un mecanismo aprobado; no expone llaves en el navegador.
- Si el entorno no tiene credenciales o presupuesto, entrega el guion y el placeholder listos y reporta exactamente qué falta. No inventes una voz final.
- Un respaldo automático en el reproductor (por ejemplo voz del navegador si falla el MP3) se permite si se etiqueta claramente como respaldo/placeholder.
- El `voiceLabel` siempre coincide con el motor/voz que realmente generó el archivo. Si no puedes verificarlo, es `UNKNOWN`.
- Una voz femenina y otra masculina pueden ofrecerse para comparar si aporta valor; **no se generan ambas por defecto**.

## 12.7 Reproductor y entregables

Botón "Demostrar demo", reproducción automática por escena, subtítulos, pausa, anterior y siguiente, capítulos, salir y explorar, selector de voz y silencio, control de velocidad, teclado (Esc cierra) y `prefers-reduced-motion`.

Entrega también `GUION_REUNION.md`: recorrido por minutos (como referencia: 12 a 18 minutos de reunión con 4 a 10 de demo), preguntas para el cliente y lista de **qué NO prometer**. La portada y el cierre llevan la marca del cliente y "VLUX" integrados según §9.7.

## 12.8 Gate DEMO-READY

Usa tres estados de madurez de la experiencia:

- `REHEARSAL_READY` — Golden Path y escenas funcionales, claims clasificados y placeholder permitido; sirve para ensayo interno, no para declararla voz final.
- `TECHNICAL_PASS · HUMAN_REVIEW_PENDING` — implementación y QA técnico completos, pero falta una aprobación humana obligatoria.
- `DEMO-READY` — todo lo técnico más las revisiones humanas exigidas están cerradas.

La demo no se declara `DEMO-READY` hasta que:
- el Golden Path visual funciona de inicio a fin;
- las escenas se pueden buscar y repetir sin efectos acumulados;
- los claims están clasificados y respaldados;
- no hay datos reales sensibles, secretos ni tokens en el frontend;
- audio final, subtítulos y spotlight están sincronizados;
- existen pausa, salto y salida;
- funciona sin audio y con movimiento reducido;
- el responsive objetivo fue revisado visualmente;
- si apunta a un sistema real, las acciones peligrosas están deshabilitadas o usan sandbox;
- existe `GUION_REUNION.md` con su lista de qué NO prometer;
- **el guion, la muestra de voz y la voz final tienen revisión humana registrada** (§12.6, etapas 3, 5 y 7).

Tú no puedes marcar la revisión humana: la registra una persona de VLUX. Una validación técnica del audio, por completa que sea, **no sustituye la escucha humana**.

---
