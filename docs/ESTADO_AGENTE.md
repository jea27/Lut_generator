# Checkpoint vigente · estabilización y procedencia binaria · 31-10-2026

PR71 lista para revisión: https://github.com/jea27/Lut_generator/pull/71.
CI de bc778e8: MVP41186741670, Studio41186741616 y validate41186741589 success.
Corregido en PS5.1 el caso de rutas cortas/proveedor detectado por CI, manteniendo
rechazo de escape de directorio. El primer fallo de CI no se ocultó ni omitió.
Prioridad siguiente del usuario: dashboard automático en rama/worktree independiente
codex/COL-006-product-dashboard; no toca código de la aplicación de esta rama.

Tarea COL013#45, rama codex/COL-013-estabilizacion-beta3 desde origin/main
cfb6d11. PR70 ya integrada por jea27 a las08:27:11 UTC. Árbol de main idéntico
a HEAD4920cf0 de70;65/66/69 son ancestros. Escaneo69 blobs cambiados sin
hallazgos de secretos/perfil local/archivos privados,6 JPEG sin EXIF de origen
CC0 o QA ya revisado. Ver STAB_03_PR70_REVIEW.json y ESTABILIZACION_03.md.

Trabajo: profiler reproducible sin modificar motor; bundle/editor comparador
con oráculo LUT escalar; verificador PS5.1 de hashes antes/después sin borrar
datos; protocolo limpio W01–09 y editores E01–05. Roadmap conserva42 tareas y
estados: ampliación futura de COL026 añade inferencia de acabado y halation,
explícitamente sin implementar ni retrasar beta. Fuente UI/landing corrige
«sin telemetría» para diferenciar WebView2/SmartScreen. No APIs/efectos nuevos.

Pruebas locales37 MVP+91 seguimiento sin omisiones, TypeScript/Vite OK.
Se corrigió solo el entorno de módulos del proceso hijo PowerShell en el test,
sin cambiar políticas ni configuración global. Pipeline16MP3 pasadas mediana
17,376s: LUT9,005/acabado6,267/PNG1,445. No mejora entregada sobre32,392s del
binario histórico; entornos distintos. Tiles256/512 experimentales conservan
píxeles en1 foto; no aplicados ni medidos RAM/cancelación. LUT textual vs oráculo
error1,091e-7 en262 puntos: infraestructura, no prueba de editor real.

Bloqueo NUEVO:95 DLL/PYD cotejados contra TOC y NSIS,44 UCRT/API-set proceden de
caché nativa de herramientas. UCRT firmado pero hash diferente al SDK REDIST
local; no presume derechos. Gate en builder detiene nuevos builds antes del
staging/NSIS; ejecutado realmente,44 bloqueos esperados. CPython también exige
conciliar proveedor/build del runtime de herramientas. Ver LICENCIAS_BINARIAS_BETA.
No se instala/sustituye Python ni se edita/elimina DLL firmada. El candidato
beta2 y su hash3e3851ee…14f permanecen intactos, retenidos solo para QA interna.
NO existe instalador beta3: rama prepara estabilización, no nuevo artefacto.
Texto UI corregido y avisos complementarios requieren siguiente candidato,
versión/hash nuevos cuando la procedencia esté resuelta. No afirmar corrección
retroactiva del NSIS beta2. Paquete QA nuevo separado, sin instalador ni datos privados.

Sin VM accesible: Get-VM/vmms, VBoxManage/vmrun, procesosVM y Sandbox no presentes
en inventario. No virtualización habilitada. Windows limpio y editores reales
siguen not_run; no contactos o respuestas reales. Beta externa/venta NO-GO,
puertas separadas GO_NO_GO_03.md. Solicitud67 se reutiliza para procedencia,
entorno limpio/editor y revisión, sin volver a pedir7-Zip.

Reanudar: git status; gh pr list; leer Issue67,45,60. Revisar nuevo informe y
PR de esta rama. Resolver procedencia del runtime antes de build_beta.ps1;
no ocultar gate fallido. Con VM/PC ya autorizado ejecutar W01–09; con editor
activado E01–05, mantener datos crudos privados. No merge/approved/cobros/
entrega externa del agente. COL001 continúa pendiente. Historial debajo.

---
# Checkpoint anterior · conciliación de integraciones · 31-10-2026

Rama actual codex/COL-026-integracion-beta2, PR70 lista para revisión:
https://github.com/jea27/Lut_generator/pull/70. Árbol conservado desde
a01ed2b, sin sobrescribir datos. GitHub confirma merges humanos por jea27:
PR69 a rama COL042 (07:59:58 UTC), PR65 a main (08:00:10), PR66 a rama
COL037 (08:00:23). Por ese orden, origin/main=0539b9f incluye65 pero no los
cambios de66/69. Nueva PR de integración hacia main reúne landing, Look Match,
auditoría y clasificación final; no repetir implementación ni auto-fusionar.
Los HEAD de ramas intermedias no demuestran integración en main. No se aplican
approved ni done; Issue68 sigue review y COL001 pendiente de entrevistas.

Instalador y evidencias del checkpoint siguiente siguen vigentes: source
a452a5f y SHA256 3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f,
recalculado en esta conciliación. Sin cambios de runtime posteriores al build.
30+91 pruebas locales y CI anteriores correctas. CI70 correcta: MVP41184058852,
Studio41184058873 y validate41184100896; publish omitido en PR como corresponde.
Sync41184098485 success y JSON público leído:42 tareas, COL026 review con enlace
real a PR70, COL001 blocked. No cambio manual de estados ni approved.
Aviso nuevo de conciliación41184100601 success; bot6541069862 menciona jea27
en67. Sin confirmación física nueva del iPhone; no reenviar el mismo aviso.
Sin nuevos participantes, editor activado o Windows limpio: NO-GO externa y venta.
No volver a notificar por permisos7-Zip o por el mismo bloqueo de QA; la nueva
decisión de integración se consolida en67, sin crear otra Issue de acción.

Reanudar: git status; gh pr list --state open; leer Issue67 y revisar la PR de
codex/COL-026-integracion-beta2 hacia main. Tras integración humana comprobar
ancestría de main y sync real antes de afirmar despliegue. No inferir aprobación
de producto de los merges. Los apartados siguientes conservan evidencia histórica.

---
# Checkpoint previo · Look Match y QA externa · 31-10-2026

Rama codex/COL-026-look-match-beta, Issue68; base32278e4 de PR66, sobre PR65.
PR65/66 auditadas abiertas y checks correctos; no merges. PR69 nueva entrega
https://github.com/jea27/Lut_generator/pull/69, base rama de PR66; revisar65→66→69. Autorización explícita
actual permite acabado manual glow/difusión/fade y preparación de beta privada;
no cobros, beta general, certificados, virtualización o contacto de participantes.

Candidato0.3.0-beta.2 construido desdea452a5f, dirty=false. Archivo266211731 bytes,
SHA256 3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f.
Ruta ignorada apps/desktop/src-tauri/target/release/bundle/nsis/. Sin firma ni
release. Manifest en LOOK_03_ARTIFACT_B2.json; no confundir con0.2 ni glob de archivos.

Implementado: Look manual v1 (receta v2) con intensidad/bypass independientes,
color primero, glow/difusión lineales por tiles con halos/alfa y fade limitado.
Presets, JSON, PNG/JPG y lotes conservan efectos. LUT solo Color Match con aviso.
V1 sin acabado compatible; halation, microcontraste dedicado e inferencia del
acabado desde referencia NO implementados. No transferencia fiel demostrada.
Paneles desktop independientes conservan el comparador; feedback offline incluido.

30 tests MVP y91 tracking locales OK, TS/Vite/build nativo OK. Binario congelado:
demo realCC0, JSONv2/LUT, lote2 y PNG idéntico byte a byte al export individual.
Benchmark16MP32.4s con PNG/RSS815MB; preview0.729s, MAE preview/export reducido
0.00476 yP95 0.01455. No validación de piel/mercado. Evidencias LOOK_03_*.
Upgrade local0.2→0.3beta1→beta2 exit0,8 archivos existentes conservados por hash; arranque
nativo0.3 muestra preset previo y preferenciasEN. No Windows limpio (MSIX Codex).

Auditoría: corregidas155 rutas compilación nativas mediante remap Rust;0 en
nuevo exe. Corregido hash/version builder que elegía primer instalador del glob.
299 entradas con licencia declarada y avisos,6 faltantes recuperados con hashes.
Payload Python/PYZ+nativo enumerado;0 local-profile/secret/dev findings, pero27
archivos/módulos con rutas proveedor/ejemplos, ya clasificados y ligados a hashes.
NO decir instalador totalmente limpio. NSIS176 extraído, WebView2 firmado y plugin contrastado; los términos
Microsoft/VC/UCRT requieren revisión final; no editar DLL firmadas ni autoaprobar auditoría legal.

Preparado plan limpio/preflight no invasivo y5 perfiles sin asignar B01–05.
Formulario QA00 descargado, synthetic/unverified/counts_as_interview=false;
solo en .research-private/beta/qa. Nadie contactado ni respuestas reales.
Bundle LUT lossless CC0 en .lumaforge-local/look03-qa/LUT-Editor-QA-CC0.zip.
7-Zip26.05 portátil autorizado/preparado/verificado; no volver a pedir permiso.
176 entradas NSIS extraídas/auditadas, WebView2 Microsoft firma válida y plugin
Tauri0.5.3 hash idéntico a release oficial.0 patrón local/token/dev,27 rutas
proveedor/ejemplo (27 genéricas/ejemplos,0 desconocidas). Copias privadas/raw no publicar.
Avisos complementarios NSIS/Tauri en packaging/notices/upstream.
Photoshop no ofrece editor verificable en nueva inspección; último bloqueo
confirmado fue login. No afirmar login resuelto o importación real; Premiere muestra selección de suscripción, no se activó ni compró nada;
Resolve sin prueba. Acción67 reutilizable, no repetir bloqueo sin novedad.

NO-GO beta privada externa y venta, por separado en BETA_QA_EXTERNA.md y
BETA_03_AUDITORIA.md. Pendientes Windows10/11 limpio, payload completo/términos,
editores activados, retratos autorizados, responsable/canal/plazo y revisión.
COL001/P0 siguen pendientes. Las cinco pruebas no cumplen10–20 de COL041.

Reanudar: git status; consultar PR65/66 y nueva PR de esta rama/Issue68; leer67
antes de notificar. Datos beta persistentes en LocalAppData/ColorStudioBetaData.
No borrar .lumaforge-local, imágenes, presets o worktrees. App nativa0.3-beta2 abierta. Feedback interno verificado en WebView2;
corregido popup y migración de presetv1 antes de activar efectos (JSONv2 GUI probado).
Servidor QA propio26292/puerto8794 y landing8792 si activos; no interfaces externas.
Build ./scripts/build_beta.ps1; tests ./.venv-mvp/Scripts/python.exe -m unittest
discover -s tests_mvp -v; audit scripts/audit_beta_artifact.py (exit2 esperado
mientras existan findings). Siguiente: derechos Microsoft y QA limpia
cuando el usuario aporte entorno. CI69 en a452a5f: MVP41181274271 y Studio41181274272 success.
Notificación69 consolidada en67: run41182721936 success y comentario bot
6540890455 menciona jea27; recepción física nueva no confirmada, no reenviar.
Sync41183485906 success: JSON público42 tareas, COL026 review/001 blocked.
Corregida etiqueta roadmap ausente de68. PR69 apilada no se enlaza como pr_url
hasta base main por política actual del sync; enlace en Issue68 y PR directa.
CI de código y documentos observada: MVP41182631211/Studio41182631230 success.
Paquete local de revisión en .lumaforge-local/beta03-review/ con setup, guías,
avisos, QA CC0 y SHA256SUMS; no entregar externamente antes de puertas/decisión.

---
# Checkpoint vigente · beta Windows · 31-10-2026

Rama raíz actual codex/COL-042-preparacion-comercial; base técnica conservada
en codex/COL-037-beta-estabilidad, Issues COL036#57/COL037#58.
Candidato0.2.0-beta.1 construido e instalado; NSIS266193722 bytes, SHA256
c1798ece22b9a8f38b6c7042a59630c16800b7a7ca295ee4119a8c157d092a4a.
Sin firma ni release pública. Herramientas autorizadas ya instaladas; no repetir
permiso de Rust/MSVC/C++/SDK/PyInstaller/Tauri. PR52/53 integradas por jea27,
main a7a8df8 incorporado por fast-forward local sin sobrescribir cambios.
Conservadas PR63/64 y docs Look Match/investigación comercial. No efectos
espaciales implementados, no modificación de cuestionario49€, COL001 pendiente.

Implementado: instalador Tauri2 con sidecar local supervisado y puerto dinámico,
sesión cookie/token/origen, presets CRUD/grupos, preferencias ES/EN, bienvenida,
demo CC0, arrastrar imágenes y lotes cancelables con recuperación interrupted.
23 tests MVP y91 seguimiento locales OK; TS/Vite y build nativo OK. Prueba real
4 CC0 de16MP, exports11.4–13.7s, RSS789–804MB; lote2 outputs verificados, ICC y
hashes originales intactos; watchdog de muerte padre OK. No evidencia de piel.
Instalación/desinstalación exit0:8 archivos privados conservados por hash, proceso
auxiliar cerrado. Reinstalado para revisión. Contexto Codex/MSIX virtualiza rutas;
no confundir con Windows limpio. Datos en LocalAppData/ColorStudioBetaData.

Artefactos ignorados: apps/desktop/src-tauri/target/release/bundle/nsis/. Evidencias
públicas saneadas en docs/evidence/BETA_02_*. Datos QA privados .lumaforge-local.
Inventario299 paquetes + avisos incluidos,6 avisos/conciliación binaria pendientes.
Sin original privado, respuestas, credenciales ni fotografías privadas publicadas.

PR65: https://github.com/jea27/Lut_generator/pull/65 (beta, base main).
PR66: https://github.com/jea27/Lut_generator/pull/66 (landing/comercial, base rama
beta; revisar después de65 y cambiar destino tras integración humana).
CI observada: MVP41176292962 y Studio41176292989 correctas en65;
MVP41176295996 y Studio41176295970 correctas en66. Validación roadmap65 OK.
Ninguna PR fusionada por el agente ni tarea aprobada.
Acción única67: bot6540038578 menciona @jea27, aviso observado; no afirmar
recepción física de este aviso nuevo. Marcadores65/66 evitaron duplicados al
activar ready. Notificaciones de revisión41176358165/41176358957 success.
Issues57/58/60/62 en revisión;59/61 blocked por QA externa. Sync Pages41176446357 success; JSON público leído y comprobado:42 tareas,
COL001 blocked;036/037/040/042 review;038/041 blocked. Última CI observada
de66 en15d6f08: MVP41176457682, Studio41176457662 y aviso41176457661 success.
No editar manualmente estados JSON. COL001 y P0 comercial pendientes.
QA landing HTTP200, JS válido, vistas390x844/1280x900 y slider70% verificados.
Landing local apps/landing con captura real, CC0, comparador y descarga pública
pendiente; borradores BETA_COMERCIAL en entrega separada. Publicar ramas/PR está
autorizado, no main/merge/approved/releases/visibilidad/gastos.
Bloqueos: Windows limpio10/11, calidad de retratos autorizados y hardware;
Photoshop pide sesión Adobe, Premiere sin importación probada, Resolve ausente;
licencias, nombre/titular/legal/fiscal/precio/código público antes de vender.
GO solo demostración técnica local; NO-GO beta general y venta.

Reanudar: git status; gh pr list --repo jea27/Lut_generator; leer solicitud humana
beta y sus comentarios antes de avisar; no repetir bloqueo ya notificado.
Landing local http://127.0.0.1:8792 mientras servidor propio activo; app nativa
reinstalada y abierta,8 archivos conservados también tras reinstalar.
Build: ./scripts/build_beta.ps1. Tests: ./.venv-mvp/Scripts/python.exe -m unittest
discover -s tests_mvp -v. Smoke empaquetado: scripts/smoke_beta.py requiere piloto
CC0 existente y escribe carpeta privada nueva. No borrar datos/worktrees históricos.
Siguiente tarea elegible: cerrar auditoría de licencias binaria; QA externa solo
tras acceso a entorno limpio/Adobe/medios autorizados. Sin aprobación automática.

---

# Estado del agente · LumaForge MVP v0.1 · 2026-10-30

## Checkpoint vigente · P1/P2 autorizado


Este bloque sustituye cualquier prohibición histórica de iniciar P1/P2 de los
checkpoints anteriores. El usuario autorizó explícitamente ambas fases técnicas
con P0 comercial pendiente. No cambia la aprobación de P0 ni autoriza merges.

### Tarea actual y ramas
- Motor/API COL007–012: codex/COL-007-mvp-color-local, PR52, Issues39–44.
- Medición/revisión: COL013/014, Issues45/46, aceptación completa pendiente.
- Estudio COL015–019: codex/COL-015-mvp-studio, Issues47–51, rama actual raíz,
  apilada sobre la del motor. Revisar motor primero y luego estudio.
- Todo P0 conservado, incluido checkpoint38 integrado localmente en esta rama;
  PR36/37/38 previas no son borradas ni se fusionan desde el agente.

### Trabajo completado
Aplicación ejecutable: referencia/destino JPG/PNG8; análisis real; dos métodos
Lab con límites; comparador, intensidad/controles, presets JSON, PNG/JPG original
con ICC y LUT global33³. Código separado apps/api, apps/web, packages/colour_core.
Sin API externa de imagen, costes por proceso, autenticación cloud o cambio de Pages.
Dependencias locales autorizadas e instaladas en .venv-mvp/node_modules, ignoradas.

### Pruebas y resultados
14 unittest MVP OK sin omisiones y87 existentes OK en runtime anterior. TypeScript
+Vite build OK, npm audit de instalación0 vulnerabilidades. CI backend Windows
correcta en PR52; consultar sus checks para la última revisión. UI tiene CI propia.
TestClient de Starlette emite aviso de deprecación httpx, no error de pruebas.
Roundtrip de LUT por lector trilineal independiente <2e-6 por canal; export real
4928x3264 PNG/JPG, LUT33³ y JSON. Smoke en docs/evidence/MVP_01_SMOKE.json.
GUI: importación, matching, intensidad0, comparación51%, exposición0.10,
preset/undo/restauración/importación JSON y descargas PNG/cube/JSON comprobadas.
Viewports390 y1280 sin overflow. Detalles en docs/evidence/MVP_01_GUI.md.
Aproximadamente10s/RSS785MB en export16MP observada; preview ~1s/RSS235MB.
No son garantías ni medición de memoria GPU. Originales y exportaciones privadas
no se publican ni se convierten en evidencia de mercado.

### Cambios pendientes y revisión
Revisión visual/humana de calidad y criterios completos por Issue; no autoaprobar.
COL013 aún no tiene benchmark completo por20 escenas/GPU, COL018 no tiene
miniaturas reales ni historial de sesión persistido en disco; sí presets JSON y
undo/redo en memoria. COL020/021/022 y P0 entrevistas/evaluación ciega no ejecutadas.
No RAW/Log/HDR/16bit/vídeo, máscaras/segmentación/Tauri ni prueba de .cube en
Photoshop/Premiere/Resolve. Estas extensiones solo diseñadas, no implementadas.

### Reanudar / abrir
Abrir http://127.0.0.1:8790 si sigue activo; en caso contrario doble clic en
Iniciar-LumaForge.cmd desde la raíz. Preparación en docs/MVP_V01_WINDOWS.md.
La API sirve el build de apps/web/dist (no publicar ese editor en Pages).
Servidor loopback únicamente; detener con Ctrl+C en su consola.
Copias temporales en .lumaforge-local/images y presets en .lumaforge-local/presets,
ignorados. Máximo8 imágenes; eliminar copias desde la UI cuando se alcance límite.
Originales externos intactos. Hay exports reales en .lumaforge-local/demo y en
Descargas generados por la GUI. No borrar esta información al reanudar.

Para pruebas: ./.venv-mvp/Scripts/python.exe -m unittest discover -s tests_mvp -v
Compilación: npm --prefix apps/web run build. La app sirve sin Internet después
 de preparar dependencias/build. No iniciar trabajo avanzado antes de estabilizar.
Siguiente: revisión humana del MVP y validación externa de LUT/otras escenas
con permisos, mientras P0 comercial continúa por su circuito independiente.

### Evidencia final y revisión
PR52 motor/API y PR53 Color Studio listas para revisión, sin merge por el agente.
CI backend Windows41118511892 y frontend41119407555 success; 14 pruebas MVP
ejecutadas sin omisiones. 87 pruebas de seguimiento anteriores OK.
Acción consolidada Issue54: aviso41119481395 success, comentario6532271615
menciona @jea27. Respuesta real del propietario6532291469: base técnica aceptada
para revisión; no equivale a merge ni aprobación de todos los criterios. No
repetir ese aviso. La próxima sesión debe leer Issue54 antes de nuevas peticiones.
Worktree adicional .codex-worktrees/MVP-core conserva rama motor; raíz en rama
Color Studio. Las dependencias/build y datos locales están preparados e ignorados.
La demo de navegador se deja abierta con imágenes CC0 y servidor loopback activo.

## Checkpoints históricos P0 (no sustituyen la autorización vigente)

### Archivo de investigación P0 · 2026-10-30

## Tarea actual y rama

COL-006 / Issue #19: checkpoint posterior a la preparación de investigación.
Rama raíz `codex/COL-006-checkpoint-investigacion`, base `origin/main f06efa3`.
GitHub registra que **jea27** integró PR #31, #32, #33 y el checkpoint anterior
#30. El agente no realizó esos merges. Se prepara una PR documental nueva
porque #30 ya está fusionada; no se duplica ninguna Issue canónica.

No hay autorización P1 ni decisión go. Main no se modifica directamente.
El historial anterior queda conservado, incluido `2ef5fc5`; no se sobrescribió
trabajo local ajeno. Las nuevas ramas se crearon desde origin/main en worktrees.

## Trabajo completado en esta continuación

| Frente | Entrega | Evidencia y límite |
|---|---|---|
| COL-004 / #18 / PR #31 | Fuentes y piloto CC0 reproducible | Cuatro JPEG reales, dos capturas rurales; 34.773.100 bytes, autor Sergej Majboroda/Poly Haven, licencia/URL/MD5 proveedor/SHA-256. Binarios solo locales |
| COL-003 / #17 / PR #32 | CanonCGT y métricas offline | Paper y repo oficial fijado; código/pesos Apache2.0, derechos de datasets aparte. Modelo no ejecutado. Sexto candidato documental sin sustituir los cinco exigidos |
| COL-002 / #16 / PR #33 | Formulario local y recibos privados | Q1-Q15 por etapas, precio después de Q11; JSON sin envío, verificación pendiente y deduplicación. Cero participantes contactados |
| COL-006 / #19 | Integración, aviso único, recuperación | 81 tests locales; sincronización consultada; ningún criterio aprobado automáticamente |

Documentación detallada: P0_PILOTO_FUENTES.md, P0_CANONCGT.md, P0_METRICAS.md,
P0_FORMULARIO_REAL.md y diarios por tarea. Decisiones globales en DIARIO_DESARROLLO.

### Dataset y evidencias separadas

- `.research-media/polyhaven-rural/`: cuatro JPEG originales ignorados. Índice
  público `data/p0/pilot.json`, sin binarios. Se verificaron tamaño, MD5 y SHA-256,
  decodificación y descripción ICC sRGB IEC61966-2.1 de los cuatro archivos.
- Revisión visual de previsualizaciones: no se observan personas identificables
  ni marcas destacadas. No es garantía jurídica ni revisión humana de cobertura.
- DSC_0106 plain 4928x3264 frente a pretty 4891x3255: no es target alineado.
  DSC_0181 comparte tamaño, pero eso tampoco prueba alineación. No se promueven
  variantes como ground truth ni se fuerzan registros listos en dataset.json.
- `data/p0/controls/identity-real-photo.json`: control de identidad sobre una
  fotografía real. DeltaE76=0, SSIM aproximadamente 1, PSNR infinito representado
  por null+indicador. 0,852 s mide lectura/preprocesado/métricas, no un modelo.
- Fixtures sintéticas solo prueban infraestructura. QA de formulario: R999,
  todas las preguntas omitidas, archivo en `.research-private/qa/` de la raíz;
  captura `.research-media/formulario-qa-sintetica.png`. No son respuestas reales.
- Autoinformes permanecen `self_report_form/submitted_unverified`. SHA-256 y
  fechas prueban integridad/recepción, no identidad ni consentimiento efectivo.
  No se convierten a `interview_notes`; recibos futuros solo en carpeta privada.

## Pruebas realizadas y herramientas

- Git y Node operativos; gh 2.103.3 localizado en `%ProgramFiles%/GitHub CLI/gh.exe`.
  Sesión jea27 activa con repo/workflow; REVIEWER_GITHUB=jea27 comprobado.
- Python 3.12.14 del runtime ya instalado; NumPy 2.3.5 y Pillow 13.0.0 disponibles.
  Sin instalaciones, cambios de permisos, tokens nuevos, pesos o Torch/LPIPS.
- Ramas por separado: piloto 67 tests, métricas 72, formulario 70, todos locales
  OK. Integración de las tres ramas en worktree P0-verificacion: **81 tests OK
  sin omisiones**, node --check formulario y app.js OK; merge local sin conflictos.
- Las diferencias del código integrado con main f06efa3 son nulas; solo difería
  el checkpoint documental. No se repiten pruebas numéricas sin cambios de código.
- CI PR31: run41097285452 success, 67 tests y dos omisiones por Pillow ausente.
  CI PR32: run41097288188 success, 72 tests y seis omisiones por NumPy ausente.
  CI PR33: run41097293957 success, 70 tests sin omisiones.
  Esas omisiones no se presentan como pruebas numéricas remotas ejecutadas.
- Publicación/sync tras merges humanos: run41097620802 validate y publish success.
  Dashboard leído por HTTP: 42 tareas, P0 con cinco blocked y COL-005 review;
  enlaces a PR31/32/33/30 reales. Sin edición manual de estados JSON.
- p0_status --github --ready: registros válidos y cero entrevistas, cero pares
  aceptados, cero casos de producto. Ninguna de las seis Issues P0 aceptada;
  sin IDs canónicos duplicados. Exit 2 esperado; no es fallo de infraestructura.
- Inspección de cambios publicados: sin credenciales, claves privadas, rutas
  personales de Windows ni fotografías/respuestas privadas. Autoría fotográfica
  pública conservada por trazabilidad. Binarios y QA privados ignorados por Git.

## Notificación y decisiones humanas pendientes

Una sola solicitud existente actualizada: [Issue #29](https://github.com/jea27/Lut_generator/issues/29),
con título requerido, siete campos y needs-human. Workflow manual
[41097290400](https://github.com/jea27/Lut_generator/actions/runs/41097290400) success;
bot menciona a @jea27 en [comentario6528828373](https://github.com/jea27/Lut_generator/issues/29#issuecomment-6528828373).
Marcadores de PR en esa misma Issue impiden avisos independientes repetidos.
La recepción en iPhone de avisos previos fue confirmada; la de este aviso nuevo
no se afirma sin confirmación. Un aviso o merge nunca sustituye una aprobación.

Pendiente:
1. Revisar preparación; COL-005 sigue review (#13/#15) hasta aceptación explícita.
2. Elegir distribución: se recomienda que jea27 comparta el instrumento por
   canal privado con tres personas conocidas A/B/C-D, defina responsable y plazo
   (propuesta: jea27, 30 días). Alternativa: autorización de canal/candidatos/texto
   concretos al agente. No contactar a nadie antes de esa decisión.
3. Aportar inicialmente 2-3 fotos propias para piel con permisos de autor/modelo
   y referencias con derechos claros, por rutas privadas. Faltan diversidad y
   revisión de 20 pares; no subirlos a Issues/PR/Pages.
4. Identificar herramientas/versiones del benchmark ya instaladas/autorizadas.
   No instalar ni contratar nada para sortear el bloqueo.
5. Ejecutar las 12 entrevistas reales, comparativas 5x20 y revisión humana.
   Formularios no sustituyen entrevistas; intención de pago no equivale a compra.

COL-001 y COL-002 siguen pendientes de entrevistas reales. COL-003/004/006
siguen bloqueadas en sus criterios de evidencia; ninguna tarea cerrada/approved
por el agente. P1 permanece detenido.

## Cambios pendientes y próximas tareas elegibles

Código de preparación integrado por jea27. Este checkpoint/diario se publica
para revisión en una rama documental independiente. Ver el estado actual de
su PR y checks antes de actuar: no asumir que un merge de preparación aprueba P0.

El siguiente trabajo con evidencia exige respuestas/permisos/acceso enumerados
en #29. Al recibirlos, registrar primero un lote pequeño y contrastar original,
consentimiento, autoría, perfiles y geometría. Ampliar fuentes CC0 según la
cobertura faltante; no duplicar 20 variantes rurales para aparentar diversidad.
No hay otro criterio P0 que pueda completarse inventando datos o usando fixtures.

## Ramas y worktrees preservados

| Carpeta relativa a raíz | Rama | Uso |
|---|---|---|
| raíz | codex/COL-006-checkpoint-investigacion | Recuperación vigente |
| .codex-worktrees/P0-verificacion | codex/COL-006-verificacion-investigacion | Integración local de PR31/32/33, 81 tests |
| .codex-worktrees/COL-003-metricas | codex/COL-003-metricas-canoncgt | Preparación PR32 |
| .codex-worktrees/COL-002-formulario | codex/COL-002-formulario-local | Preparación PR33 |
| .codex-worktrees/COL-002 | codex/COL-002-evidencia-entrevistas | Entrega anterior conservada |
| .codex-worktrees/COL-003 | codex/COL-003-protocolo-benchmark | Entrega anterior conservada |
| .codex-worktrees/COL-004 | codex/COL-004-manifiesto-dataset | Entrega anterior conservada |

No borrar ni recrear estas ramas/carpetas. La rama piloto sigue conservada en
Git, además de su integración humana en main. Las carpetas .research-media y
.research-private de la raíz están ignoradas también mediante exclude local.
El servidor QA se limita a 127.0.0.1 y se detiene al finalizar la revisión.

## Instrucciones concretas de reanudación

Desde esta raíz, comprobar git status/branch y leer Issue29 antes de contactar
participantes o instalar herramientas. En PowerShell, sin depender de WindowsApps:

```powershell
git status --short
git branch --show-current
git fetch origin
& "$env:ProgramFiles\GitHub CLI\gh.exe" issue view 29 --repo jea27/Lut_generator
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/p0_status.py --github --gh-path "$env:ProgramFiles\GitHub CLI\gh.exe" --ready
```

Exit 2 es lo esperado mientras falten evidencias. No subir originales, respuestas
ni contactos. Para comprobar hashes del piloto, `prepare_pilot.py --download`
reutiliza archivos existentes verificándolos; desde otra carpeta no apunta a los
medios raíz. El formulario está en research/form.html y su procedimiento en
P0_FORMULARIO_REAL.md. Abrir ramas nuevas solo para una Issue P0 elegible y
conservar siempre lo pendiente; nunca escribir directamente en main.

## Continuación · enlace web COL-005 (checkpoint de trabajo)
PR34 ya integrada en ae34ea0, árbol inicial limpio. Rama raíz actual
codex/COL-005-formulario-web. 87 tests locales OK y cuatro viewports móviles
comprobados. Source research/ y empaquetado allowlist para Pages preparados;
publicación depende de merge humano y Actions. R101/102/103 reservados sin
asignar; R999 QA privada, bloqueado en registro real. Se continúa con permisos
fotográficos/COL004 y controles CC0/COL003 sin contactar participantes.

## Checkpoint vigente · formulario web y controles P0 · 2026-10-30

### Tarea actual y rama
COL006 / Issue19, rama raíz codex/COL-006-checkpoint-formulario. Sustituye como
estado vigente las secciones históricas anteriores. PR34 estaba integrada al
iniciar; árbol limpio y sin commits pendientes respecto a main. PR35 fue
integrada posteriormente por jea27 (86d2137), no por el agente.

### Trabajo completado
- COL005/PR35: formulario público https://jea27.github.io/Lut_generator/investigacion/
  con tres códigos reservados: #R101, #R102 y #R103. Sin identidades asignadas,
  invitaciones enviadas ni respuestas reales. Consentimiento y esquema v1
  conservados. JSON solo por acción de la persona, previsualización/descarga/
  compartir con fallback; no servidor de respuestas ni nuevos proveedores.
- Allowlist HTML/JS/CSS en ambos workflows existentes; un sync posterior también
  conserva el formulario. Archivos generados ignorados. No se cambian permisos.
- COL004/PR36: guía y plantilla vacía para autoría/licencia, consentimiento de
  personas identificables, alcance interno, custodia y retirada. Cumplimentar
  solo en privado; no autoriza ninguna foto por sí misma.
- COL003/PR37: experimentos posibles y runner de controles sobre los cuatro
  originales CC0 existentes. Doce lecturas reales (tres por foto), identidad y
  repetición reproducibles. Tiempos de infraestructura, nunca inferencia.
  DSC0106 no alineado por tamaño; DSC0181 sin revisión de target pese a igual
  tamaño. Cero productos ejecutados y cero pares aceptados por esta entrega.

### Pruebas y evidencias
- Rama web: 87 unittest locales OK, sin omisiones. Rama controles: 85 OK.
- Integración en .codex-worktrees/P0-web-verificacion: **91 unittest OK sin
  omisiones**, node --check y empaquetado allowlist correctos, sin conflictos.
- Viewports locales 320x568, 390x844, 430x932 y 844x390: sin desbordamiento;
  botón >=44px, consentimiento sin premarcar. Tres etapas y JSON sintético R999
  descargado y validado, separado de participantes. Importador rechaza R999.
- Pages real: run41114395315 success. HTTP HTML/JS/CSS comparados con SHA-256 de
  blobs Git en main, coincidencia exacta. La copia Windows tiene CRLF; por eso
  se comparó contra blobs Git canónicos, sin confundir finales de línea.
- Navegador sobre HTTPS: tres etapas y descarga R999 válidas. Vista pública a
  390px también sin desbordamiento. Share: mocks de éxito/cancelación/fallo;
  no se afirma entrega ni prueba física de Safari/iPhone.
- QA sintética privada en .research-private/qa/R999-web-mobile-20261030.json y
  R999-public-pages-20261030.json. Ningún recibo de participante creado. Captura
  local en .research-media/formulario-publico-movil-qa.png; no evidencia de usuario.
- p0_status --github --ready: exit2 esperado, cero entrevistas, cero pares
  aceptados, cero runs de producto, ninguna tarea aceptada; sin duplicados.
- CI de ramas y sincronización: consultar los checks de PR35/36/37 y de esta PR;
  NumPy/Pillow ausentes en CI implican ocho omisiones opcionales explícitas.
  Las pruebas locales numéricas sí se ejecutaron. No repetir por cambios solo MD.

### Bloqueos humanos y aviso
Solicitud existente #29 actualizada, needs-human y siete campos. Un solo aviso
nuevo: run41114232338 success y comentario6531560480 menciona @jea27. PR36/37
reutilizan esa solicitud sin nuevos avisos. No se confirma recepción física de
este aviso nuevo. Se corrigió su cuerpo al conservar UTF-8 al leer JSON de gh;
no se vuelven a decodificar bytes UTF-8 con la página de códigos de Windows.

Pendiente: prueba R999 en Safari/iPhone, guardado en Archivos y devolución del
JSON sintético por canal privado. Responsable/canal/conservación para personas
reales siguen por acordar; propuesta jea27/30 días no es consentimiento obtenido.
El usuario distribuye los enlaces cuando esa información esté acordada; el agente
no contacta personas por iniciativa propia. Fotos para piel con permisos y acceso
a herramientas autorizadas siguen pendientes. COL001 no completada; P1 detenido.

### Próximos pasos elegibles y reanudación
Leer docs/P0_FORMULARIO_WEB.md para recogida/importación privada; usar
scripts/register_form_response.py solo con JSON de persona real y código asignado,
no con R999. El recibo conserva pending_human y counts_as_interview=false.
Leer docs/P0_GUIA_FOTOGRAFIAS_PERMISOS.md antes de recibir fotos y
P0_EXPERIMENTOS_PILOTO.md antes de ejecutar productos; ambas entregas en sus PR
si todavía no están integradas. Solo registrar entrevistas realmente celebradas.

Nuevos worktrees conservados dentro de .codex-worktrees/:
- COL-004-permisos: codex/COL-004-guia-permisos.
- COL-003-controles: codex/COL-003-controles-piloto.
- P0-web-verificacion: codex/COL-006-verificacion-web.
No borrar los worktrees previos. El código web está ya en main por merge humano.

Desde la raíz: git status --short; git branch --show-current; consultar Issue29.
Python explícito del runtime (comandos arriba) y p0_status --github --ready.
Para rerun de controles usar --media-root .research-media/polyhaven-rural, reporte
nuevo; no sobrescribir el informe original ni rellenar benchmark.json con controles.
No publicar JSON de respuestas, fotos, permisos firmados, contactos ni EXIF privado.


Actualización final de clasificación: las27 coincidencias de rutas se han
resuelto técnicamente como cuentas genéricas de compilación de proveedor o
placeholders/ejemplos de documentación (incluido ntpath.splitroot).0 perfiles de
origen sin clasificar. Hashes de cada archivo/contenedor cotejados con el NSIS
completo en LOOK_03_PATH_CLASSIFICATION.json. El scanner bruto conserva sus27
hallazgos y no se ocultan ni alteran DLL; no son rutas del perfil local, secretos
o datos de clientes. No constituye aprobación de COL040 ni prueba universal de
privacidad. Siguen las puertas de Windows limpio y derechos/condiciones Microsoft.


## Checkpoint independiente del dashboard · 31-10-2026

Rama codex/COL-006-product-dashboard en worktree propio, relacionada con Issue19;
la decisión P0 permanece bloqueada y las42 tareas originales intactas. No se
modifica apps/ ni packages/. Reglas/contrato en DASHBOARD_PRODUCTO.md.
Panel Color Studio con15 capacidades/8 entregables núcleo, ejes técnicos y
humanos separados, puertas beta/comercial, PR/CI, versiones y acciones humanas.
Snapshot GitHub real:8/8 alcance técnico acotado,0/8 humano,1/5 beta,0/4 venta;
ninguna release publicada o descarga autorizada. No significa producto terminado.
107 tests locales de seguimiento OK; suite de aplicación no tocada. QA navegador
1280,390,320,430 y844 sin overflow; filtros y42 tareas conservadas comprobados,
0 errores de consola. Capturas y PRODUCT_QA.json. No iPhone físico ni despliegue
de esta rama. Se conserva Pages actual hasta integración humana.
Siguiente: CI/PR de esta rama, revisar sin merge del agente; después de merge
humano verificar workflows y JSON público. Un nuevo fallo conserva snapshot
anterior y muestra antigüedad, nunca inventa éxito. Reanudar leyendo esta sección,
Issue19/67, PR de dashboard y scripts/sync_product.py. Fuente de verdad y reglas
de entrega permiten al agente actualizar capacidades en su PR sin que el usuario
edite roadmap. Estabilización de app sigue separada en PR71; runtime/QA limpia
requieren intervención de67. No aplicar approved ni release-approved:TAG.


### Conciliación del checkpoint de dashboard

Issue canónica72 [COL043], creada por el otro chat durante la ejecución; se
reutiliza sin duplicar. PR74: https://github.com/jea27/Lut_generator/pull/74.
Rama publicada sigue codex/COL-006-product-dashboard; es una operación fuera
de42 tareas y métricas. Main71 integrada por jea27(5b6a910) se incorporó a
esta rama local, conservando ambos registros del diario. Diff contra main no
cambia apps/ o packages/. CI inicial74 MVP41188254939, Studio41188254955 y
validate41188254963 success, con consulta real de GitHub sin ampliar permisos.
La nueva revisión se validará de nuevo. Coordinación73: entregar esta PR y
checkpoint antes de que otro chat tome el worktree. No merge remoto del agente.


## Checkpoint COL044 · revisión humana individual · 31-10-2026

Worktree propio COL-044-human-review, rama codex/COL-044-human-review, Issue76,
PR79: https://github.com/jea27/Lut_generator/pull/79. No apps/packages modificados,
42 tareas intactas, ninguna capacidad real aprobada, sin merge del agente.
Mis revisiones con11 capacidades reales pendientes, checklist/pasos/versión/
evidencias y observaciones en memoria. Copiar/abrir Issue y publicar conjea27;
no token en Pages. Protocolo/autenticación/límites en REVISIONES_HUMANAS.md.
Recibos por ID+huella, revocación al editar/borrar, cambios relacionados requieren
nueva revisión; labels/merges nunca aprueban capacidades. Historial de GitHub
conservado; notas no se copian al JSON público. Cola para agente sin prometer24/7.

126 tests de seguimiento+37 MVP locales OK, JS válido, demo real en Issue77:
approval6541989840 → Actions41191045868 → estado QA aprobado; cambios6542024460
→ Actions41191317941 → Correcciones solicitadas; replay41191386973 no reactivó
aceptación ni duplicó recibos(2). Los3 jobs de Pages quedaron omitidos. Artefactos
reales verifican0 aprobaciones de producto. HUMAN_REVIEW_DEMO.json/capturas5
anchos sin overflow y0 errores. No iPhone físico ni nueva beta/instalación.

Pendiente: CI final/revisión humana de PR79. issue_comment y publicación del
nuevo flujo necesitan integración humana en main; solo demo de rama validada,
no afirmar ya activado en Pages. Tras merge humano, repetir únicamente demo y
comprobar evento real+sync+HTTP público. No merge para forzar una prueba.
Reanudar: git status en esta rama; gh pr checks79; leer Issue76 y PR79. Conservar
worktrees/documentación anteriores. No emitir approve sobre capacidades reales.

## Checkpoint vigente · COL045/046/047 · 31-10-2026

Tarea: primera entrega Creator/Pro/Shot Planner con seguridad local. Rama
codex/COL-045-creator-pro, worktree COL-045-creator-pro desde main8674566.
Issues81/82/83. No tocar raíz codex/COL-013-estabilizacion-beta3 ni otros worktrees.
Project OS/COL048 se está tratando en otro chat; no modificar su código web.

Completado para revisión técnica: modos guiado/técnico sobre motor compartido,
catálogo de capacidades/proveedor local, preview obligatoria de receta actual,
acabado manual conservado, plan local con límites/fuentes/diagrama/JSON. No hay
recuperación fiel del rodaje ni aprobación visual/profesional. Se mantienen las
42 tareas y los denominadores MVP8/beta/venta;18 capacidades en el catálogo.

Pruebas:58 unittest API/motor,128 seguimiento,3 Node y build Vue/TS correctos.
Ocho tests de planner se repitieron tras añadir etiquetas, ya incluidos en58.
QA funcional de navegador y seis medidas móviles/pequeñas más escritorio,
0 errores de consola; feedback local con CSP permitido. PNG/JSON descargados
se verificaron en privado, sin datos personales. Capturas y hashes en
CREATOR_045_QA.json y SHOT_PLANNER_047_*.jpg. Fuentes y uso en
CREATOR_PRO_SHOT_PLANNER.md. Plan JSON se exporta pero no se reimporta todavía.

Dos fotos CC0 de16MP perfiladas; DSC0106 coincide con input/receta/PNG previo,
16.912s esta vez. DSC0181 22.097s es otro input. No promedio o mejora universal;
ni tile mayor ni cambio de matemática adoptados. Perfiles/scope versionados.
OSV566 y npm audit:2 paquetes Cargo con avisos globales, ninguno en árbol
Windows223. No se ocultan ni se sustituyen paquetes sin comprobar plataforma.

PR86 en borrador: https://github.com/jea27/Lut_generator/pull/86.
Rama publicada, tres capacidades enlazadas a esta entrega. Trabajo local
completado para revisión; consultar borrador/lista y últimos checks en PR86.
La aceptación humana y las puertas de distribución siguen pendientes. No merge/aprobación del agente. La producción
de Mis revisiones (#79) sí fue activada y validada tras el merge de jea27:
https://github.com/jea27/Lut_generator/issues/76#issuecomment-6542238759.

Bloqueos humanos: #67, preparar runtime oficial aislado requiere autorización
expresa pendiente; Windows10/11 limpio y Adobe/Resolve activados requieren entorno
real. No reinstalar herramientas ni instalar virtualización para sortearlo.
Autoría/consentimiento/canal del piloto siguen pendientes. Ningún nuevo NSIS,
release, venta o participante. No inferir que un merge aprueba esas puertas.

Reanudar desde este worktree: git status --short; leer Issues81/82/83 y PR
asociada; comprobar CI antes de modificar. Python disponible en el entorno MVP
compartido, Node existente mediante junction node_modules ignorada. Para preview:
`& ../../.venv-mvp/Scripts/python.exe -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8817 --no-access-log --no-proxy-headers`.
El servidor solo sirve esta rama y usa datos ignorados propios.
Leer el protocolo y las evidencias antes de ampliar funciones. Próximo paso:
revisión de esta entrega y resolver #67; después validar el plan con escena y
medios autorizados reales, sin afirmar que la demo rural reconstruye un rodaje.

### Recuperación de publicación — PR86

Código3761999 publicado, CI41210911012/41210911018/41210911004 y sincronización
41210911087 success. Manifiesto enlaza las3 capacidades nuevas a PR86 sin
presentarlas como implementadas en main. Colector real de GitHub validado en
lectura; evidencia CREATOR_045_SYNC.json, archivos generados originales restaurados
por bytes. Revisión de Color Match/lotes/receta/Windows queda obsoleta en el
candidato por huellas relacionadas, conservando historial previo. Producción
sigue en main8674566 hasta integración humana. No publicar porcentajes locales
como si fueran el dashboard real. El código y la evidencia quedan publicados en la rama. El estado final
de CI/PR y el único aviso de revisión se registran en el último comentario
de Issue81 y en PR86; consultarlos antes de actuar. No asumir un merge o
aprobación humana a partir de este checkpoint histórico.
