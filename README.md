# MSA-VLUX — metodología portable para agentes

**Versión principal: V5.0.0.** Skill genérica para Codex y Claude Code. Incluye autoevaluación, continuidad verificable entre sesiones y propuesta de mejoras basada en resultados. No precarga información de aplicaciones, clientes o proyectos.

> **Importante:** una skill NO es un sandbox, no concede permisos, no instala barreras técnicas ni sincroniza automáticamente conversaciones. Ningún push, merge, despliegue, lectura privada o acción con efectos externos queda autorizado por el mero hecho de instalarla.

## Instalación rápida

1. Usa el código expandido de [`msa-vlux/`](msa-vlux/) o descarga [`dist/MSA-VLUX-V5-CODEX-CLAUDE.zip`](dist/MSA-VLUX-V5-CODEX-CLAUDE.zip).
2. Para Codex, copia `msa-vlux/` al directorio de skills que tenga configurado Codex (por ejemplo `~/.agents/skills/msa-vlux/` o `.agents/skills/msa-vlux/` dentro del proyecto).
3. Para Claude Code, copia `msa-vlux/` a `~/.claude/skills/msa-vlux/` o `.claude/skills/msa-vlux/`.
4. Reinicia la sesión y solicita `$msa-vlux`. En Claude Cloud, adjuntar el ZIP no implica instalación persistente ni ejecución de scripts.

## Comprobación

```bash
cd msa-vlux
python scripts/msa.py doctor
python scripts/msa.py verify-package
python -m unittest discover -s tests -v
python scripts/msa.py eval --traces evals/traces-pass.json
```

La evaluación adversarial `python scripts/msa.py eval --traces evals/traces-fail.json` debe fallar intencionalmente.

## Versiones

| Versión | Función distintiva | Archivo |
|---|---|---|
| V4.0.0-rc3 | Base histórica (archivo) | [`dist/MSA-VLUX-V4-RC3-CODEX-SKILL.zip`](dist/MSA-VLUX-V4-RC3-CODEX-SKILL.zip) |
| V4.1 | Autoevaluación, integridad y pruebas negativas | [`dist/MSA-VLUX-V4.1-CODEX-CLAUDE.zip`](dist/MSA-VLUX-V4.1-CODEX-CLAUDE.zip) |
| V4.2 | Transferencia de expedientes y revisiones | [`dist/MSA-VLUX-V4.2-CODEX-CLAUDE.zip`](dist/MSA-VLUX-V4.2-CODEX-CLAUDE.zip) |
| **V5.0** | Evaluación basada en baseline/candidato/holdout, con revisión humana | [`dist/MSA-VLUX-V5-CODEX-CLAUDE.zip`](dist/MSA-VLUX-V5-CODEX-CLAUDE.zip) |

[Paquete con todas las versiones](dist/MSA-VLUX-EVOLUCION-4.1-4.2-5-COMPLETO.zip) · [Historial de versiones](docs/VERSIONES.md) · [Informe de validación](docs/VALIDACION.md) · [Prompt de arranque](docs/PROMPT-ARRANQUE.md)

## Seguridad y continuidad

- Los paquetes de handoff conservan exclusivamente lo expresamente incluido y verificado; no representan memoria automática ni guardan código no seleccionado.
- Los permisos externos no se transfieren entre sesiones; cada entorno debe aplicar sus propios controles efectivos.
- Las pruebas reportadas hasta aquí son **locales y sintéticas**, no certifican el comportamiento de una instancia real de Codex o Claude.
- Las carpetas `.msa/`, archivos `.env` y credenciales **no deben publicarse**. [Política de seguridad](docs/SEGURIDAD.md).

## Licencia

No se incluye una licencia de código abierto. Los términos de uso y redistribución están pendientes de definición por quien controla el repositorio.