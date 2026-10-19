# MSA-VLUX V6.0.0


## Capacidades de V6.0.0

- V5.1: `observe`, `metrics`, `calibrate` con registros suministrados y sin verificación automática de procedencia.
- V5.2: `benchmark` matemático sintético (PSO/random) y `paired-experiment` (datos pareados, holdout y revisión humana).
- V6.0: `adaptive-plan` por riesgo; opcional `--experiment` informativo sin promover ni autorizar acciones.


---

# MSA-VLUX 5.0.0 — cambios de esta distribución

**Origen conservado:** núcleo V4.0.0-rc3 y 12 módulos, sin contenido de aplicaciones.

- V4.1: CLI estándar sin red, expedientes aislados, cadena de evidencias, autoevaluación y suite adversarial con control negativo. La puerta de autorización es una advertencia deny-all, no un hook.
- V4.2: transferencia explícita verificada, restauración segura, archivos de evidencia seleccionados, roles y continuidad Codex/Claude, sin heredar permisos.
- V5.0: mediciones reproducibles, comparación baseline/candidato/holdout, hipótesis de mejora automáticas y bloqueo de regresiones; publicación y autoedición prohibidas.

No se han ejecutado pruebas sobre los runtimes de terceros reales ni se verificaron hooks/ACL de sus entornos; sí se prueban localmente los scripts de la distribución.
