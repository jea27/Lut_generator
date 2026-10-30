# Estado de recuperación del agente · 2026-10-30

## Tarea actual y rama

Coordinación y puerta de P0 (COL-006, Issue #19), rama
`codex/COL-006-coordinacion-p0`. No es una decisión go/no-go ni aprobación.
P1 y el motor de color permanecen sin autorizar.

## Trabajo conservado y completado

- Inicio limpio desde origin/main e819461; documentación previa conservada.
- COL-005: PR #14 integrada por jea27, Issue #13 abierta y sin approved.
  Estado review correcto; falta aceptación documental humana. No implica
  que las hipótesis se hayan contrastado. No cerrar/aprobar desde el agente.
- COL-001: Issue #6 abierta, sin entrevistas reales registradas.
- Seguimiento, Pages y recepción Mobile verificados en sesiones anteriores.

## Tareas independientes en preparación

| Tarea | Issue | Rama | Carpeta local desde la raíz |
|---|---|---|---|
| COL-002 | #16 | codex/COL-002-evidencia-entrevistas | .codex-worktrees/COL-002 |
| COL-003 | #17 | codex/COL-003-protocolo-benchmark | .codex-worktrees/COL-003 |
| COL-004 | #18 | codex/COL-004-manifiesto-dataset | .codex-worktrees/COL-004 |
| COL-006 | #19 | codex/COL-006-coordinacion-p0 | raíz actual |

Son worktrees independientes, sin agentes adicionales. No borrar ni mezclar
sus archivos. La carpeta contenedora se excluye solo en .git/info/exclude.

## Pruebas y cambios pendientes

Base integrada: 21 unittest ya comprobadas. No repetir sin cambios relevantes.
Checkpoint 1: avisos con título/campos obligatorios, deduplicación por PR y
petición de Issue; modo manual con target validado. 27 unittest raíz OK.
COL-004 tiene manifiesto de 20 slots y validador de integridad, 30 unittest OK
(incluye 9 nuevas). Faltan medios: 0 pares listos. Publicación todavía pendiente.
Siguiente trabajo independiente: registro de actas COL-002 y protocolo COL-003.

## Bloqueos humanos

- COL-001/002: hacen falta participantes y actas reales anonimizadas.
- COL-004: hacen falta medios y revisión documentada de permisos de uso.
- COL-003: dataset listo y acceso permitido a las herramientas; no comprar,
  crear cuentas ni subir imágenes a servicios externos sin autorización.
- COL-005: aceptar o corregir el instrumento, no las hipótesis como hechos.
- COL-006: evidencia P0 completa y autorización humana explícita para P1.

## Próximas tareas elegibles

Preparar y probar las herramientas de registro COL-004/002 y protocolo COL-003;
documentar la puerta COL-006 y consolidar solicitudes humanas sin duplicados.
La preparación parcial no satisface los criterios finales de entrevistas,
dataset ni benchmark. No inventar datos para hacer pasar un gate.

## Cómo reanudar

1. `git status --short --branch` y `git worktree list`; no reset/stash destructivo.
2. Leer este archivo, AGENTS y comentarios nuevos de Issues #6, #13, #16–#19.
3. Consultar PR/Actions y obtener origin/main sin modificarlo directamente.
4. Entrar en la carpeta del worktree de la tarea y comprobar su estado antes
   de editar. Conservar cambios ajenos. Reutilizar Issue/PR, no duplicarlas.
5. Ejecutar `python -m unittest discover -s tests -v` con Python funcional
   (puede usarse el ejecutable incluido en Codex). gh está en
   `%ProgramFiles%/GitHub CLI/gh.exe` si no aparece en PATH.
6. Tras pruebas: commit/push solo a la rama de tarea, PR hacia main y aviso
   `[LUMAFORGE] ACCIÓN REQUERIDA — ...` con los siete campos exigidos.
7. Actualizar este punto de recuperación con commits, PR, checks y bloqueos.
   No aprobar, cerrar Issues de producto ni hacer merge.
