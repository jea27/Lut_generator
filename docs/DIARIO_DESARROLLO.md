# Diario de desarrollo y decisiones

> Codex debe añadir una entrada breve y verificable por entrega. No borrar entradas anteriores ni atribuir pruebas no ejecutadas.

## 2026-10-30 · [COL-005] Actualización comercial y comercialización España/UE
- Trabajo aislado en `.codex-worktrees/COL-005-investigacion-comercial-ue`, rama `codex/COL-005-investigacion-comercial-ue`, creada desde `origin/main` (86d2137); raíz compartida estaba limpia en `codex/COL-015-mvp-studio`. No se tocaron `apps/` ni `packages/`.
- GitHub consultado antes de empezar: COL-005 Issue #13 abierta con `status:review`, aviso de revisión #15 ya existente y PR #14/35 integradas. Se conserva el estado `review`; no se duplica Issue ni notificación.
- Fuentes oficiales de producto consultadas 30-10-2026: Luttie, fylm.ai, Colourlab Ai 4 y Neurapix. Hallazgo: modelos freemium, pase temporal, pago por foto, suscripción anual/mensual y perpetua; Colourlab tiene tarifas incompatibles entre su página de producto y documentación de licencia, y declara Windows pendiente. Importes y discrepancias quedan delimitados en `docs/P0_COMERCIAL_ESPANA_UE.md` y resumidos en los competidores del roadmap; no son compras ni benchmark ejecutado.
- Se documentó una matriz inicial de venta B2C España/UE: LSSI/consumo, descarga y desistimiento, conformidad digital, IVA/OSS, RGPD/medios, cookies, accesibilidad y licencias. Es desk research, no asesoría jurídica/fiscal; no se abrió checkout, no hay precio acordado ni venta.
- El estímulo de 49 € de COL-005 queda intacto; se recomienda contrastar uso episódico frente a licencia local, pase por proyecto y suscripción ligada a servicio recurrente. Sigue sujeto a revisión de la Issue #15. No hay entrevistas, compra o conversión nuevas.
- No se alteró manualmente ningún estado de `site/data/roadmap.json`; solo campos descriptivos de precios de competidores. `git diff --check` pasó y el parser Python del runtime del proyecto cargó el JSON correctamente. No se ejecutaron tests (cambio documental). PR #55 abierta; checks validate/notify quedaron queued en primera consulta.
- El evento `pull_request.opened` ganó la carrera a la actualización del marcador y el workflow creó Issue #56 con needs-human y un aviso. Se editó #56 para dirigir a la solicitud consolidada #15, sin cerrar Issues ni retirar/reaplicar etiquetas; #15 conserva la misma revisión para #14/#55. No se envió una notificación manual adicional.

## 2026-10-30 · Handoff inicial
- Estado: se entrega starter de roadmap + material de contexto y workflows de notificaciones; motor de edición todavía NO implementado.
- Decisión: arquitectura local-first, motor de color determinista, IA local opcional, soporte foto + vídeo.
- Control: GitHub Issues/PR y revisión humana antes de `main`.
- Bloqueos: no hay repositorio remoto, usuario de notificación, ni publicación Pages configurados.

## 2026-10-30 · Corrección de estructura del repositorio
- Solicitud directa de mantenimiento, sin iniciar ni modificar tareas COL.
- Rama local: `codex/fix-repository-root`; sin PR ni push.
- Movidos los 24 archivos versionados de `lumaforge/` a la raíz; conservados `.git`, historial, documentación y las 42 tareas con sus estados.
- Actualizadas README, guía Windows y prompt inicial para usar `jea27/Lut_generator`, manteniendo LumaForge como nombre provisional. Rutas de workflows y scripts revisadas; no necesitan cambios de contenido tras el traslado.
- Pruebas: 11 unittest OK, importador DRY RUN de 42 tareas, sintaxis JS OK, ambos YAML válidos y recursos HTTP con respuesta 200 bajo `/Lut_generator/`.
- Consulta Pages de solo lectura: `build_type: workflow`. Sin cambios remotos; despliegue real pendiente de aprobación, push e integración humana en `main`.
- Evidencia, limitaciones y commit propuesto: `docs/REESTRUCTURACION_RAIZ.md`.
- Autorización posterior del usuario: crear commit, subir esta rama y abrir PR hacia `main`; sin merge ni cambios de configuración remota. El enlace y el resultado de publicación se registran en la entrega de la sesión y en la PR.

## 2026-10-30 · Separar validación PR y despliegue Pages
- Solicitud directa del usuario para actualizar la PR #1 en `codex/fix-repository-root`.
- Causa verificada: Pages rechazaba el despliegue del ref de la PR por las protecciones del entorno.
- Job `validate` para PR/push con lectura y pruebas; job `publish` solo en push a `main`, condicionado a validación correcta y con entorno/permisos Pages propios. Checkout del commit del evento; artefacto `site/` y base `/Lut_generator/` conservados.
- Eliminados disparadores Issues/cron/manual. La sincronización de estados ahora se publica con el siguiente push a `main`; guías actualizadas.
- Evidencia local: 11 pruebas OK, sintaxis JS y JSON OK, YAML y contrato de eventos/permisos/rutas comprobados, diff sin errores. Detalles en `docs/REESTRUCTURACION_RAIZ.md`.
- Autorizado commit y push a la rama de la PR; sin merge ni modificación de protecciones. Despliegue real pendiente de integración humana.

## 2026-10-30 · [COL-001] Validación real de notificaciones humanas
- Solicitud expresa: configurar y comprobar avisos de jea27/Lut_generator, crear PR de la entrega y detener solo trabajo dependiente de autorizaciones.
- Rama independiente: `codex/COL-001-validacion-avisos` desde origin/main. Conservada sin cambios la rama local anterior de preparación P0.
- GitHub CLI localizada en `C:\Program Files\GitHub CLI\gh.exe`, autenticada como jea27. Variable existente REVIEWER_GITHUB=jea27 consultada; no se cambió.
- Issue de prueba #3 creada con opciones y recomendación, y etiquetada needs-human después de la pregunta: https://github.com/jea27/Lut_generator/issues/3.
- Workflow real https://github.com/jea27/Lut_generator/actions/runs/41079364488: success; job notify y paso de mención correctos.
- Mención del bot verificada: https://github.com/jea27/Lut_generator/issues/3#issuecomment-6526303053.
- Usuario confirmó en el chat: «Sí, recibida en el móvil». Recorrido por needs-human validado; ninguna aprobación de producto se infiere de la recepción.
- Actualizados AGENTS.md, protocolo y texto del bot: solo se detiene el trabajo dependiente; continúan tareas independientes autorizadas.
- Sin cambios de permisos, protecciones, tokens ni configuración del móvil; sin merge, cierres ni etiquetas approved. COL-001 sigue pendiente de entrevistas; esta entrega es preparación de seguimiento.
- Limitación: prueba real del recorrido por etiqueta, no de fallos críticos ni del disparador manual.
- Verificación de la entrega: 11 unittest OK con Python incluido en Codex; diff sin errores. Texto y evidencias de PR en `docs/PR_VALIDACION_AVISOS.md`.
- PR publicada: https://github.com/jea27/Lut_generator/pull/4. Su primer aviso de revisión falló con 403 al comentar en la PR; no se ampliaron permisos. Corregido para crear Issue de revisión vinculada, con opciones/recomendación, needs-human y mención; deduplicación por PR y evento synchronize.
- Corrección comprobada realmente: run https://github.com/jea27/Lut_generator/actions/runs/41080088759 success; bot creó Issue #5 y mención https://github.com/jea27/Lut_generator/issues/5#issuecomment-6526363671. CI validate success en run 41080088573, sin despliegue desde PR.
- Añadidas pruebas del script exacto de Actions con dobles de API; no requieren permisos ni red.
- Suite ampliada ejecutada: 15 unittest OK (incluye aviso en Issue, login inválido y deduplicación). El aviso de revisión utiliza los permisos originales; la integración en main queda a revisión humana en PR #4.

## 2026-10-30 · [COL-001] Preparación oficial local de P0
- Solicitud del usuario: preparar entorno y seguimiento, comenzar P0 y pedir autorización antes de escrituras remotas.
- Estado inicial limpio, raíz correcta, remoto jea27/Lut_generator; PR #1 integrada y despliegue main verificado success. Cero Issues COL en la consulta inicial.
- Rama: `codex/COL-001-preparacion-p0` desde origin/main `fa9883e`; sin push ni PR nueva.
- Preparados comprobador Windows, sincronización por eventos desde main, reglas de estado y fallback, avisos de revisión/decisión/fallo y documentación de operación. No se han cambiado configuración ni permisos remotos.
- Evidencia: 17 unittest y 8 pruebas Node OK; DRY RUN 42 tareas; YAML sin duplicados y contratos de eventos/permisos correctos; prueba negativa del comprobador exit 1. Navegador publicado: filtro P0 y detalle COL-001 correctos.
- COL-001: guion de entrevistas, segmentos candidatos y registros anonimizados; ninguna entrevista realizada. Criterio de aceptación aún pendiente. Las 42 tareas versionadas conservan sus estados originales.
- gh no disponible; autenticación, REVIEWER_GITHUB y recepción móvil no verificadas. Aviso histórico skipped no demuestra envío.
- Decisión: preparar PR parcial sin cierre automático de Issue. Publicación, etiquetas, Issue y prueba móvil pendientes de autorización; merge y aprobación a cargo humano.
- Informes: `PREPARACION_DESARROLLO.md`, `P0_COL-001_SEGMENTOS.md`, `PR_COL-001_PREPARACION.md`.
- Motor sin iniciar; siguiente paso local de producto: recoger evidencia P0 antes de COL-006.

## 2026-10-30 · [COL-001] Publicación autorizada de la preparación P0
- Autorización explícita de publicar la rama codex/COL-001-preparacion-p0, crear Issue y abrir PR; sin merge ni aprobación propia.
- Incorporado origin/main 871a37c preservando el workflow de avisos de PR #4 y el protocolo humano. Retirado el manejador previo no usado; conflictos resueltos en la rama de trabajo.
- Issue canónica #6: https://github.com/jea27/Lut_generator/issues/6, abierta, roadmap y status:in-progress; faltan entrevistas reales y mapa validado.
- gh localizado ya instalado en %ProgramFiles%/GitHub CLI/gh.exe y autenticado. Sin reinstalaciones ni cambios de permisos.
- 21 unittest OK, sintaxis JS correcta; búsqueda de secretos y revisión de archivos públicos sin hallazgos en la entrega. Rutas de perfil sustituidas por placeholders; historial local preliminar conservado en respaldo local y publicación consolidada desde main con identidad noreply.
- La sincronización de esta entrega reutiliza una ejecución de main ya desplegada; no se edita JSON para simular progreso. El nuevo refresco por eventos solo se activará después de integración humana.
- Informe y límites: PUBLICACION_COL-001.md. Los enlaces de PR y ejecuciones reales se registran en la Issue y en la entrega del chat tras crearse.
- PR #7 abierta: https://github.com/jea27/Lut_generator/pull/7; CI run 41081007929 success con 21 tests OK. Aviso run 41081007870 success, mención a jea27 en Issue #8.
- Repetición del workflow existente de main, run 41080377557 intento 2: validate y publish success. JSON publicado comprobado con COL-001 review, Issue #6 y PR #7; no completada ni aprobada. Sin push ni merge a main.

## 2026-10-30 · [COL-001] Retomar publicación y revalidar Mobile sin duplicados
- Comprobados git status limpio, rama activa codex/COL-001-preparacion-p0, HEAD local y remoto coincidentes en 944e67c; trabajo conservado. Issue #6 y PR #9 reutilizadas, sin duplicar.
- gh 2.103.3 autenticado como jea27; REVIEWER_GITHUB=jea27 comprobado. Sin reinstalaciones, cambios de permisos ni configuración sensible.
- 21 unittest locales OK. Checks previos de PR #9 correctos; sincronización automática run 41081400237 success.
- Nueva prueba real en Issue #3: pregunta con opciones/recomendación antes de retirar y volver a aplicar needs-human. Run 41081563516 success, mención https://github.com/jea27/Lut_generator/issues/3#issuecomment-6526618289.
- Usuario confirmó «Sí, recibido en el móvil». Recepción registrada como prueba, nunca como aprobación.
- JSON público comprobado con COL-001 review, Issue #6 y PR #9; no completada. Actualizado por workflow, sin editar estados manualmente.
- Informe: docs/REVALIDACION_AVISO_COL-001.md. Evidencias publicadas en la misma rama/PR autorizadas. Sin merge, aprobación, cierre de Issue ni inicio del motor.

## 2026-10-30 · [COL-005] Hipótesis y cuestionario de disposición a pagar
- Árbol local limpio; documentación anterior conservada e incorporada en origin/main 43e2480 (PR #11 integrada por jea27). No había cambios pendientes que sobrescribir ni fue necesario duplicar documentación.
- Rama independiente codex/COL-005-hipotesis-negocio desde origin/main. Issue canónica creada tras comprobar que no existía: https://github.com/jea27/Lut_generator/issues/13, roadmap y status:in-progress.
- Preparadas tres hipótesis falsables: problema recurrente, valor de portabilidad y compra real futura. Umbrales exploratorios propuestos, denominador y refutación explícitos; sin cambiar arquitectura ni puertas de fase.
- Cuestionario neutral de 15 preguntas y actas vacías; conducta antes del concepto y precio. 49 € es estímulo hipotético de investigación dentro de la banda heredada, no precio comercial, oferta, cobro ni gasto autorizado.
- Decisión: separar señal declarada de compra real. Preparar el instrumento no requiere terminar COL-001; ejecutarlo depende de entrevistas reales COL-001/COL-002. El piloto comercial necesita autorización y un entregable real.
- Sin entrevistas nuevas, participantes reclutados, compras, citas ni resultados inventados. COL-001 y su Issue #6 siguen pendientes, sin approved; motor sin iniciar y paso a P1 reservado al usuario.
- Validación de la entrega: 21 unittest existentes OK y diff sin errores; revisión manual de trazabilidad entre hipótesis, preguntas y criterios de refutación. Pruebas/ejecuciones remotas se registran en Issue y PR al terminar.
- Documentos: P0_COL-005_HIPOTESIS_NEGOCIO.md, P0_COL-005_CUESTIONARIO.md y PR_COL-005.md. Revisión humana solicitada sobre instrumento, umbrales y precio de investigación, sin autoaprobación.
- Otras P0: COL-003 requiere dataset y comparativas reales; COL-004 aún requiere medios con derechos; COL-002 requiere participantes reales. Ninguna se declara completada por preparar documentos. COL-006 no se inicia sin evidencia.

## Plantilla para próximas entregas

### AAAA-MM-DD · [COL-XXX] Título
- Rama / PR:
- Qué se implementó:
- Tests (comando, resultado):
- Decisiones y cambios de alcance:
- Riesgos / pendientes:
- Próximo paso propuesto:

## 2026-10-30 · [COL-006] Coordinación autónoma y formato de avisos
- Rama codex/COL-006-coordinacion-p0; Issue #19. Estado de recuperación guardado antes de avanzar con worktrees independientes de COL-002/003/004.
- COL-005 conciliada: PR #14 integrada y Issue #13 abierta sin approved significan review. Se sustituyó status:in-progress por status:review; no se cerró ni aprobó. Issue #15 reutilizada con formato concreto sin repetir el aviso.
- Avisos propuestos: título LUMAFORGE ACCIÓN REQUERIDA, siete campos, contenido no vacío, CRLF aceptado y deduplicación por PR/contenido. Modo manual con Issue explícita y sin interpretar entradas como código.
- 27 unittest OK. Permisos del workflow conservados; sin cambios de configuración sensible ni tokens. Puerta P0 documentada como pendiente, nunca como go.
- Checkpoint 1: COL-004 preparada en worktree, 30 unittest OK y cero medios listos; se continúa con COL-002/003.

## 2026-10-30 · [COL-006] Auditoría integrada de P0 y cierre de evidencia
- Continuadas entregas independientes: COL-004 PR22 (integridad), COL-002 PR23 (actas) y COL-003 PR26 (benchmark); GitHub registra integración por jea27. Detalles en docs/diario/COL-002.md, COL-003.md y COL-004.md. No se ejecutó merge por el agente.
- Integradas de forma segura en la rama de coordinación, sin sobrescribir documentación ni datos. Añadido p0_status.py, de solo lectura: resume registros y aceptación GitHub, ignora Issues de aviso y falla cerrado con duplicados/lectura no disponible. Nunca concede P1.
- Corregido un caso de permisos de dataset: basis no textual/vacía no cuenta como registro de uso completo.
- 64 unittest OK. Comprobación real de readiness: 0 entrevistas, 0 pares, 0 ejecuciones; los tres validadores y p0_status --github --ready devuelven 2, esperado. Las seis Issues P0 siguen sin aceptación humana.
- Fuentes oficiales de COL-003 muestran diferencia entre landing antigua y requisitos actuales de Colourlab v4; no se presupone disponibilidad ni se instalan herramientas.
- Checkpoint completo en ESTADO_AGENTE.md. Siguientes pasos requieren revisión, actas, medios con permiso y acceso autorizado; no se inventa progreso ni se inicia P1.

### Checkpoint remoto de la sesión intensiva
- PR #28 de auditoría/recuperación publicada; run41091623916 success con 64 tests. Se prepara para revisión sin fusionarla.
- Una solicitud de insumos reales en Issue #29, título LUMAFORGE ACCIÓN REQUERIDA y siete campos completos, creada antes de needs-human. Run41091807276 success; bot menciona a jea27 en comentario6528069841. No se afirma recepción física de este aviso nuevo ni se interpreta como aprobación.
- Las Issues #6/#16/#17/#18/#19 están blocked; #13 en revisión. Todas siguen abiertas y sin approved. Sincronización run41091807163 success; estado publicado se comprueba al terminar.
- No queda ejecución P0 con entradas disponibles: continuar exige actas, medios/permisos o acceso autorizado. Se preservan todos los worktrees y commits; ESTADO_AGENTE contiene comandos y dependencias para reanudar.

## 2026-10-30 · [COL-006] Continuación de investigación P0 y checkpoint
- Se preservó trabajo anterior; nuevas ramas independientes COL-004-piloto-trazable, COL-003-metricas-canoncgt y COL-002-formulario-local. PR31/32/33 integradas por jea27 durante esta sesión; PR30 anterior también integrada por jea27. El agente no fusiona ni aprueba.
- Piloto: cuatro JPEG reales CC0 de Poly Haven/Sergej Majboroda, 34.773.100 bytes, licencia/procedencia/tamaño/MD5/SHA-256/decodificación y descripción ICC comprobadas. Imágenes solo locales. Variantes de una captura no se asumen ground truth; DSC_0106 difiere en geometría. Cobertura de piel/diversidad/20 pares pendiente.
- CanonCGT investigado mediante paper y repositorio oficial fijado a 229a7d3ec24af19ea5d97bb136f0317762bb9261. Código y pesos Apache2.0, datasets/presets con condiciones propias. Sexto candidato documental; no se ejecuta ni adopta arquitectura P1.
- Métricas offline ΔE76 D65/PSNR/SSIM/gradientes, repetibilidad y estadística de tiempos con contratos de alineación, ICC y hashes. Control de identidad sobre foto real = infraestructura, no calidad del producto. Sin instalaciones, pesos ni Torch/LPIPS.
- Formulario Q1-Q15 local por etapas, descarga JSON sin envío. Recibos privados y controles de duplicados; autoinforme no se convierte a entrevista. QA sintética R999 separada, cero participantes contactados y cero entrevistas nuevas.
- 81 unittest locales en integración sin omisiones; JS comprobado. CI separada: PR31 67 con 2 omisiones Pillow, PR32 72 con 6 omisiones NumPy, PR33 70 sin omisiones; todos success. Publicación/sync run41097620802 success tras merges humanos. Dashboard HTTP: 42 tareas y P0 5 blocked/1 review. No se falsificó JSON.
- Solicitud #29 reutilizada: decisión de distribución/canal/responsable/conservación, primeros medios propios con derechos y acceso ya autorizado. Una ejecución manual 41097290400 success, mención @jea27 en comentario6528828373; sin afirmar recepción física nueva. No repetir aviso por marcadores de PR.
- p0_status --github --ready mantiene 0 entrevistas, 0 pares aceptados, 0 casos de producto, cero tareas P0 aceptadas, exit2 esperado. COL-001 pendiente, COL-005 review; no hay permiso P1. ESTADO_AGENTE actualizado con rutas privadas ignoradas, ramas, pruebas y pasos para reanudar.

## 2026-10-30 · [COL-005] Preparar enlace de investigación y QA móvil
- PR34 integrada; raíz limpia y sin commits pendientes. Rama codex/COL-005-formulario-web desde origin/main ae34ea0.
- Allowlist HTML/JS/CSS hacia site/investigacion en ambos workflows existentes. Sin nuevos permisos ni proveedor; no se modifica main ni se fusiona.
- Consentimiento original conservado; exportación JSON voluntaria con compartir por función disponible y fallback de descarga. Respuestas en memoria; se aclara registro técnico de IP por Pages.
- Códigos R101/R102/R103 reservados y sin asignar. R999 solo QA, rechazado por el registro de participantes. Recogida privada documentada.
- 87 unittest locales OK. Cuatro tamaños móviles emulados sin overflow, controles >=44px, consentimiento sin premarcar; tres etapas y JSON sintético descargado/verificado, sin respuestas reales. Share probado con mocks; Safari/iPhone físico pendiente.

## 2026-10-30 · [COL-006] Enlace publicado, permisos y controles verificables
- PR34 revisada/integrada al inicio; sin cambios ni commits pendientes en raíz. PR35 del formulario integrada por jea27 durante la sesión, no por el agente. Pages run41114395315 success: /investigacion/ disponible, HTML/JS/CSS coinciden con hashes de blobs Git.
- Flujo HTTPS y descarga R999 sintética válidos. QA en 320/390/430 y paisaje; sin overflow ni consentimiento premarcado. Importador bloquea R999; originales QA privados, sin respuestas reales. Safari/iPhone físico pendiente, no se confunde con emulación.
- PR36 guía de incorporación/consentimiento fotográfico y plantilla vacía, sin permisos ficticios ni medios nuevos. PR37 controles reales de los cuatro JPEG CC0: 12 lecturas, identidad/repetición reproducibles, tiempos solo de infraestructura. Sin ground truth inventado ni productos ejecutados.
- 91 unittest en integración local sin omisiones; empaquetado y JS correctos, integración sin conflictos. CI tiene ocho omisiones opcionales por dependencias ausentes, documentadas. No instalaciones, proveedor nuevo ni cambios de permisos.
- Issue29 reutilizada para revisión/prueba iPhone/canal/responsable/conservación. Workflow41114232338 success, bot6531560480 menciona jea27. Una sola mención nueva; marcadores evitan avisos por PR36/37. Cuerpo conservado como UTF-8 al consultar gh.
- Puerta P0 mantiene 0 entrevistas, 0 pares aceptados y 0 casos de productos, exit2 esperado y ninguna tarea aprobada. COL001 pendiente. No se inicia P1 ni se fusionan PR por el agente. Recuperación detallada añadida a ESTADO_AGENTE.

## 2026-10-30 · [COL-007] Autorización y MVP real P1/P2
- El usuario autoriza expresamente desarrollo P1/P2 con P0 comercial incompleta. Registrado en AGENTS y DECISION_MVP_P1_P2; no se interpreta como cierre de P0 ni aprobación de tareas.
- Núcleo independiente en packages/colour_core y FastAPI en apps/api: JPEG/PNG8/EXIF/ICC, estadísticas Lab/luminancia/histogramas/paleta, baselines Lab statistics y mean-only acotados, intensidad y ajustes globales. Receta horneada33³ y render trilineal por esa misma LUT; sin adaptación escondida al exportar.
- Archivos reales PNG/JPG4928x3264 con ICC, .cube y JSON generados a partir de fotos CC0 locales; no se publica ninguna fotografía. Reporte MVP_01_SMOKE con hashes/tiempos/RSS, no validación comercial. Export original ~9-11s y ~785MB RSS muestreado en esa ejecución; no GPU ni pico exacto.
- 14 unittest MVP OK: identidad/intensidad0, primarias D65/roundtrip, extremos/monotonicidad, alfa/EXIF/ICC, dos baselines, LUT trilineal <2e-6, API/JSON no finito/origen/formatos/presets/limpieza. Suite existente87 OK; P0 no cambia.
- Dependencias autorizadas aisladas en .venv-mvp y fijadas; Node/Vue/Quasar con package-lock. CI Windows de backend en PR52, sin ampliar permisos ni modificar Pages.

## 2026-10-30 · [COL-015] Color Studio funcional
- Vue3/TypeScript/Quasar en apps/web, Vite8 compilado, FastAPI sirve el build local. UI oscura con paneles, importación real, comparador sincronizado con zoom, intensidad/controles, undo/redo30 estados de sesión y biblioteca JSON persistente local.
- GUI real: dos importaciones CC0, matching, intensidad0/100, comparación, exposición, guardar/aplicar preset, undo e importar receta; PNG4928x3264 y LUT33³/JSON descargados y verificados. JPG real probado por API. Captura/artefactos se mantienen locales e ignorados.
- Iniciar-LumaForge.cmd y setup_mvp.ps1 permiten preparación/arranque Windows sin cambiar PATH ni políticas. Instalación inicial necesita Internet; procesamiento posterior no usa Internet ni tokens. No hay IA avanzada, FFmpeg, Tauri o editores externos implementados.
- Interfaz en rama apilada sobre motor; integra también el checkpoint P0 pendiente de PR38 sin sobrescribir su contenido. No merge remoto ni approved por el agente. Revisión y límites completos en MVP_V01_WINDOWS y MVP_COLOR_CONTRACT.


## 2026-10-31 · [COL-036] [COL-037] Candidato beta Windows
- Con autorización explícita se instalaron Rust1.99.1, C++/SDK de Microsoft, PyInstaller6.22.3 y Tauri2; WebView2 existía. No permisos de repositorio, compras o reinstalación gh.
- Implementación real: NSIS por usuario con frontend+motor, sesión loopback protegida, supervisión PID e instancia única, presets CRUD/grupos, ES/EN, demo CC0, lotes cancelables y escritura atómica/recuperación interrupted. Sin updater/rollback automático ni efectos Look Match.
-23 tests MVP,91 de seguimiento tras incorporar main a7a8df8, build TS/Vite/nativo OK. Pipeline candidato manual preparado, no ejecutado remotamente ni release publicada.
- Smoke binario real4 paisajes CC0 de16MP, exports11.4–13.7s/RSS789–804MB, lote2, ICC/dimensiones/hashes intactos, watchdog OK. Instalación/desinstalación exit0,8 archivos privados conservados por hash, sin procesos huérfanos. Codex/MSIX virtualizado, no Windows limpio.
- PR52/53 y63/64 integradas por jea27 durante la sesión; cambios incorporados sin sobrescritura. Investigación P0 y propuesta Look Match conservadas; sin entrevistas/respuestas nuevas ni autoaprobación.
- Inventario299 entradas/avisos incluidos; seis avisos y revisión binaria pendientes. SHA256, inputs dirty declarados y límites en BETA_02_*; no firma ni reproducibilidad bit a bit.


## 2026-10-31 · [COL-040] [COL-042] Revisión y preparación comercial
- PR65 beta y PR66 landing/borradores listas para revisión; no merge. CI MVP/Studio correctas en ambas. Estados57/58/60/62 review,59/61 blocked; ninguna tarea aprobada.
- Landing independiente local HTTP200, vistas390/1280, comparador70% funcional, captura auténtica y derivadosCC0 con hashes; descarga pública pendiente. Sin despliegue/cobros. Borradores legal/privacidad/EULA/soporte, estrategia código público/marca/firma/pago sin activación. Conserva P0_COMERCIAL_ESPANA_UE y LOOK_MATCH_REQUIREMENTS integrados.
- Notificación única Issue67, comentario bot6540038578 menciona jea27; recepción nueva no confirmada. Marcadores PR65/66 previos a ready evitaron avisos duplicados. Runs41176358165/41176358957 success. Reinstalación comprobada,8 archivos privados intactos; checkpoint ESTADO_AGENTE actualizado.

- Sync final41176446357 success; JSON público42 tareas verificado (BETA_02_SYNC.json). CI66 en15d6f08: MVP41176457682/Studio41176457662/aviso41176457661 success. Advertencias Actions de migración Node20/Ubuntu26 observadas, sin fallos ni permisos nuevos.

## 2026-10-31 · [COL-026] Acabado manual, auditoría de candidato y QA externa
- PR65/66 auditadas abiertas con CI correcta; Issue67 sin nueva autorización. Rama independiente/Issue68, sin completar P3 ni P0 comercial.
- Look manual: glow/difusión/fade, receta v2 compatible con v1 sin efectos, bypass/intensidades separadas, render/lotes/JSON y LUT solo color con aviso. Halation y análisis automático pendientes.
-30 tests MVP/91 tracking y build TS/nativo OK. Smoke empaquetado: efectos, lote2, PNG byte-identical y feedback incluido. Foto CC0 de16MP:32.392s con PNG/RSS815.4MB, originales intactos. No benchmark de piel/usuarios.
- Corregidas rutas nativas (155→0), selección incorrecta de hash por glob y desplazamiento de paneles. Inventario299/0 avisos ausentes; payload27 patrones proveedor/ejemplos aún sin clasificación, scope NSIS/condiciones Microsoft pendiente. No declarar ausencia universal de PII.
- Setup0.3 limpio desde396a508, SHA256 ae47f44e6f9382810e20a7a98b0b46bf6d53411e7f1c8b0fb2e9c7acf595ac21,266203035 bytes. Upgrade local exit0/8 archivos conservados y arranque nativo. No VM limpia, firma ni release.
- Preparados preflight, guía, cinco recorridos, feedback offline y bundle lossless de LUT. QA00 sintético descargado/separado; ningún participante contactado. Photoshop sin documento/editor verificable; no compatibilidad real afirmada. GO/NO-GO privado y venta separados.

- Cierre beta2: feedback nativo con iframe (sin popup ni pérdida de sesión), migración GUI de presetsv1→v2 con glow/exportJSON verificada. Candidato limpio a452a5f,266211731 bytes, SHA256 3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f. Upgrade preserva8 archivos.
-7-Zip portátil oficial autorizado: extracción segura del SFX como archivo, sin ejecutar instalador/MSI. NSIS176 entradas auditadas; WebView2 firma Microsoft válida; pluginTauri0.5.3 coincide SHA oficial. Diferencia nativo empaquetado3 bytes UNK→NSS validada contra fuenteTauri.27 patrones de rutas proveedor/ejemplo (2 genéricos/25 pendientes),0 perfiles locales/tokens/dev. Avisos NSIS/plugin preparados como acompañantes; licencias Microsoft/privacidad no autoaprobadas.
- Premiere intentado: selector de suscripción; sin compra/prueba activada. Photoshop sin editor accesible. Importación externa pendiente. PR69 nueva, CI30MVP/Studio correctas en a452a5f, no merges; acción67 se reutiliza para revisión y recursos de QA.

- Cierre del seguimiento: etiqueta roadmap faltante de Issue68 corregida. Sync41183485906 success y JSON público42 tareas confirmado, COL026 review/COL001 blocked; pr_url de69 apilada espera base main según política existente (enlace real en Issue68). Aviso67 run41182721936 success, bot6540890455 menciona jea27 sin nueva confirmación de recepción; marcadores evitan duplicados. Clasificación de27 patrones completada con hashes,0 desconocidos; quedan QA limpia y términos/recursos humanos, no datos inventados.
# Conciliación final de ramas · 31-10-2026

Consulta real de GitHub: jea27 integró69 en COL042, luego65 en main y después66
en COL037. Main0539b9f conserva65 pero no incorpora66/69 por el orden de las
ramas apiladas. Conservado a01ed2b en codex/COL-026-integracion-beta2 y preparada
PR hacia main para todo lo pendiente; no se hizo merge ni push directo a main.
Hash del instalador beta2 recalculado sin variación. Solo cambia documentación
de conciliación, no el runtime probado. Issue68 permanece en revisión, sin
aceptación automática. Solicitud67 reutilizada para revisión de integración y
recursos QA, evitando una nueva Issue/aviso para los mismos bloqueos.

## 2026-10-31 · [COL-013] Estabilización0.3, revisión70 y procedencia

- Merge70 ya realizado por jea27, maincfb6d11 coincide por árbol; fuentes65/66/69
  incorporadas.69 blobs revisados,0 patrones de secreto/perfil local/archivos
  privados y6 JPEG CC0/QA sin EXIF. No merge del agente ni autoaprobación.
-37 MVP+91 seguimiento OK y TS/Vite OK. Nuevas pruebas cubren conservación de
  datos (cambio/ausencia/nuevos), bloqueo de path traversal, oráculo LUT, ICC/
  dimensiones, perfil sin alterar píxeles y gate de procedencia/tampering.
- Perfil real16MP: mediana17,376s en fuente local; LUT9,005, acabado6,267 y
  PNG1,445.3 pasadas iguales, original intacto. Diferente entorno al binario
  histórico32,392s: no se anuncia optimización entregada. Tiles256/512 ensayados
  sin aplicar, mismos píxeles en1 fotografía; memoria/cancelación pendientes.
- Nuevo hallazgo:44 DLL UCRT/API-set desde caché nativa de herramientas.95 PE
  cotejados por hash con TOC y NSIS. Firma/origen de bytes no concede derechos.
  Build bloquea ahora entradas de esa clase; no se genera nuevo instalador ni
  se modifican dependencias del candidato. CPython requiere cadena de suministro.
- Corrección de textos fuente sobre diagnósticos/SmartScreen WebView2; beta2
  existente no cambia. Protocolos W01–09/E01–05 y GO/NO-GO separados. No VM
  accesible o editor real nuevo; no instalaciones, participantes o entrevistas.
- COL026 amplía planificación de inferencia de acabado/halation posteriores a
  beta, manteniendo42 IDs y estados sin simular progreso. Solicitud67 reutilizada.

## 2026-10-31 · [COL-006] Dashboard real de producto

Worktree independiente desde maincfb6d11; sin cambios en código de Color Studio
ni estados/criterios de42 tareas. Colector público y contrato versionado separan
15 capacidades/8 entregables, verificación técnica, aprobación humana y puertas
de beta/venta. PR, CI, releases y artefactos se consultan automáticamente.
Sin descargar/ejecutar artefactos, cuerpos de Issues o logs; metadatos permitidos
y error de API falla cerrado. No permisos ampliados ni merges del agente.
107 pruebas locales y QA real de navegador en5 tamaños: sin overflow,42 tareas
visibles, filtros correctos y0 errores. Capturas versionadas; no iPhone físico
ni despliegue en Pages antes de integración humana. Issue19 reutilizada, no
se duplica decisión P0 ni se inventan porcentajes/aceptaciones.


Conciliación de seguimiento: se detectó COL043#72 creada por el otro chat.
Se reutiliza para la PR74, sin duplicar Issue ni cambiar42 tareas. COL006#19
conserva su decisión P0 histórica. Main71 integrado localmente sin perder
los dos registros del diario; aplicación igual a main. Coordinación por73.


## 2026-10-31 · [COL-044] Revisiones individuales por versión

Worktree separado, Issue76/PR79. Mis revisiones, checklist e instrucciones con
comentario autenticado y sin secretos en navegador. Validación por cuenta+ID,
Issue/commit/huella, checklist e inmutabilidad; recibo bot idempotente y historial.
Aprobación aislada de Glow/Difusión/Fade y resto, sin cerrar/aprobar tareas.
Correcciones dejan cola por capacidad; no se inventa un agente24/7. Huella de
blobs/criterios invalida cambios relacionados, conservando aceptación anterior.
126 tests+37 MVP OK. QA real de navegador en5 anchuras, sin overflow ni errores.
Demo77 en Actions: aprobación, cambios y replay (runs41191045868/41191317941/
41191386973) correctos, sin Pages y0 aprobaciones reales. Copy/open de GitHub
probado; observaciones quedan en comentario público, no se copian al dashboard.
Activación por issue_comment en main pendiente de integración humana, sin merge
ni altas de autenticación/servicios por agente. Capturas/informe versionados.

## 2026-10-31 · COL045/046/047 — Creator, Pro y Shot Planner local inicial

Worktree nuevo COL-045-creator-pro desde main8674566, raíz y worktrees anteriores
preservados. Issues81/82/83 diferenciadas y vinculadas;42 tareas intactas. Otra
sesión desarrolla Project OS/COL048; aquí no se modifican site UI ni sync code,
solo el catálogo versionado y dos regresiones del contrato de producto.

Creator guiado y Pro comparten motor/receta. Presets y modos conservados, ayuda
manual explícita; exportar exige preview de receta/imagen actuales. Shot Planner
local con observaciones SDR, decisiones del usuario, incertidumbre, fuentes
ARRI/ASC, esquema cenital editable y JSON independiente con receta. No inferencia
fiel, óptica/luz/cámara originales, vídeo nuevo ni validación profesional.

Seguridad: cuerpo realmente contado y concurrencia limitada; PNG íntegro/JPEG
estricto, EXIF privado ausente; UUID, contención y enlaces internos rechazados,
registros corruptos conservados/omitidos. CSP local sin eval/CDN, docs externas
FastAPI desactivadas, feedback iframe comprobado. Sin dependencias o instalaciones
nuevas. OSV566 versiones:2 paquetes con avisos conservados; ausentes del árbol
Windows223 paquetes únicos. npm audit0 avisos reportados. No auditoría universal
ni aprobación jurídica/redistribución del runtime.

58 tests API/motor,128 seguimiento y3 cliente correctos. Build Vue/TypeScript OK.
QA navegador CC0: PNG1024x678 ICC sin EXIF, efectos manuales, diagrama conservado,
JSON y aviso/bloqueo por plan desactualizado, feedback local bajo CSP;0 errores y
320/390/844/1280 sin overflow observado. Fixtures no cuentan como participantes.
DSC0106 16MP/receta anterior:16.912s, píxeles SHA256 idénticos y original intacto;
DSC0181:22.097s, otro input, sin comparación de mejora. Una ejecución por foto,
no aceleración general ni prueba del instalador. Evidencia CREATOR_045_*.

Se conserva el candidato existente; no se reconstruye ni distribuye otro. #67
sigue pendiente de runtime/procedencia oficial autorizada, Windows limpio,
editores activados y derechos/operativa del piloto. COL001 sin entrevistas reales.
Publicación en rama/PR y CI se registrará al terminar; ninguna aprobación real
emitida por el agente. Las capacidades nuevas requieren revisión individual.

### PR86 y sincronización real

https://github.com/jea27/Lut_generator/pull/86 (borrador durante comprobaciones).
Commit de código3761999, CI remota MVP41210911012/Studio41210911018/validación
41210911004/sync41210911087 correctas. Se han enlazado las3 capacidades a PR86.
El colector se ejecutó con lecturas reales autenticadas de GitHub:18 capacidades,
3 entregas en progreso sin marcar implementadas/aprobadas por estar aún sin
integrar, MVP8 y42 tareas intactas, beta/venta NO-GO. Se restauraron por bytes
los2 archivos de seguimiento generados; no hay estados simulados publicados.
Evidencia CREATOR_045_SYNC.json distingue checkout candidato de producción.
Las aceptaciones previas de Color Match/lotes/receta/Windows requieren nueva
revisión en el candidato por cambios relacionados de UI/API; no se borraron
recibos ni se emitieron nuevas decisiones humanas. CI final de metadatos y
solicitud de revisión se comprobarán antes de marcar lista la PR.
# 31-10-2026 · COL036 · auditoría posterior a PR86 y preparación de beta

PR86 integrada por jea27 en5799531; se preservan rama y worktrees anteriores.
Continuación aislada codex/COL-036-qa-integracion, Issue57/#67, sin autoaprobación.
Corregidas carrera de preferencias al arrancar, mutaciones durante operaciones
y pérdida silenciosa de ediciones del Planner. Guía no técnica Creator/Pro/Planner
en PRUEBA_CREATOR_PRO_PLANNER.md. Sin nuevos efectos o matemática de color.

61 tests MVP/API/harness,128 seguimiento,7 Node y build Vue correctos. QA real
del motor congelado interno con PATH Windows/cwd vacío;71 módulos de bundle/SO,
ninguna herramienta de desarrollo encontrada en PATH del hijo. Modos preservan
PNG/receta/imágenes; plan conserva ediciones y confirma regeneración. Navegador
escritorio y390×844,0 warnings/errores. Cuatro JPG CC0 ~16MP,15.601–16.181s,
RSS muestreado794.1–846.8MB, sin pérdida de resolución/originales; no benchmark
comparativo ni aceptación visual/Windows limpio. INTEGRACION_036_QA.json.

Gate95 PE mantiene44 DLL bloqueadas. Payload158 archivos,27 hallazgos de cadenas
de rutas upstream;0 perfil local/secretos/development según escáner, no garantía
universal. No NSIS nuevo ni autorización externa. Plan de build PSF3.14.10 con
23 pins/wheels compatibles por metadatos solamente; no instalado ni probado.
Se necesita respuesta concreta en67 y operador Windows limpio/editor activado.
Auditoría y comandos en INTEGRACION_BETA_036.md; beta y venta siguen NO-GO.

31-10-2026 · Cierre verificable COL036: PR88 lista para revisión, código60958b4.
Historial corregido con prueba unitaria y UI;7 Node,61 MVP/API/harness y128
seguimiento. MVP41223999971, studio41224000016, validate41223999953 y
sync41223998116 correctos. Colector real + Pages documentados,42 tareas y18
capacidades intactas,0/8 aceptación del MVP. Aviso único67 comprobado en
41224150508 y comentario6546679381 (@jea27), no recepción/aprobación supuesta.
Beta/venta NO-GO; no nuevo setup ni modificaciones de main. Reanudación y gates
pendientes en ESTADO_AGENTE.md y solicitud67.

Comprobación final Creator: preview neutra/importar no completan detección;
receta nueva invalida comparación previa. Unitarios y secuencia real del UI
congelado documentados, sin cambiar motor ni repetir perfiles equivalentes.

## 01-11-2026 · COL036 · runtime embebible oficial

Autorización expresa registrada en67, comentario6547117844. PR88 integrada por
jea27 en05b4983. Nueva rama aislada preserva su trabajo. CPython3.14.10 PSF y19
wheels fijados, hashes/RECORD/60 PE AMD64 verificados; importaciones nativas,
firmas requeridas y primeros recorridosAPI reales correctos.70 tests reales con
intérprete3.14 y núcleo del bundle; extrasQA aislados. Se mantiene dataroot beta2.
Scanner corrige falsos positivos de prefijosURL/bytes comprimidos, con tests sin
relajar detección de perfiles/secretos. Cero hallazgos bloqueantes; no permisos
nuevos, instalaciones globales o DLL de otras aplicaciones. Native release
compilado sin installer; falta preparar NSIS/QA completa y Windows limpio.

### COL036 · candidato interno oficial beta3 y QA · 01-11-2026

PR89 continúa PR88 ya integrada por jea27. Candidato construido desde cf1d451
limpio con PSF3.14.10 embeddable y19 wheels fijados;923 archivos/60 PE, sin DLL
del host.945 archivos NSIS extraídos y cotejados, plugins x86 oficiales y launcher
x64. Git autocrlf rompía hashes de avisos originales: se preservan como bytes con
.gitattributes; fuentes propios del runtime usan LF canónico. Guías `.agents` y
hooks de desarrollo de wheels excluidos sin tocar licencias. Corrigida lectura
UTF-8 explícita en un test de revisión humana bajo Python3.12/Windows.

El auditor distingue los3 bytes UNK→NSS que Tauri2.12.4 cambia temporalmente al
empaquetar; rechaza cualquier otra diferencia del launcher. NSIS oficial completo,
plugins, avisos, arquitectura/imports y payload son gates del builder. El workflow
manual solo sube informes saneados; mantiene binarios internos. Inventario289 con
avisos no se confunde con SBOM completa ni aprobación legal. Firma propia ausente.

73 pruebas en build;78 host/embebido locales y79 en CI tras ampliar el auditor;
128 seguimiento y7 Node correctos. Build remoto41292426593 success, fuentes36fbb789.
Cuatro CC0 ~16MP15.113–16.588s, lote2, originales intactos; sin cambio de motor o
mejora general atribuida. Aislamiento con tripwires real y71 módulos cotejados.
Dos ensamblados finales conservan923 hashes; dirty es la única diferencia de
manifiesto del segundo ensayo. No se declara instalador idéntico bit a bit.

Instalación real en contexto Codex/MSIX: preset de beta2 conservado, Creator/Pro/
Planner y cinco exports nativos comprobados. Desinstalar/instalar/reinstalar0;
sentinel dentro de instalación,6 archivos QA y9 existentes preservados. Se cerró
el ensayo y retiró solo su sentinel. Actualización directa silenciosa devolvió2
y ruta interactiva esperó al idioma del desinstalador previo, no accesible al
controlador. Causa no confirmada; no se oculta con el recorrido manual correcto.
Faltan Windows limpio, desconexión física y editores reales; NO-GO externo/venta.
Recibos RUNTIME_036_* con fuente/hash/alcance; sin datos privados, approved o merge.

El check del colector real encontró cuatro rutas nuevas no admitidas en la huella
de revisión. Se admite únicamente runtime.lock, python314._pth y los dos builders
exactos, leyendo hashes Git sin ejecutarlos ni ampliar permisos. Dos regresiones
adicionales verifican el catálogo versionado completo, cambio de pin y rechazo de
otras rutas;130 seguimiento pasan. Sync real de lectura reconoce PR89 y conserva
aceptación MVP0/8/NO-GO. Pages mantiene beta2/main hasta merge humano; sus42 tareas
no se editaron para simular progreso. Los cuatro archivos generados se restauran.

PR89 pasó a revisión y57 status:review, sin merge/approved. Aviso canónico67
verificado en41294069249 y comentario6556221187; recepción física nueva no
confirmada. Cola sync canceló ejecuciones sin steps durante la ráfaga de eventos;
se comprueba reintento en reposo sin modificar permisos/concurrencia del workflow.
Identidad Git del checkpoint no-reply por comando; ninguna reescritura remota.

### COL036 · investigación de actualización y entorno QA interno

Nueva autorización del usuario para beta3 interna/VM Windows11 oficial y Resolve
gratuito. PR89 integrada por jea27 en918cb638. Se trabaja en rama/worktree propio
COL-036-actualizacion-segura. Preflight detecta gestor Hyper-V ausente, elevación740
y RAM disponible insuficiente para VM recomendada; no cambios de host ni reinicio.
Registro Blackmagic requiere intervención personal; Resolve ausente, Adobe sin
activación acreditada. Guías preparadas, sin simular ejecución de Windows/editor.

El código2 histórico es aborto NSIS genérico; la traza /S actual pasa WebView2 y
alcanza Install (parada diagnóstica90), sin lanzar desinstalador. La observación
interactiva del idioma es otra ruta. No atribuir una causa por documentación sola:
NSISdl aceptó HTTPS y devolvió success, pero un fixture loopback observó HTTP plano
para URL https, sin saludo TLS. Descarga diagnóstica no ejecutada. Se conserva la
evidencia privada y se continúa con reproducción, corrección y recuperación reales.


## 01-11-2026 · COL036 · preparación transaccional de actualización

PR89 integrada por jea27; nueva rama aislada desde918cb638. Se repitió actualización
original beta2→beta3 sin desinstalación intermedia:0, preset de QA por API preservado,
legacy runtime retenido. La línea base beta2 requirió retirada anterior únicamente
para el experimento. No reproduce el2 histórico ni se afirma causa resuelta.
Probe de transporte NSISdl a loopbackhttps recibió plaintextHTTP, distinto del
histórico. Decisión material: usar bootstrapper oficial Microsoft firmado fijado por
hash y transporte HTTPS en construcción, con licencia propietaria/gate externo
pendiente. No copiar DLLs del host, ni desactivar protecciones.

Nueva beta4 en preparación: stage hermano con ledger completo, mutex/lock, validación,
backup/rollback y diario; antiguo desinstalador no se ejecuta para actualizar. Logs
por fases sin rutas/datos. Extras personales de raíz se conservan; componentes
legacy quedan en backup privado, no runtime activo ni material redistribuible.
Interrupciones sintéticas no son cortes eléctricos. Windows limpio/Resolve/offline
real pendientes de operador; solicitud67 única, workflow41316675082 y mención
6559335054 comprobados. No se habilitó Hyper-V ni reinició el host. Guías preparadas.


## 02-11-2026 · COL036 · revisión independiente y defensa de archivos

El candidato intermedio25c/e317 supera build/auditoría951 archivos y CI41347038273,
pero la revisión detectó Delete de MainBinaryName del registro sin validar. Se
retira esa limpieza; no es necesaria con stage nuevo y backup. El candidato queda
superado antes de distribución. Se añade preflight de directorios/ancestros del
desinstalador: rechaza reparse/junction antes del primer Delete, sin ejecutar un
Python instalado que pudiera haberse redirigido. Prueba roja funcional encontró
registroSystem incorrecto; corregido a r17/r18. Verde5 casos reales con NSIS
verificado y junctions sin administrador, marcadores intactos. No permisos nuevos.
No ejecutar uninstall.exe de backups: conservar evidencia y recuperación guiada.

Evidencias intermedias: ambos updates directos0; errorWin32=32 controlado restaura
bytes de app y datos, reintento0; aplicación abierta aborta2 antes de copiar.
GUI real y descargasPNG/receta/PlannerJSON en25c, Creator→Pro conserva60%; no
aceptación visual humana.105 tests con Python embebido,130 seguimiento,7frontend;
se suman5 probes de guard en el próximo candidato. Codecs, fechas, rutasMSIX y
sufijos de descarga del harness se corrigieron sin atribuirlos a defectos del producto.
Windows limpio/desconexión/editores/licencias/aceptación siguen NO-GO/pending.

## 02-11-2026 · COL036 · candidato final y conservación pendiente de diagnóstico

PR90 permanece borrador. Candidato limpio8f4c60e/f002769d…ca4bf, extracción951
archivos/924runtime y construcciónCI41399176754 correctas;60PE y bootstrapper
coinciden CI/local, setups no idénticos, sin publicar ejecutables. Directos beta3→4
0/8,016s y beta2→4 0/7,110s. Fallo nativo Winerror32 durante cambio de carpetas:
NSIS2/hijo2, rollback byte-idéntico, reintento0/8,438s. No identifica2 histórico.
Pruebas reales de registro manipulado/junction final y desinstalación preservan
stores; runtime restaurado, sin operaciones propias a medias. GUI intermedia25c
tiene apps/packages idénticos a8f; no se presenta como retest visual final.

Se corrigió el auditor QA para leer rutas del loader PSAPI en lugar de nombres de
secciones mapeadas que conservaban la ruta del stage renombrado. No relaja origen
ni hashes;3 regresiones.116 MVP host y116 con Python embebido pasan,3 symlink
omitidos; smoke2CC0 e aislamiento71módulos correctos. Instrumento de diagnóstico
PowerShell probado con3 casos inertes y ejecutado en lectura real; no distribuye
dependencias QA ni requiere otro setup. Capturas solo demo autorizada.

Bloqueo material:9 archivos de captura inicial frente a5 actuales,4 imágenes
temporales ausentes y0 cambios de hash entre presentes. El operador niega limpieza:
no aceptar conservación global ni atribuirla a otra API. Comparaciones de cada
instalación son iguales, pero no cubren el intervalo. Búsquedas/historial sin causa;
USN lecturaAccesoDenegado5. Se prepara comparación fuera de Codex/lectura elevada
por operador con identidades NTFS actuales, salida privada y sin restauración,
borrado ni permisos cambiados. Guía DIAGNOSTICO_TEMPORALES_BETA4 y checkpoint.
Manifiesto incorpora PR90/evidencia y puerta independiente de conservación;
roadmap histórico intacto. Beta externa y venta NO-GO; Windows limpio/offline real,
Resolve/Adobe y revisión de derechos/humana pendientes. Solicitud67 se reutiliza.

Seguimiento final132 tests correctos. Consulta GitHub real con manifiesto de PR90:
Windows bloqueado, no aprobado, conservación false y beta/venta NO-GO. Detectado y
corregido que needs_review/changes_requested reemplazaba visualmente blocked;
historial/observaciones conservados, regresión incluida. Pages de main consultado:
COL036 bloqueada con PR90, versiónbeta3; mejoras de PR90 aún sin desplegar.
Issue57 blocked, sin in-progress; solicitud67 actualizada con diagnóstico concreto.
Workflow41410069177 success, mención6572098610 a jea27 comprobada; no recepción
física nueva confirmada. No repetir aviso ni aprobar por CI. CI810bf44 MVP/Studio/
validate/sync correctos; último head consultable en checks de PR90. Checkpoint listo.

## 02-11-2026 · COL036 · incidente P0 y contención de eliminaciones

Recibido diagnóstico privado:4 PNG con FILE_DELETE/CLOSE; no identifica proceso.
Se preservan originales/copias/hash y se correlaciona hora local/UTC con tareas y
logs sin atribuir causa al instalador. El candidato final se construyó después.
La vista externa1/9 y Codex5/9 tienen identidades de directorio distintas; otros2PNG
y2presets siguen disponibles con hash original, copiados a evidencia privada sin
restaurar. Baseline original no tenía identidad física. No afirmar ocho pérdidas
globales ni que las comparaciones inmediatas resuelven el incidente.

Reproducción aislada con audit hook: código anterior DELETE borra6PNG sin
consentimiento específico; contención423 conserva9. Cleanup .part anterior borra
un archivo preexistente tras fallar creación exclusiva; corrección lo conserva.
PID registrado es del fixture, no del incidente. DELETE privados/UI deshabilitados,
guard de temporales por creación/inode, reserva de lote exclusiva y estado solo tras
persistir. Instalación/recuperación rechazan almacén privado; NSIS ya no purgaAppData.
QA baselinev2 liga volumen/directorio y rechaza otra identidad o baseline antiguo.

Probes sintéticos, host y runtime oficial embebido de contención; frontend7/build
y seguimiento se verifican. Conteos/resultados reales en INCIDENT_036_QA.json.
No nuevo instalador, pruebas destructivas reales, restore, cambios de permisos,
logging, controlador o uso de Procmon. Preparados script de auditoría existente y
protocolo Procmon de solo fixtures. Security pendiente de operador; ausencia de
eventos no prueba ausencia de borrado. Hipótesis históricas siguen abiertas.

PR90 continúa borrador. Candidato f002 en cuarentena y descargas bloqueadas por
evidencia de seguridad faltante/no validada, incluso histórica autorización de tag.
Manifiesto/recibo enlazan incidente; estados de las42 tareas sin edición manual.
Beta externa/venta NO-GO, ninguna capacidad aprobada, merge ni publicación binaria.

Resultados finales locales:135 MVP host y135 con Python3.14.10 embebido,0 fallos,
3 symlinks omitidos;7 probes NSIS reales inertes. Seguimiento134, frontend7/build
correctos. La nueva prueba de texto del hold detectó lectura por defecto cp1252 en
el harness Windows; JS era UTF8 válido y el test ahora lee explícitamente UTF8.
Las primeras trazas fallidas se conservan privadas; no eran pérdida de datos real.

## 02-11-2026 · COL036 · Security sin coincidencias y preparación de Procmon

Recibido resultado privado del operador: consulta Security existente sin eventos
coincidentes. Original/hash preservados; no repetir ni inferir ausencia de borrado
o exoneración. Revisión adicional de historial propio/tres agentes sin orden de
borrado identificada en la ventana; no prueba contra procesos en segundo plano.
Defender/AppModel/AppX consultados sin atribución, sin cambios de configuración.

Preparado ZIP oficial Process Monitor4.12 en carpeta ignorada del workspace. Hash
ZIP477754bf…3a10, x64 SHA28495e64…885 y tres firmas Microsoft válidas. /NoConnect
verificado en ayuda incorporada firmada. No ejecución, aceptación de EULA, carga
de controlador ni inclusión en instalador. Captura con fixture preparada; requiere
acción/consentimiento del operador para arranque privilegiado. No reconstruye el PID
histórico por sí sola. Causa abierta, PR90 borrador y beta/venta NO-GO.

Solo evidencia/documentación; sin nuevos cambios del producto. JSON saneados y
diff comprobados; no se repiten suites ya verificadas135/135/134/7. CI comprobará
el nuevo commit. El resultado privado no se adjunta a Issues/PR.

## 02-11-2026 · COL036 · Procmon abierto por operador; control elevado pendiente

El usuario confirma ventana abierta y autoriza continuar. Mediante la habilidad
Computer Use se observa Process Monitor receptivo, vacío y captura desactivada.
Activar ventana funciona; clic en Filter y Ctrl+L no abren menú/diálogo; solo título
accesible. Tokens consultados sin modificación: Procmon alto/elevado y diagnóstico
medio/no elevado; compatible con UIPI, sin atribuir el fallo a un canal interno
no inspeccionado. No elevar agentes ni modificar permisos, logging o protecciones.

No se ejecutan probes nuevos sin confirmar filtro. Se solicita solo configurar
Path begins with el prefijo sintético privado, sin otras Include, Drop Filtered
Events y arrancar captura. Después Codex ejecutará los cuatro probes existentes;
PML/CSV permanecerán privados. Apertura satisfecha, captura todavía pendiente.
No es nueva evidencia de atribución histórica. PR90 borrador y distribución NO-GO.

Solicitud67 reutilizada conservando marcadores y needs-human, sin quitar/reaplicar
etiqueta. Dispatch41452456160 success y comentario6578231215 del bot con @jea27
verificados; no afirmar recepción física nueva. JSON e invariantes NO-GO correctos,
diff sin rutas privadas/credenciales y evidencia privada ignorada por Git. Solo
cuatro archivos de documentación/evidencia; no repetir suites de producto sin cambio.

## 02-11-2026 · COL036 · conservación atómica y recuperación de lotes

El usuario pide reintentar Procmon y continuar desarrollo si falla. Ventana nueva
localizada; Ctrl+L de nuevo sin efecto, sin eventos/captura desactivada. Se pospone
solo la captura nativa, sin nuevos avisos por el mismo bloqueo ni cambios de permisos.

Reproducción sintética previa al parche:5 tests de storage/colisión producen6
fallos (subtests JSON/bytes),0 errores;2 tests de persistencia del trabajador fallan.
Limpiar por nombre borraba un sustituto ajeno; UUID forzado sobrescribía un archivo
existente; fallo inicial de save dejaba el lote activo indefinidamente. No atribuye
ninguno de estos defectos al evento histórico. Trazas solo privadas.

Parche: identidad de temporal antes de publicar/limpiar, protección compartida con
lotes, creaciones sin reemplazo/409 y ediciones atómicas preservadas. Fallos de
persistencia del trabajador quedan en failed/reintentables; si no se guarda ese
estado, reinicio muestra interrupted. No fallback destructivo ni purga nueva.
147 host y147 embebidos correctos,12 regresiones nuevas;3 omisiones host por symlink.
Runtime QA nuevo oficial offline/dirty declarado,924 archivos/60 nativos; aislamiento
71 módulos/reinicio y smoke2CC0 correctos, originales intactos, sin instalación.
Recibo INCIDENT_036_STORAGE_QA.json y hashes por fuente; no confundir con Windows limpio.

Manifiesto conserva IDs y estados: añade pruebas/PR90/dependencias de huella y retira
del guion humano la eliminación de presets, actualmente bloqueada. No setup nuevo,
aprobaciones, merge o escrituras de main. PR90 borrador; causa abierta y NO-GO.

Seguimiento134 correcto tras el ajuste de manifiesto. JSON/hashes de fuentes
probadas, enlaces de pruebas/huellas e invariantes NO-GO cotejados. Escaneo de los
11 archivos de entrega sin credenciales/rutas privadas; trazas privadas ignoradas.
42 tareas históricas sin cambios. Sin nuevos tests frontend al no cambiar UI;
la CI de la PR comprobará la entrega completa. No repetir aviso del bloqueo Procmon.

## 03-11-2026 · COL036 · consolidación y candidato interno beta.5

Revisión desde edf82d0 con preservación del worktree y custodia de las copias.
Junctions NTFS reales detectan recuperación directa sin comprobar ancestros y
root de almacén resuelto antes de comprobar enlaces; corregidos. No atribución
histórica. Prueba real de readonly conserva preferencias, fotos, presets y receta;
bloqueo Win32 de directorio aborta switch y permite retry con stage nuevo, como NSIS.
El primer harness intentó reutilizar stage con extras ya copiados: corregido el
harness para crear stage fresco; fallo/trace retenidos.154 host correctos,3 omitidos.
CI Linux añadida para ejecutar los3 symlinks originales; NTFS se prueba en Windows.

VM actual no disponible: gestor ausente,3,41GiB libres. No activar features, reiniciar
o ejecutar Procmon en host; fase nativa queda para entorno aislado. Custodia privada
2PNG+2presets y preferencias cotejada contra hashes sin restauración/publicación.
Preparar versión beta.5 y build interno, guardando etapas/recibos/launcher previos.
Gate global usa data_safety_validated=false: una causa desconocida no sustituye
evaluación preventiva y aceptación humana. Tests no conceden GO ni aprobación.
Nuevo test de sincronización usa evidencia futura sintética, nunca modifica el recibo
real. Sin merge/cierre/release ni permisos cambiados. Build/auditorías aún pendientes.

03-11: ebdfbe5 compilado/auditado en limpio: preliminar beta5 d1cbdd…68ea,
48.482.443bytes,951 archivos/924 runtime,289 componentes con avisos. Sin instalación.
Tres symlinks pasan en LinuxCI41585993189; no prueba de file-symlink Windows.
Revisión posterior de sustitutos detecta pérdida del diario si aparece un destino
ajeno tras el move del old: reproducción real de colisión falla y corrección retiene
diario+backup+receta ajena. La recuperación no sobrescribe ese destino; tras revisión
manual de la carpeta el fixture puede recuperar el old.36 tests focales correctos.
Regenerar beta5 después del commit, archivando preliminar. CI candidata41586295244
cancelada por fuente superada, no por pérdida de datos. No publicar instaladores.

Kit VM preparado con guard/modelo/ruta, hashes, instaladores fijados y fuentes legacy
con SHA; pruebas directas no se presentan como HTTP. Inputs PNG/receta sintéticos,
sin dependencias de desarrollo globales. Pendiente generar/testear kit final tras
build. Readiness de conservación apunta a aceptación preventiva nueva, todavía
false; conserva el recibo histórico y no lo convierte en una aceptación retrospectiva.


## 03-11-2026 · COL036 · candidato beta5 final y kit privado verificable

Compilado desde29fb77a limpio, beta.5 SHA789983…8bb69,48.473.299bytes. Auditoría
NSIS951/924runtime/60nativos correcta;289 paquetes con avisos y0ausentes; firmas
PSF/MS requeridas válidas. Sin instalar en host, sin firmas compradas ni publicación.
Se preservan beta4 y preliminar beta5. Fuentes posteriores solo CI/herramientas/docs;
apps/packages/packaging siguen iguales. Build mueve staging a archivo privado y
conserva launcher/setup/recibos; TEMP/TMP locales se restauran. No copia DLL del host.

Kit privado17entradas+manifiesto,95.194.508bytes, SHAabf342…fd4015; candidato,
beta3 fijada, fuentes QA allowlist,2PNG/receta sintéticos. CRC/todos hashes correctos.
Scripts rechazan host, guest/ruta no esperados, enlaces y payload cambiado; no se
han ejecutado en Windows11 limpio. No hay Python/Node/Git global requerido en guest.
Primer intento con Python del sistema falló por dependencias ausentes; se conservó
su carpeta parcial y se generó otro kit con el venv existente, sin instalaciones.

160 host (3omitidos), primer runtime160 correcto, aislamiento71módulos y smoke
2CC0 correctos. Una repetición del runtime dio1error directory_switch_failed en
fixture de interrupción tras el move de una instalación limpia. No registró causa
Win32, por tanto no atribuirla. Recibo fallido preservado;20repeticiones del caso y
una suite completa diagnóstica pasan. Runner ahora registra omitidos y report de
InstallError sin rutas; serie limitada adicional en curso. No declarar resuelto por
repeticiones verdes. No relacionarlo con el actor histórico sin evidencia.

CI8876535 MVP/cliente/seguimiento correctos;3symlinks originales pasan en Windows
CI y Linux. Job Windows153 tests con clase7guardas NSIS omitida por cache ausente;
los7sí pasan en build local160. Primer CI29fb falló por checkout superficial sin
fuente legacy fijada: corregido fetch-depth0, sin modificar permisos. Build completo
remoto41649084841 en curso; sube solo informes, no instalador.

Recibos públicos beta5 y agregado de incidente actualizados sin aceptar seguridad
ni causa histórica. Capturas beta4 existentes revisadas: demo CC0 y UI, sin rutas
privadas; no presentarlas como GUIbeta5.42tareas intactas y aceptación por capacidad
independiente de merge/CI. Windows/Procmon/red real/editores siguen NOT_RUN; NO-GO.

Cierre diagnóstico limitado: cinco suites adicionales160/3omitidos correctas, sin
InstallError nuevo; no explica el único fallo previo. Sigue registrado y PRborrador.
Colector GitHub real:42tareas, COL036blocked/PR90, aceptación0/8, beta5 en cuarentena
y NO-GO. Generated files preservados byte a byte. Pages publica beta3/main918cb638;
los recibos/cambios de esta rama esperan integración humana. Ver BETA5_036_SYNC.json.

Build independiente41649084841 success sobre8876535:160tests/0omitidos, incluyendo
3symlinks nativos y7guards NSIS, auditoría951/924/60 y firmas correctas. Solo4recibos
subidos; no EXE. SHA e5862a…27da difiere del candidato local789983…8bb69. Mismas
fuentes apps/packages/packaging entre29fb/8876, no afirmar identidad de binarios.
Recibo BETA5_036_CI_BUILD.json. CI1d917c7 MVP/cliente/seguimiento success.
Solicitud67 actualizada con7campos y VM concreta; aviso41650561917 success y bot
@jea27 en67#issuecomment-6605944403. No nueva confirmación física. Sin toggles de
needs-human ni Issue duplicada; no repetir aviso. Algunos sync cancelados en cola
sin steps, verificar despliegue final. PR90 sigue borrador; incertidumbre y NO-GO.


## 05-11-2026 · COL036 · cierre MVP y QA asistida de VM existente

Usuario confirma VMWindows11Pro/HyperV con checkpoints. Cmdlets presentes;
Get-VM falla en contexto no elevado y no hay consola accesible. No modificación
administrativa ni checkpoint. Preparado asistente PowerShellDirect con identidad
BIOS/guest, kitSHA, selección/atestación checkpoint, sin shares/credenciales guardadas.
Ciclo guest prepara semillaAPI3, baselineNTFS, bloqueo Win32/fracaso nativo, retry
update5, API/reinicio/cancelación, fixtures, red guest real/finally y desinstalación.
No ejecutado en guest. La confirmación del operador no se confunde con verificación
automática del contenido del checkpoint ni con aprobación de producto.

Cliente nuevo probado por HTTP real con runtime empaquetado beta5, fuente29fb:
2pases semilla/reinicio, modo Creator/Pro byteigual, receta/presets,LUT sin óptica,
Planner/incertidumbre/fuentes y cancelación realPASS. Sintéticos768x1024, nada de
fotos personales ni AppData real. No prueba GUI ni Windows limpio.

4tests nuevos primero y suite164/3omitidos correctos; nueva prueba de hash host
falló porque WindowsPowerShell5 heredaba PSModulePath7 y ocultaba Get-FileHash.
Test corregido con entorno propio del hijo, sin instalaciones/cambios globales;
5tests focales correctos. Regresión adicional comprueba captura de fallo inesperado
antes de limpiar el fixture. Cause histórica e intermitente no resueltas.

MVP_CLOSURE_036 clasifica8bloqueos; manifiesto añade evidencias/tests/huellas de
herramientas de QA, sin aprobación. Preparación comercial existente conciliada:
no duplicar feedback/guías,49€ de COL005 conserva significado,0respuestas inventadas.
Falta licencia propia y decisiones humanas/legales. NoGO beta externa/venta.

Cierre de verificación: primer kitv2 bloqueado antes del ZIP porque beta3 no tiene
ledger transaccional. Se preservó su carpeta y se corrigió la verificación con
runtime+launcher ligados al NSIS auditado; regresión real metadata beta3 correcta.
CIe246 detectó GET/404 en fixtureAPI antes del buildUI. El cliente del kit conserva
web200 obligatorio; el fixture unitario API lo declara no probado. CI9f3702a MVP,
cliente y seguimiento correctos. Sin cambios de apps/packages/packaging.

Kit final22entradas+manifest,95.299.557bytes, SHAa304c5…b0a1f4, toolsource9f3702a,
apps29fb. CRC/hashes y extractorWindowsPS5 reales correctos;3archivesmalformados
rechazados antes de extraer. Runtime167/3omitidos correcto; host166/3omitidos más
regresiónlegacy focal, seguimiento135.100repeticionesinstrumentadas pasan sin
explicar fallo anterior; fixture inesperado se conserva si reaparece. No ejecución
guest, copiaVM ni cambio decheckpoint. VMMSRunning/GetVMpermiso insuficiente confirmado.
Actualización nativa, UI, offline real y editores siguen NOT_RUN y NO-GO.

Handoff final: guía visual actualizada a beta5, sin recomendar reinstalación como
prueba de upgrade. Separados almacenes QA/Inicio para evitar conclusiones entre
vistas distintas. Verificador de enlacesoffline con regresión; kit23miembros,
95.299.851bytes, SHA c3521f…bc011, toolsource539a159. Kit9f previo preservado.
Archivo/hash/extracción WindowsPS5 y enlaces correctos. Host168/3omitidos correcto;
embebido167/3omitidos anterior más prueba focal de enlaces correcta. No nativeVM.
Notificaciónúnica42014330354 success, bot@jea27 en67#issuecomment-6656140492; no
confirmación física nueva. Body67 actualizado al hash final sin volver a disparar
aviso. Coordinación73 y comentarios60/61/62 publicados; nadie contactado, sin pagos,
merge, aprobaciones o publicación de instalador. Datos privados recuperados intactos.


### COL036 · no reutilizar un perfil con otra instalación · 06-11-2026

La preparación del ciclo asumía que C:\LF-QA vacío implicaba perfil limpio. Se
corrige antes de copiar el kit y en el guest: presencia del almacén predeterminado,
directorios conocidos o clave de desinstalación exacta (HKCU/HKLM, vistas32/64)
bloquea sin modificar. Acceso a registro fallido también bloquea. Así se evita
que beta3 encuentre por registro otra instalación fuera de la carpeta dedicada.
13 tests focales correctos con sondas sintéticas; no hay instalación real, cambios
de registro, VM/checkpoints o lectura de fotos/presets del usuario. No identifica
el actor histórico. Kits anteriores retenidos; beta externa y venta NO-GO.

### COL-036 · Bloqueos temporales durante la actualización · 11-11-2026

El cambio de directorio admite tres reintentos acotados para errores de Windows
5, 32 y 33. Antes de reintentar, comprueba identidad, enlaces, huella del árbol y
que el destino esté libre. Si el bloqueo persiste, conserva la aplicación anterior
o su respaldo y el registro de recuperación. El diagnóstico distingue mover la
instalación previa y activar el paquete preparado.

Handles reales de Windows sobre directorios sintéticos comprobaron recuperación
de ambas fases y conservación ante bloqueo persistente. Una modificación del
paquete durante la espera detuvo la operación y restauró la instalación previa.
Suite MVP local 171 casos, 168 correctos y 3 omitidos por permisos de symlinks.
Esta evidencia corresponde al helper en desarrollo. El beta.5 ya construido
conserva sus bytes y SHA para la QA beta.3 → beta.5. La causa histórica de las
eliminaciones sigue desconocida. La VM devuelve acceso denegado desde Codex.

### COL-046 · Proyectos locales · 11-11-2026

Pro recupera una copia de edición con las dos imágenes importadas, receta y
comparador. API privada por sesión, referencias por UUID y huella SHA-256,
registros acotados y escritura atómica sin sobrescritura. Confirmación antes
de cambiar una edición abierta. El navegador recorrió demo CC0, guardar,
recargar, abrir y exportación disponible. Suite de API verificó reinicio,
PNG idéntico y rechazo de medio cambiado, ausente o fuera del almacén.
166 casos MVP, 162 correctos y 4 omitidos en este worktree. Tres requieren
symlinks y la clase NSIS requiere el caché fijado del worktree COL036.
Siete pruebas de cliente y build correctos. Validación de VM pendiente en #67.
