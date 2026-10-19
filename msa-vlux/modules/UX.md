# MSA-VLUX V4 · Módulo UX

MSA_VERSION=4.0.0-rc3 · Módulo: UX · Se carga en: dimensiones 3 y 4 de AUDIT, átomos `UX_IMPROVEMENT`, rol Experience
Depende del núcleo. La identidad visual de VLUX (§9.7) y el sistema visual de prospección (§16.3) siguen en sus módulos; este módulo audita y mejora aplicaciones existentes.

---

# 22. AUDITORÍA UX/UI PROFESIONAL

## 22.1 Principio

Se audita como un equipo senior de Product Design: tareas, evidencia y criterios verificables. "Más bonito" o "estilo Apple" no son hallazgos. La UX mejora **sin cambiar reglas de negocio**: si una mejora exige cambiar una regla, es `CHANGE_REQUEST` (§2.6), no UX.

## 22.2 Método

1. **Tareas críticas.** Lista las 3 a 7 tareas más usadas o más riesgosas, desde la operación del cliente (§8.1), uso medido o el Golden Path. Para cada una: actor, frecuencia (medida o declarada como supuesto), consecuencia de un error.
2. **Recorridos reproducibles.** Recorre cada tarea con datos sintéticos en el SHA y ambiente declarados. Con Playwright o navegador real cuando estén disponibles; si no, recorrido manual con capturas. Registra: pasos, cambios de pantalla, clics, campos, tiempo, errores y estados ambiguos. Sin herramienta para medir tiempo, se registra `TIME=NOT_MEASURED`.
3. **Inspección por criterio** (tabla §22.3), cada hallazgo con captura o paso reproducible.
4. **Separar funcional de visual.** Si la tarea falla o produce un dato incorrecto, es `BUG` (dimensión 2), aunque se haya visto en la interfaz. Si funciona pero cuesta, confunde o es inaccesible, es UX. Si sólo es inconsistencia estética, es visual (dimensión 4).
5. **Priorizar** con §22.4 y proponer cambios con criterio de aceptación verificable.
6. **Registrar** cada hallazgo UX con el formato de AUDIT §20.4. `EXPECTED` (criterio o heurística esperada, con su fuente: WCAG, §22.3, flujo aprobado) y `OBSERVED` (lo que se vio, con selector o archivo:línea y método) son **obligatorios también en UX**; una tabla resumen puede abreviar, pero cada fila remite a un hallazgo completo.

## 22.3 Criterios

| Criterio | Qué se verifica (ejemplos de evidencia) |
|---|---|
| Arquitectura de información | ¿Las secciones corresponden a cómo trabaja el cliente? Nombres que el usuario reconoce; profundidad de navegación medida |
| Navegación | ¿Se llega a la tarea crítica en pocos pasos? ¿Hay retorno y ubicación clara? |
| Jerarquía visual | ¿La acción principal domina? ¿Una sola acción primaria por vista? |
| Formularios | Etiquetas, validación en línea, mensajes específicos, valores por defecto, orden lógico, no perder datos al fallar |
| Tablas y dashboards | Orden, filtros, densidad, números alineados (`tabular-nums`), totales verificables, estado de carga |
| Feedback del sistema | Cada acción muestra estado (cargando, éxito, error); doble envío prevenido |
| Estados vacíos | Explican qué falta y cómo empezar; no parecen errores |
| Estados de error | Dicen qué pasó y qué hacer; no exponen detalles técnicos ni datos |
| Accesibilidad | Contraste WCAG 2.1 AA, foco visible, navegación por teclado, etiquetas accesibles, `prefers-reduced-motion`; axe u otra herramienta cuando exista |
| Responsive | Viewports objetivo reales (al menos los que el cliente usa); sin scroll horizontal |
| Consistencia | Mismos componentes para lo mismo; tokens de color/tipografía/espaciado |
| Densidad de información | Adecuada al usuario experto u ocasional; no esconder datos necesarios |
| Prevención de errores | Confirmaciones proporcionales, deshacer, impacto antes de acciones destructivas (§10.3 punto 6) |
| Descubribilidad | ¿Las funciones existentes se encuentran sin manual? |
| Rendimiento percibido | Tiempo hasta interacción, esqueletos de carga, respuesta inmediata al clic (medido o `NOT_MEASURED`) |
| Eficiencia de tareas | Pasos, tiempo y errores por tarea crítica, antes y después |
| Honestidad de la interfaz | Sin botones decorativos ni CTAs falsos (§9.6) |

## 22.4 Priorización

Para cada hallazgo UX con evidencia reproducible:

```text
UX_SCORE = (IMPACT × FREQUENCY × RISK) / EFFORT
IMPACT    1–5  (cuánto empeora la tarea para el usuario)
FREQUENCY 1–5  (qué tan seguido ocurre; medido o supuesto declarado)
RISK      1–3  (1 = molestia, 2 = retrabajo o dato erróneo recuperable, 3 = error costoso o irreversible)
EFFORT    1–5  (estimación de VLUX)
```

- Cada factor declara si es **medido** o **supuesto**. Un score con supuestos se rotula `UX_SCORE (supuestos)`.
- El resultado obligatorio es el **Top 5**: los cinco cambios con mayor score cuyo beneficio se puede **comprobar** con un criterio antes/después (pasos, tiempo, errores, contraste, accesibilidad). Un cambio sin criterio comprobable no entra al Top 5.
- Desempate: primero lo que reduce riesgo 3, luego lo que toca el Golden Path.

## 22.5 Propuesta de mejora

Cada mejora: hallazgo(s) que resuelve, cambio concreto (no "rediseñar"), lo que **no** cambia (reglas, datos, permisos), criterio de aceptación medible y cómo se verificará (prueba E2E, recorrido, axe, captura en viewports). Se ejecuta como átomo: Lite si es aislado, Full si cambia flujo, permisos o puede inducir una acción destructiva (§4.1).

## 22.6 Diseño visual y sistema de diseño (dimensión 4)

Inventario de componentes y tokens existentes; inconsistencias con captura; propuesta de tokens y componentes mínimos. La marca del cliente es la principal; VLUX aparece según §9.7. Las piezas de motion siguen el principio "la experiencia observa, no controla".
