# COL-006 · Diagnóstico de la duplicación #56 / #15 y propuesta

**Fecha:** 30 de octubre de 2026. **Alcance:** análisis de registros de GitHub
y del workflow de aviso; no se cambia el workflow en esta entrega.

## ¿Es duplicada la Issue #56?

**Sí.** Ambas solicitudes pedían la misma revisión humana de COL-005/PR #55:

- #15 era la solicitud `needs-human` vigente para revisar la documentación COL-005.
- Al abrir PR #55, el workflow creó #56, añadió `needs-human` y publicó una
  mención `@jea27` en su comentario automático. El aviso quedó en
  [#56, comentario 6532658538](https://github.com/jea27/Lut_generator/issues/56#issuecomment-6532658538).
- El cuerpo actual de #56 dirige a #15 y dice que no se requiere respuesta
  separada. #15 contiene ahora los enlaces a PR #14/#55 y la referencia a #56.
  Ambas Issues siguen abiertas; este análisis no cierra ni cambia etiquetas.

La mención automática de #56 ya fue enviada. No se puede retirar de los avisos
del móvil. La corrección dejó un único lugar de respuesta: #15; no se volvió a
notificar manualmente.

## Causa comprobable

El workflow vigente es [`.github/workflows/alert-human.yml`](../.github/workflows/alert-human.yml):

1. Escucha `pull_request.opened`, `ready_for_review`, `reopened` y `synchronize`.
2. Extrae `[COL-###]` del título, pero crea una marca
   `lumaforge-review-pr:<número-de-PR>` y busca únicamente esa marca en Issues.
   La revisión no se identifica por la tarea ni por la solicitud humana activa.
3. Si no encuentra la marca, crea una Issue nueva por PR, aplica
   `needs-human` y comenta con `@REVIEWER_GITHUB`.
4. El grupo de concurrencia también usa el número de PR; dos PR de la misma
   tarea no se serializan entre sí.

Para este caso, el evento de PR #55 se procesó antes de que #15 tuviera la marca
de PR #55. Por ello, aunque después se añadió el marcador y las ejecuciones
siguientes reconocieron la solicitud existente, el primer run ya había creado
#56 y enviado el aviso. Además, la clave por PR permitiría que otra PR de
COL-005 cree una tercera solicitud si nadie añadiera de antemano otra marca.

**Resumen de causa:** condición de carrera al actualizar manualmente el
marcador, combinada con una deduplicación por PR que no representa la decisión
humana compartida por la tarea.

## Mejora recomendada para el workflow

Unificar la identidad por **tarea y decisión humana**, no por PR:

- Añadir a la solicitud activa una marca estable, por ejemplo
  `<!-- lumaforge-review-task:COL-005 -->`, y mantener una relación con su Issue
  canónica.
- Ante una PR etiquetada `[COL-005]`, localizar la solicitud activa de
  `COL-005`. Si ya existe, añadir la nueva PR a sus enlaces de contexto y salir
  sin crear otra Issue, sin volver a añadir/reaplicar `needs-human` y sin otra
  mención móvil.
- Crear una nueva solicitud solo si no hay una solicitud activa para esa tarea.
  Escribir la marca estable antes de publicar el aviso.
- Tratar `synchronize` y reintentos como operaciones idempotentes. Una nueva
  notificación debe requerir una decisión humana nueva, no simplemente otro
  evento de PR. No usar una cola global de Actions sin control: una sola
  concurrencia global puede descartar eventos pendientes.
- Si concurren varias PR de la misma tarea, serializar por la clave COL o
  resolver el registro de forma atómica, para que ambas ejecuciones no observen
  «no existe» y creen dos solicitudes a la vez.

### Pruebas de aceptación propuestas para la futura corrección

1. Con #15 ya marcada como solicitud activa de COL-005, abrir o actualizar dos
   PR no borrador `[COL-005]`: ambas quedan enlazadas a #15, no nace otra Issue
   de acción y no se añade otra mención.
2. Repetir `synchronize`, `ready_for_review` y un reintento no vuelve a enviar
   el aviso ni cambia etiquetas.
3. Una nueva tarea sin solicitud activa crea exactamente una Issue válida,
   añade `needs-human` una sola vez y emite una sola mención.
4. Dos eventos simultáneos para la misma COL no dejan solicitudes duplicadas.

Esta propuesta no cambia código, permisos, labels o workflows y no reutiliza la
investigación comercial de PR #55. Se comunica en la Issue #19 para que el
responsable del workflow pueda coordinar una corrección aparte.
