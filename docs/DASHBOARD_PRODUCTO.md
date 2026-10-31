# Centro de control de Color Studio

Entrega COL043#72/PR74; operación independiente, no modifica la decisión P0,
las42 tareas o código de apps/packages. Worktree independiente. Auditoría inicial:
sync_github.py publica un estado, Issue y PR principal por tarea; no catalogaba
capacidades, versiones, instalador, CI, puertas de entrega o aceptación separada.
El dashboard anterior medía aprobación de planificación, no trabajo técnico del MVP.

## Fuentes y reglas

`site/data/product-manifest.json` es el contrato versionado:15 capacidades,
8 entregables del núcleo con criterio explícito, Issues/PR ya existentes, tests,
predicados de evidencia y denominadores. Glow/difusión/fade son componentes de
un solo entregable de acabado; futuro e integraciones no inflan ese contador.
No duplica las42 tareas ni cambia sus estados, títulos o criterios.

`scripts/sync_product.py` consulta únicamente metadatos de repositorio público:
Issues, PR, últimos100 runs generales y100 de main, releases, artefactos recientes
y SHA de main. No descarga/ejecuta artefactos, logs o código de PR. Lee evidencias
solo del checkout confiable de main. Salida allowlist en product.json y fallback
JS; el navegador no recibe tokens. Capturas locales son previsualización del
pipeline con datos reales, nunca prueba de despliegue de esta PR en Pages.

- **Implementado:** archivo de código versionado y entrega declarada integrada
  hacia main. Un merge en rama intermedia no basta.
- **Verificado técnicamente:** implementación anterior, tests existentes, CI
  requerida correcta para el SHA exacto de main y todos los predicados de
  evidencia. Es verificación de alcance declarado; no calidad estética total.
- **Para revisar:** entrega implementada sin aceptación explícita. Borrador
  nuevo o status:in-progress muestra trabajo activo sin borrar baseline previo.
- **Aprobado (capacidad):** comentario autenticado de jea27 y recibo Actions para
  ese ID y huella de código. Ni cerrar una Issue compartida ni su etiqueta approved
  aprueban capacidades. Las42 tareas mantienen sus reglas históricas de aceptación.
  Ver REVISIONES_HUMANAS.md.
- **Bloqueado:** etiquetas reales de la Issue tienen precedencia; los ejes
  implementado/verificado siguen visibles. Futuro permanece pendiente aunque
  comparta Issue con el acabado manual aceptado.

Contadores muestran x/y, denominadores definidos; porcentaje solo cuando todos
los valores son conocidos. Datos ausentes → Sin datos, nunca cero inventado.
Beta y venta tienen puertas distintas; la inspección local del instalador no
cumple Windows limpio. Ninguna métrica otorga GO o permiso de publicación.

Release publicada se muestra como hecho. **Descarga habilitada** exige también
etiqueta humana `release-approved:TAG_EXACTO` en Issue62 y asset.exe uploaded
cuyo digest SHA256 de GitHub coincide con manifiesto versionado de commit limpio
de esa versión. Esta etiqueta es específica de distribución, no approved de
funcionalidades. El agente no la aplica. Sin coincidencia, autorización o con
snapshot obsoleto/no actualizado no aparece botón de descarga. No se ha creado
release, etiqueta de aprobación o descarga externa en esta entrega.

## Actualización automática

Se amplía el workflow existente, sin cambiar permisos del token/repositorio:
Issues editadas/etiquetadas/cerradas, PR abiertas/sincronizadas/cerradas (incluye
merge), releases publicadas/editadas/eliminadas, CI relevante completada y cron.
Push a main conserva validación/publicación anterior y recoge manifiestos nuevos.
La compilación de candidato completada refresca metadatos de artefactos, aunque
un ZIP de Actions no se convierte en candidato auditado por existir.

pull_request_target solo dispara lectura de **main**; nunca checkout del head,
descarga de artefacto o interpolación de cuerpos en shell. workflow_run no incluye
Sincronizar roadmap, evitando bucle propio. No se amplían permisos sensibles.
Si un endpoint público devuelve403 por alcance del token, se intenta GET anónimo
solo después de constatar repositorio público; no es escalada de permisos.
429/errores transitorios tienen reintentos limitados. Paginación con límite y
validación de forma falla cerrada. Error → no reemplazar snapshot ni desplegar;
Pages conserva última publicación completa y UI indica antigüedad>2h/fallo fetch.
Funciones puras son idempotentes para las mismas entradas/observed_at.

El CI de la PR prueba consultas reales con token contents:read y fallback público,
además de tests deterministas sin red. Publicación automática nueva solo queda
activada **después de integración humana**, no al abrir la PR.

## Contrato del agente que entrega producto

Al preparar una funcionalidad: conservar ID de capacidad si ya existe; actualizar
criterio/tests/evidencia y PR de integración en este manifiesto dentro de la misma
entrega, sin editar porcentajes o product.json manualmente. Las etiquetas/PR/CI
actualizan automáticamente estados publicados; el responsable no edita roadmap.
Una capacidad nueva solo añade un ID de producto y relación con tarea histórica,
sin crear duplicado de Issue o alterar las42 tareas. Hasta integración confiable,
su PR ya aparece en actividad/CI; no se ejecuta su manifiesto no revisado desde
workflow privilegiado. Incluirla en un denominador requiere criterio definido,
no contar líneas o aumentar porcentaje al añadir subtareas.

Builds se reconocen en docs/evidence/*ARTIFACT*.json, con versión válida, source
SHA40, sha256, tamaño positivo y dirty=false para candidato. El agente prepara
ese manifiesto saneado como evidencia de entrega; rutas/credenciales quedan
fuera. No se renombra una versión arbitraria de un ZIP para llamarla verificada.

Comprobar tras cada integración: run de sync/publicación success; HTTP de
data/product.json con source_version, main_sha, contadores y enlaces reales.
Si falta API o evidencia, conservar Sin datos y corregir la causa.

COL043 fue creada por el otro chat durante esta sesión y se reutiliza como
operación canónica. Su estado se consulta por Issue72/PR74, fuera de las42
tareas y denominadores. La rama conserva su nombre publicado COL006 para
preservar commits/enlaces; no se crea otra Issue equivalente. Coordinación
en73: no tomar el worktree mientras este chat esté activo; al terminar quedan
commits protegidos para comparar/completar únicamente huecos.
