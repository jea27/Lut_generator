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
