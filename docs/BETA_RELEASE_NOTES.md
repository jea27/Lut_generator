# 0.3.0-beta.1 · candidato local, sin release publicada

31-10-2026. Source396a508, dirty=false; SHA256
 ae47f44e6f9382810e20a7a98b0b46bf6d53411e7f1c8b0fb2e9c7acf595ac21.
266203035 bytes. Sin firma; NO-GO entrega externa/venta hasta completar QA y
auditoría de payload/NSIS y condiciones Microsoft.

- Acabado manual experimental: glow de altas luces, difusión y fade; receta v2
  compatible con v1 sin efectos, intensidades/bypass independientes.
- PNG/JPG y lotes incluyen acabado; LUT solo color con aviso y JSON conserva receta.
- Paneles desplazables manteniendo comparador visible; ayuda y feedback offline.
- Remapeo de rutas de compilación Rust y manifiesto ligado a versión exacta.
-299 entradas de licencia con avisos, seis textos recuperados y fuentes fijadas.
-30 tests MVP y91 tracking; smoke congelado de efectos/JSON/LUT/lote byte-identical.

Pendientes:27 patrones de rutas de terceros/ejemplos por clasificar, inspección
completa NSIS/runtime, Windows limpio/editores activados/piel y revisión humana.
No halation ni extracción automática del acabado. Rendimiento real16MP y
límites de preview en LOOK_MATCH_V1.md. Notas0.2 conservadas a continuación.

---

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
