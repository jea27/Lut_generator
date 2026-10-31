# Release preparada · 0.2.0-beta.1 (sin publicar)

Candidato técnico Windows x64; nombre provisional Color Studio Beta. Esta nota
no autoriza lanzamiento comercial ni creación de release pública.

Novedades: instalador NSIS con motor local, biblioteca de presets con edición y
grupos, demo CC0 y bienvenida, preferencias ES/EN, arrastrar imágenes al editor,
lotes básicos cancelables, estados durables/recuperación interrupted, sesión
loopback protegida y supervisión de procesos. Se conservan métodos globales
Lab, comparador, controles y exportaciones PNG/JPG/JSON/.cube33³.

Datos: por usuario y fuera del directorio de programa. No se sobrescriben
originales; desinstalación conserva datos privados. Sin subidas/telemetría/cuentas.

Adjuntos propuestos tras autorización: setup.exe, SHA256SUMS, inventory.json,
avisos y QA. No incluir originales privados, registros, respuestas, contactos,
permisos firmados o secretos. Comprobar hash exacto de candidato, procedencia de
build y firma. GitHub Actions artifact temporal no es aceptación comercial.

Límites: sin firma, sin QA limpia Windows10/11 completada ni prueba externa Adobe;
calidad de piel/diversidad pendiente, JPG/PNG8 SDR, no RAW/Log/HDR/vídeo/máscaras,
no actualización automática/rollback. La validación comercial P0 no cambia.
GO/NO-GO y decisiones en BETA_COMERCIAL.md y evidence/BETA_02_QA.md.

Procedimiento futuro de release: revisión humana del commit y QA → autorización
concreta de versión/audiencia → compilar y firmar → validar hash → etiquetar el
commit aceptado → prerelease autorizada con notas y avisos → verificar descarga
en Windows limpio. No ejecutar estos pasos remotos automáticamente.
