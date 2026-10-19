# MSA-VLUX — metodología portable para Codex y Claude

**Rama candidata V6.0.0.** Evolución ejecutable y sin contexto de aplicaciones o clientes.

- V5.1: observabilidad local, autoevaluación calibrada y ciclo PDCA/DMAIC.
- V5.2: experimentos pareados y benchmarks matemáticos offline PSO/random.
- V6.0: planeación adaptativa supervisada por riesgos, sin permisos autónomos.

Las pruebas son sintéticas; **no existe** instrumentación automática acreditada de ejecuciones reales de Codex/Claude y las skills **no** son barreras técnicas de seguridad. No hay despliegue, lectura de clientes ni autoaplicación de mejoras.

## Instalación

Copiar [msa-vlux/](msa-vlux/) a una carpeta de skills configurada de Codex o Claude Code o utilizar el ZIP indicado. La transferencia de sesiones (handoff) sigue requiriendo archivar y compartir el ZIP explícitamente.

```bash
cd msa-vlux
python scripts/msa.py doctor
python scripts/msa.py verify-package
python -m unittest discover -s tests -v
```

## Distribuciones

- [V5.1](dist/MSA-VLUX-V5.1.0-CODEX-CLAUDE.zip)
- [V5.2](dist/MSA-VLUX-V5.2.0-CODEX-CLAUDE.zip)
- [V6.0](dist/MSA-VLUX-V6.0.0-CODEX-CLAUDE.zip)
- [Evolución consolidada](dist/MSA-VLUX-V5.1-V5.2-V6.0-COMPLETO.zip)

Conservamos [distribuciones históricas](dist/) y [documentación de evolución](docs/EVOLUCION-V6.md).

## Seguridad y licencia

Todo acceso externo requiere aprobación específica y controles reales en el sistema operativo/proveedor. Sin archivo LICENSE: derechos y redistribución no concedidos automáticamente.
