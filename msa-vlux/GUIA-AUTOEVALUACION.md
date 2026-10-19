# Autoevaluación para personas y agentes

La autoevaluación cubre **el trabajo realizado**, no la autoestima ni un perfil personal. Seis dimensiones de 0 a 4 con evidencia y posibilidad de discrepancia por pares/humanos. Usa el mismo criterio en Codex, Claude Code, Cloud u otro entorno.

### Escala

- `0`: falló una obligación o no hay resultado aceptable.
- `1`: incompleto o con errores sustanciales.
- `2`: parcialmente verificado, hay huecos explícitos.
- `3`: probado con artefactos PASS y huellas de ejecución.
- `4`: reproducido y documentado con controles negativos y evidencia suficiente. Una puntuación 4 **no significa revisión independiente por sí sola**.

### Protocolo

1. El agente registra cada evidencia mínima con ruta/referencia, resultado y `artifact_sha256` mediante `record --type evidence`. **Nunca valores de tokens, PIN, contraseñas ni payloads personales**.
2. Completa las seis dimensiones en una copia de `templates/SELF-ASSESSMENT.json` y referencia `evidence_ids` correspondientes del ledger.
3. Ejecuta `assess --input ...`: para obtener más de 2 puntos en cualquier categoría, debe proporcionar al menos un evento PASS con SHA-256 sintácticamente válido. El CLI comprueba referencias, no reejecuta todas las pruebas ni autentica el origen del artefacto.
4. Una persona distinta revisa el mismo SHA usando `templates/HUMAN-REVIEW.md`, anota diferencias, contraejemplos, limitaciones y decisión independiente.
5. Si hay diferencias, se registran como nuevos hallazgos, sin borrar la primera evaluación.

### Validación de ejemplo

```bash
python scripts/msa.py init --project-dir ./evaluacion-demo --name "Ensayo"
python scripts/msa.py record --project-dir ./evaluacion-demo --type evidence --data-file templates/EVIDENCE-EVENT.json
python scripts/msa.py assess --project-dir ./evaluacion-demo --input templates/SELF-ASSESSMENT.json
```

La plantilla base obtiene `12/24` (seis veces 2) y está explícitamente marcada como autoinforme no independiente. Repetir la evaluación después de cada átomo para registrar progresión con evidencia. El score no autoriza el despliegue.
