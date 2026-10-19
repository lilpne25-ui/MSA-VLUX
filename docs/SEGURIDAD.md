# Alcance de seguridad

MSA-VLUX es una metodología y un conjunto de herramientas locales, NO una barrera de seguridad técnica por sí sola. Los gates informativos y manifestaciones SHA-256 no reemplazan aislamiento, revisiones de permisos, secretos gestionados fuera del repositorio ni políticas de GitHub.

- Nunca añadir `.env`, tokens, llaves, bases o expedientes de proyectos/usuarios al repositorio.
- Las evidencias de handoff son sensibles; guardarlas en almacenamiento privado y revisarlas antes de compartirlas.
- Los hashes detectan corrupción, pero no aportan autenticidad criptográfica independiente frente a quien controla contenido y manifiesto.
- Ninguna aprobación de una sesión se transfiere automáticamente a otra.
- La rama principal contiene solo metodología genérica: NO hay registros particulares de clientes ni aplicaciones.
- La distribución rc3 archivada no debe tomarse como garantía de controles técnicos del entorno.
- Las pruebas de CI ejecutan código del repositorio; revise las contribuciones antes de aceptarlas.
