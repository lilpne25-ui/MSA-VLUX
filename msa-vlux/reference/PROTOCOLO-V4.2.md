# MSA-VLUX V4.2 — orquestación, revisión y continuidad entre entornos

**Acumulativa sobre V4.1.** En cada inicio se cargan `PROTOCOLO-V4.1.md` y este documento; V4.0.0-rc3 sigue siendo la metodología fuente. Sólo se lee el módulo específico de la tarea, por carga progresiva.

## Separación de responsabilidades

- Maestro: coordina el único átomo activo, sin afirmar revisiones ajenas que no han ocurrido.
- Scout: inventario de fuentes y estado, sin inferir requerimientos.
- Architect: opciones y trade-offs, solo recomendaciones.
- Security: amenazas, permisos y pruebas negativas.
- Verifier: intenta refutar conclusiones mediante evidencias y contraejemplos.
- Experience: UX y accesibilidad cuando aplica.
- Operations: despliegue, backup, rollback y observabilidad.
- Commercial: alcance, costo y base comercial verificados, sin inventar contratos.
- Demo: fidelidad de la demostración al producto real.

Una revisión independiente exige **otro proceso/contexto con separación efectiva**, identidad de ejecución, mismo SHA y evidencia de la revisión. Si solo existen lentes conceptuales, marcar `NOT_INDEPENDENT`.

## Handoff explícito

Un entorno efímero pierde el directorio. Se debe **crear y entregar** el archivo de handoff antes de abandonar la sesión, guardarlo en almacenamiento privado elegido por el usuario y verificar SHA-256. El sistema no tiene sincronización automática ni custodia perpetua.

```bash
python scripts/msa.py handoff --project-dir PROYECTO --runtime codex --output traspaso.zip
python scripts/msa.py verify-handoff --archive traspaso.zip
python scripts/msa.py import-handoff --archive traspaso.zip --target DIRECTORIO_NUEVO
python scripts/msa.py resume --project-dir DIRECTORIO_NUEVO
```

El handoff contiene `state.json`, `history.jsonl` y manifiesto, con integridad y consistencia validadas. **No incluye repositorio, diffs, base de datos, archivos sueltos, resultados binarios, secretos ni historial de conversación.** Para preservar informes de trabajo aprobados, agregarlos individualmente con `--include docs/informe.md` (máximo 20; texto UTF-8 bajo el proyecto). La importación coloca esos archivos en `.msa/imported-evidence/`, sin sobrescribir contenido. La revisión de privacidad corresponde al responsable del proyecto.

**La autorización externa se revoca siempre al transferir**: el nuevo runtime debe obtener consentimiento específico y verificar el SHA/línea base antes de operar. Las funciones del CLI no ejecutan acciones remotas.

## Secuencia para una sesión nueva

1. Verificar integridad del paquete y el manifiesto externo SHA-256 obtenido por canal confiable.
2. Importar en proyecto separado; nunca sobrescribir `.msa` existente.
3. `resume`, `verify-ledger`, `status`. Reportar última decisión, átomo activo, baseline y vacíos.
4. Recuperar las fuentes reales y comparar repositorio/commit; no asumir que la información guardada sigue vigente.
5. Ejecutar pruebas pendientes. Las evidencias transportadas no acreditan el estado del entorno nuevo.
6. Solicitar de nuevo las autorizaciones externas. Solo entonces continuar.

## Límites de integridad y privacidad

Los SHA-256 detectan corrupción accidental sin autenticación del emisor. Quien pueda reemplazar ZIP y manifiesto puede falsificar ambos: verificar huella original por canal independiente, controles de acceso o firma externa del anfitrión. El filtro de secretos es conservador e incompleto; no sustituye revisión humana, DLP ni cifrado del almacenamiento privado. Nunca enviar el paquete a destinos públicos por defecto.

## Revisión delegada estructurada

`role-packet` crea un paquete sin código ni secretos, ligado al átomo y baseline SHA; `check-review` comprueba su respuesta y detecta auto-revisiones obvias, discrepancias de SHA y campos faltantes. **No lanza subagentes de forma automática**: eso depende del anfitrión. Consultar `roles/ROLES-Y-REVISION.md` para la secuencia reproducible.
