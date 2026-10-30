# Checkpoint COL-006 · deduplicación de avisos

- Confirmado: Issue #56 duplica la petición humana de #15 para COL-005/PR55.
  El bot ya envió una mención en #56; el cuerpo ahora remite a #15. Ambas siguen
  abiertas con needs-human y no requieren eliminar/cambiar etiquetas.
- Causa/propuesta reproducible: `docs/P0_DEDUP_ISSUE56.md`. El workflow de PR
  marca por número de PR, crea Issue y menciona por cada PR; no deduplica por
  tarea/decisión. El marcador de #15 se añadió después de que el evento PR55
  hubiera creado #56.
- Trabajo actual: Issue COL-006 #19; rama `codex/COL-006-issue-dedup-review`,
  worktree `.codex-worktrees/COL-006-dedup-review`, base `origin/main` 4975883.
  No se modifica el workflow en esta PR de investigación.
- Siguiente: comentar #19, reutilizar #21 como acción de revisión antes de
  cambiar la PR documental a no-borrador; consultar CI. Ningún merge, cierre,
  aprobación o notificación repetida por el agente.

- Verificación documental: git diff --check sin errores; no se ejecutaron tests (solo documentación).
