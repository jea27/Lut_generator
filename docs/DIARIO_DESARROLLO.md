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

## Plantilla para próximas entregas

### AAAA-MM-DD · [COL-XXX] Título
- Rama / PR:
- Qué se implementó:
- Tests (comando, resultado):
- Decisiones y cambios de alcance:
- Riesgos / pendientes:
- Próximo paso propuesto:
