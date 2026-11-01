# Puertas separadas de distribución · 01-11-2026

## Beta privada: NO-GO actual

PR89 aporta candidato interno0.3.0-beta.3, hash y manifiesto de fuentes limpias
cf1d451.945 archivos NSIS conciliados;923 runtime/60 PE,19 wheels oficiales
fijados, sin copiar DLL del equipo. No contiene las44 DLL de caché de beta2.
`RUNTIME_036_QA.json` separa pruebas reales de pendientes: actualización directa
falló en Codex; desinstalar/instalar y conservar preset/datos sí pasó allí.
No se extrapola a Windows limpio ni a una cuenta normal fuera de MSIX.

- [x] Integración70 en main comprobada por árbol y ancestros.
- [x] Candidato beta2 con hash/versión y pruebas locales trazables, sin originales modificados.
- [x] Fixtures offline, guías, feedback sin envío propio y protocolo de datos preparados.
- [x] Procedencia técnica del nuevo runtime/NSIS conciliada con archivos oficiales, hashes, arquitectura y avisos; DLL del setup viejo no reutilizadas.
- [x] Candidato beta3 con privacidad corregida, avisos incorporados, nueva versión/hash y pruebas locales.
- [ ] Derechos/condiciones de redistribución aceptados por el titular (#60); la procedencia y una firma válida no sustituyen este gate.
- [ ] Actualización directa beta2→beta3 superada fuera de Codex; fallo local de código2/diálogo previo pendiente de conciliar.
- [ ] Procesamiento con red físicamente desconectada en entorno objetivo; PATH restringido no demuestra ese caso.
- [ ] W01–W09 ejecutados en Windows10/11 limpio, con/sin WebView2, offline; upgrade/uninstall sin pérdida.
- [ ] E01–E03 en editores reales acordados, o alcance de beta explícitamente limitado por el titular sin promesa de compatibilidad.
- [ ] Calidad visual aceptada sobre medios autorizados, incluidos retratos si se anuncian.
- [ ] Titular, canal privado, conservación y consentimiento del piloto definidos; invitaciones autorizadas aparte.
- [ ] Revisión y autorización humana de entrega a cinco usuarios concretos.

Firma ausente es riesgo de confianza/distribución que debe resolver el titular;
no comprar certificado ni desactivar protecciones. El funcionamiento offline de
procesamiento no garantiza ausencia de conexiones del runtime/Windows cuando
hay red. No confundir pruebas locales de desarrollo con W01–W09.

## Venta comercial: NO-GO independiente

- [ ] Todas las puertas técnicas de beta privada resueltas, soporte e incidencias evaluados.
- [ ] P0 comercial con entrevistas/evidencias reales y decisión humana; COL001 pendiente.
- [ ] Calidad/cobertura y compatibilidad ofrecidas demostradas, limitaciones publicadas.
- [ ] Derechos completos del código propio/terceros, titular, marca y contratos revisados.
- [ ] Privacidad/diagnósticos de terceros, soporte, actualizaciones y conservación definidos.
- [ ] Fiscalidad, precio, condiciones de compra/desistimiento/conformidad y medios de pago revisados por el responsable.
- [ ] Canal de distribución/confianza y aprobación expresa de lanzamiento/cobros.

Un merge, recepción de aviso, benchmark o piloto de cinco personas no sustituye
estas puertas ni completa COL041(10–20 usuarios). No hay venta, publicación
externa, contratos aceptados o participantes contactados en este ciclo.
