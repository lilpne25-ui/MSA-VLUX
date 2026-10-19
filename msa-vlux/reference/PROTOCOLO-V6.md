# MSA-VLUX V6.0 — Ingeniería adaptativa supervisada

## Planeación conservadora

`adaptive-plan` transforma un perfil **declarado** del átomo en estrategia `LITE`, `FULL` o `FULL_ADVERSARIAL`, y exige gates de acuerdo con riesgo, complejidad y sensibilidad de los datos.

- `unknown` se trata como riesgo alto; información restringida eleva controles.
- La ejecución con efectos externos solicita autorización humana específica, verificada por barreras reales del entorno.
- No se permiten escrituras externas, acceso a secretos, auto-edición o promoción automática mediante este plan.
- Se requieren evidencias, pruebas negativas e independencia efectiva en tareas elevadas; IDs de revisores por sí solos no prueban independencia.

## Ciclo de evolución propuesto

Observar (V5.1) → Investigar causas PDCA/DMAIC → Experimentar (V5.2) → Solicitar revisión humana → Evaluar sobre nuevas tareas → Decidir una versión candidata → Publicar separadamente.

No llame "aprendizaje automático" a una adaptación por reglas. La versión 6 realiza **selección determinista supervisada de estrategia**, no aprendizaje online, no modificación de prompts autónoma y no captura autónoma de datos en Cloud.

## Aplicación de PSO en operaciones

Una instancia futura de *VLUX Optimization Engine* puede reutilizar el motor de objetivos y semillas, pero necesita adaptadores de dominio, datos autorizados, restricciones reales, evaluación fuera de muestra y control humano. El benchmark sintético no autoriza integración con ningún producto.

`adaptive-plan --experiment <reporte-pareado.json>` permite considerar una propuesta de laboratorio, **sin cambiar** la estrategia de seguridad elegida ni activar permisos. Ningún conjunto sintético acredita automáticamente mejoras reales.
