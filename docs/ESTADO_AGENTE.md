# Estado del agente · sesión intensiva 2026-10-30

## Tarea actual y rama

COL-006, Issue #19: auditoría de evidencia publicada en PR #28 y cierre del checkpoint P0.
Rama raíz `codex/COL-006-coordinacion-p0`. No hay go ni autorización P1.
Última base incorporada sin sobrescribir trabajo: origin/main ce670b1.

## Trabajo completado (preparación, no validación de mercado)

| Frente | Entrega | Estado de evidencia |
|---|---|---|
| COL-001 / #6 | Guion conservado | Cero actas nuevas; entrevistas pendientes |
| COL-002 / #16 | Registro, operativa y validador; PR #23 | Registro vacío, cero sesiones |
| COL-003 / #17 | Cinco fuentes primarias, protocolo y validador; PR #26 | Cero pruebas de producto |
| COL-004 / #18 | Manifiesto 20 slots y validador; PR #22 | Cero pares listos, cero medios descargados |
| COL-005 / #13 | Hipótesis/cuestionario en PR #14 | Documento integrado, aceptación humana pendiente |
| COL-006 / #19 | Puerta documental y avisos en PR #20; auditoría p0_status nueva | Evidencia incompleta, P1 sin iniciar |

GitHub registra PR #20/#22/#23/#26 integradas por jea27, no por el agente.
COL-005 permanece review porque #13 está abierta sin approved: merge no es
aceptación. Se reutilizó #15, con título/estructura nuevos, sin reenviar el
mismo bloqueo. No se cerró ni aprobó ninguna tarea.

## Pruebas realizadas

- Root integrado más auditoría final: 64 unittest OK; CI de PR #28 run 41091623916 success.
- Incluye avisos completos/CRLF/deduplicación/manual, dataset (10 tests propios),
  entrevistas (10), benchmark (9) y auditoría P0 (8), más tests previos.
- Los tres registros vacíos son estructuralmente válidos; --ready devuelve 2.
- p0_status --github --ready: exit 2; 0 entrevistas, 0 pares listos, 0 casos
  automáticos; ninguna de las seis Issues aceptada y sin IDs canónicos duplicados.
- Fixtures de tests no se escriben a los registros ni cuentan como evidencia.
- Checks reales: PR20 run 41088346523/aviso41088346462; PR22 run41089220665/
  aviso41089220791; PR23 run41089234703/aviso41089234711; PR26 run41090372324/
  aviso41090372385. Todos validate/notify success, Pages omitido desde PR.
- PR #28: https://github.com/jea27/Lut_generator/pull/28. Auditoría inicial con
  64 tests validada por CI run41091623916; los últimos cambios de documentación
  se verifican en sus checks antes de terminar. Sin autoaprobación.
- Solicitud consolidada #29 con los siete campos, needs-human y mención real:
  run41091807276 success, comentario6528069841. Una sola nueva petición para
  aportar evidencia; la solicitud previa de COL-005 (#15) no se reenvía.
- Sync run41091807163 success. El dashboard procede solo de GitHub; la consulta
  final comprobará bloqueos sin inferir que las tareas estén aprobadas.

## Ramas y carpetas conservadas

| Rama | Carpeta desde la raíz | Commit de entrega |
|---|---|---|
| codex/COL-002-evidencia-entrevistas | .codex-worktrees/COL-002 | e968719 |
| codex/COL-003-protocolo-benchmark | .codex-worktrees/COL-003 | 163c957 |
| codex/COL-004-manifiesto-dataset | .codex-worktrees/COL-004 | b9de8d2 |
| codex/COL-006-coordinacion-p0 | raíz | 209650c, 2d15fe7 y 7c689dc; checkpoint final en HEAD |

Son worktrees propios, no agentes paralelos. El contenedor está excluido solo
localmente en .git/info/exclude. No borrarlos ni volver a crear las ramas.

## Cambios pendientes y bloqueos humanos

- Auditoría/estado publicados en PR #28; revisión humana y checks finales.
- Canonicales #6/#16/#17/#18/#19 marcadas blocked por insumos pendientes;
  #13 sigue status:review. Ninguna cerrada ni approved por el agente.
- Acción humana consolidada: https://github.com/jea27/Lut_generator/issues/29.
- Revisar/aceptar o corregir instrumentos y herramientas. El agente no aplica approved.
- Usuario: aportar actas anonimizadas reales o autorizar un canal/candidatos
  concretos de reclutamiento; no publicar contactos en GitHub.
- Usuario: aportar 20 pares privados con registros de uso/preparación de color.
  Informar la ubicación por canal privado, no subir fotos o permisos con PII.
- Dataset listo y acceso autorizado son prerrequisitos del benchmark. Colourlab
  v4 documenta Apple silicon; no presumir Windows por una promesa antigua.
- No crear cuentas, instalar herramientas, aceptar condiciones, gastar o enviar
  fotos a servicios externos sin autorización específica.
- P0 completo y autorización explícita son condiciones separadas antes de P1.

## Próximas tareas elegibles

Ahora solo faltan revisión, evidencia real o acceso. No queda una ejecución de
investigación P0 que pueda producirse sin esos insumos. Al llegar datos: validar
el primer lote de COL-002 o COL-004, registrar ausencias/fallos, sintetizar
COL-001 y después ejecutar COL-003. No repetir investigación documental o
pruebas ya pasadas si no hay cambios o fallo nuevo.

## Instrucciones concretas de reanudación

1. Leer AGENTS y este estado; `git status --short --branch`; `git worktree list`.
2. `git fetch origin main`; consultar Issues #6, #13, #16–#19 y sus solicitudes
   humanas nuevas. No confundir comentario/merge con aceptación de tarea.
3. Conservar modificaciones locales y reutilizar ramas/PR. Incorporar main
   solo si es seguro; no reset destructivo, force push ni merge de PR por IA.
4. Comprobar el registro local autorizado con:

```powershell
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/p0_status.py --github --ready
```

Exit 2 por falta de evidencia/aprobación es esperado, no error que deba taparse.
Opciones --interviews/--dataset/--benchmark y --media-root leen ubicaciones
privadas explícitas. No publicar respuestas ni rutas privadas en informes.
5. Si existe nueva evidencia o código modificado, ejecutar tests adecuados y
   documentar el resultado. Si no, no repetir las 64 pruebas por rutina.
6. Actualizar la Issue de tarea y el checkpoint, publicar solo su rama y abrir
   PR. Solicitudes nuevas: título LUMAFORGE ACCIÓN REQUERIDA y siete campos;
   reutilizar marcador para no duplicar notificaciones del mismo bloqueo.
7. Jamás iniciar el motor/P1 por un exit 0: p0_status no concede autorización.
