# Beta Windows · plan de entregas y auditoría

2026-10-30. Autorización técnica nueva: P1/P2 y estabilización/distribución.
Prioridad P0 de esta tabla significa bloqueo de **beta**, no aprobación de la
investigación comercial P0. COL001 sigue pendiente de entrevistas reales.

| Prioridad | Issue existente | Entrega y criterio pendiente |
|---|---|---|
| P0 | COL036 #57 | Instalador Tauri2+NSIS x64 por usuario, frontend+motor incluidos; prueba limpia Windows10/11 pendiente |
| P0 | COL037 #58 | Supervisión sidecar, sesión loopback, escritura atómica, lotes cancelables, presets CRUD y recuperación; revisión humana pendiente |
| P0 | COL038 #59 | LUT33³ sRGB consistente con renderer; importación real en Adobe bloqueada por inicio de sesión; Resolve ausente |
| P0 | COL040 #60 | Inventario/licencias y privacidad; decisión sobre código público, marca y revisión legal pendientes |
| P0 | COL041 #61 | Matriz calidad/hardware e instalación limpia; faltan retratos autorizados y pruebas externas |
| P1 | COL042 #62 | Landing local, borradores comerciales, firma/distribución propuestas; sin cobros ni lanzamiento |
| P2 | COL037 #58 | Actualizaciones firmadas con rollback, diagnóstico opt-in, no implementados; reinstalación manual únicamente |

## Lo conservado y lo experimental

PR52 y PR53 fueron integradas por jea27 durante la sesión; se reutilizan motor
Lab y editor Vue, sin rehacerlos. Main actualizado incorporado por fast-forward
local en la rama beta, conservando documentación posterior PR63/64.
El matching es una transformación global estadística con límites, no segmenta
piel ni comprende contenido. La intensidad0 es identidad del RGB normalizado;
ICC/orientación/8bits implican conversiones documentadas. Preview y exportación
usan la misma LUT; cambiar resolución puede cambiar la percepción, no la receta.
No prometer resultados naturales universales antes de pruebas visuales variadas.

Las imágenes importadas se convierten a copias privadas sRGB PNG; no se escriben
originales. Los presets, preferencias, jobs y outputs sobreviven al reinicio.
El historial undo/redo y las asignaciones de imagen del editor son de sesión.
Un lote interrumpido conserva resultados y se marca interrupted, no se reanuda
ni se inventa completado. Nuevo intento crea carpeta nueva. Máximo16 fotos/lote,
32 copias temporales, 24MP/32MiB por entrada y100 presets.

## Herramientas aprobadas

Rust1.99.1/MSVC, Visual Studio Build Tools2022 17.14.44 C++/SDK, PyInstaller6.22.3
y CLI Tauri2 instalados con permiso explícito; no se reinstalan herramientas.
WebView2 ya existía. Compilación bloqueada por Cargo.lock/package-lock y pip;
esto no garantiza binarios idénticos: toolchain Windows/WebView2/NSIS también
deben conservarse con sus hashes antes de una release estable.

`scripts/build_beta.ps1` compila candidato local. El workflow manual
beta-candidate solo conserva artefacto7d, no crea Releases ni cambia permisos.
No se instala un actualizador automático, no se envían imágenes ni telemetría.

Ver BETA_WINDOWS.md, BETA_COMERCIAL.md y evidence/BETA_02_QA.md para ejecución,
límites y decisión GO/NO-GO. Ningún check ni esta documentación aprueba tareas.
