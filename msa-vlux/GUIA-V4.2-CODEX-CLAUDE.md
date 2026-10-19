# Guía práctica: pasar un proyecto de Codex a Claude Cloud y viceversa

**Prerequisito:** la distribución V4.2 o V5 instalada o accesible en ambos entornos. El proyecto no tiene que ser el mismo directorio, pero sí debe recuperar el repo/artefactos por un canal que realmente exista. Los comandos solo trabajan en una carpeta local autorizada.

## Sesión 1 — cualquiera de los runtimes

```bash
python scripts/msa.py doctor
python scripts/msa.py init --project-dir ./laboratorio --name "Ensayo sin cliente"
python scripts/msa.py set-atom --project-dir ./laboratorio --id A0 --mode AUDIT --status in_progress --baseline-sha abc123
python scripts/msa.py record --project-dir ./laboratorio --type evidence --data-file templates/EVIDENCE-EVENT.json
python scripts/msa.py handoff --project-dir ./laboratorio --runtime codex --output ./MSA-TRASPASO.zip
python scripts/msa.py verify-handoff --archive ./MSA-TRASPASO.zip
```

Antes de salir, guardar `MSA-TRASPASO.zip` en almacenamiento privado controlado. Comparar el hash SHA-256 que imprime el comando con el valor recibido en el nuevo entorno **por un canal confiable**.

**Para incluir un informe escrito:** `--include docs/reporte.md` al llamar `handoff`; solo si el archivo no contiene datos privados ni secretos. No se incluirán datos ni fuentes automáticamente.

## Sesión 2 — Codex, Claude Code o Cloud con shell

1. Cargar/instalar la misma skill (o una más reciente compatible) y adjuntar el ZIP de traspaso.
2. Verificar integridad y confirmar el SHA esperado por un canal confiable.
3. Importar y reanudar:

```bash
python scripts/msa.py verify-handoff --archive ./MSA-TRASPASO.zip
python scripts/msa.py import-handoff --archive ./MSA-TRASPASO.zip --target ./proyecto-recuperado
python scripts/msa.py resume --project-dir ./proyecto-recuperado
python scripts/msa.py verify-ledger --project-dir ./proyecto-recuperado
```

4. Comparar la línea base con `git rev-parse HEAD` **dentro del repo correcto y tras revisar su configuración**; el handoff no lleva código fuente.
5. Revisar los archivos en `.msa/imported-evidence/` y reestablecer accesos según las políticas del entorno.
6. Obtener **nueva autorización** para push, PR, merge, deploy, correo o modificación externa. La anterior nunca se transfiere.

## Si Cloud no permite ejecutar Python o extraer el ZIP

El agente no podrá usar esta utilidad automáticamente. En ese caso, el humano o un servicio confiable extrae/verifica en su computadora y aporta `state.json`, `history.jsonl` e informes autorizados como archivos de referencia. La sesión debe declarar `CONTINUITY_PARTIAL`, no fingir restauración. Un modelo no puede prometer almacenar o reconstruir archivos perdidos entre sesiones.

## Datos que NO recupera el handoff

Variables de entorno, credenciales, archivos no seleccionados, bases de datos, mensajes anteriores, contenidos de servicios externos y permisos. Tampoco sustituye respaldos de código ni contratos. Para trabajo complejo, conservar aparte bundles Git o repositorios privados **con autorización específica**, respaldos y evidencias pertinentes.
