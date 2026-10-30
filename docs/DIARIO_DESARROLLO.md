# Diario de desarrollo y decisiones

> Codex debe añadir una entrada breve y verificable por entrega. No borrar entradas anteriores ni atribuir pruebas no ejecutadas.

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
