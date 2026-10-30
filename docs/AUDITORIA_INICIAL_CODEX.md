# Auditoría inicial · 2026-10-30

## Alcance y estado

Leídos PROMPT_INICIAL_CODEX.md, AGENTS.md, todos los documentos de docs,
README.md, GUIA_WINDOWS_CODEX.md y roadmap.json. Revisados scripts, tests,
workflows y fuentes del dashboard. El material adjunto aporta contexto y
reglas del proyecto; no constituye autorización para sus ejemplos de altas
remotas, instalaciones o publicación.

Extraído el ZIP en `lumaforge/` dentro del workspace. No se han hecho commits,
cambios de rama, altas remotas, autenticación, instalación de herramientas,
push, importación real de Issues ni envío de notificaciones. No se ha
implementado el motor de color.

## Evidencia local

- Git 2.54.0.windows.1; Node v24.15.0; npm y Codex localizados.
- Git del workspace: rama inicial `master`, sin commits y sin remotos;
  `lumaforge/` figura como carpeta no seguida. No hay repositorio Git propio
  dentro de esa carpeta.
- `gh` y `actionlint` no están en PATH. Autenticación GitHub no verificada.
- `python` resuelve al alias WindowsApps y no ejecuta Python; `py` ausente.
- Python incluido en Codex: 3.12.14, ejecutable
  `C:\Users\jeast\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
- Con ese ejecutable, `-m unittest discover -s tests -v`: **11 tests OK**
  (8 del sincronizador, 3 del importador).
- Con ese ejecutable, `scripts/import_issues.py`: **DRY RUN, 42 candidatas**,
  sin llamadas de escritura remota.
- `node --check site/app.js` y `node --check site/data/fallback.js`: OK.
- Comprobación con Node/assert: 42 IDs únicos consecutivos COL-001…COL-042,
  seis fases válidas, criterios presentes, todas planificadas, 0 aprobadas;
  `fallback.js` y `roadmap.json` contienen los mismos datos iniciales.
- No se ha hecho prueba visual en navegador ni ejecución de Actions/Pages.

## Hallazgos antes de publicar

1. **Raíz Git incorrecta para subir directamente.** Los workflows están en
   `lumaforge/.github/workflows`, pero Git está en el directorio padre.
   Hay que alinear la raíz del proyecto y de Git antes del primer commit.
   Propuesta: mover el contenido del starter a la raíz actual, sin sobrescribir
   archivos existentes; conservar el `.git` ya creado. Revisar destinos antes.
2. **No hay CI que pruebe el código propuesto en las PR.** El único workflow de
   tests hace checkout explícito de `main`; no escucha `synchronize`.
   Crear CI independiente para el commit de la PR y actualizaciones de rama.
3. **Aviso manual inoperante.** `workflow_dispatch` está declarado en el aviso,
   pero su condición de job solo permite eventos Issues o PR. Además no recibe
   número de Issue. Usar la etiqueta sobre una Issue de prueba, o corregir
   explícitamente la interfaz manual y probarla.
4. **Prueba de simulación insuficiente.** `test_dry_run_never_uses_gh` únicamente
   comprueba `callable(main)`. Debe ejecutar main con argumentos controlados y
   verificar que subprocess/gh no se llama.
5. **Aprobación sin PR para tareas de código.** COL-018 (biblioteca) y COL-039
   (instrumentación) tienen `requires_pr: false`. Decidir y corregir antes de
   confiar en que toda implementación exige una PR fusionada.
6. **Asociación de PR ambigua.** El sync elige la PR más recientemente actualizada
   por ID; una PR nueva o descartada puede desplazar una previamente fusionada.
   No valida base `main` ni distingue PR borrador al marcar revisión. Faltan
   pruebas de API/paginación, duplicados y múltiples PR por tarea.
7. **`needs-human` no equivale a bloqueo visual.** El sincronizador solo reconoce
   `blocked`. Acordar si se aplican ambas etiquetas al esperar una decisión.
8. **Datos de respaldo y conexión.** El sync actualiza JSON pero no fallback;
   una primera carga sin red puede mostrar la planificación inicial. Tras un
   error posterior de red la UI conserva “GitHub conectado” sin indicar fallo.
9. **Publicación desde evento PR.** El workflow intenta desplegar desde eventos
   PR aunque haga checkout de main. Revisar las reglas del entorno Pages y
   separar validación de PR de publicación autorizada desde main/cron.
10. **Documentación desalineada.** README dice que falta crear importador cuando
    ya existe; describe PR solo por cron aunque el workflow escucha eventos PR.
    El dashboard conserva decisiones como “Propuesto” que el traspaso presenta
    como acordadas. No corregir estados de tareas para simular avance.
11. **Privacidad y permisos aún sin validar.** La solución de dos repositorios
    no existe. No publicar automáticamente metadatos de un futuro repo privado.
    Con las credenciales del propietario, las instrucciones por sí solas no
    imponen separación técnica de aceptación.
12. **Comprobador de herramientas débil.** `check_setup.ps1` confunde el alias
    de Python con una instalación, no comprueba Node y no garantiza código de
    salida de fallo cuando falla un comando nativo.

Referencias oficiales consultadas para preparar la configuración:
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments

No se han revalidado precios o afirmaciones del estudio de mercado; se conservan
como investigación heredada, sin asumir vigencia ni verificación independiente.

## Secuencia propuesta, por etapas

1. Preparación local: alinear raíz, corregir bloqueos del seguimiento, añadir
   pruebas significativas y volver a ejecutar comprobaciones. Instalar gh y
   un Python accesible si se acuerda; autenticar interactivamente sin registrar
   tokens. Sin instalación ni autenticación realizadas en esta auditoría.
2. Confirmar propietario/repositorio y visibilidad. Consultar identidad y
   repositorio con gh en modo lectura. Preparar primer commit de bootstrap;
   la publicación inicial de main es una excepción que exige autorización
   expresa, porque AGENTS prohíbe los push ordinarios a main.
3. Solicitar aprobación de la operación remota exacta. Para repo nuevo,
   una vez confirmada la raíz correcta, el comando propuesto será:
   `gh repo create OWNER/REPO --public --source . --remote origin --push`
   (o `--private` según la decisión; nunca reutilizar origin sin comprobarlo).
   No ejecutarlo con placeholders ni antes de la aprobación. Si ya existe el
   repo, preparar otro procedimiento tras inspeccionarlo.
4. En una autorización posterior: habilitar Pages con Actions y configurar
   `gh variable set REVIEWER_GITHUB --body LOGIN --repo OWNER/REPO`.
   El contenido que se publicará debe ser revisado antes. Validar entorno,
   permisos y ejecución; no afirmar URL publicada antes de comprobarla.
5. Simular otra vez la importación; consultar IDs existentes en el repo real.
   Pedir aprobación explícita para crear/actualizar las seis etiquetas y
   ejecutar `python scripts/import_issues.py --apply` (hasta 42 Issues).
6. Pedir aprobación de una Issue temporal COL-000 y etiqueta needs-human.
   Comprobar ejecución del aviso y comentario del bot. El usuario confirma
   recepción en GitHub Mobile; workflow verde no demuestra entrega al teléfono.
   El cierre de prueba queda a cargo humano.
7. Validación integral: cambio real de etiqueta en una Issue acordada,
   workflow de sincronización correcto, JSON publicado con enlaces reales,
   dashboard coherente desde móvil y prueba del aviso confirmada. Conservar
   enlaces de ejecuciones y evidencia. No autoaprobar tareas para probar.
8. Solicitar autorización del procedimiento ordinario de ramas codex/COL-…,
   push y PR; nunca merge, cierre de Issues ni aplicación de approved por IA.
   Primera entrega sugerida: COL-001, documento y plantilla de entrevistas
   para revisión humana; no inventar entrevistas realizadas. Motor pendiente
   además del go/no-go explícito de COL-006.

Estado final de la auditoría: comprobaciones locales parciales satisfactorias;
seguimiento remoto y notificaciones móviles **no validados**.
