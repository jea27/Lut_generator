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
