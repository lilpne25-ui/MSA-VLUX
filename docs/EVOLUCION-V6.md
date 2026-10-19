# Evolución MSA-VLUX V5.1 → V5.2 → V6.0

## Entregado

| Versión | Nuevo comportamiento ejecutable | Comandos |
|---|---|---|
| V5.1 | Métricas locales, privacidad mínima, deduplicación por ID y autoevaluación calibrada | `observe`, `metrics`, `calibrate` |
| V5.2 | Benchmarks offline PSO/random y comparación pareada baseline/holdout | `benchmark`, `paired-experiment` |
| V6.0 | Selección de estrategia por riesgo, gates y aprobación humana obligatoria | `adaptive-plan` |

## Inicio reproducible

```bash
python scripts/msa.py doctor
python scripts/msa.py verify-package
python -m unittest discover -s tests -v
python scripts/msa.py init --project-dir ./demo-sintetica --name Demo
python scripts/msa.py observe --project-dir ./demo-sintetica --input templates/OBSERVATION.example.json
python scripts/msa.py metrics --project-dir ./demo-sintetica
python scripts/msa.py benchmark --config templates/BENCHMARK.example.json
python scripts/msa.py adaptive-plan --input templates/ADAPTIVE.example.json
```

## Lo que todavía NO se puede afirmar

- No hay integración observada en sesiones reales de Codex/Claude Cloud ni extracción automática de telemetría.
- No existe autenticación criptográfica de revisores, encriptación de handoffs ni enforcement de permisos a nivel SO.
- No se entrenó un modelo ni se adoptaron mejoras auto-modificadas.
- Los ensayos PSO son exclusivamente funciones numéricas artificiales, no optimización de entregas de VLUX.
- Se requiere revisar seguridad, privacidad y almacenamiento antes de usarlo en sistemas productivos.

## Próximo piloto interno (NO desplegado)

Elegir 20+ tareas sintéticas de cambios en código en un entorno aislado. Medir calidad y duración con ambas herramientas. Registrar procedencia y artefactos; generar paquetes de revisión separados; validar con controles negativos. Las mejoras deben superar pruebas independientes, no únicamente autoevaluación ni indicadores del mismo conjunto.
