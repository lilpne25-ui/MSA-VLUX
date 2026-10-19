# MSA-VLUX V4 · Módulo SECURITY

MSA_VERSION=4.0.0-rc3 · Módulo: SECURITY · Se carga en: dimensión 7 de AUDIT, todo átomo Full con disparadores de seguridad (§4.1), PILOT, PRODUCTION, `SECURITY_EVENT`
Depende del núcleo. La seguridad **del agente** (hooks, permisos, credenciales) se verifica por separado en `reference/ADAPTACION-CODEX.md`; este módulo cubre la seguridad **del producto del cliente**.

---

# 23. SEGURIDAD Y PRIVACIDAD DEL PRODUCTO

## 23.1 Revisión por puntos

Cada punto: `PASS` · `FAIL` · `UNKNOWN` · `N/A`, con evidencia (archivo:línea, comando, respuesta HTTP observada).

| # | Punto | Cómo se verifica sin mutar |
|---|---|---|
| 1 | Secretos en el código y **en el historial Git** | Escaneo del árbol y del historial (`gitleaks`, `git log -p` filtrado, script del proyecto); un secreto histórico se trata como comprometido (§10.4) |
| 2 | Autenticación | Bypass de login, credenciales por defecto, expiración y revocación de sesión, recuperación de contraseña |
| 3 | Autorización (RBAC) | Cada acción sensible verificada **en el servidor**; prueba de un rol sin permiso contra el endpoint |
| 4 | Exposición de archivos | Descargas con control de acceso; nombres saneados; sin listados públicos; buckets privados |
| 5 | Webhooks y APIs entrantes | Firma verificada, idempotencia (patrón 3), límites de tamaño y tasa |
| 6 | Dependencias | Auditoría del gestor de paquetes; vulnerabilidades críticas con mitigación o plan |
| 7 | Datos personales | Inventario de datos personales, minimización, retención, logs sin datos sensibles |
| 8 | Operaciones destructivas | Permiso + vista previa del impacto + confirmación + auditoría (§10.3 punto 6) |
| 9 | Transporte | HTTPS forzado (redirección HTTP→HTTPS), HSTS, cookies `Secure`/`HttpOnly`/`SameSite` |
| 10 | Aislamiento entre clientes | Bases, secretos, dominios, storage y deploy separados; ramas o instancias compartidas declaradas (§8.4) |
| 11 | Respaldos | Cifrado, acceso restringido, fuera del host, restauración probada (§21.3 punto 7) |
| 12 | Superficie expuesta | Puertos, paneles de administración, endpoints de diagnóstico y demo accesibles desde internet |

## 23.2 Reglas

- Un `FAIL` en los puntos 1, 2, 3 o 10 con datos reales es `CRITICAL` y bloquea toda promoción (§2.7).
- La revisión **no rota credenciales, no cambia configuraciones y no prueba ataques contra ambientes productivos**. Las pruebas activas (fuerza bruta, fuzzing, escaneo de red) requieren autorización explícita y un ambiente acordado.
- Un hallazgo de seguridad de otro cliente encontrado al revisar reutilización no se escribe en el expediente del cliente actual (§8.4); se reporta en el chat y, si requiere acción, en un expediente interno de VLUX.
- El reporte de seguridad no incluye secretos completos: sólo su ubicación y un prefijo enmascarado.

## 23.3 `SECURITY_EVENT` en operación

Si hay indicios de compromiso: contener (con autorización), preservar evidencia (logs, SHA, accesos), no borrar rastros, rotar credenciales sólo con autorización y notificar a los responsables definidos. Las obligaciones legales de notificación son decisión humana.
