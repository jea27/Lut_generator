# COL036 · incidente de datos P0: abierto

Fecha: 02-11-2026. [Issue57](https://github.com/jea27/Lut_generator/issues/57),
[solicitud67](https://github.com/jea27/Lut_generator/issues/67) y
[PR90](https://github.com/jea27/Lut_generator/pull/90), en borrador.
**Causa histórica y proceso responsable sin demostrar. Beta externa y venta NO-GO.**

## Evidencia y alcance

- Se preservaron copias y hashes del diagnóstico privado. No se publica JSON,
  nombres, rutas, identificadores NTFS ni filas USN. No se restauraron archivos.
- Cuatro PNG tienen eventos FILE_DELETE/CLOSE en el diario aportado por el operador.
  Coinciden con los cuatro nombres ausentes de la primera comparación. El diario
  prueba cambios de archivos, no identifica por sí solo al proceso responsable.
- La comparación externa tiene1 presente/8 ausentes respecto a9. Las capturas
  dentro y fuera de Codex tienen identidades de directorio distintas.
- Los otros2 PNG y2 presets están disponibles en la vista/cache privada de Codex,
  con hashes iguales a la instantánea. Se preservaron copias, sin restaurarlas a
  la otra ubicación. No se demuestra una pérdida global de esos cuatro archivos.
  La instantánea inicial no guardó identidad física: falta resolver su procedencia.
- La hora se normalizó de Madrid a UTC y se contrastó con el historial de tareas,
  recibos de instalación y registros accesibles. El detalle cronológico permanece
  privado. El candidato final f002… se construyó después del momento registrado;
  no hay prueba que atribuya el borrado a ese setup ni a otros instaladores.
- Application/System/PowerShell no aportaron eventos en la ventana examinada;
  Security no es accesible desde esta sesión, Sysmon no está disponible y
  TaskScheduler/Operational está desactivado. No se cambió configuración de logs.
  La API nativa anterior no conservaba un registro de acceso HTTP utilizable para
  atribuir retrospectivamente una llamada. Estos límites no exoneran procesos.

## Operaciones auditadas

| Ruta | Hallazgo y medida |
|---|---|
| DELETE de imágenes | Autenticación de sesión pero sin consentimiento específico verificado en servidor; glob de todos los PNG, sin distinguir origen o referencias. Deshabilitado:423 |
| DELETE de presets | Eliminación permanente del archivo; deshabilitada:423 |
| UI de limpieza | Tenía confirmación cliente, que podía omitirse llamando a la API. Control desactivado; explica que conserva imágenes/presets |
| Inicialización, lectura de presets y recetas antiguas | No se encontró eliminación automática de imágenes huérfanas, no referenciadas o presets inválidos. Nuevas regresiones conservan esos casos |
| Recuperación de lotes | Cambia estado del registro a interrumpido; conserva entradas/salidas. No es prueba de que todo proceso histórico haya usado esta ruta |
| Limpieza de `.part` | Defecto demostrado: si falla `open('xb')` por existencia previa, el finally antiguo borra el archivo ajeno. Ahora exige creación propia e identidad de archivo coincidente |
| Reserva del lote | Directorio nuevo exclusivo; colisiones preservadas. Si falla guardar el registro, no queda un trabajo fantasma activo |
| Escrituras atómicas | Temporales creados con exclusión; fallo de sustitución conserva el registro anterior. Se prueba con preferencias sintéticas |
| Evidencia de conservación | Baseline v2 ligado a volumen/directorio; rechaza otra identidad aun con bytes iguales y no certifica con baselines v1. No reconstruye la identidad histórica ausente |
| Build/staging | Limpieza limitada al árbol generado, marcado y cotejado. Runtime nuevo en carpeta privada; no copia DLL del host |
| Actualización/rollback/diario | Backup sin purga automática. Nuevos guards rechazan la carpeta privada por nombre y solapamiento del override, incluso en recuperación |
| Desinstalación | Retirados checkbox y purga recursiva de AppData/WebView; guard rechaza carpeta privada o un ancestro de ella antes de borrar recursos |

No hay recolector automático que elimine por falta de referencia en una receta.
La ruta antigua de imágenes sí eliminaba indiscriminadamente por extensión.
El defecto `.part` no explica por sí mismo los PNG/presets del incidente: afecta
a salidas parciales del lote, en otra ubicación. No se confunden ambos hallazgos.

## Reproducción controlada

[Script reproducible](../../scripts/reproduce_private_deletion.py) y
[resultados sanitizados](INCIDENT_036_REPRO.json). No acepta un directorio de usuario:
crea uno nuevo bajo el workspace y un audit hook rechaza borrados fuera del fixture.
Los fixtures y trazas se conservan. Ejecuta el blob anterior de Git únicamente en
un proceso de prueba aislado; no instala ni abre el Color Studio real.

| Prueba | Antes de contención | Con contención |
|---|---|---|
|9 archivos sintéticos; DELETE sin consentimiento específico |200;6 PNG borrados;3 originales restantes |423;9 originales conservados;0 eventos de borrado |
| `.part` preexistente antes de creación exclusiva |1 borrado del fixture ajeno |Fixture ajeno conservado;0 eventos de borrado |

El PID y las operaciones se registran en la traza privada del proceso Python de
reproducción. **No identifican al autor del incidente histórico**. Son pruebas de
infraestructura/seguridad, no fotografías reales ni validación comercial.

Contención elegida: ninguna eliminación permanente de imágenes/presets en esta
beta, incluso con una petición autenticada o parámetros `confirm=true`. No se ha
implementado una nueva papelera o backend. Una futura limpieza requerirá diseño
reversible, selección exacta, consentimiento ligado a contenido/versión y recibo
duradero; no se reabre el borrado por pasar CI. Se conserva el límite32 de imágenes:
no se invita a limpiar cuando se alcanza y no se incrementa sin evaluar recursos.

## Verificaciones

[Recibo de pruebas y límites](INCIDENT_036_QA.json). Regresión host y Python
embebido de contención:135 cada uno,3 symlinks omitidos por privilegios;
seguimiento134, frontend7 y build correctos;7 guards NSIS inertes. Los tests de
transacción usan6 imágenes/2 presets/preferencias sintéticos y comprueban hashes
durante error, interrupción, rollback y recuperación. Los guards NSIS se ejecutan
con fixtures inertes en el workspace; no es una desinstalación del producto real.

El runtime de QA se construyó offline con entradas oficiales fijadas. Su manifiesto
declara working tree con cambios; no es un instalador candidato ni una release.
**No se ha instalado esta corrección sobre el directorio real**, ejecutado un
nuevo NSIS completo o demostrado Windows limpio. El setup f002… queda en cuarentena
en el manifiesto; el sync conserva su historia y evita candidato/descarga incluso
con una autorización de release sintética. La puerta de seguridad deshabilita además
los enlaces de descarga históricos del dashboard mientras falte evidencia o permanezca
sin validar. No es un bloqueo del sistema operativo ni de descargas externas a Pages.
La UI muestra el motivo de retirada.
Estos cambios de dashboard están en PR90, pendientes de integración humana.

## Auditoría existente recibida; captura controlada pendiente

El operador completó la consulta Security existente: no aportó eventos coincidentes
en la ventana solicitada. El original y su custodia permanecen privados. No se
interpreta como ausencia de borrado, de auditoría en otros momentos o exoneración.
No repetir la misma consulta ni activar auditoría para reconstruir el pasado.
La revisión adicional del historial propio y sus tres agentes tampoco identifica
una orden de borrado del almacén en esa ventana. No descarta procesos en segundo plano.
Defender/AppModel/AppX existentes tampoco aportaron atribución; no se modificaron.

No restaurar archivos mientras se investiga. El código de
contención en la rama no protege automáticamente procesos/versiones ya abiertos.

Process Monitor oficial4.12 está preparado de forma privada. Sus tres firmas
Microsoft son válidas y sus hashes/arquitecturas están en
[recibo de preparación](INCIDENT_036_TOOL_PREP.json). El operador ya ha abierto la
ventana y ha autorizado continuar. No se ha aceptado la licencia ni elevado la
herramienta por el agente. La herramienta no se
incluye en el instalador de Color Studio ni se publica su binario.

Comprobación de la sesión: ventana receptiva, sin eventos y captura desactivada.
La automatización consigue traerla al frente, pero ni el clic en Filter ni Ctrl+L
abren el diálogo; la accesibilidad solo expone ventana/título. Una consulta de
tokens de solo lectura confirma Procmon elevado (integridad alta, RID12288) y
el proceso de diagnóstico sin elevación (integridad media, RID8192). Es compatible
con la restricción [UIPI de SendInput](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput);
no es un diagnóstico del canal interno de la herramienta de automatización.
No se han cambiado privilegios, permisos ni protecciones para sortearla.
**Aún no hay captura Procmon, PML/CSV ni nuevas reproducciones de esta sesión.**
El operador debe configurar el filtro y arrancar la captura; después Codex puede
ejecutar las cuatro pruebas por CLI. Rutas e instrucciones completas solo privadas.

La ayuda incorporada firmada confirma `/NoConnect`: no empieza a recopilar eventos
al abrir. La carga privilegiada y licencia requieren al operador. Para observar
el proceso y la pila nativos de una reproducción nueva:

1. El operador revisa [Process Monitor oficial](https://learn.microsoft.com/sysinternals/downloads/procmon),
   su EULA y el recibo verificado. Autoriza el arranque privilegiado y abre desde
   este worktree, en su PowerShell elevada:

   ```powershell
   & ./.lumaforge-local/tools/procmon-477754bf299c9e5b/Procmon64.exe /NoConnect
   ```

   No usar `/AcceptEula`. Leer y aceptar la licencia solo si está de acuerdo.
   Confirmar que la captura está detenida antes de preparar filtros. El agente
   no inicia la carga del controlador automáticamente ni cambia protecciones.
2. Confirmar captura detenida; no borrar registros existentes. En esta sesión la
   vista está vacía. Configurar Include por
   ruta que comience por el workspace + `.lumaforge-local\data-incident-repro-`.
   No dejar otras reglas Include y activar Filter > Drop Filtered Events antes
   de iniciar. Excluir actividad ajena al fixture de la captura guardada. Guardar el PML solo
   dentro de la carpeta privada. No filtrar únicamente por nombre del proceso:
   se busca también un posible proceso externo que toque el fixture.
3. Iniciar captura y ejecutar desde este worktree, con el Python de QA existente:

   ```powershell
   & ../../.venv-mvp/Scripts/python.exe -B scripts/reproduce_private_deletion.py --mode legacy --probe images
   & ../../.venv-mvp/Scripts/python.exe -B scripts/reproduce_private_deletion.py --mode contained --probe images
   & ../../.venv-mvp/Scripts/python.exe -B scripts/reproduce_private_deletion.py --mode legacy --probe batch-part
   & ../../.venv-mvp/Scripts/python.exe -B scripts/reproduce_private_deletion.py --mode contained --probe batch-part
   ```

4. El operador detiene la captura y guarda los eventos mostrados como PML y CSV
   en archivos nuevos privados, sin sobrescribir trazas. Codex verifica que el
   filtro está activo antes de ejecutar las pruebas. Correlacionar ruta sintética, PID, imagen/command line del proceso,
   tiempo y operaciones CreateFile/SetDispositionInformationFile/CloseFile, resultado
   y stack disponible. Conservar PML y CSV privados; publicar solo un resumen saneado.
5. Esto verifica una reproducción nueva; no convierte una operación similar en
   atribución de los eventos históricos. No probar instaladores/desinstaladores
   nativos del producto en el host: hacerlo después en VM aislada autorizada.

## Hipótesis pendientes y decisión

### Consolidación preventiva · 03-11-2026

Se revisa la PR completa desde edf82d0 y se prepara beta.5 solo interna. Pruebas
NTFS nuevas verifican root/ancestros de staging, entradas enlazadas y recuperación
directa. Esta última y la raíz del almacén ocultaban aliases antes de comprobarlos;
se rechazan antes de resolve/recuperación. Readonly real conserva preferencias,
imágenes, presets y receta. Un handle Win32 sin delete-sharing provoca el fallo de
switch y el reintento con stage nuevo conserva los datos.154 host correctos;
135 seguimiento y7 frontend correctos. No son pruebas de una instalación completa.

Los3 omitidos originales son symlink de archivo, root de staging y padre. Los2
casos de directorio tienen ahora equivalentes reales NTFS junction; el payload
tiene además una junction probada sin leer destino externo. CI Linux ejecutará
los3 originales sin privilegios (pendiente hasta verificar su run). Eso no prueba
la creación/semántica nativa de un symlink de archivo en Windows: se requiere
ejecutarlo en la VM con privilegios ya concedidos por su operador. No se activa
Developer Mode ni se cambia una política del host para ocultar la omisión.

Garantías acotadas: almacén soportado separado del programa, DELETE bloqueado,
creación sin reemplazo, guardado atómico y backup completo retenido al actualizar.
Los tests incluyen recetas personales dentro de extras que se conservan. No se
promete protección contra un proceso del mismo usuario manipulando rutas entre
checks ni contra guardar manualmente datos sobre un archivo gestionado del runtime:
el desinstalador elimina recursos de programa por rutas fijadas, no clasifica su
contenido. Las imágenes/recetas deben guardarse en el almacén o fuera del directorio
de instalación. Riesgo residual y validación nativa siguen pendientes de aceptación.

El usuario permite causa desconocida si se demuestra prevención y acepta el riesgo.
Por ello la puerta global pasa a data_safety_validated, que **continúa false**;
no se inventa root_cause_resolved ni se abre ninguna descarga. La autorización de
release y la aceptación por capacidad siguen siendo humanas e independientes.
Custodia de2PNG+2presets revalidada privada, sin restauración. VM no disponible en
el preflight actual: gestor ausente y3,41GiB libres. Procmon solo se usará en entorno
aislado; no se repite sobre el host. Build de beta.5/auditorías pendientes.

### Continuación autorizada: escrituras y recuperación seguras

El operador pidió reintentar el control de Procmon y, si no funcionaba, continuar
el desarrollo independiente. El reintento sobre la ventana actual tampoco abrió
Ctrl+L: sin eventos y captura desactivada. No hay nueva captura nativa; se pospone
solo ese paso, sin repetir el aviso de la misma solicitud67.

Se reprodujeron y corrigieron tres riesgos adicionales con fixtures nuevos:

- La limpieza de `.pending-*` borraba por nombre un archivo sustituto, incluso
  después de un commit correcto. Ahora exige identidad de volumen/archivo de la
  creación propia, archivo regular y ausencia de reparse point. Antes de publicar
  también comprueba que el temporal sigue siendo el propio. Los temporales de
  lote reutilizan la misma protección. No es un sandbox contra sustituciones por
  otro proceso del mismo usuario entre comprobación y operación.
- Una colisión de UUID forzada sobrescribía la imagen o preset existente. Las
  creaciones usan publicación sin reemplazo; devuelven409 y conservan bytes ante
  colisión. Las ediciones explícitas de presets/preferencias conservan su guardado
  atómico. Windows usa rename sin reemplazo; la estrategia POSIX usa link sin
  fallback destructivo ([semántica oficial de Python3.14](https://docs.python.org/3.14/library/os.html#os.rename)).
- Un fallo al persistir el primer estado del trabajador dejaba el lote activo
  indefinidamente. Ahora se captura como fallo, permite reintentar y conserva
  entradas/salidas. Si también falla persistir el error, lo indica en memoria;
  el reinicio recupera el registro durable como interrupted, nunca completed.

[Recibo de esta corrección](INCIDENT_036_STORAGE_QA.json):12 regresiones nuevas,
147 tests host (3 omitidos por privilegios) y147 embebidos correctos. Las pruebas
de concurrencia publican un único ganador íntegro y conservan las colisiones.
Las pruebas de fallos conservan los9 originales sintéticos y permiten otro lote.
Los fallos anteriores a la corrección y sus trazas quedan privados.

Runtime nuevo de QA con entradas oficiales verificadas offline y cambios de
working tree declarados; no setup ni instalación. Aislamiento/reinicio y71 módulos
cotejados correctos. Smoke con las2 fotos demo CC0: Creator/Pro mantienen bytes,
receta/preset/acabado, lote2, LUT y Planner correctos; originales intactos.
No son pruebas en Windows limpio ni importación en un editor externo.

El manifiesto enlaza pruebas/PR90 y añade storage a las huellas de revisión de
lotes/Windows. No modifica estados históricos ni aprueba capacidades. El guion de
presets ya no pide eliminar un archivo cuando esa operación está deshabilitada.
Estos hallazgos **no atribuyen el incidente histórico** ni validan seguridad global:
data_safety_validated=false, PR90 borrador y beta externa/venta NO-GO.

Una llamada al DELETE antiguo, otra herramienta/proceso o una limpieza exterior
podrían explicar los cuatro PNG. No existe prueba de cuál ocurrió. Para los otros
cuatro ausentes de la vista externa, la existencia de copias en otro contexto es
evidencia separada; no se afirma un borrado adicional ni una migración demostrada.
La revisión de código y las reproducciones reducen riesgos futuros, no cierran
el incidente ni autorizan distribución. PR90 sigue en borrador y no se aprueba nada.

Fuentes primarias: [estructura y límites del USN](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ns-winioctl-usn_record_v2),
[semántica del diario](https://learn.microsoft.com/en-us/windows/win32/fileio/change-journal-records),
[Process Monitor](https://learn.microsoft.com/sysinternals/downloads/procmon).


### Candidato interno beta5 y entrega de QA aislada · 03-11

[Auditoría y alcance](BETA5_036_QA.json), [artefacto](BETA5_036_ARTIFACT.json) y
[NSIS completo](BETA5_036_NSIS.json). El candidato final incluye la retención de
journal/backup ante destino sustituto. No fue instalado en este host. SHA y fuente
29fb77a fijados; fuentes de aplicación sin cambios posteriores. El ZIP privado con
beta3→beta5 está verificado y listo para transferir al guest, no para distribución.
Guía: [QA interna](../QA_BETA5_INTERNA.md). No contiene las copias del incidente.

Los3symlinks omitidos del host pasan ahora en Windows y Linux CI41648801203; no
prueban instalación Windows11. Las4junctions NTFS, readonly y sharing-lock se
prueban en host. Una repetición posterior de la suite embebida dio1error en el
fixture de interrupción de instalación limpia (directory_switch_failed); diagnóstico
original sin errno/winerror. Se conservó el fallo;20repeticiones focales y una suite
completa pasan. Más detalle de errores añadido al runner. No exonerar procesos,
atribuirlo a antivirus ni confundir este fallo con las eliminaciones históricas.
La discrepancia y validación nativa pendientes impiden cerrar la contención.

Cierre acotado:5suites adicionales160/3omitidos pasan con diagnóstico nuevo; no
se conoce la causa del error previo. Build WindowsCI independiente41649084841
pasa160/0omitidos y audita el NSIS completo. No es un Windows11 limpio ni resuelve
la discrepancia retrospectiva. Se conserva PR90borrador y NO-GO. Un único aviso
de la solicitud67 pide preparar guest aislado; no reintentar Procmon sobre el host.
