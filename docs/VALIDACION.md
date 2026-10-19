# MSA-VLUX — Informe de construcción y validación local

## Resumen

Se generaron **tres distribuciones acumulativas** para Codex y Claude Code/Cloud basadas en MSA V4.0.0-rc3. En cada una se conserva sin cambios el núcleo histórico y los 12 módulos originales. No se incorporó contexto de aplicaciones, clientes o repositorios.

| Versión | Archivos | Tests ejecutados | Funciones no aplicables/omitidas | Evaluaciones sintéticas | SHA256 del ZIP |
|---|---:|---:|---:|---|---|
| 4.1.0 | 38 | 10 | 12 | 6/6 trazas conformes y 6/6 mutaciones detectadas | `c624b446130170785ed4b27a74c93f2f05a026130d4625feafb9dfad3689fafd` |
| 4.2.0 | 43 | 18 | 4 | 6/6 trazas conformes y 6/6 mutaciones detectadas | `b23902c62b44e801dc6f446fa02b5335bc98463f8b45e20781e17a03845fc587` |
| 5.0.0 | 49 | 22 | 0 | 6/6 trazas conformes y 6/6 mutaciones detectadas | `3e4b26f9cda995842ca0b22e37dcfc9bcee72415df65e4e061b28757707ab666` |

## Capacidades entregadas

**V4.1:** autoevaluación estructurada 0–4 por seis dimensiones; resultados altos exigen evidencia referenciada con SHA256; ledger de eventos con cadena de hashes; tests de rechazo, integridad, seguridad y control negativo; preflight y gate deny-all informativo.

**V4.2:** suma transferencia de trabajo (`handoff`/`verify-handoff`/`import-handoff`/`resume`), material autorizado por inclusión explícita, restauración contra corrupción, revocación de permisos entre sesiones y paquetes de revisión estructurados para roles especializados.

**V5.0:** suma comparador baseline/candidato/holdout, compuertas de no regresión, hipótesis de mejora generadas por métricas, bloqueo de autoaplicación y exigencia de revisión humana.

## Prueba end-to-end en entorno local

1. Extracción de cada ZIP y validación del manifiesto: **PASS**.
2. Preflight de 12 módulos en cada ZIP: **PASS**.
3. Test de trazas conformes: **PASS 6/6**; controles adversariales sintéticos: **6/6 detectados**.
4. Solicitud de acción remota a gate informativo: **DENY** en los tres ZIP.
5. Expediente V4.2 creado; traspaso verificado y restaurado en V5, con un archivo de evidencia expresamente incluido: **PASS**.
6. Permisos de escritura del estado restaurado: **DENY**.
7. Paquete a Verifier y resultado: **DECLARED_INDEPENDENT_NOT_ATTESTED**, sin afirmar independencia no demostrada.
8. Comparación V5 de mejora ficticia y holdout: **PROPOSE_FOR_HUMAN_REVIEW**.
9. Comparación V5 con regresión de política: **REJECT_OR_MORE_EVIDENCE**.

## Limitaciones que NO se ocultan

- Las 6 trazas de prueba son **sintéticas**. No se ejecutó una auditoría completa de un agente de Codex ni Claude Cloud real. Las pruebas unitarias demuestran la lógica de herramientas locales, no obediencia del modelo.
- Ninguna skill, `gate` o JSON sustituye sandbox del SO, política de GitHub, aislamiento de credenciales o controles efectivos de autorización. `gate` es informativo y deniega siempre.
- Los hashes SHA256 verifican integridad relativa a un manifiesto; no prueban autoría ni sustituyen firmas autenticadas. Un actor con control de ZIP+manifest puede reemplazarlos.
- El traspaso requiere exportación y conservación por el usuario en un destino privado; no existe sincronización automática entre Codex y Claude ni recuperación de conversaciones, datos externos o archivos no seleccionados.
- El filtro de secretos rechaza patrones evidentes y extensiones riesgosas, pero no garantiza la ausencia de datos personales ni garantiza confidencialidad; revise cualquier informe antes de compartir.
- V5 **optimiza decisiones de propuesta** a partir de reportes suministrados y pruebas reservadas; no aprende automáticamente del trabajo real si el host no suministra trazas y métricas genuinas y no se reescribe a sí misma.

## Cómo comprobarlo

Descomprime un ZIP. Desde `msa-vlux/` ejecuta:

```bash
python scripts/msa.py doctor
python scripts/msa.py verify-package
python -m unittest discover -s tests -v
python scripts/msa.py eval --traces evals/traces-pass.json
python scripts/msa.py eval --traces evals/traces-fail.json
```

El último comando **debe salir con código 1**: la suite adversarial detecta fallos intencionales.

## Compatibilidad

Python 3.9+ y biblioteca estándar; probado aquí en contenedor Linux Python 3.13 con procesos separados. No se probó aún en Windows/PowerShell ni dentro de Codex/Claude Cloud reales. En Claude Cloud sin ejecución de Python la skill opera solo como instrucciones y archivos que el servicio pueda leer.
