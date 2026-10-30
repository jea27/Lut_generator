# Publicación de preparación COL-001 · 2026-10-30

## Alcance y estado real

El usuario autorizó publicar `codex/COL-001-preparacion-p0`, crear la Issue
canónica COL-001 y abrir PR a main. Sin merge ni aprobación por el agente.

Issue de producto: https://github.com/jea27/Lut_generator/issues/6.
Etiquetas roadmap y status:in-progress, abierta; no approved. Preparados
segmentos hipotéticos, guion y plantillas; faltan entrevistas y mapa validado.
La PR es una entrega parcial de preparación, sin cierre automático de la Issue.

## Integración y conservación

Se incorporó origin/main `871a37c`, que contiene la PR #4 integrada por jea27.
Se conservaron el protocolo de AGENTS, las evidencias históricas y el workflow
de avisos probado. Los conflictos se resolvieron en la rama de trabajo.
Se retiraron el manejador CJS anterior y sus pruebas porque el workflow
integrado usa el script inline probado; no se publican dos implementaciones.

La rama añade el refresco de roadmap desde main por eventos y cron, pruebas del
sync, fallback coherente y el material de P0. Su activación queda pendiente de
integración humana. Para reflejar esta entrega sin modificar main se reutiliza
el workflow ya desplegado: repetir la ejecución push de main, que consulta
Issues/PR y despliega el artefacto. No se cambia JSON manualmente ni se hacen
commits de estados ficticios.

## Herramientas, pruebas y privacidad

- gh ya instalado en `%ProgramFiles%\GitHub CLI\gh.exe`, autenticado como jea27;
  no se reinstaló. El comprobador local ahora lo encuentra aunque falte en PATH.
- Python 3.12 incluido en Codex: **21 unittest OK**, incluyendo cuatro pruebas
  del script exacto del aviso de Actions y seis nuevas de sync.
- Sintaxis de app.js/fallback.js correcta; importación continúa en simulación.
- Revisión de archivos y diff: documentación, scripts, pruebas y workflows;
  sin medios privados, grabaciones ni datos de participantes.
- Barrido local de texto para claves privadas, tokens GitHub/AWS, URL con
  credenciales, correos y rutas de perfil personal: sin hallazgos en la entrega.
  Se sustituyeron rutas locales por placeholders. Las referencias a tokens
  son nombres de variables de Actions y valores ficticios de tests.
- Se publica un commit consolidado basado en main para no publicar rutas de
  perfil de los commits locales preliminares; el trabajo original se conserva
  en una rama de respaldo exclusivamente local. Autor del nuevo commit con
  identidad pública y correo noreply de GitHub.

Esto documenta una inspección y búsqueda de patrones, no una garantía universal
de detección. No se imprimieron ni copiaron credenciales del almacén local.

## Notificaciones

REVIEWER_GITHUB=jea27 comprobado por API. Se mantiene el workflow que publica
avisos en Issues con needs-human, sin ampliar permisos. Prueba real previa:
https://github.com/jea27/Lut_generator/actions/runs/41079364488 y confirmación
del usuario «Sí, recibida en el móvil» en la Issue #3/chat.
Revisión mediante Issue vinculada validada en run 41080088759 y deduplicación
en run 41080353905. Los enlaces de la nueva PR y sus checks se registran en la
Issue y en la entrega del chat después de su creación.

## Revisión humana pendiente

Revisar esta preparación y solicitar cambios o integrar personalmente la PR.
No aceptar COL-001 hasta recoger evidencia real de entrevistas. Ningún aviso
ni check verde equivale a aprobación. El motor permanece sin iniciar.
