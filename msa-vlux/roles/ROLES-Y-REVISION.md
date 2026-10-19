# Roles y definición de independencia — V4.2+

| Rol | Salida comprobable | Límite |
|---|---|---|
| Scout | Inventario de fuentes y huecos | No atribuye requisitos inferidos al cliente |
| Architect | Opciones y trade-offs | No aplica cambios sin permiso |
| Security | Modelo de amenazas y pruebas de abuso | No lee ni publica secretos innecesarios |
| Verifier | Refutación y controles negativos | No declara PASS sin ejecución |
| Experience | UX y accesibilidad | Diferencia simulación y prueba en dispositivo real |
| Operations | Backup, restauración, releases, monitoreo | No deploy sin autorización específica |
| Commercial | Alcance y supuestos medibles | No inventa precios ni contratos |
| Demo | Recorrido honesto de lo disponible | No muestra mock como producto implementado |

La independencia **no se obtiene escribiendo dos nombres de rol en una misma respuesta**. Requiere proceso/contexto separado, artefacto SHA congelado y evidencia. Si el runtime no permite lanzar subagentes, ejecutar lentes secuenciales y señalar NOT_INDEPENDENT. Reportar autor, ejecutor, fuente, SHA, resultado, límites y conflicto de interés.

## Paquete ejecutable de delegación

En V4.2/V5, tras inicializar el expediente y fijar el átomo con SHA:

```bash
python scripts/msa.py role-packet --project-dir PROYECTO --role verifier --master-execution-id master001 --output reviewer-task.json
```

Entregar el JSON a **otro agente/proceso** si el runtime lo permite. Su reporte debe incluir `reviewer_execution_id`, `master_execution_id`, `role`, `artifact_sha`, `findings`, `result`, `independence_declared`. Validar:

```bash
python scripts/msa.py check-review --packet reviewer-task.json --review reviewer-result.json
```

`DECLARED_INDEPENDENT_NOT_ATTESTED` significa que **el propio sistema no puede demostrar** que hubo un proceso separado, ni imponer realmente solo lectura. Los logs del runtime deben acreditar la independencia y los permisos. `NOT_INDEPENDENT` es el resultado correcto para un segundo lente en el mismo agente.
