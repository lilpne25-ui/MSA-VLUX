# MSA-VLUX V4 · Módulo PROSPECT-PAGE

MSA_VERSION=4.0.0-rc3 · Módulo: PROSPECT-PAGE · Se carga en: Átomo P
Depende del núcleo. §16 es texto de V3.2 sin cambios.

---

# 16. PÁGINA DE PROSPECCIÓN (Átomo P)

Una página de una sola vista que hace que el prospecto **quiera una llamada de diagnóstico**. No vende, no cotiza y no promete. Se usa antes del Átomo 0 completo o en paralelo con él, cuando la relación empieza por un referido o un primer contacto.

Se construye como átomo propio (`Átomo P`), nivel **Lite** salvo que capture datos del prospecto (formulario con envío real), en cuyo caso es **Full**.

## 16.1 Entradas obligatorias antes de diseñar

- Investigación pública del prospecto (§8.1) con cada dato etiquetado (§2.4).
- Referente, si existe: nombre exacto como lo quiere escrito y su permiso para ser mencionado.
- Nombre de quien firma por VLUX y canal de contacto real (número de WhatsApp, correo).
- Logos VLUX desde Drive, carpeta "LOGOS VLUX" (§9.7).
- Logo y colores del cliente, si existen.

Si falta el contacto real, el botón queda deshabilitado (§9.6). Nunca se inventa un número.

## 16.2 Contenido: estructura fija

En este orden. Cada bloque responde a una pregunta del prospecto.

| Bloque | Pregunta que responde | Regla |
|---|---|---|
| 1. Titular | ¿Esto es para mí? | Habla de su operación con sus palabras ("Acero a medida. Sin vueltas."). Nombra al prospecto en una línea pequeña arriba |
| 2. Demostración visual del oficio | ¿Entienden mi negocio? | Una animación con un objeto real del giro del cliente que cuenta lo que hacemos en 3 segundos (§16.4) |
| 3. "¿Les pasa?" | ¿Tienen ese problema? | 5 o 6 situaciones típicas **del giro**, nunca afirmadas sobre el cliente: "No sabemos si aplican a [cliente]". Interruptores que el prospecto activa |
| 4. Antes / después | ¿Cómo se vería mejor? | Un caso con datos inventados y declarados como ejemplo ilustrativo. El después deja la decisión en manos del cliente |
| 5. Herramienta útil pequeña | ¿Me sirve desde ya? | Algo que funcione de verdad y le ahorre un cálculo (calculadora de peso, de tiempos, de costos sin precios). Con nota de "valores típicos de referencia" |
| 6. Qué hace VLUX | ¿Quiénes son? | Tres verbos (Entender, Construir, Automatizar), cada uno con un ejemplo. Cierre: "Son ejemplos de lo posible…" |
| 7. Cómo empezamos | ¿Qué me piden? | Tres pasos: llamada de 30 min, resumen escrito, ellos deciden |
| 8. Cierre | ¿Cómo los contacto? | Referente, "¿Platicamos 30 minutos?", "Sin precios y sin compromiso", WhatsApp con mensaje prellenado y botón para copiar el número |

**Prohibido en la página:** precios, plazos, ROI o porcentajes de ahorro, nombres de otros clientes (§8.4), integraciones presentadas como existentes, reseñas o datos de directorios no verificados, el prototipo o sistema si ya se construyó algo (eso convierte la llamada en venta).

Antes de publicar, el Verifier revisa el claims ledger (§12.5) de la página: cada afirmación con nivel y fuente.

## 16.3 Sistema visual VLUX: "luz sobre acero"

La identidad de VLUX es una V de vidrio con el filo iluminado en cian sobre azul noche, logotipo geométrico muy espaciado y, en su versión horizontal, una placa de acero cepillado.

**Tokens base (no cambiar sin decisión registrada):**

```css
--noche:#04080f;      /* fondo */
--superficie:#0c131c; /* tarjetas y paneles */
--texto:#c9d4dd;
--titular:#f2f7f9;
--tenue:#7f8e9c;
--luz:#5fd0e8;        /* cian VLUX: SÓLO como luz */
--sans:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI Variable Display","Segoe UI",Roboto,sans-serif;
```

**Reglas:**
- Un solo mundo oscuro, declarado con `color-scheme: dark`.
- El cian **sólo** es luz: filos, resplandor, indicadores encendidos, el anillo de un medidor. Nunca bloques de color ni fondos planos. El único botón con fondo cian es la acción principal del cierre.
- El material del cliente entra en la página. Si el cliente trabaja con acero, madera, comida o ropa, la textura y los objetos de la página salen de ese material, iluminados con la luz de VLUX.
- La marca principal es la del cliente. VLUX va en la barra superior, en el cierre y en el pie, discreto.

**Logos (§9.7 aplicado):**
- No usar los JPG con fondo ni el ícono de app con marco cuadrado.
- Extraer la V y el logotipo del logo principal convirtiendo luminancia en transparencia (PIL: alfa = brillo máximo por píxel menos un umbral de ~28–40), recortar al contenido y revisar sobre fondo oscuro antes de usarlo.
- Insertarlos en la página como `data:` URI para que la página sea un solo archivo.

**Tipografía (estilo Apple):**
- Fuente del sistema (SF Pro en Apple, Segoe en Windows).
- Tracking negativo que crece con el tamaño: titular principal `-0.045em`, titulares de sección `-0.035em`, cuerpo cercano a `0`.
- Interlineado corto en titulares grandes (1.02–1.06) y cómodo en cuerpo (1.55).
- Jerarquía por peso + tamaño + color, no sólo por tamaño.
- Números con `font-variant-numeric: tabular-nums`.

## 16.4 Movimiento (estilo Apple)

Principio: el movimiento explica, no decora. Un solo momento memorable arriba; todo lo demás responde a lo que hace la persona.

**Obligatorio:**
- **Resortes** para todo lo que la persona toca o que cambia de valor. Implementar con damping y response, como iOS: `ω = 2π / response`, `k = ω²`, `c = 2·damping·ω`. Por defecto `damping 1.0, response 0.35–0.5`. Con rebote (`damping ~0.8`) sólo cuando hay inercia (algo se separa, se lanza o se suelta).
- **Interrumpible:** cada animación parte del valor actual en pantalla, nunca del valor objetivo.
- **Respuesta en el toque:** botones con `:active { transform: scale(.96–.97) }` en 100 ms.
- **`prefers-reduced-motion`:** mostrar el estado final con un fundido; sin láser, sin chispas, sin scroll ligado.
- **`prefers-reduced-transparency`:** barra superior sólida.

**Repertorio probado (usar los que apliquen):**

| Componente | Comportamiento |
|---|---|
| Barra superior translúcida | `backdrop-filter: saturate(180%) blur(20px)`, sombra difusa sólo cuando hay scroll |
| Demostración del oficio (hero) | Ejemplo Pibasa: una solera completa que una línea de luz corta en 4 piezas con chispas; los trozos se separan con resorte y los contadores cambian (1 → 4 piezas, 1,200 → 300 mm, 11.92 kg). Se dispara al entrar en pantalla y tiene botón "Volver a cortar" |
| Frase que se enciende | Un titular de sección cuyas palabras pasan de 18 % a 100 % de opacidad con el scroll |
| Interruptores iOS | Perilla que se estira al presionar y se desliza con curva de rebote; alimentan un anillo medidor animado con resorte |
| Control segmentado | Indicador que se desliza con resorte (`damping .85`) |
| Antes / después | El "antes" reproduce un chat con burbujas y "escribiendo…"; el "después" arma una orden campo por campo hasta el folio |
| Calculadora | Botones − / + que repiten al mantener presionados, total que cuenta con resorte, dibujo de la pieza a escala que se transforma con resortes |
| Ruta de pasos | Línea de luz que se llena con el scroll y enciende cada paso |
| Avisos | Toast translúcido abajo ("Número copiado") |

**Lo que no se hace:** entradas de fundido-y-subida en cada sección, animaciones infinitas decorativas, objetos 3D que deformen el logo, efectos sin relación con el oficio del cliente.

## 16.5 Implementación

- **Un solo archivo HTML** con CSS y JS en línea, sin dependencias ni CDN de librerías. Logos como `data:` URI.
- `<meta charset="utf-8">`, `<meta name="viewport" … viewport-fit=cover>` y `<meta name="robots" content="noindex, nofollow">`.
- Reset mínimo: `html,body{margin:0}`, `[hidden]{display:none!important}`, `img{max-width:100%}`. (Sin la regla de `hidden`, un `display:grid` propio la anula.)
- WhatsApp: `https://wa.me/52XXXXXXXXXX?text=<mensaje codificado>` con `target="_blank" rel="noopener"`, más un botón "Copiar número" con respaldo de selección si el portapapeles falla.
- Formularios: no se envían a ningún lado salvo que el átomo sea Full y exista un destino real autorizado.
- Responsive hasta 375 px de ancho, sin scroll horizontal. Foco de teclado visible en todos los controles.

## 16.6 QA antes de publicar

El átomo P no se cierra sin estas comprobaciones, hechas en un navegador real con capturas:

- [ ] Portada, demostración del oficio, cada sección y cierre en escritorio (1280 px) y en teléfono (375 px).
- [ ] Cada componente interactivo probado: interruptores y medidor, control segmentado, calculadora en todas sus formas, botón de repetir, WhatsApp, copiar número.
- [ ] Números de la herramienta verificados a mano con un caso conocido (Pibasa: solera D2 12.7 × 101.6 × 300 mm, 4 piezas = 11.92 kg).
- [ ] Acentos y caracteres especiales correctos (si se ven como `Ã¡`, falta el `meta charset`).
- [ ] Movimiento reducido: la página se entiende y funciona.
- [ ] Consola sin errores.
- [ ] Claims ledger revisado por el Verifier; ningún dato sin fuente ni promesa.
- [ ] Nombres de personas escritos exactamente como los dio el usuario.

Errores encontrados en la primera página y cómo evitarlos:

| Error | Causa | Evitarlo |
|---|---|---|
| Logo deformado | Ponerlo sobre una cara 3D en perspectiva | Logos siempre de frente |
| "Caja de zapatos" | Objeto 3D plano, sin luz ni relación con el mensaje | La demostración del oficio cuenta algo; el material lleva brillo y reflejo |
| Logo de cabeza tras girar | Acomodo a 180° | Acomodar en vueltas completas o no girar |
| Uniones visibles entre trozos | Varios elementos juntos simulando uno | Una pieza continua encima que desaparece en el primer corte |
| Fila oculta que sigue visible | `display` propio anula `hidden` | Regla global `[hidden]{display:none!important}` |

## 16.7 Publicación

- Primero como artifact privado para revisión de VLUX.
- **Revisión humana** del diseño y del texto por una persona de VLUX, registrada con nombre y fecha (igual que §12.8: el agente no la marca).
- Despliegue en Vercel **sólo con autorización explícita** (§3.3): carpeta con el `index.html` y un `vercel.json` con `X-Robots-Tag: noindex, nofollow`; `vercel deploy --prod --name <vlux>-<cliente>`. Verificar que el dominio público responde 200 sin pedir sesión y revisarlo en el navegador.
- Registrar en `MSA-ATOMOS.md` la URL publicada, la fecha y el SHA o versión del archivo.
- Antes de enviar el enlace: confirmar que ningún repositorio público del proyecto contradiga la página (prototipos con marca del cliente, precios o plazos). Si existe, pasarlo a privado con autorización.
- Cualquier cambio posterior a la página exige volver a desplegar; el artifact y Vercel no se sincronizan solos.

## 16.8 Kit que acompaña a la página

Junto con la página se entregan, como material interno que nunca se comparte con el prospecto:
- Mensaje para que el referente lo reenvíe y una variante para que VLUX escriba directo.
- Guía de llamada de 30 minutos: agenda por minutos, 12–15 preguntas de diagnóstico por proceso, señales a favor y en contra, qué no prometer y cierre sin presión.
- Lista de datos por confirmar con el referente y el prospecto.
