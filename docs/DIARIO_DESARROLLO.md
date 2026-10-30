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

## Plantilla para próximas entregas

### AAAA-MM-DD · [COL-XXX] Título
- Rama / PR:
- Qué se implementó:
- Tests (comando, resultado):
- Decisiones y cambios de alcance:
- Riesgos / pendientes:
- Próximo paso propuesto:
