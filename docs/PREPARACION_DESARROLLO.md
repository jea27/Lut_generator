# Preparación oficial del desarrollo · 2026-10-30

> Registro de la preparación inicial. Estado posterior, integración de avisos,
> herramientas localizadas y publicación autorizada: `PUBLICACION_COL-001.md`.
> El manejador CJS preparado inicialmente fue sustituido por el workflow inline
> validado de main. La suite actual tiene 21 pruebas Python.

## Estado comprobado al comenzar

- Raíz Git: `%USERPROFILE%/Documents/ChatGPT/Lut generator`, estructura ya corregida.
- Árbol limpio en `codex/fix-repository-root`; no se sobrescribieron cambios ajenos.
- Remoto: `https://github.com/jea27/Lut_generator.git`, público, rama principal main.
- Fetch de solo lectura: main en `fa9883e08641f7025be5ab9b9c809d3d724509aa`.
- [PR #1](https://github.com/jea27/Lut_generator/pull/1) integrada por el propietario.
- [Despliegue existente](https://github.com/jea27/Lut_generator/actions/runs/41076651158): success.
- [Validación anterior de PR](https://github.com/jea27/Lut_generator/actions/runs/41076449914): success.
- [Aviso anterior](https://github.com/jea27/Lut_generator/actions/runs/41075737859): skipped,
  no acredita envío ni entrega móvil.
- Consulta API pública de todas las Issues y PR: una PR histórica, **cero Issues COL**.
- [Web](https://jea27.github.io/Lut_generator/) y su JSON: HTTP 200;
  mode github, repository_url correcto, updated_at `2026-10-30T15:00:36.865482Z`.
  42 tareas planned, cero aprobadas. Navegador: inicio, hoja de ruta, filtro P0
  (seis tareas), detalle COL-001 y criterio de aceptación visibles y funcionales.
  No se ha probado físicamente en un teléfono ni cambiado contenido publicado.

## Entorno y verificaciones

Sin instalaciones, cambios de PATH persistente, tokens ni cambios de permisos.
Python WindowsApps sigue siendo un alias; el comprobador ahora lo evita y usa
Python 3.12.14 ya incluido en Codex, o la ruta indicada con `-PythonPath`.
`gh` no encontrado en PATH ni ubicaciones inspeccionadas: autenticación gh,
variables Actions y configuración Mobile sin verificar. No se infiere ausencia
de credenciales Git a partir de la ausencia de gh.

En el terminal inicial: Git 2.54.0.windows.1 y Node 24.15.0. El proceso Windows
PowerShell del comprobador devolvió Git 2.56.0.windows.3 y Node 26.13.0. No se
instalaron esas versiones en esta sesión. La CI conserva Node 22 y Python 3.12;
su ejecución nueva sigue pendiente. No se afirma reproducibilidad de CI sin run.

Comandos ejecutados desde la raíz:

```powershell
# Python mediante el ejecutable ya incluido en Codex:
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
node --test tests/notify_human.test.cjs
node --check site/app.js
node --check site/data/fallback.js
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/check_setup.ps1 -SkipGitHub
git diff --check
```

Resultados: **17 unittest OK**, **8 pruebas Node OK**, sintaxis JS correcta,
DRY RUN de 42 tareas, comprobador local exit 0 con GitHub omitido explícitamente.
Prueba negativa con ruta Python inexistente: exit 1, como corresponde.
La integración del sync se prueba con ficheros temporales: el ejemplo done del
log pertenece exclusivamente a fixtures de prueba, no al roadmap versionado.

PyYAML 6.0.3 ya disponible en la carpeta temporal de la sesión anterior, sin
instalarlo de nuevo: tres YAML válidos, sin claves duplicadas; comprobaciones
de contratos de eventos, checkout main, permisos y exclusión mutua Pages OK.
No hay actionlint disponible. La validación local no sustituye Actions real.
Verificación de JSON/fallback: mismos datos, IDs COL-001…COL-042 únicos,
seis fases, todos los estados intactos. No se ha modificado roadmap.json ni su
fallback versionado para reflejar trabajo que aún no está publicado en GitHub.

## Cambios locales preparados

- Rama nueva `codex/COL-001-preparacion-p0`, creada desde origin/main actualizado.
- Seguimiento: tests reales de dry-run; sync bloquea needs-human, no presenta
  PR borrador como lista, limita PR a main, conserva merges frente a PR descartadas
  y sincroniza también fallback dentro del artefacto publicado.
- Nuevo workflow independiente `Sincronizar roadmap`, desde main, para Issues,
  finalización de validación de PR, cron y manual. Misma cola y mismos permisos
  Pages que el despliegue existente; sin cambios remotos de configuración.
- Validación de PR conserva solo lectura y no usa el entorno Pages. El nuevo
  refresco por workflow_run no ejecuta código ni descarga artefactos de la PR.
- Avisos: prueba manual con número de Issue, blocked/needs-human, revisión COL y
  fallos/timeout del mismo repo. Manejador solo de main, deduplicación por run e
  intento. No cambia aprobaciones ni cierra Issues. Las etiquetas y la variable
  deben existir; fallos de forks, del agente desconectado y del propio aviso
  quedan fuera de este mecanismo. Si main todavía no tiene el nuevo manejador,
  el aviso deja warning y no envía: repetir prueba después de integración.
- COL-001: preparación del guion, segmentos y registros, sin fabricar evidencia.
  Detalle: `P0_COL-001_SEGMENTOS.md`; descripción PR: `PR_COL-001_PREPARACION.md`.

No hay Issue real ni PR nueva; las operaciones de escritura esperan autorización
del usuario. La preparación local no se declara tarea aceptada. El motor y la
arquitectura de producto no se han modificado.

## Operaciones remotas propuestas, no ejecutadas

Opción recomendada: publicar esta entrega en su rama, crear solo la Issue COL-001
y abrir PR de preparación parcial. Importar las otras 41 puede esperar.
El usuario revisa e integra; el agente no hace merge ni push a main.

Una vez gh esté disponible y su autenticación se compruebe, los comandos son:

```powershell
git push -u origin codex/COL-001-preparacion-p0
gh label create roadmap --color 0969DA --repo jea27/Lut_generator
gh label create status:in-progress --color 1D76DB --repo jea27/Lut_generator
gh label create needs-human --color F9A825 --repo jea27/Lut_generator
gh label create blocked --color D73A4A --repo jea27/Lut_generator
gh issue create --repo jea27/Lut_generator --title "[COL-001] Definir segmentos y trabajos por resolver" --body-file docs/P0_COL-001_SEGMENTOS.md --label roadmap --label status:in-progress
gh pr create --repo jea27/Lut_generator --base main --head codex/COL-001-preparacion-p0 --title "[COL-001] Preparar validación P0 y seguimiento verificable" --body-file docs/PR_COL-001_PREPARACION.md
```

Antes se consultarán de nuevo etiquetas, Issues y PR para reutilizar existentes,
evitar duplicados y no sobrescribir colores/descripciones. No se instalará gh
sin autorización; una alternativa es usar una ruta ya instalada aportada por el
usuario o preparar la operación equivalente con la API autenticada existente.

Para la prueba móvil tras integrar, solicitar autorización separada para
configurar `REVIEWER_GITHUB=jea27` si falta, crear una Issue COL-000 de prueba y
ejecutar el workflow manual con su número real. La solicitud detallada de la
prueba irá en la Issue; el usuario confirma recepción y realiza el cierre.
Verificar run, comentario bot y recepción. No alterar permisos/protecciones,
crear tokens ni provocar fallos de producción para esta prueba.

La alternativa es mantener todo local hasta revisar cambios. Impide validar
los workflows nuevos y el móvil, pero conserva la publicación actual intacta.

## Pendientes reales

- Autorización de push/PR y creación de la primera Issue; gh operativo o API autorizada.
- Integración humana y validación de Actions nuevos; prueba móvil real.
- Entrevistas y aceptación de COL-001; continuar COL-002/004/005 de P0.
- Revisar en una futura tarea requires_pr de COL-018 y COL-039 antes de P2/P5;
  no se altera esa política silenciosamente en esta entrega.
- P0 y COL-006 sin superar; motor detenido.

Referencia de seguridad de la preparación: [eventos workflow_run de GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_run).
