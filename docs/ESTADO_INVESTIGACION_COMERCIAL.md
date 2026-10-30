# Checkpoint de investigación comercial · 2026-10-30

## Estado de trabajo

- Trabajo en curso: COL-005, Issue #13; rama independiente
  `codex/COL-005-look-match-positioning`, worktree
  `.codex-worktrees/COL-005-look-match-positioning`, base `origin/main` 4975883.
- #56 se confirma duplicada de #15: ambas solicitaban la revisión COL-005/PR55.
  #56 conserva needs-human y redirige a #15; no se cerró ni etiquetó ninguna Issue.
- PR #55 ya fue integrada por jea27. No se vuelve a modificar ni repetir su
  investigación de precios/licencias/España-UE.
- El checkout principal está en `codex/COL-037-beta-estabilidad` con cambios
  locales; no se alteró ni se escribió desde este worktree.

## Alcance Look Match

- Producto propuesto para objetivo comercial v1.0: Color Match y Look Match como
  operaciones separadas, con el acabado visual además del color.
- Estado verificado contra los documentos/evidencias disponibles: Color Match
  global Lab, intensidad, exposición, contraste, saturación y temperatura
  implementados en v0.1; curvas editables pendientes. Ningún efecto Look Match
  tiene implementación o experimento ejecutado. Bloom/glow, halation, difusión,
  blur suave, fade, microcontraste, suavizado y atmósfera siguen pendientes.
- Desk research solo con documentación oficial; no se ejecutaron competidores,
  benchmark, entrevistas o pruebas de Look Match. Ver
  `docs/LOOK_MATCH_REQUIREMENTS.md`.
- Se propone en GitHub coordinar COL-005 (hipótesis), COL-019 (render/export) y
  COL-026 (composición de looks). No se modifica manualmente el roadmap JSON
  mientras la rama beta del agente principal está activa.

## Verificación / reanudación

- Pendiente: finalizar publicación de PR documental no borrador, incorporar su
  enlace a la solicitud #15 existente antes de activar `ready_for_review`, y
  consultar CI. No ejecutar tests locales por ser cambio documental; registrar
  los resultados automáticos si el workflow los ejecuta.
- Ningún trabajo en `apps/`, `packages/` o motor. P0 entrevistas y benchmark
  siguen pendientes de datos reales/permisos.
