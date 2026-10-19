# MSA-VLUX — versión autónoma de metodología para Codex y Claude

**Es una skill, no un modelo entrenado, servidor, memoria automática ni infraestructura de seguridad.** No carga contexto de ninguna aplicación, organización, cliente o repositorio. Mantiene la metodología de MSA-VLUX V4.0.0-rc3 y sus 12 módulos, con sucesivas capacidades ejecutables.

## Instalación

Extraer el ZIP conservando la carpeta raíz `msa-vlux` y el archivo `SKILL.md`.

- Codex local: agregar la carpeta al directorio de skills que use tu instalación (por ejemplo `~/.agents/skills/msa-vlux/` o la carpeta de skills del proyecto) y reiniciar la sesión.
- Claude Code local: colocarla en `~/.claude/skills/msa-vlux/` o `.claude/skills/msa-vlux/` si el entorno lo admite.
- Claude Cloud/chat: adjuntar el ZIP o archivos en una sesión que pueda leerlos y ejecutar scripts, o configurar la skill en el entorno que facilite el proveedor. Un ZIP adjunto **no implica** instalación persistente ni ejecución de Python en ese servicio.

Para leer el comportamiento disponible: `python scripts/msa.py doctor`. El runtime requiere Python 3.9+ (se recomienda 3.10+), bibliotecas estándar. No instala dependencias ni hace solicitudes de red.

## Comprobación inmediata

```bash
python scripts/msa.py doctor
python scripts/msa.py verify-package
python -m unittest discover -s tests -v
python scripts/msa.py eval --traces evals/traces-pass.json
python scripts/msa.py eval --traces evals/traces-fail.json
```

**Esperado:** la segunda evaluación adversarial termina con **exit 1**. Sus fallos son intencionales y prueban que la verificación detecta conductas claramente prohibidas en trazas sintéticas. No prueba por sí mismo que un agente real obedezca.

## Primer proyecto ficticio

```bash
python scripts/msa.py init --project-dir ./laboratorio --name "Ensayo sintético"
python scripts/msa.py set-atom --project-dir ./laboratorio --id A0 --mode AUDIT --status in_progress --baseline-sha abc123
python scripts/msa.py record --project-dir ./laboratorio --type evidence --data-file templates/EVIDENCE-EVENT.json
python scripts/msa.py verify-ledger --project-dir ./laboratorio
python scripts/msa.py assess --project-dir ./laboratorio --input templates/SELF-ASSESSMENT.json
```

Los comandos trabajan sobre **`--project-dir/.msa`** y no sobre repositorios remotos. Antes de hacer pruebas usa un directorio seguro sin datos productivos.

## Distribuciones progresivas

- **V4.1:** autoevaluación, tests adversariales, historial con hashes, gates deny-by-default informativos.
- **V4.2:** V4.1 + roles y revisión delegada estructurada (`role-packet`/`check-review`) y handoff explícito entre entornos con importación y restauración verificadas.
- **V5.0:** V4.2 + comparación métrica con holdout, bloqueo de regresiones y propuestas revisables; sin autoedición.

## Precauciones

- Los hashes de datos son de **integridad, no autenticidad**. Comparar la huella entregada por un canal de confianza.
- Las herramientas no reemplazan control de GitHub, política OS, sandbox, credenciales mínimas ni autorizaciones de quien usa la herramienta.
- Los informes en zip no deben guardarse en sitios públicos; un escáner básico de secretos no garantiza privacidad de datos personales.
- En entornos efímeros el usuario debe descargar y guardar el handoff en almacenamiento privado; las sesiones no se sincronizan automáticamente.
- Los experimentos V5 usan reportes suministrados. Su resultado solo admite **propuestas**, jamás modificación automática de la skill.

## Evolución candidata V6.0.0

Ver `docs-EVOLUCION-V6.md` y los protocolos presentes bajo `reference/`. Esta variante se valida con pruebas sintéticas. NO utiliza sistemas productivos ni presupone autorizaciones.
