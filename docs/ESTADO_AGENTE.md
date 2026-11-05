# Checkpoint vigente · cierre MVP/COL-036 · 05-11-2026

Rama codex/COL-036-actualizacion-segura, PR90borrador, Issue57 y acción67.
Base3514146 preservada. Main y worktree de Project OS no modificados; su carpeta
functions/ no versionada es ajena y no se toca. No merge/cierre/approved/release.

Nuevo alcance autorizado: cierre técnico/QA y preparación comercial, con VM
ColorStudio-QA-Win11 ya instalada por el usuario y checkpoints existentes. Hyper-V
está presente, pero Get-VM falla en esta sesión no elevada; no hay consola VM abierta.
No cambiar permisos, features, checkpoints ni levantar NO-GO para sortear ese bloqueo.

Implementado: asistente host qa_vm_assistant.ps1 y ciclo guest qa_vm_cycle.ps1.
SHA/ZIP/miembros, VMId/BIOSUUID frente a SMBIOS, checkpoint existente elegido y
confirmación del estado limpio por operador. Solo PowerShell Direct y kit sintético;
no shares/WinRM/red/credenciales guardadas. Instala3, prueba API/semilla/baseline,
provoca fallo real con handle Win32, verifica preservación y actualización directa5,
API/reinicio/cancelación/fixtures, desconecta adaptadores guest con restauración en
finally, y desinstala comprobando datos. No se ha ejecutado dentro de la VM.

Nuevo cliente HTTP estándar qa_guest_api.py probado contra runtime extraído beta5:
semilla y reinicio reales con imágenes sintéticas768x1024, Creator/Pro preservan
bytes; preview igual al export de ese tamaño, presets/receta,LUT solo color, Planner
con fuentes y cancelación realPASS. No prueba GUI instalada ni calidad estética.
Suite focal5tests y regresión de diagnóstico de instalador correctas. Primer pase
MVP164/3omitidos correcto; suite final166 y seguimiento pendientes tras commit.
El venv existente se utiliza sin instalar dependencias. El hijo WindowsPowerShell5
necesita inicializar su PSModulePath; el test elimina únicamente la variable heredada
PS7 en el proceso hijo. No cambia módulos ni variables globales.

Intermitente: la causa del antiguo directory_switch_failed sigue sin demostrar.
El harness ahora conserva árbol sintético+errno/winerror antes del cleanup si reaparece.
Una inyección controlada verifica esa conservación; stress acotado100casos pasa; no resuelve la causa anterior.
No atribuir al instalador/antivirus los4borrados históricos. Copias2PNG+2presets+
preferencias siguen privadas; no restaurar, subir o ensayar sobre AppData real.

Inventario de8bloqueos y categorías en MVP_CLOSURE_036.json. Inventario289avisos,
0ausentes, pero falta licencia propia de raíz y aceptación de derechos/titular.
Se corrigen documentos existentes: beta5 actual, bootstrapper WebView2 puede
necesitar red, DELETE/limpieza deshabilitados, guías/feedback ya existentes, sin
nuevos precios ni entrevistas. Estímulo49€ de COL005 se conserva, no precio aprobado.
Preparar cinco perfiles no acredita10–20equipos históricos de COL041.

Reanudar: git status; gh pr view90/checks; QA_VM_ASISTIDA.md. Herramientas publicadas en9f3702a y kitv2 generado en limpio
hacia .lumaforge-local/vm-qa-beta5-cycle-20261105 (v1 y parcial preservados). No recompilar app:
bytes apps/packages/packaging siguen source29fb77a beta5 SHA789983…8bb69. Verificar
kit completo y producir recibo privado closure-20261105/kit-receipt.json. Ejecutar
MVP/embebido/seguimiento y escaneo. Actualizar57/60/61/62 y coordinar73 sin duplicar
Issues ni avisos. La única nueva acción humana es ejecutar el asistente desde host
con acceso Hyper-V y credenciales locales guest; no reenviar la antigua petición
«preparar VM» ya cumplida. CapturaProcmon/Resolve/UI nativas siguen NOT_RUN.

Beta externa y venta **NO-GO**. Todas las aceptaciones humanas siguen pendientes.

Resultado de cierre: kit23archivos+manifiesto,95.299.851bytes; SHA256
c3521f63507502d1b76e18d304246947d08514c938571378beb6cfe2ae6bc011.
Recibo privado closure-20261105/kit-receipt.json y QA pública MVP_CLOSURE_036_QA.
CRC/todos hashes correctos; extractor de host WindowsPowerShell5 pasa con el kit
real y rechaza traversal/duplicados/absolutos antes de extraer. Runtime embebido167
correcto/3omitidos; host166/3omitidos y regresión beta3 focal correcta; seguimiento135.
CI9f3702a MVP42013403805/cliente42013404035/seguimiento42013403865 correctos.
CI anterior detectó pruebaAPIunittest que exigía UI antes de compilarla: el cliente
real sigue exigiendo web200; solo el fixtureAPIunitario omite ese check. Fallo de
kit por ausencia legítima de ledgerbeta3 corregido usando launcher/runtime fijados
al NSIS auditado, sin inventar metadatos. Parcial preservado, no reutilizarlo.
No ejecutar/recompilar aplicación en host. Se requiere operador para PowerShellDirect.

Último kit: toolsource539a159; recibo closure-20261105/kit-receipt.json. El kit9f
se conserva como vm-qa-beta5-cycle-20261105-source-9f3702a.zip; NO usarlo para la
guía visual actual. Se corrigió guía que aún decía beta3/reinstalar y se separan
almacenes QA/Inicio para no confundir vistas.23miembros y navegaciónoffline verificados.
Host168/3omitidos correcto, embebido167/3omitidos y nueva regresión de enlaces focal
correctos; seguimiento135. No más aplicación recompilada ni suite repetida sin cambios.
Solicitud67 actualizada con comando exacto del host y SHA final. Aviso único
42014330354 success, bot@jea27 en67#issuecomment-6656140492; recepción física nueva
no confirmada. No repetir aviso tras cambios de documentación. Coordinado73 y
actualizadas60/61/62 por comentarios sin crear Issues/aprobar. PR90 sigue borrador.
No se ha iniciado una sesión PowerShellDirect ni copiaVM. Paso inmediato: operador
con accesoHyperV ejecuta QA_VM_ASISTIDA, introduce credenciales guest localmente y
conserva informe privado. Si hay error, diagnosticarlo sin restaurar checkpoints ni
eliminar pruebas por automatismo. Beta externa y venta NO-GO.

---

## Historial conservado (el checkpoint vigente está arriba)

# Checkpoint vigente · COL-036 · candidato interno beta.5 · 03-11-2026

## Tarea, rama y límites

Issue57 / PR90; solicitud humana canónica67. Rama
`codex/COL-036-actualizacion-segura`, worktree `COL-036-actualizacion-segura`.
Continuación desde edf82d0; commits ebdfbe5,29fb77a,8876535 publicados. Consultar
Git/PR para el head posterior. Main y los otros worktrees se conservan.
No merge, approved, cierre de tarea, release ni distribución externa autorizados.

**Incidente P0 abierto; causa histórica sin atribución. Beta externa y venta NO-GO.**
PR90 permanece borrador durante la investigación del ensayo intermitente indicada abajo.

## Trabajo completado

- DELETE de imágenes/presets y limpieza UI bloqueados; escrituras atómicas con
  identidad propia y creaciones sin reemplazo/409. Fallos del trabajador permiten
  reintentar y recuperar interrupted, sin fingir una finalización.
- Root/ancestros del almacén y recuperación rechazan enlaces antes de resolverlos.
  Cuatro junctions NTFS reales, readonly y bloqueo Win32 de directorio ejercitados.
- Si aparece un destino sustituto después de mover el programa antiguo, se conserva
  destino+backup+diario. La recuperación no sobrescribe el contenido ajeno.
- Actualización por stage/ledger/backup; sin purga AppData ni eliminación de backups.
  Builds archivan etapas, launcher, setup y recibos anteriores. TEMP/TMP se confinan
  al build y se restauran; no se cambian variables globales o permisos.
- Candidato final **0.3.0-beta.5** compilado desde29fb77a limpio,48.473.299bytes,
  SHA256789983ea5c8e71b92271b91e2fc7a76ad6d6fef3272ac5ac24d96ac4c308bb69.
  Sin firma, no instalado en el host. Preliminar d1cbdd…68ea preservado y superado.
- Auditoría completa del NSIS:951 archivos/924runtime/60nativos, hashes y procedencia
  cotejados; privacidad0bloqueos;289 componentes con avisos,0ausentes. PSF/Microsoft
  con firmas requeridas válidas. Eso no supone aceptación legal ni GO.
- ZIP privado de QA generado/verificado,17 entradas+manifiesto; incluye beta3 fijada,
  beta5, guías, fixtures y PNG/receta sintéticos. No contiene diagnóstico ni fotos
  personales. SHA256abf342a86405434dc6506e5dbe0cce57fcb48544398cc2d1b43fc1c4abfd4015,
  95.194.508bytes. Fuentes de herramientas8876535; aplicación29fb77a, sin cambios
  posteriores en apps/packages/packaging. No se afirma NSIS reproducible bit a bit.

## Pruebas y discrepancia en investigación

Host:160 pruebas,0fallos/errores,3symlinks omitidos;7 guards NSIS inertes incluidos.
Primer pase runtime extraído:160 sin fallos/errores; aislamiento71 módulos,
reinicio y preferencias/preset correctos. Smoke HTTP con2demo CC0: Creator/Pro
mantienen bytes, receta/preset/acabado, lote2,LUT y Planner correctos; originales
intactos. No es una prueba de GUI instalada ni de calidad visual aceptada.

Una repetición posterior del runtime:1error en la inyección de interrupción de
instalación limpia, phase=directory_switch_failed; el código original no registró
errno/winerror, por lo que no se atribuye a antivirus ni a otro proceso. Se conserva
el recibo fallido.20 repeticiones focales y una suite diagnóstica completa pasan.
Se añadió detalle saneado de InstallError y contador de omitidos al runner; cinco
suites completas adicionales pasan,160cada una/3omitidos. Causa del error pendiente. No borrar ni ocultar esta discrepancia si vuelve a pasar.

Seguimiento135 y frontend7/build correctos. CI8876535: MVP41648801203, cliente
41648801729 y seguimiento41648801678 success. Los3symlinks originales pasan tanto
en Windows como Linux CI. MVP remoto153 tests y una clase NSIS omitida por caché
no preparada; no presentarlo como160. Build candidato independiente41649084841
success:160tests/0omitidos, NSIS completo correcto. Solo publica4recibos saneados;
no sube EXE ni crea release. Su setup e5862a…27da difiere del local789983…8bb69:
no hay reproducibilidad bit a bit demostrada. Aplicación fuente29fb=8876535.

## Custodia y bloqueos humanos

Privados en `.lumaforge-local/incidents/COL-036-20261102/`: diagnóstico/USN/cache.
2PNG+2presets+preferencias cotejados, preservados, sin restauración. Cuatro borrados
PNG USN confirmados; actor desconocido. Las dos vistas tienen distintas identidades
NTFS; no confundir8ausencias externas con8borrados globales demostrados. No publicar
rutas, nombres, JSON, PML/CSV o eventos originales. No probar sobre AppData real.

Preflight03-11: gestión Hyper-V/VBox/VMware ausente,3,41GiB RAM libres; no VM creada.
No habilitar features, elevar agentes ni reiniciar por sorpresa. Hace falta preparar
Windows11 limpio con ISO/licencia/evaluación válida y recursos; guía QA_BETA5_INTERNA.
Procmon solo en guest aislado con datos sintéticos. Siguen NOT_RUN: instalación/
actualización NSIS y recuperación nativas, GUI instalada beta5, desinstalación,
desconexión real y LUT en Resolve/Adobe. La autorización y aceptación son humanas.

## Archivos y reanudación

Evidencias públicas: BETA5_036_ARTIFACT.json, BETA5_036_NSIS.json, BETA5_036_QA.json;
INCIDENT_036_QA conserva data_safety_validated=false y aceptación preventiva=false.
El colector detecta automáticamente *_ARTIFACT*.json; candidato en cuarentena,
sin descargas. Pages lee main: no simular publicación de archivos de esta rama.

Privado: `.lumaforge-local/containment-20261103/`; kit
`.lumaforge-local/vm-qa-beta5-final-29fb77a.zip`. Setup final en
`apps/desktop/src-tauri/target/release/bundle/nsis/Color Studio Beta_0.3.0-beta.5_x64-setup.exe`.
Un intento de kit sin dependencias quedó parcial y preservado; usar solo el ZIP final
con SHA anterior. El entorno de build existente está en `../../.venv-mvp/Scripts/python.exe`.

Reanudar: `git status --short`; `gh pr view 90`; `gh pr checks 90`; leer
BETA5_036_QA y QA_BETA5_INTERNA. Consultar primero logs/recibos de diagnóstico y CI,
no repetir build de aplicación sin cambios. Verificar CI del head final y estado remoto; commit/push
solo de esta rama. Actualizar57/67 sin repetir el aviso de la misma acción VM.
Preparar revisión de contención sin equipararla a aceptación Windows ni GO.
Siguiente trabajo elegible: QA aislada, condicionado a disponibilidad del guest;
ninguna nueva funcionalidad grande.

Sincronización GitHub real probada sin modificar archivos generados:42tareas,
COL036blocked/PR90, aceptación0/8, beta5 en cuarentena/NO-GO. Pages continúa beta3
sobre918cb638 hasta integración humana; no fingir que el recibo de rama está publicado.

Cierre remoto: commit1d917c7 publicado y CI MVP41650393122/cliente41650393107/
seguimiento41650393173 success. Solicitud67 sustituye el bucle Procmon host por
preparación de Windows11 aislado. Aviso único41650561917 success; bot mencionó
@jea27 en67#issuecomment-6605944403; nueva recepción física no confirmada. No repetir.
Algún sync de la ráfaga fue cancelled antes de steps; no es fallo de test. Verificar
el último despliegue cuando terminen las ediciones de Issue/PR. PR90 sigue borrador
por discrepancia de fixture registrada y QA nativa pendiente; sin cierre ni GO.

---

## Historial conservado; no describe el estado vigente

Los siguientes checkpoints se conservan íntegros para trazabilidad. El estado
vigente y las instrucciones de reanudación están al principio de este archivo.

# Checkpoint vigente · consolidación COL036 · 03-11-2026

Punto de continuación: ebdfbe5 produjo un preliminar beta.5 limpio,48.482.443bytes,
SHA d1cbdd9073af8e42ff73c241b6769ef64a2b5b300fa405f9af6c00f4364468ea; NO usarlo
como candidato final. Revisión posterior detectó diario descartado si reaparece
un destino ajeno tras mover el old a backup. Nuevo test lo reproduce; corregido
para conservar diario/backup/destino sustituto, recuperación tras revisar ese
destino.36 pruebas focales correctas (3 symlinks omitidos). Falta regenerar beta.5
desde el nuevo commit, preservando el preliminar; build archiva también setup.
Kit VM preparado en scripts/prepare_vm_qa_kit.py + qa_guest_checks.ps1 y guía
QA_BETA5_INTERNA.md: guard de guest, hashes, instalación, fixtures y probes sin
Git/httpx globales. Datos/fotos/presets solo sintéticos; fuentes legacy fijadas.
Todavía no se ejecuta en VM ni se certifica su compatibilidad real. Después del
build: QA embebido/smoke/aislamiento, generar ZIP privado y notificar una sola
acción concreta para disponer de Windows11 limpio. No ejecutar instaladores
en el host. CI candidato preliminar41586295244 cancelada por código superado.
Los3 symlinks originales pasaron CI Linux41585993189; no equivalen a NTFS file symlink.

Continuación desde edf82d0 autorizada: preparar candidato interno beta.5 sin GO
externo/venta. Host154 tests correctos,3 symlinks aún omitidos por privilegios;
cuatro casos NTFS junction nuevos y un bloqueo Win32 real pasan. Nuevos guards
rechazan root/ancestros enlazados del almacén y recuperación directa por alias.
CI Linux añadida para los3 symlinks originales, pendiente de ejecución remota.
Custodia privada revalidada2PNG+2presets+preferencias, sin restaurar ni publicar.
Preflight03-11: gestorVM ausente,3,41GiB libres; no VM ni Procmon aislado ejecutados.
Versión interna beta.5 preparada en fuentes; build y auditorías aún pendientes.
135 tests de seguimiento y7 frontend correctos; AST build_beta.ps1 sin errores.
Build preserva stage/launcher/recibos anteriores y rechaza cambios de fuente durante
compilación. Gate de distribución pasa a seguridad preventiva validada, todavía
false; causa histórica sigue desconocida y aceptación/release requieren al humano.
Ver .lumaforge-local/containment-20261103/ para logs. No instalar sobre AppData real.

**P0 abierto. PR90 BORRADOR. Beta externa/venta NO-GO. No instalar ni distribuir
f002…: candidato en cuarentena. No restaurar ni limpiar el almacén real.**

Tarea57, solicitud canónica67; rama codex/COL-036-actualizacion-segura, worktree
COL-036-actualizacion-segura. Main y raíz ajenos preservados. Sin merge/aprobación.
Último head previo a esta contención: eb3866d; consultar Git/PR90 para el actual.

Continuación actual autorizada: reintento Ctrl+L sin efecto, Procmon sin eventos y
captura desactivada. Se deja pendiente esa captura y se continúa estabilización.
Nueva corrección de storage: limpieza solo de temporal propio por identidad;
creación de imagen/preset sin sobrescribir ante colisión (409), edición atómica
conservada; fallos de persistencia del trabajador ya no dejan lotes activos sin
fin. Reinicio de un fallo no persistido muestra interrupted. No nuevas funciones.
12 regresiones añadidas,147 host/147 embebidos correctos (host3 omitidos). Runtime
QA privado .lumaforge-local/atomic-worker-containment-runtime, source98f9ab9 dirty
declarado, manifiesto SHA0f7095f3e1a83ffb9c27ea7247f5a453ed0f9d0f8ffc6e3347edff1165bf1c4c.
71 módulos/aislamiento/reinicio correctos; smoke2 demo CC0 pasa Creator/Pro,
presets/receta/acabado/lote/LUT/Planner y originales. Sin setup ni instalación.
Recibo nuevo docs/evidence/INCIDENT_036_STORAGE_QA.json; logs fallidos/correctos
privados. Manifiesto añade tests/PR90 y dependencias de huella, no autoaprobación.
No hace falta otro aviso del mismo bloqueo. Causa histórica continúa abierta.

Evidencia privada: .lumaforge-local/incidents/COL-036-20261102/. Dos diagnósticos
copiados/verificados, baseline e índice privados. El operador confirma4 eventos
PNG FILE_DELETE/CLOSE del02-11-2026 07:12:44 Madrid =06:12:44Z. Actor no identificado.
La vista externa tiene1/9; la vista/cache Codex5/9 y distintas identidades NTFS.
Otros2PNG+2presets siguen disponibles con hashes originales, preservados junto
a preferencias; no restaurados. No confundir ocho ausencias externas con ocho
borrados demostrados ni mezclar identidades. No subir JSON, nombres, rutas o USN.

Correlación de tareas/recibos/logs sin atribución. El build final empezó después
de la hora del evento. Security fue consultado por el operador sin coincidencias;
original privado recibido y conservado. No repetir consulta ni exonerar procesos.
Historial adicional de tres agentes propios revisado sin atribución; no descarta
procesos en segundo plano. Sysmon no disponible, TaskScheduler
desactivado; no se modificó logging. API anterior sin access log retrospectivo útil.
El detalle temporal y los procesos observados quedan en informe privado.

Defectos demostrados en fixtures: DELETE anterior sin consentimiento específico
borra6PNG (9→3); contención423 conserva9. Cleanup anterior borra un .part preexistente
cuando falla open('xb'); nueva versión lo conserva y comprueba identidad de sus
propios temporales. Audit hooks registran el PID de reproducción, no el histórico.

Cambios: DELETE imágenes/presets deshabilitados y UI protegida; directorio de lote
exclusivo, sin trabajo fantasma ante fallo inicial; guard privado de instalación y
recuperación; retirada purga AppData/checkbox NSIS. Baselinev2 exige volumen/NTFSID,
rechaza otro almacén aunque tenga mismos bytes y no acepta v1 como certificación.
Quarantined en manifiesto y hold de seguridad bloquean candidato y descargas,
incluidas releases históricas autorizadas. Windows no queda técnicamente validado
por el CI previo; evidencia actual data_safety_validated=false.42 tareas intactas.

Pruebas/logs: host MVP, runtime embebido nuevo de contención, seguimiento y7 frontend
con build:147 host,147 embebido y134 seguimiento correctos tras el ajuste de manifiesto. Los resultados finales
están en docs/evidence/INCIDENT_036_QA.json.
Runtime de primera contención en .lumaforge-local/incident-containment-runtime;
el actual está en atomic-worker-containment-runtime (ambos dirty declarados,
entradas oficiales offline); no nuevo setup ni instalación sobre datos reales.
Probes NSIS inertes7 casos y pruebas de actualización/interrupción con9 sentinelas.
Tres symlinks omitidos por privilegios; no se cambiaron permisos.

Pendiente: atribución histórica, nueva QA nativa en entorno aislado y aceptación
humana. No empezar más distribución ni resolver por updates verdes. Process Monitor
oficial4.12 descargado dentro del workspace y firmas Microsoft verificadas;
el operador ya abrió la ventana y autorizó continuar. EULA/elevación no realizadas
por el agente. ZIP477754bf…3a10,
x64 SHA28495e64…885; recibo INCIDENT_036_TOOL_PREP.json. Binarios solo privados.
Ventana receptiva, vacía y captura desactivada. Clic y Ctrl+L automatizados sin efecto;
solo título accesible. Tokens de solo lectura: Procmon alto/elevado, diagnóstico
medio/no elevado; compatible con UIPI, no prueba de canal interno. No cambios de
seguridad ni nuevas reproducciones Procmon. Paso de captura pendiente: operador configura Path begins
with prefijo privado del fixture, sin otras Include, activa Drop Filtered Events e
inicia captura. Confirmar visualmente filtro/captura; ejecutar los cuatro comandos
del informe, pedir detener/guardar PML+CSV privados y analizar. No ejecutar pruebas
si no se puede confirmar el filtro. No prometer atribución retrospectiva.
Archivo de Security recibido: .lumaforge-local/incidents/COL-036-20261102/
received-security-empty.json; no copiarlo a GitHub. Queda cerrada solo la petición
de consulta, no el incidente ni la autorización de distribución.

Reanudar: git status/branch; leer Issue67/PR90 y el informe privado. Preservar
baseline/copies/traces y no eliminar fixtures antes de capturar Procmon si procede.
No usar antiguos scripts nativos de install/uninstall en el host durante el incidente.
Documentación saneada: docs/evidence/INCIDENT_036.md y reproduciones/recibo JSON.
Datos reales completos únicamente en el directorio privado citado.

---

# Histórico · beta.4 probada; conservación bloqueada · 02-11-2026

Tarea COL036/Issue57, solicitud canónica67; PR90 en BORRADOR. Rama
`codex/COL-036-actualizacion-segura`, worktree COL-036-actualizacion-segura, base
main918cb638. Raíz y otros worktrees preservados. No merge ni aprobaciones.

**Candidato seleccionado:** fuente limpia8f4c60ecbbb25a5681796f7509e20e2eebe6f144,
0.3.0-beta.4, SHA256f002769da0c37d8a85a8fa8bf6351053ea3608a298cbf368d0c442f164eca4bf,
48.473.370bytes. Setup en apps/desktop/src-tauri/target/release/bundle/nsis/.
Cambios QA posteriores no cambian apps/ ni packaging/ de ese binario. Intermedio
25c943dc queda superado y conservado; beta2/beta3/backups intactos. No distribuir.

Completado: stage+ledger+mutex/lock/backup/rollback, bootstrapper Microsoft fijado
y firmado, retirada Delete dirigido por registro y guards NSIS de junction.
Extracción951 archivos/924runtime y privacidad sin hallazgos. Actualizaciones
DIRECTAS beta3→beta4 exit0/8,016s y beta2→beta4 exit0/7,110s, stores inmediatos
intactos y preset por API. Fallo real controlado Winerror32/errno13: NSIS2/hijo2,
old_restored=true, bytes intactos, reintento0/8,438s. Registro manipulado con fixture
propio preservado. Uninstaller final con junction aborta2 antes de borrar launcher;
runtime restaurado byte a byte (checkpoint privado restored=true). Desinstalación
normal finalizada sin cambiar stores; exit del hijo temporal no observado.

Pruebas:116 MVP host y116 con Python embebido instalado sin fallos (3 symlink
omitidos por privilegios);5 guards NSIS reales pasan sin elevación. Auditor loader
PSAPI coteja71 módulos, hashes y límites: no aceptar DLL externa por bytes iguales.
Aislamiento con CWD/env contaminados y reinicio de prefs/preset pasa. API con2CC0:
Creator/Pro byte-idénticos, PNG/JPEG/LUT/receta/óptica/lote2/Planner y originales
intactos. GUI/capturas/descargas reales en intermedio25c, árboles apps/packages
idénticos a8f; no confundir con retest visual del setup final ni aceptación humana.
Histórico2 beta3 sigue sin causa atribuida.7frontend anteriores pasan;132 tests de
seguimiento correctos: conservación independiente de CI/etiquetas y bloqueo visible
frente a revisión obsoleta/cambios solicitados, con historial conservado.

CI del paquete8f: construcción41399176754 success, MVP41399182517, Studio41399182514
y validate41399182518 success.4JSON de CI verificados por digest; no .exe publicado.
60PE/runtime/bootstrapper coinciden, setup CI/local no byte-idénticos. CI de los
instrumentos QA810bf44: MVP41409829710, Studio41409829747, validate41409829738 y
sync41409827751 success. Los siguientes cambios corrigen prioridad visual del bloqueo
y agregan recibo de integración; consultar checks de PR90 para el último head, sin
reconstruir el setup de8f porque apps/packaging siguen iguales.

**BLOQUEO REAL:** captura privada9→5 archivos;4 imágenes temporales ausentes,5
presentes con hashes idénticos (2 imágenes,2 presets,prefs). El usuario niega limpieza
y exige investigar antes de aceptar. Búsquedas e historial acotado sin causa ni copias.
Vistas actuales coinciden; captura antigua no tenía identidad de volumen/directorio.
No atribuir a otras API: sus defaults usan su propio worktree. No restaurar/borrar.
USN lectura devuelve5 desde Codex; no se elevaron permisos. Instrumento probado
scripts/diagnose_private_store.ps1 compara solo lectura y guarda identidades NTFS
actuales/filas coincidentes en JSON privado. Necesita operador fuera de Codex y
consola elevada solo para USN. Resultado únicamente por chat privado, nunca GitHub.
No aceptar conservación global por las comparaciones inmediatas o por CI.

Issue57 marcada blocked, retirada status:in-progress;67 mantiene needs-human y
marcador de PR90 para evitar solicitud duplicada. Un solo aviso nuevo para diagnóstico:
workflow41410069177 success y comentario6572098610 con mención@jea27 verificados.
Recepción física de este aviso no confirmada. No repetirlo. La web pública ya
refleja COL036 bloqueada/PR90 y beta.3 de main; corrección visual de producto y
metadatos beta.4 quedan únicamente en PR90. UPGRADE_036_SYNC.json verifica proyección
con datos GitHub reales y puerta de conservación false, sin desplegar ni aprobar.

Pendientes humanos secundarios ya notificados: Hyper-V/RAM/ISO oficial/licencia
válida y Resolve gratuito/registro propio. Gestor VM/Resolve ausentes; sin Windows
limpio, desconexión física ni editor real. Beta externa y venta NO-GO. Issue60
derechos pendiente. No permisos nuevos, reinicio, pagos, release o fotos personales.

Reanudar en este worktree:

```powershell
git status --short
git branch --show-current
gh issue view 67 --repo jea27/Lut_generator
# Solo el operador fuera de Codex; consola elevada para leer USN existente:
.\scripts\diagnose_private_store.ps1 -ReadUsn
```

Conservar informe nuevo bajo .lumaforge-local; comparar identidades/contexto y
registros sin publicar nombres/hashes/rutas privados. No inferir causa de ausencia
de USN por retención. Después decidir siguiente investigación; no aprobar nada.
Fuentes/evidencias: docs/evidence/UPGRADE_036_QA.md y JSON asociados; diagnóstico
en docs/DIAGNOSTICO_TEMPORALES_BETA4.md. Manifiesto enlaza PR90 y puerta separada
de conservación; estados publicados proceden de GitHub Actions. No quedan
instalaciones, handles de prueba ni junctions propios a medio restaurar. Trabajo
independiente de estabilización preparado; siguiente paso depende del diagnóstico
del operador y del entorno limpio, no de añadir funcionalidades.

---

# Histórico · revisión de seguridad beta4 · 02-11-2026

PR90 borrador, rama codex/COL-036-actualizacion-segura. Candidato intermedio de
fuentee317c02, SHA25c943dc…505f construido/auditado y probado realmente. CI de
construcción41347038273 success; solo4JSON públicos. No distribuir ni dar GO.

Actualizaciones directas beta3→beta4 (9,313s) y beta2→beta4 (8,125s):0; presets,
preferencias, imágenes y store privado conservados. Fixture sintético de raíz
preservado también en backup; se limpió solo la copia propia activa. Fallo real
controlado con handle de stage: Winerror32/errno13, instalador2/hijo2, rollback
old_restored=true, bytes de app/datos intactos. Reintento0. Guard de app abierta2
antes de copiar. Desinstalación normal observada completa sin borrar stores; no
se observó directamente el exit del hijo temporal del desinstalador.

GUI real en25c: Creator→Pro conserva imagen e intensidad60%, descargaPNG/receta y
ShotPlannerJSON reales; tipos de observación/estimación/recomendación/fuente,
fuentes y límites visibles; cierre normal y children detenidos. Capturas CC0
UPGRADE_036_*.png pendientes de incorporar. Runtime instalado105 tests/3 symlink
omitidos, aislamiento71 módulos y smoke2CC0 pasan. Historial2 beta3 no atribuido.

REVISIÓN DETECTÓ: Delete heredado usa MainBinaryName del registro sin validar.
Eliminado en working tree;25c/e317 quedan superados como selección final. Añadido
preflight NSIS de reparse/junction antes de cualquier Delete del desinstalador.
La prueba roja real detectó un error de registrosSystem r7/r8 vsR7/R8; corregido
a r17/r18 y prueba verde5/5: carpetas normales/ausentes0, junction en recurso/raíz/
ancestro2 y marcadores intactos. Nuevo desinstalador aún no compilado/ejecutado.
Reconstruir
fuente limpia, nuevaCI, auditoría951 archivos y retests selectivos de update/fallo.
Resolver_inventory terminó reciboCI histórico, marcado superseded, en
UPGRADE_036_CI_BUILD.json. No confundircon recepción del móvil ni aprobación.

Pendiente humano: Windows limpio/Hyper-V+RAM/ISO y descargaResolve con registro
personal, Issue67 ya notificada41316675082/mención6559335054. No repetir bloqueo.
SinVM, sin desconexión real, sin editor real; externa/venta NO-GO. No ejecutar
uninstall.exe de backups: puede retirar registro de instalación activa.

Reanudar: git status y revisar mensajes de agentes; corregirSystemtrasredtest;
no alterar otros worktrees. Los logs/instaladores/fixtures están en .lumaforge-local
(privado). Conservar25ccomo intermedio, archivosbeta2/beta3 y todoslosbackups.
No main, merge, approved, releases ni herramientas/permisos nuevos.

---

# Checkpoint vigente · COL036 actualización segura · 01-11-2026

Rama `codex/COL-036-actualizacion-segura`, worktree independiente; base main918cb638
(PR89 fusionada por jea27). Issue57 en curso,67 solicitud canónica. No se toca el
worktree del agente principal ni se fusiona nada. Beta externa/venta siguen NO-GO.

Repetición real beta2→beta3 silenciosa:0, preset QA recuperado por API, datos
conservados. No reproduce ni explica el2 histórico. Overlay retuvo runtime antiguo.
Probe NSISdl loopback con URL https recibió HTTP plano; transporte sustituido por
bootstrapper oficial Microsoft fijado/firmado, sin ejecutarlo ni instalar Evergreen.

Preparado candidato correctivo beta.4: extracción a stage nuevo, ledger SHA fijado,
mutex de app y lock de transacción, backup completo, rollback de errores de rename,
diario recuperable sin borrado automático y logs de fases sanitizados. Código en
apps/desktop/installer_helper.py y packaging/nsis/installer.nsi. PR90 borrador: https://github.com/jea27/Lut_generator/pull/90. Nativo y NSIS ya
compilan; auditoría manual completa951 archivos/924 runtime,0 hallazgos, SHA del
probe5a6a1648…4227 (fuente d3eef7f). No ejecutado. El pipeline detectó un import
incorrecto al ejecutar el auditor como script; corregido con carga exacta del
validador y regresión aislada. Se reconstruye desde fuente limpia antes de elegir
el candidato final y probar actualización/rollback nativos. Probe anterior privado
conservado; beta2 y beta3 intactos.

Pruebas:130 seguimiento y7 frontend pasan. Runtime embebido103 tests pasan
(3 symlink omitidos por permisos), aislamiento y smoke CC0 de2 fotos correctos;
71 módulos nativos observados, ninguno inesperado. Después se añadieron un caso
de journal malformado y uno de import CLI: siguiente suite completa105. CI de
PR90/d3eef7f: MVP41346633128, Studio41346633108 y validate41346633292 success;
sync41346633137 success. Ninguna aprobación humana derivada de esos checks.

Bloqueos reales: Hyper-V gestión no habilitado, elevación740 y RAM libre~5GB;
Resolve no instalado/registro personal pendiente. Guías QA_WINDOWS11_VM y
QA_RESOLVE_BETA3 preparadas. Solicitud67 publicada y workflow41316675082 success,
mención6559335054 confirmada. No nueva confirmación de entrega física al iPhone.
No repetir aviso sobre ese bloqueo. Ninguna VM/ISO/editor/desconexión física probada.

Reanudar: git status; leer ACTUALIZACION_SEGURA_WINDOWS; preparar inputs oficiales
con scripts/prepare_installer_inputs.py; ejecutar build_beta.ps1 usando Python de
build existente y cachés verificadas; auditar NSIS y probar actualización directa
con store QA privado antes de crear PR correctiva de57. Conservar beta2/beta3,
backups, logs crudos y datos privados; publicar solo recibos sanitizados. Si falla,
identificar fase y código real, no atribuir el histórico por analogía. No GO externo,
no merge, no approved. Trabajo independiente autorizado continúa.

---

# Checkpoint vigente · estabilización y procedencia binaria · 31-10-2026

PR71 lista para revisión: https://github.com/jea27/Lut_generator/pull/71.
CI de bc778e8: MVP41186741670, Studio41186741616 y validate41186741589 success.
Corregido en PS5.1 el caso de rutas cortas/proveedor detectado por CI, manteniendo
rechazo de escape de directorio. El primer fallo de CI no se ocultó ni omitió.
Prioridad siguiente del usuario: dashboard automático en rama/worktree independiente
codex/COL-006-product-dashboard; no toca código de la aplicación de esta rama.

Tarea COL013#45, rama codex/COL-013-estabilizacion-beta3 desde origin/main
cfb6d11. PR70 ya integrada por jea27 a las08:27:11 UTC. Árbol de main idéntico
a HEAD4920cf0 de70;65/66/69 son ancestros. Escaneo69 blobs cambiados sin
hallazgos de secretos/perfil local/archivos privados,6 JPEG sin EXIF de origen
CC0 o QA ya revisado. Ver STAB_03_PR70_REVIEW.json y ESTABILIZACION_03.md.

Trabajo: profiler reproducible sin modificar motor; bundle/editor comparador
con oráculo LUT escalar; verificador PS5.1 de hashes antes/después sin borrar
datos; protocolo limpio W01–09 y editores E01–05. Roadmap conserva42 tareas y
estados: ampliación futura de COL026 añade inferencia de acabado y halation,
explícitamente sin implementar ni retrasar beta. Fuente UI/landing corrige
«sin telemetría» para diferenciar WebView2/SmartScreen. No APIs/efectos nuevos.

Pruebas locales37 MVP+91 seguimiento sin omisiones, TypeScript/Vite OK.
Se corrigió solo el entorno de módulos del proceso hijo PowerShell en el test,
sin cambiar políticas ni configuración global. Pipeline16MP3 pasadas mediana
17,376s: LUT9,005/acabado6,267/PNG1,445. No mejora entregada sobre32,392s del
binario histórico; entornos distintos. Tiles256/512 experimentales conservan
píxeles en1 foto; no aplicados ni medidos RAM/cancelación. LUT textual vs oráculo
error1,091e-7 en262 puntos: infraestructura, no prueba de editor real.

Bloqueo NUEVO:95 DLL/PYD cotejados contra TOC y NSIS,44 UCRT/API-set proceden de
caché nativa de herramientas. UCRT firmado pero hash diferente al SDK REDIST
local; no presume derechos. Gate en builder detiene nuevos builds antes del
staging/NSIS; ejecutado realmente,44 bloqueos esperados. CPython también exige
conciliar proveedor/build del runtime de herramientas. Ver LICENCIAS_BINARIAS_BETA.
No se instala/sustituye Python ni se edita/elimina DLL firmada. El candidato
beta2 y su hash3e3851ee…14f permanecen intactos, retenidos solo para QA interna.
NO existe instalador beta3: rama prepara estabilización, no nuevo artefacto.
Texto UI corregido y avisos complementarios requieren siguiente candidato,
versión/hash nuevos cuando la procedencia esté resuelta. No afirmar corrección
retroactiva del NSIS beta2. Paquete QA nuevo separado, sin instalador ni datos privados.

Sin VM accesible: Get-VM/vmms, VBoxManage/vmrun, procesosVM y Sandbox no presentes
en inventario. No virtualización habilitada. Windows limpio y editores reales
siguen not_run; no contactos o respuestas reales. Beta externa/venta NO-GO,
puertas separadas GO_NO_GO_03.md. Solicitud67 se reutiliza para procedencia,
entorno limpio/editor y revisión, sin volver a pedir7-Zip.

Reanudar: git status; gh pr list; leer Issue67,45,60. Revisar nuevo informe y
PR de esta rama. Resolver procedencia del runtime antes de build_beta.ps1;
no ocultar gate fallido. Con VM/PC ya autorizado ejecutar W01–09; con editor
activado E01–05, mantener datos crudos privados. No merge/approved/cobros/
entrega externa del agente. COL001 continúa pendiente. Historial debajo.

---
# Checkpoint anterior · conciliación de integraciones · 31-10-2026

Rama actual codex/COL-026-integracion-beta2, PR70 lista para revisión:
https://github.com/jea27/Lut_generator/pull/70. Árbol conservado desde
a01ed2b, sin sobrescribir datos. GitHub confirma merges humanos por jea27:
PR69 a rama COL042 (07:59:58 UTC), PR65 a main (08:00:10), PR66 a rama
COL037 (08:00:23). Por ese orden, origin/main=0539b9f incluye65 pero no los
cambios de66/69. Nueva PR de integración hacia main reúne landing, Look Match,
auditoría y clasificación final; no repetir implementación ni auto-fusionar.
Los HEAD de ramas intermedias no demuestran integración en main. No se aplican
approved ni done; Issue68 sigue review y COL001 pendiente de entrevistas.

Instalador y evidencias del checkpoint siguiente siguen vigentes: source
a452a5f y SHA256 3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f,
recalculado en esta conciliación. Sin cambios de runtime posteriores al build.
30+91 pruebas locales y CI anteriores correctas. CI70 correcta: MVP41184058852,
Studio41184058873 y validate41184100896; publish omitido en PR como corresponde.
Sync41184098485 success y JSON público leído:42 tareas, COL026 review con enlace
real a PR70, COL001 blocked. No cambio manual de estados ni approved.
Aviso nuevo de conciliación41184100601 success; bot6541069862 menciona jea27
en67. Sin confirmación física nueva del iPhone; no reenviar el mismo aviso.
Sin nuevos participantes, editor activado o Windows limpio: NO-GO externa y venta.
No volver a notificar por permisos7-Zip o por el mismo bloqueo de QA; la nueva
decisión de integración se consolida en67, sin crear otra Issue de acción.

Reanudar: git status; gh pr list --state open; leer Issue67 y revisar la PR de
codex/COL-026-integracion-beta2 hacia main. Tras integración humana comprobar
ancestría de main y sync real antes de afirmar despliegue. No inferir aprobación
de producto de los merges. Los apartados siguientes conservan evidencia histórica.

---
# Checkpoint previo · Look Match y QA externa · 31-10-2026

Rama codex/COL-026-look-match-beta, Issue68; base32278e4 de PR66, sobre PR65.
PR65/66 auditadas abiertas y checks correctos; no merges. PR69 nueva entrega
https://github.com/jea27/Lut_generator/pull/69, base rama de PR66; revisar65→66→69. Autorización explícita
actual permite acabado manual glow/difusión/fade y preparación de beta privada;
no cobros, beta general, certificados, virtualización o contacto de participantes.

Candidato0.3.0-beta.2 construido desdea452a5f, dirty=false. Archivo266211731 bytes,
SHA256 3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f.
Ruta ignorada apps/desktop/src-tauri/target/release/bundle/nsis/. Sin firma ni
release. Manifest en LOOK_03_ARTIFACT_B2.json; no confundir con0.2 ni glob de archivos.

Implementado: Look manual v1 (receta v2) con intensidad/bypass independientes,
color primero, glow/difusión lineales por tiles con halos/alfa y fade limitado.
Presets, JSON, PNG/JPG y lotes conservan efectos. LUT solo Color Match con aviso.
V1 sin acabado compatible; halation, microcontraste dedicado e inferencia del
acabado desde referencia NO implementados. No transferencia fiel demostrada.
Paneles desktop independientes conservan el comparador; feedback offline incluido.

30 tests MVP y91 tracking locales OK, TS/Vite/build nativo OK. Binario congelado:
demo realCC0, JSONv2/LUT, lote2 y PNG idéntico byte a byte al export individual.
Benchmark16MP32.4s con PNG/RSS815MB; preview0.729s, MAE preview/export reducido
0.00476 yP95 0.01455. No validación de piel/mercado. Evidencias LOOK_03_*.
Upgrade local0.2→0.3beta1→beta2 exit0,8 archivos existentes conservados por hash; arranque
nativo0.3 muestra preset previo y preferenciasEN. No Windows limpio (MSIX Codex).

Auditoría: corregidas155 rutas compilación nativas mediante remap Rust;0 en
nuevo exe. Corregido hash/version builder que elegía primer instalador del glob.
299 entradas con licencia declarada y avisos,6 faltantes recuperados con hashes.
Payload Python/PYZ+nativo enumerado;0 local-profile/secret/dev findings, pero27
archivos/módulos con rutas proveedor/ejemplos, ya clasificados y ligados a hashes.
NO decir instalador totalmente limpio. NSIS176 extraído, WebView2 firmado y plugin contrastado; los términos
Microsoft/VC/UCRT requieren revisión final; no editar DLL firmadas ni autoaprobar auditoría legal.

Preparado plan limpio/preflight no invasivo y5 perfiles sin asignar B01–05.
Formulario QA00 descargado, synthetic/unverified/counts_as_interview=false;
solo en .research-private/beta/qa. Nadie contactado ni respuestas reales.
Bundle LUT lossless CC0 en .lumaforge-local/look03-qa/LUT-Editor-QA-CC0.zip.
7-Zip26.05 portátil autorizado/preparado/verificado; no volver a pedir permiso.
176 entradas NSIS extraídas/auditadas, WebView2 Microsoft firma válida y plugin
Tauri0.5.3 hash idéntico a release oficial.0 patrón local/token/dev,27 rutas
proveedor/ejemplo (27 genéricas/ejemplos,0 desconocidas). Copias privadas/raw no publicar.
Avisos complementarios NSIS/Tauri en packaging/notices/upstream.
Photoshop no ofrece editor verificable en nueva inspección; último bloqueo
confirmado fue login. No afirmar login resuelto o importación real; Premiere muestra selección de suscripción, no se activó ni compró nada;
Resolve sin prueba. Acción67 reutilizable, no repetir bloqueo sin novedad.

NO-GO beta privada externa y venta, por separado en BETA_QA_EXTERNA.md y
BETA_03_AUDITORIA.md. Pendientes Windows10/11 limpio, payload completo/términos,
editores activados, retratos autorizados, responsable/canal/plazo y revisión.
COL001/P0 siguen pendientes. Las cinco pruebas no cumplen10–20 de COL041.

Reanudar: git status; consultar PR65/66 y nueva PR de esta rama/Issue68; leer67
antes de notificar. Datos beta persistentes en LocalAppData/ColorStudioBetaData.
No borrar .lumaforge-local, imágenes, presets o worktrees. App nativa0.3-beta2 abierta. Feedback interno verificado en WebView2;
corregido popup y migración de presetv1 antes de activar efectos (JSONv2 GUI probado).
Servidor QA propio26292/puerto8794 y landing8792 si activos; no interfaces externas.
Build ./scripts/build_beta.ps1; tests ./.venv-mvp/Scripts/python.exe -m unittest
discover -s tests_mvp -v; audit scripts/audit_beta_artifact.py (exit2 esperado
mientras existan findings). Siguiente: derechos Microsoft y QA limpia
cuando el usuario aporte entorno. CI69 en a452a5f: MVP41181274271 y Studio41181274272 success.
Notificación69 consolidada en67: run41182721936 success y comentario bot
6540890455 menciona jea27; recepción física nueva no confirmada, no reenviar.
Sync41183485906 success: JSON público42 tareas, COL026 review/001 blocked.
Corregida etiqueta roadmap ausente de68. PR69 apilada no se enlaza como pr_url
hasta base main por política actual del sync; enlace en Issue68 y PR directa.
CI de código y documentos observada: MVP41182631211/Studio41182631230 success.
Paquete local de revisión en .lumaforge-local/beta03-review/ con setup, guías,
avisos, QA CC0 y SHA256SUMS; no entregar externamente antes de puertas/decisión.

---
# Checkpoint vigente · beta Windows · 31-10-2026

Rama raíz actual codex/COL-042-preparacion-comercial; base técnica conservada
en codex/COL-037-beta-estabilidad, Issues COL036#57/COL037#58.
Candidato0.2.0-beta.1 construido e instalado; NSIS266193722 bytes, SHA256
c1798ece22b9a8f38b6c7042a59630c16800b7a7ca295ee4119a8c157d092a4a.
Sin firma ni release pública. Herramientas autorizadas ya instaladas; no repetir
permiso de Rust/MSVC/C++/SDK/PyInstaller/Tauri. PR52/53 integradas por jea27,
main a7a8df8 incorporado por fast-forward local sin sobrescribir cambios.
Conservadas PR63/64 y docs Look Match/investigación comercial. No efectos
espaciales implementados, no modificación de cuestionario49€, COL001 pendiente.

Implementado: instalador Tauri2 con sidecar local supervisado y puerto dinámico,
sesión cookie/token/origen, presets CRUD/grupos, preferencias ES/EN, bienvenida,
demo CC0, arrastrar imágenes y lotes cancelables con recuperación interrupted.
23 tests MVP y91 seguimiento locales OK; TS/Vite y build nativo OK. Prueba real
4 CC0 de16MP, exports11.4–13.7s, RSS789–804MB; lote2 outputs verificados, ICC y
hashes originales intactos; watchdog de muerte padre OK. No evidencia de piel.
Instalación/desinstalación exit0:8 archivos privados conservados por hash, proceso
auxiliar cerrado. Reinstalado para revisión. Contexto Codex/MSIX virtualiza rutas;
no confundir con Windows limpio. Datos en LocalAppData/ColorStudioBetaData.

Artefactos ignorados: apps/desktop/src-tauri/target/release/bundle/nsis/. Evidencias
públicas saneadas en docs/evidence/BETA_02_*. Datos QA privados .lumaforge-local.
Inventario299 paquetes + avisos incluidos,6 avisos/conciliación binaria pendientes.
Sin original privado, respuestas, credenciales ni fotografías privadas publicadas.

PR65: https://github.com/jea27/Lut_generator/pull/65 (beta, base main).
PR66: https://github.com/jea27/Lut_generator/pull/66 (landing/comercial, base rama
beta; revisar después de65 y cambiar destino tras integración humana).
CI observada: MVP41176292962 y Studio41176292989 correctas en65;
MVP41176295996 y Studio41176295970 correctas en66. Validación roadmap65 OK.
Ninguna PR fusionada por el agente ni tarea aprobada.
Acción única67: bot6540038578 menciona @jea27, aviso observado; no afirmar
recepción física de este aviso nuevo. Marcadores65/66 evitaron duplicados al
activar ready. Notificaciones de revisión41176358165/41176358957 success.
Issues57/58/60/62 en revisión;59/61 blocked por QA externa. Sync Pages41176446357 success; JSON público leído y comprobado:42 tareas,
COL001 blocked;036/037/040/042 review;038/041 blocked. Última CI observada
de66 en15d6f08: MVP41176457682, Studio41176457662 y aviso41176457661 success.
No editar manualmente estados JSON. COL001 y P0 comercial pendientes.
QA landing HTTP200, JS válido, vistas390x844/1280x900 y slider70% verificados.
Landing local apps/landing con captura real, CC0, comparador y descarga pública
pendiente; borradores BETA_COMERCIAL en entrega separada. Publicar ramas/PR está
autorizado, no main/merge/approved/releases/visibilidad/gastos.
Bloqueos: Windows limpio10/11, calidad de retratos autorizados y hardware;
Photoshop pide sesión Adobe, Premiere sin importación probada, Resolve ausente;
licencias, nombre/titular/legal/fiscal/precio/código público antes de vender.
GO solo demostración técnica local; NO-GO beta general y venta.

Reanudar: git status; gh pr list --repo jea27/Lut_generator; leer solicitud humana
beta y sus comentarios antes de avisar; no repetir bloqueo ya notificado.
Landing local http://127.0.0.1:8792 mientras servidor propio activo; app nativa
reinstalada y abierta,8 archivos conservados también tras reinstalar.
Build: ./scripts/build_beta.ps1. Tests: ./.venv-mvp/Scripts/python.exe -m unittest
discover -s tests_mvp -v. Smoke empaquetado: scripts/smoke_beta.py requiere piloto
CC0 existente y escribe carpeta privada nueva. No borrar datos/worktrees históricos.
Siguiente tarea elegible: cerrar auditoría de licencias binaria; QA externa solo
tras acceso a entorno limpio/Adobe/medios autorizados. Sin aprobación automática.

---

# Estado del agente · LumaForge MVP v0.1 · 2026-10-30

## Checkpoint vigente · P1/P2 autorizado


Este bloque sustituye cualquier prohibición histórica de iniciar P1/P2 de los
checkpoints anteriores. El usuario autorizó explícitamente ambas fases técnicas
con P0 comercial pendiente. No cambia la aprobación de P0 ni autoriza merges.

### Tarea actual y ramas
- Motor/API COL007–012: codex/COL-007-mvp-color-local, PR52, Issues39–44.
- Medición/revisión: COL013/014, Issues45/46, aceptación completa pendiente.
- Estudio COL015–019: codex/COL-015-mvp-studio, Issues47–51, rama actual raíz,
  apilada sobre la del motor. Revisar motor primero y luego estudio.
- Todo P0 conservado, incluido checkpoint38 integrado localmente en esta rama;
  PR36/37/38 previas no son borradas ni se fusionan desde el agente.

### Trabajo completado
Aplicación ejecutable: referencia/destino JPG/PNG8; análisis real; dos métodos
Lab con límites; comparador, intensidad/controles, presets JSON, PNG/JPG original
con ICC y LUT global33³. Código separado apps/api, apps/web, packages/colour_core.
Sin API externa de imagen, costes por proceso, autenticación cloud o cambio de Pages.
Dependencias locales autorizadas e instaladas en .venv-mvp/node_modules, ignoradas.

### Pruebas y resultados
14 unittest MVP OK sin omisiones y87 existentes OK en runtime anterior. TypeScript
+Vite build OK, npm audit de instalación0 vulnerabilidades. CI backend Windows
correcta en PR52; consultar sus checks para la última revisión. UI tiene CI propia.
TestClient de Starlette emite aviso de deprecación httpx, no error de pruebas.
Roundtrip de LUT por lector trilineal independiente <2e-6 por canal; export real
4928x3264 PNG/JPG, LUT33³ y JSON. Smoke en docs/evidence/MVP_01_SMOKE.json.
GUI: importación, matching, intensidad0, comparación51%, exposición0.10,
preset/undo/restauración/importación JSON y descargas PNG/cube/JSON comprobadas.
Viewports390 y1280 sin overflow. Detalles en docs/evidence/MVP_01_GUI.md.
Aproximadamente10s/RSS785MB en export16MP observada; preview ~1s/RSS235MB.
No son garantías ni medición de memoria GPU. Originales y exportaciones privadas
no se publican ni se convierten en evidencia de mercado.

### Cambios pendientes y revisión
Revisión visual/humana de calidad y criterios completos por Issue; no autoaprobar.
COL013 aún no tiene benchmark completo por20 escenas/GPU, COL018 no tiene
miniaturas reales ni historial de sesión persistido en disco; sí presets JSON y
undo/redo en memoria. COL020/021/022 y P0 entrevistas/evaluación ciega no ejecutadas.
No RAW/Log/HDR/16bit/vídeo, máscaras/segmentación/Tauri ni prueba de .cube en
Photoshop/Premiere/Resolve. Estas extensiones solo diseñadas, no implementadas.

### Reanudar / abrir
Abrir http://127.0.0.1:8790 si sigue activo; en caso contrario doble clic en
Iniciar-LumaForge.cmd desde la raíz. Preparación en docs/MVP_V01_WINDOWS.md.
La API sirve el build de apps/web/dist (no publicar ese editor en Pages).
Servidor loopback únicamente; detener con Ctrl+C en su consola.
Copias temporales en .lumaforge-local/images y presets en .lumaforge-local/presets,
ignorados. Máximo8 imágenes; eliminar copias desde la UI cuando se alcance límite.
Originales externos intactos. Hay exports reales en .lumaforge-local/demo y en
Descargas generados por la GUI. No borrar esta información al reanudar.

Para pruebas: ./.venv-mvp/Scripts/python.exe -m unittest discover -s tests_mvp -v
Compilación: npm --prefix apps/web run build. La app sirve sin Internet después
 de preparar dependencias/build. No iniciar trabajo avanzado antes de estabilizar.
Siguiente: revisión humana del MVP y validación externa de LUT/otras escenas
con permisos, mientras P0 comercial continúa por su circuito independiente.

### Evidencia final y revisión
PR52 motor/API y PR53 Color Studio listas para revisión, sin merge por el agente.
CI backend Windows41118511892 y frontend41119407555 success; 14 pruebas MVP
ejecutadas sin omisiones. 87 pruebas de seguimiento anteriores OK.
Acción consolidada Issue54: aviso41119481395 success, comentario6532271615
menciona @jea27. Respuesta real del propietario6532291469: base técnica aceptada
para revisión; no equivale a merge ni aprobación de todos los criterios. No
repetir ese aviso. La próxima sesión debe leer Issue54 antes de nuevas peticiones.
Worktree adicional .codex-worktrees/MVP-core conserva rama motor; raíz en rama
Color Studio. Las dependencias/build y datos locales están preparados e ignorados.
La demo de navegador se deja abierta con imágenes CC0 y servidor loopback activo.

## Checkpoints históricos P0 (no sustituyen la autorización vigente)

### Archivo de investigación P0 · 2026-10-30

## Tarea actual y rama

COL-006 / Issue #19: checkpoint posterior a la preparación de investigación.
Rama raíz `codex/COL-006-checkpoint-investigacion`, base `origin/main f06efa3`.
GitHub registra que **jea27** integró PR #31, #32, #33 y el checkpoint anterior
#30. El agente no realizó esos merges. Se prepara una PR documental nueva
porque #30 ya está fusionada; no se duplica ninguna Issue canónica.

No hay autorización P1 ni decisión go. Main no se modifica directamente.
El historial anterior queda conservado, incluido `2ef5fc5`; no se sobrescribió
trabajo local ajeno. Las nuevas ramas se crearon desde origin/main en worktrees.

## Trabajo completado en esta continuación

| Frente | Entrega | Evidencia y límite |
|---|---|---|
| COL-004 / #18 / PR #31 | Fuentes y piloto CC0 reproducible | Cuatro JPEG reales, dos capturas rurales; 34.773.100 bytes, autor Sergej Majboroda/Poly Haven, licencia/URL/MD5 proveedor/SHA-256. Binarios solo locales |
| COL-003 / #17 / PR #32 | CanonCGT y métricas offline | Paper y repo oficial fijado; código/pesos Apache2.0, derechos de datasets aparte. Modelo no ejecutado. Sexto candidato documental sin sustituir los cinco exigidos |
| COL-002 / #16 / PR #33 | Formulario local y recibos privados | Q1-Q15 por etapas, precio después de Q11; JSON sin envío, verificación pendiente y deduplicación. Cero participantes contactados |
| COL-006 / #19 | Integración, aviso único, recuperación | 81 tests locales; sincronización consultada; ningún criterio aprobado automáticamente |

Documentación detallada: P0_PILOTO_FUENTES.md, P0_CANONCGT.md, P0_METRICAS.md,
P0_FORMULARIO_REAL.md y diarios por tarea. Decisiones globales en DIARIO_DESARROLLO.

### Dataset y evidencias separadas

- `.research-media/polyhaven-rural/`: cuatro JPEG originales ignorados. Índice
  público `data/p0/pilot.json`, sin binarios. Se verificaron tamaño, MD5 y SHA-256,
  decodificación y descripción ICC sRGB IEC61966-2.1 de los cuatro archivos.
- Revisión visual de previsualizaciones: no se observan personas identificables
  ni marcas destacadas. No es garantía jurídica ni revisión humana de cobertura.
- DSC_0106 plain 4928x3264 frente a pretty 4891x3255: no es target alineado.
  DSC_0181 comparte tamaño, pero eso tampoco prueba alineación. No se promueven
  variantes como ground truth ni se fuerzan registros listos en dataset.json.
- `data/p0/controls/identity-real-photo.json`: control de identidad sobre una
  fotografía real. DeltaE76=0, SSIM aproximadamente 1, PSNR infinito representado
  por null+indicador. 0,852 s mide lectura/preprocesado/métricas, no un modelo.
- Fixtures sintéticas solo prueban infraestructura. QA de formulario: R999,
  todas las preguntas omitidas, archivo en `.research-private/qa/` de la raíz;
  captura `.research-media/formulario-qa-sintetica.png`. No son respuestas reales.
- Autoinformes permanecen `self_report_form/submitted_unverified`. SHA-256 y
  fechas prueban integridad/recepción, no identidad ni consentimiento efectivo.
  No se convierten a `interview_notes`; recibos futuros solo en carpeta privada.

## Pruebas realizadas y herramientas

- Git y Node operativos; gh 2.103.3 localizado en `%ProgramFiles%/GitHub CLI/gh.exe`.
  Sesión jea27 activa con repo/workflow; REVIEWER_GITHUB=jea27 comprobado.
- Python 3.12.14 del runtime ya instalado; NumPy 2.3.5 y Pillow 13.0.0 disponibles.
  Sin instalaciones, cambios de permisos, tokens nuevos, pesos o Torch/LPIPS.
- Ramas por separado: piloto 67 tests, métricas 72, formulario 70, todos locales
  OK. Integración de las tres ramas en worktree P0-verificacion: **81 tests OK
  sin omisiones**, node --check formulario y app.js OK; merge local sin conflictos.
- Las diferencias del código integrado con main f06efa3 son nulas; solo difería
  el checkpoint documental. No se repiten pruebas numéricas sin cambios de código.
- CI PR31: run41097285452 success, 67 tests y dos omisiones por Pillow ausente.
  CI PR32: run41097288188 success, 72 tests y seis omisiones por NumPy ausente.
  CI PR33: run41097293957 success, 70 tests sin omisiones.
  Esas omisiones no se presentan como pruebas numéricas remotas ejecutadas.
- Publicación/sync tras merges humanos: run41097620802 validate y publish success.
  Dashboard leído por HTTP: 42 tareas, P0 con cinco blocked y COL-005 review;
  enlaces a PR31/32/33/30 reales. Sin edición manual de estados JSON.
- p0_status --github --ready: registros válidos y cero entrevistas, cero pares
  aceptados, cero casos de producto. Ninguna de las seis Issues P0 aceptada;
  sin IDs canónicos duplicados. Exit 2 esperado; no es fallo de infraestructura.
- Inspección de cambios publicados: sin credenciales, claves privadas, rutas
  personales de Windows ni fotografías/respuestas privadas. Autoría fotográfica
  pública conservada por trazabilidad. Binarios y QA privados ignorados por Git.

## Notificación y decisiones humanas pendientes

Una sola solicitud existente actualizada: [Issue #29](https://github.com/jea27/Lut_generator/issues/29),
con título requerido, siete campos y needs-human. Workflow manual
[41097290400](https://github.com/jea27/Lut_generator/actions/runs/41097290400) success;
bot menciona a @jea27 en [comentario6528828373](https://github.com/jea27/Lut_generator/issues/29#issuecomment-6528828373).
Marcadores de PR en esa misma Issue impiden avisos independientes repetidos.
La recepción en iPhone de avisos previos fue confirmada; la de este aviso nuevo
no se afirma sin confirmación. Un aviso o merge nunca sustituye una aprobación.

Pendiente:
1. Revisar preparación; COL-005 sigue review (#13/#15) hasta aceptación explícita.
2. Elegir distribución: se recomienda que jea27 comparta el instrumento por
   canal privado con tres personas conocidas A/B/C-D, defina responsable y plazo
   (propuesta: jea27, 30 días). Alternativa: autorización de canal/candidatos/texto
   concretos al agente. No contactar a nadie antes de esa decisión.
3. Aportar inicialmente 2-3 fotos propias para piel con permisos de autor/modelo
   y referencias con derechos claros, por rutas privadas. Faltan diversidad y
   revisión de 20 pares; no subirlos a Issues/PR/Pages.
4. Identificar herramientas/versiones del benchmark ya instaladas/autorizadas.
   No instalar ni contratar nada para sortear el bloqueo.
5. Ejecutar las 12 entrevistas reales, comparativas 5x20 y revisión humana.
   Formularios no sustituyen entrevistas; intención de pago no equivale a compra.

COL-001 y COL-002 siguen pendientes de entrevistas reales. COL-003/004/006
siguen bloqueadas en sus criterios de evidencia; ninguna tarea cerrada/approved
por el agente. P1 permanece detenido.

## Cambios pendientes y próximas tareas elegibles

Código de preparación integrado por jea27. Este checkpoint/diario se publica
para revisión en una rama documental independiente. Ver el estado actual de
su PR y checks antes de actuar: no asumir que un merge de preparación aprueba P0.

El siguiente trabajo con evidencia exige respuestas/permisos/acceso enumerados
en #29. Al recibirlos, registrar primero un lote pequeño y contrastar original,
consentimiento, autoría, perfiles y geometría. Ampliar fuentes CC0 según la
cobertura faltante; no duplicar 20 variantes rurales para aparentar diversidad.
No hay otro criterio P0 que pueda completarse inventando datos o usando fixtures.

## Ramas y worktrees preservados

| Carpeta relativa a raíz | Rama | Uso |
|---|---|---|
| raíz | codex/COL-006-checkpoint-investigacion | Recuperación vigente |
| .codex-worktrees/P0-verificacion | codex/COL-006-verificacion-investigacion | Integración local de PR31/32/33, 81 tests |
| .codex-worktrees/COL-003-metricas | codex/COL-003-metricas-canoncgt | Preparación PR32 |
| .codex-worktrees/COL-002-formulario | codex/COL-002-formulario-local | Preparación PR33 |
| .codex-worktrees/COL-002 | codex/COL-002-evidencia-entrevistas | Entrega anterior conservada |
| .codex-worktrees/COL-003 | codex/COL-003-protocolo-benchmark | Entrega anterior conservada |
| .codex-worktrees/COL-004 | codex/COL-004-manifiesto-dataset | Entrega anterior conservada |

No borrar ni recrear estas ramas/carpetas. La rama piloto sigue conservada en
Git, además de su integración humana en main. Las carpetas .research-media y
.research-private de la raíz están ignoradas también mediante exclude local.
El servidor QA se limita a 127.0.0.1 y se detiene al finalizar la revisión.

## Instrucciones concretas de reanudación

Desde esta raíz, comprobar git status/branch y leer Issue29 antes de contactar
participantes o instalar herramientas. En PowerShell, sin depender de WindowsApps:

```powershell
git status --short
git branch --show-current
git fetch origin
& "$env:ProgramFiles\GitHub CLI\gh.exe" issue view 29 --repo jea27/Lut_generator
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/p0_status.py --github --gh-path "$env:ProgramFiles\GitHub CLI\gh.exe" --ready
```

Exit 2 es lo esperado mientras falten evidencias. No subir originales, respuestas
ni contactos. Para comprobar hashes del piloto, `prepare_pilot.py --download`
reutiliza archivos existentes verificándolos; desde otra carpeta no apunta a los
medios raíz. El formulario está en research/form.html y su procedimiento en
P0_FORMULARIO_REAL.md. Abrir ramas nuevas solo para una Issue P0 elegible y
conservar siempre lo pendiente; nunca escribir directamente en main.

## Continuación · enlace web COL-005 (checkpoint de trabajo)
PR34 ya integrada en ae34ea0, árbol inicial limpio. Rama raíz actual
codex/COL-005-formulario-web. 87 tests locales OK y cuatro viewports móviles
comprobados. Source research/ y empaquetado allowlist para Pages preparados;
publicación depende de merge humano y Actions. R101/102/103 reservados sin
asignar; R999 QA privada, bloqueado en registro real. Se continúa con permisos
fotográficos/COL004 y controles CC0/COL003 sin contactar participantes.

## Checkpoint vigente · formulario web y controles P0 · 2026-10-30

### Tarea actual y rama
COL006 / Issue19, rama raíz codex/COL-006-checkpoint-formulario. Sustituye como
estado vigente las secciones históricas anteriores. PR34 estaba integrada al
iniciar; árbol limpio y sin commits pendientes respecto a main. PR35 fue
integrada posteriormente por jea27 (86d2137), no por el agente.

### Trabajo completado
- COL005/PR35: formulario público https://jea27.github.io/Lut_generator/investigacion/
  con tres códigos reservados: #R101, #R102 y #R103. Sin identidades asignadas,
  invitaciones enviadas ni respuestas reales. Consentimiento y esquema v1
  conservados. JSON solo por acción de la persona, previsualización/descarga/
  compartir con fallback; no servidor de respuestas ni nuevos proveedores.
- Allowlist HTML/JS/CSS en ambos workflows existentes; un sync posterior también
  conserva el formulario. Archivos generados ignorados. No se cambian permisos.
- COL004/PR36: guía y plantilla vacía para autoría/licencia, consentimiento de
  personas identificables, alcance interno, custodia y retirada. Cumplimentar
  solo en privado; no autoriza ninguna foto por sí misma.
- COL003/PR37: experimentos posibles y runner de controles sobre los cuatro
  originales CC0 existentes. Doce lecturas reales (tres por foto), identidad y
  repetición reproducibles. Tiempos de infraestructura, nunca inferencia.
  DSC0106 no alineado por tamaño; DSC0181 sin revisión de target pese a igual
  tamaño. Cero productos ejecutados y cero pares aceptados por esta entrega.

### Pruebas y evidencias
- Rama web: 87 unittest locales OK, sin omisiones. Rama controles: 85 OK.
- Integración en .codex-worktrees/P0-web-verificacion: **91 unittest OK sin
  omisiones**, node --check y empaquetado allowlist correctos, sin conflictos.
- Viewports locales 320x568, 390x844, 430x932 y 844x390: sin desbordamiento;
  botón >=44px, consentimiento sin premarcar. Tres etapas y JSON sintético R999
  descargado y validado, separado de participantes. Importador rechaza R999.
- Pages real: run41114395315 success. HTTP HTML/JS/CSS comparados con SHA-256 de
  blobs Git en main, coincidencia exacta. La copia Windows tiene CRLF; por eso
  se comparó contra blobs Git canónicos, sin confundir finales de línea.
- Navegador sobre HTTPS: tres etapas y descarga R999 válidas. Vista pública a
  390px también sin desbordamiento. Share: mocks de éxito/cancelación/fallo;
  no se afirma entrega ni prueba física de Safari/iPhone.
- QA sintética privada en .research-private/qa/R999-web-mobile-20261030.json y
  R999-public-pages-20261030.json. Ningún recibo de participante creado. Captura
  local en .research-media/formulario-publico-movil-qa.png; no evidencia de usuario.
- p0_status --github --ready: exit2 esperado, cero entrevistas, cero pares
  aceptados, cero runs de producto, ninguna tarea aceptada; sin duplicados.
- CI de ramas y sincronización: consultar los checks de PR35/36/37 y de esta PR;
  NumPy/Pillow ausentes en CI implican ocho omisiones opcionales explícitas.
  Las pruebas locales numéricas sí se ejecutaron. No repetir por cambios solo MD.

### Bloqueos humanos y aviso
Solicitud existente #29 actualizada, needs-human y siete campos. Un solo aviso
nuevo: run41114232338 success y comentario6531560480 menciona @jea27. PR36/37
reutilizan esa solicitud sin nuevos avisos. No se confirma recepción física de
este aviso nuevo. Se corrigió su cuerpo al conservar UTF-8 al leer JSON de gh;
no se vuelven a decodificar bytes UTF-8 con la página de códigos de Windows.

Pendiente: prueba R999 en Safari/iPhone, guardado en Archivos y devolución del
JSON sintético por canal privado. Responsable/canal/conservación para personas
reales siguen por acordar; propuesta jea27/30 días no es consentimiento obtenido.
El usuario distribuye los enlaces cuando esa información esté acordada; el agente
no contacta personas por iniciativa propia. Fotos para piel con permisos y acceso
a herramientas autorizadas siguen pendientes. COL001 no completada; P1 detenido.

### Próximos pasos elegibles y reanudación
Leer docs/P0_FORMULARIO_WEB.md para recogida/importación privada; usar
scripts/register_form_response.py solo con JSON de persona real y código asignado,
no con R999. El recibo conserva pending_human y counts_as_interview=false.
Leer docs/P0_GUIA_FOTOGRAFIAS_PERMISOS.md antes de recibir fotos y
P0_EXPERIMENTOS_PILOTO.md antes de ejecutar productos; ambas entregas en sus PR
si todavía no están integradas. Solo registrar entrevistas realmente celebradas.

Nuevos worktrees conservados dentro de .codex-worktrees/:
- COL-004-permisos: codex/COL-004-guia-permisos.
- COL-003-controles: codex/COL-003-controles-piloto.
- P0-web-verificacion: codex/COL-006-verificacion-web.
No borrar los worktrees previos. El código web está ya en main por merge humano.

Desde la raíz: git status --short; git branch --show-current; consultar Issue29.
Python explícito del runtime (comandos arriba) y p0_status --github --ready.
Para rerun de controles usar --media-root .research-media/polyhaven-rural, reporte
nuevo; no sobrescribir el informe original ni rellenar benchmark.json con controles.
No publicar JSON de respuestas, fotos, permisos firmados, contactos ni EXIF privado.


Actualización final de clasificación: las27 coincidencias de rutas se han
resuelto técnicamente como cuentas genéricas de compilación de proveedor o
placeholders/ejemplos de documentación (incluido ntpath.splitroot).0 perfiles de
origen sin clasificar. Hashes de cada archivo/contenedor cotejados con el NSIS
completo en LOOK_03_PATH_CLASSIFICATION.json. El scanner bruto conserva sus27
hallazgos y no se ocultan ni alteran DLL; no son rutas del perfil local, secretos
o datos de clientes. No constituye aprobación de COL040 ni prueba universal de
privacidad. Siguen las puertas de Windows limpio y derechos/condiciones Microsoft.


## Checkpoint independiente del dashboard · 31-10-2026

Rama codex/COL-006-product-dashboard en worktree propio, relacionada con Issue19;
la decisión P0 permanece bloqueada y las42 tareas originales intactas. No se
modifica apps/ ni packages/. Reglas/contrato en DASHBOARD_PRODUCTO.md.
Panel Color Studio con15 capacidades/8 entregables núcleo, ejes técnicos y
humanos separados, puertas beta/comercial, PR/CI, versiones y acciones humanas.
Snapshot GitHub real:8/8 alcance técnico acotado,0/8 humano,1/5 beta,0/4 venta;
ninguna release publicada o descarga autorizada. No significa producto terminado.
107 tests locales de seguimiento OK; suite de aplicación no tocada. QA navegador
1280,390,320,430 y844 sin overflow; filtros y42 tareas conservadas comprobados,
0 errores de consola. Capturas y PRODUCT_QA.json. No iPhone físico ni despliegue
de esta rama. Se conserva Pages actual hasta integración humana.
Siguiente: CI/PR de esta rama, revisar sin merge del agente; después de merge
humano verificar workflows y JSON público. Un nuevo fallo conserva snapshot
anterior y muestra antigüedad, nunca inventa éxito. Reanudar leyendo esta sección,
Issue19/67, PR de dashboard y scripts/sync_product.py. Fuente de verdad y reglas
de entrega permiten al agente actualizar capacidades en su PR sin que el usuario
edite roadmap. Estabilización de app sigue separada en PR71; runtime/QA limpia
requieren intervención de67. No aplicar approved ni release-approved:TAG.


### Conciliación del checkpoint de dashboard

Issue canónica72 [COL043], creada por el otro chat durante la ejecución; se
reutiliza sin duplicar. PR74: https://github.com/jea27/Lut_generator/pull/74.
Rama publicada sigue codex/COL-006-product-dashboard; es una operación fuera
de42 tareas y métricas. Main71 integrada por jea27(5b6a910) se incorporó a
esta rama local, conservando ambos registros del diario. Diff contra main no
cambia apps/ o packages/. CI inicial74 MVP41188254939, Studio41188254955 y
validate41188254963 success, con consulta real de GitHub sin ampliar permisos.
La nueva revisión se validará de nuevo. Coordinación73: entregar esta PR y
checkpoint antes de que otro chat tome el worktree. No merge remoto del agente.


## Checkpoint COL044 · revisión humana individual · 31-10-2026

Worktree propio COL-044-human-review, rama codex/COL-044-human-review, Issue76,
PR79: https://github.com/jea27/Lut_generator/pull/79. No apps/packages modificados,
42 tareas intactas, ninguna capacidad real aprobada, sin merge del agente.
Mis revisiones con11 capacidades reales pendientes, checklist/pasos/versión/
evidencias y observaciones en memoria. Copiar/abrir Issue y publicar conjea27;
no token en Pages. Protocolo/autenticación/límites en REVISIONES_HUMANAS.md.
Recibos por ID+huella, revocación al editar/borrar, cambios relacionados requieren
nueva revisión; labels/merges nunca aprueban capacidades. Historial de GitHub
conservado; notas no se copian al JSON público. Cola para agente sin prometer24/7.

126 tests de seguimiento+37 MVP locales OK, JS válido, demo real en Issue77:
approval6541989840 → Actions41191045868 → estado QA aprobado; cambios6542024460
→ Actions41191317941 → Correcciones solicitadas; replay41191386973 no reactivó
aceptación ni duplicó recibos(2). Los3 jobs de Pages quedaron omitidos. Artefactos
reales verifican0 aprobaciones de producto. HUMAN_REVIEW_DEMO.json/capturas5
anchos sin overflow y0 errores. No iPhone físico ni nueva beta/instalación.

Pendiente: CI final/revisión humana de PR79. issue_comment y publicación del
nuevo flujo necesitan integración humana en main; solo demo de rama validada,
no afirmar ya activado en Pages. Tras merge humano, repetir únicamente demo y
comprobar evento real+sync+HTTP público. No merge para forzar una prueba.
Reanudar: git status en esta rama; gh pr checks79; leer Issue76 y PR79. Conservar
worktrees/documentación anteriores. No emitir approve sobre capacidades reales.

## Checkpoint vigente · COL045/046/047 · 31-10-2026

Tarea: primera entrega Creator/Pro/Shot Planner con seguridad local. Rama
codex/COL-045-creator-pro, worktree COL-045-creator-pro desde main8674566.
Issues81/82/83. No tocar raíz codex/COL-013-estabilizacion-beta3 ni otros worktrees.
Project OS/COL048 se está tratando en otro chat; no modificar su código web.

Completado para revisión técnica: modos guiado/técnico sobre motor compartido,
catálogo de capacidades/proveedor local, preview obligatoria de receta actual,
acabado manual conservado, plan local con límites/fuentes/diagrama/JSON. No hay
recuperación fiel del rodaje ni aprobación visual/profesional. Se mantienen las
42 tareas y los denominadores MVP8/beta/venta;18 capacidades en el catálogo.

Pruebas:58 unittest API/motor,128 seguimiento,3 Node y build Vue/TS correctos.
Ocho tests de planner se repitieron tras añadir etiquetas, ya incluidos en58.
QA funcional de navegador y seis medidas móviles/pequeñas más escritorio,
0 errores de consola; feedback local con CSP permitido. PNG/JSON descargados
se verificaron en privado, sin datos personales. Capturas y hashes en
CREATOR_045_QA.json y SHOT_PLANNER_047_*.jpg. Fuentes y uso en
CREATOR_PRO_SHOT_PLANNER.md. Plan JSON se exporta pero no se reimporta todavía.

Dos fotos CC0 de16MP perfiladas; DSC0106 coincide con input/receta/PNG previo,
16.912s esta vez. DSC0181 22.097s es otro input. No promedio o mejora universal;
ni tile mayor ni cambio de matemática adoptados. Perfiles/scope versionados.
OSV566 y npm audit:2 paquetes Cargo con avisos globales, ninguno en árbol
Windows223. No se ocultan ni se sustituyen paquetes sin comprobar plataforma.

PR86 en borrador: https://github.com/jea27/Lut_generator/pull/86.
Rama publicada, tres capacidades enlazadas a esta entrega. Trabajo local
completado para revisión; consultar borrador/lista y últimos checks en PR86.
La aceptación humana y las puertas de distribución siguen pendientes. No merge/aprobación del agente. La producción
de Mis revisiones (#79) sí fue activada y validada tras el merge de jea27:
https://github.com/jea27/Lut_generator/issues/76#issuecomment-6542238759.

Bloqueos humanos: #67, preparar runtime oficial aislado requiere autorización
expresa pendiente; Windows10/11 limpio y Adobe/Resolve activados requieren entorno
real. No reinstalar herramientas ni instalar virtualización para sortearlo.
Autoría/consentimiento/canal del piloto siguen pendientes. Ningún nuevo NSIS,
release, venta o participante. No inferir que un merge aprueba esas puertas.

Reanudar desde este worktree: git status --short; leer Issues81/82/83 y PR
asociada; comprobar CI antes de modificar. Python disponible en el entorno MVP
compartido, Node existente mediante junction node_modules ignorada. Para preview:
`& ../../.venv-mvp/Scripts/python.exe -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8817 --no-access-log --no-proxy-headers`.
El servidor solo sirve esta rama y usa datos ignorados propios.
Leer el protocolo y las evidencias antes de ampliar funciones. Próximo paso:
revisión de esta entrega y resolver #67; después validar el plan con escena y
medios autorizados reales, sin afirmar que la demo rural reconstruye un rodaje.

### Recuperación de publicación — PR86

Código3761999 publicado, CI41210911012/41210911018/41210911004 y sincronización
41210911087 success. Manifiesto enlaza las3 capacidades nuevas a PR86 sin
presentarlas como implementadas en main. Colector real de GitHub validado en
lectura; evidencia CREATOR_045_SYNC.json, archivos generados originales restaurados
por bytes. Revisión de Color Match/lotes/receta/Windows queda obsoleta en el
candidato por huellas relacionadas, conservando historial previo. Producción
sigue en main8674566 hasta integración humana. No publicar porcentajes locales
como si fueran el dashboard real. El código y la evidencia quedan publicados en la rama. El estado final
de CI/PR y el único aviso de revisión se registran en el último comentario
de Issue81 y en PR86; consultarlos antes de actuar. No asumir un merge o
aprobación humana a partir de este checkpoint histórico.
# Checkpoint vigente · COL036 · integración posterior a PR86 · 31-10-2026

Rama `codex/COL-036-qa-integracion`, worktree `COL-036-beta-qa`, desde main5799531.
PR86 ya integrada por jea27; no confundirlo con aprobación de Creator/Pro/Planner.
Issue57 es la tarea;67 el único bloqueo canónico de distribución. Raíz y trabajo
anterior conservados; ProjectOS/COL048 en otro chat, sin cambios de su código.

Completado localmente: correcciones de carrera al cargar modo/preferencias,
controles durante operaciones, confirmación del Planner y aviso de borrado;
guía manual no técnica y smoke del congelado aislando PATH/cwd/módulos.
61 tests MVP,128 seguimiento,6 Node y build correctos; QA real con demo/fotos CC0,
cuatro exportaciones ~16MP a resolución completa, modo/receta/imágenes/plan
conservados. Evidencia INTEGRACION_036_QA.json y capturas. Detalles y límites
en INTEGRACION_BETA_036.md. Snapshot del congelado anterior a commit identificado
por base+hashes fuente; no es otro setup0.3.0-beta.2 ni release.

Pendiente en este checkpoint: publicar rama/PR de seguimiento, vincular manifiesto
y verificar CI/sync. La última sección de publicación prevalece cuando exista.
Bloqueos humanos:67 requiere autorización del runtime PSF aislado propuesto,
Windows10/11 limpio/operador y editor activado.44 DLL y27 rutas upstream pendientes;
beta/venta NO-GO, sin nueva VM/runtime/NSIS, invitaciones, pagos, merge o approved.
COL001 y P0 comercial siguen pendientes de evidencia real. Próxima tarea técnica:
reconstruir con runtime oficial solo tras autorización; ejecutar W01–W09 y E01–E05
con entornos reales. No iniciar nuevas capacidades para evitar esas puertas.

Reanudar: `git status --short`; consultar PR86, Issue57/67 y última PR de esta rama;
leer su CI y comentarios antes de actuar. Usar la venv compartida solo para las
pruebas existentes; no sustituirla para otro runtime. Scripts/comandos reproducibles
en INTEGRACION_BETA_036.md; guía para el responsable PRUEBA_CREATOR_PRO_PLANNER.md.
No eliminar worktrees previos ni cambios ajenos. Nunca tratar aviso/merge como GO.

## Publicación COL036 · PR88

Rama publicada en216af93; PR88 abierta hacia main, seguimiento de #57 y #67:
https://github.com/jea27/Lut_generator/pull/88. Primer CI remoto MVP41223288357,
studio41223288363 y validate41223288358 correctos. Manifiesto enlaza entrega88
con Windows/Creator/Pro/Planner sin autoaceptación. Se conserva el denominador8,
las18 capacidades y42 tareas. Colector real con API GitHub confirma MVP técnico8/8
frente a aceptación0/8, beta/venta NO-GO; archivos generados restaurados por bytes.
La instantánea de rama no equivale a publicación en Pages. Las evidencias nuevas
solo formarán parte de main tras integración humana. CI/checks finales y aviso
canónico se consultan en PR88 y #67; no repetir needs-human para el mismo texto.
El trabajo de código está terminado para revisión; queda validación humana,
runtime oficial autorizado y QA limpia. No hay cambios de main o de otros agentes.

## Checkpoint final de integración · PR88 · 31-10-2026

Tarea actual: COL036/Issue57, rama codex/COL-036-qa-integracion. PR88 abierta,
lista para revisión hacia main; código final60958b4. Sin merge ni approved.
Se corrigió también el historial de preset/importación/reset:7 Node correctos,
undo/redo real en el congelado (preset0.05↔0.1, reset0↔0.05, import0.4↔0.05).
61 tests motor/API/harness y128 seguimiento conservados. Build Vue/TS correcto.
CI del código final: MVP41223999971, studio41224000016, validate41223999953,
sync41223998116 success. Sync anterior cancelado sin steps fue recuperado en
41223541881 intento2, sin cambios de permisos. CI del checkpoint documental se
consulta en PR88/checks; el último comentario de Issue57 guarda su resultado.

Evidencia: INTEGRACION_036_QA.json (hashes fuente/bundle, fases reales y límites),
INTEGRACION_036_SYNC.json (colector GitHub + lectura separada de Pages). Los cuatro
archivos generados fueron restaurados byte a byte.42 tareas:8 bloqueadas,
17 en revisión,1 en progreso y16 planificadas en la consulta17:22Z.18 capacidades,
MVP técnico8/8 y aceptación0/8, beta/venta NO-GO. Los cuatro enlaces Windows,
Creator/Pro/Planner apuntan a PR88. La lectura pública17:21:19Z todavía precedía
ready_for_review; no se presenta como actualización instantánea. Los workflows
posteriores publican desde main; evidencias nuevas de rama esperan merge humano.

Aviso único canónico verificado: workflow41224150508 success, comentario
https://github.com/jea27/Lut_generator/issues/67#issuecomment-6546679381 menciona
@jea27. ready_for_review41224148591 reconoció la solicitud existente sin otra
Issue/aviso. No hay confirmación nueva de recepción física ni aprobación implícita.

Cambios pendientes de código: ninguno local. Solo aceptación/revisión de PR88,
autorización runtime aislado y QA real de distribución. No hay nuevo instalador.
44 DLL y27 archivos con cadenas upstream siguen sujetos a revisión; no hay
prueba Windows limpio ni Adobe/Resolve. COL001/P0 comercial siguen pendientes.
Los servidores temporales y su pestaña de QA se cerraron; datos/resultados
internos permanecen ignorados en .lumaforge-local. Raíz y otros worktrees intactos.

Próximo trabajo elegible: tras respuesta RUNTIME3.14.10 en67, preparar build aislado
sin sustituir la venv compartida; después W01–W09 con operador autorizado y
E01–E05 en editor activado. Sin esa decisión no sortear el gate ni ampliar
capacidades. Para reanudar: abrir este worktree, git status --short, gh pr view 88,
gh pr checks 88 y leer67/57; comandos exactos en INTEGRACION_BETA_036.md.

### Última comprobación Creator

El último commit de PR88 separa transferencia realizada de preview neutra:
importar ambas fotos y comparar sin fit mantiene «Detectar color» pendiente;
fit real avanza a «Ajustar». Comparar avanza a «Comparar», cambiar receta vuelve
a pedir comparación. Siete Node/build correctos y secuencia real en congelado,
0 warnings/errores, captura INTEGRACION_GUIA_036.jpg. API/matemática sin cambios;
no repetir benchmark16MP para flags UI. Hashes/fases en INTEGRACION_036_QA.json.
Payload final conserva158/27,0 hallazgos de perfil local/secretos/desarrollo según
patrones. Sin cambios de autorización67 ni avisos duplicados. Pruebas CI del
head final y estado publicado se registran en el comentario de57; sigue PR88
lista para revisión, worktree conservado y sin cambios pendientes al publicar.

## En curso · COL036 runtime oficial · 01-11-2026

Rama codex/COL-036-runtime-oficial, worktree COL-036-runtime-oficial. PR88 integrada
por jea27, rama adelantada a05b4983 sin perder cambios. Usuario autoriza runtime
oficial aislado y candidato interno; ningún permiso de beta externa, merge o venta.

Preparado: lock CPython3.14.10 embeddable PSF +19 wheels runtime verificados,
extracción con RECORD, aislamiento._pth, origen/arquitectura/imports de60 PE,
conservación de avisos, comparación fuente y guardas ante tampering. No DLL del
host copiadas. No instalación global. Smoke API/demo/mode/preset/plan/lote/watchdog
real correcto con PATH Windows y módulos de bundle/SO.70 unittest ejecutados con
Python3.14.10 y núcleo del bundle;3 extras HTTP de QA separados, nunca en producto.
Nueve pruebas nuevas de seguridad del empaquetado; firmas PSF/Microsoft requeridas
Valid. Scanner de fuentes/binarios/bytecode3.14:0 hallazgos bloqueantes. No GO legal.

Cambios locales pendientes: builder/auditores, runnerWindows embeddable, datos
por usuario idénticos a beta2, versión0.3.0-beta.3 y pruebas. Compilación nativa
sin bundle terminó correctamente(4m10s); instalador final no construido todavía.
Quedan inventario actualizado, builder NSIS, reproducibilidad de payload, GUI,
instalación/upgrade/uninstall locales y auditoría de todo el NSIS. No Windows
limpio ejecutado; no herramientas de VM presentes al último inventario. Adobe/
Resolve quedan pendientes. #67 es solicitud canónica, no repetir permiso runtime.

Reanudar desde este worktree: git status --short; leer log privado
.lumaforge-local/native-build.log y artefactos runtime-build-3. Build Python de
herramientas existente en ../../.venv-mvp; no usar sus DLL en producto. Los19
wheels y ZIP se guardan en .lumaforge-local/downloads; builder puede validar
--offline. No borrar worktrees, datos privados ni staging sin comprobar su marca.

## Checkpoint de candidato interno · COL036 / PR89 · 01-11-2026

Tarea COL036/Issue57; solicitud canónica67. Rama codex/COL-036-runtime-oficial
en worktree COL-036-runtime-oficial. PR89 hacia main, sin merge ni approved.
PR88 integrada por jea27 en05b4983; raíz y otros worktrees preservados.

Runtime PSF3.14.10 embeddable +19 wheels oficiales fijados por lock/RECORD/hash,
sin DLL del host.923 archivos/60 PE;945 extraídos de NSIS. Compilador/plugins y
avisos cotejados con origen oficial; firmas requeridas PSF/MS Valid. Guías/hooks
de desarrollo upstream excluidos. Auditoría completa integrada en el build.

Candidato local0.3.0-beta.3,46683099 bytes, fuente limpia cf1d451,
SHA2560350f5b44be2850f828a148debc4174b8f134953b080d895bbbca8620576b5cd.
NSIS sin firma; no certificado comprado. Recibo RUNTIME_036_ARTIFACT.json. Los
commits posteriores añaden auditores, evidencia y documentación; inputs de la
aplicación empaquetada siguen iguales.923 payloads idénticos en dos ensamblados;
manifiestos difieren solo en dirty del segundo, con auditores aún sin commit.
No se afirma NSIS idéntico bit a bit ni equivalencia visual universal.

Pruebas:73 al construir;78 locales host/embebido después;79 host/embebido en
CI36fbb789 (41292429730 success),128 seguimiento y7 Node correctos; build Vue/TS
correcto. Flags de aislamiento1; cwd/PYTHON* contaminados no alteran imports.
71 PE cargados del bundle/SO cotejados por hash, ninguno inesperado. API con
cuatro CC0 de16MP:15.113–16.588s, lote2 y originales intactos; no es una mejora
general demostrada. LUT conserva hash4fb41b…8d331. Watchdog real correcto.

QA instalada desde Codex/MSIX de este PC: Creator/Pro/Planner, demo y descargas
PNG/JPG/receta/.cube/planJSON reales. PNG/JPG1024×678 con ICC; plan mantiene
human_validated=false. Desinstalar beta2, instalar beta3, desinstalar beta3 y
reinstalar:0; preset beta2,6 archivos QA y sentinel sintético conservados.
9 archivos del almacén existente con hashes intactos; sus datos no se publican.
Sentinel retirado al acabar; todos los procesos propios del ensayo cerrados.

Fallo abierto: actualización directa /S devolvió2; asistente interactivo esperó
al desinstalador previo y su idioma no resultó accesible al controlador. Causa
raíz no confirmada. No hay VM/Windows limpio, corte físico de red ni importación
LUT nueva en Adobe/Resolve. Beta externa y venta NO-GO; derechos/titular/piloto
y revisión humana pendientes. Sin aprobar capacidades ni completar P0 comercial.

Build Windows remoto41292426593 terminó success sobre36fbb789, incluyendo NSIS
completo y guardas de procedencia. Solo sube informes saneados, no instaladores.
La documentación/manifiesto y recibos están comprometidos en6fdd593. El cierre
de checks del último head y la solicitud humana se registran en PR89/57/67;
consultar https://github.com/jea27/Lut_generator/pull/89/checks antes de continuar.
El paso final es pasar PR89 a revisión y comprobar un único aviso desde67,
con marcador lumaforge-review-pr:89; no repetir aviso para este mismo bloqueo.
Las evidencias de esta rama esperan merge humano para Pages; sincronizar Issues/PR
desde main no publica archivos de una rama abierta. Recibos JSON preservados
byte a byte por .gitattributes para mantener sus hashes tras un checkout Windows.

Reanudar aquí: git status --short; gh pr view 89; gh pr checks 89; leer67 y
RUNTIME_WINDOWS_EMBEBIDO.md. Python de build ../../.venv-mvp/Scripts/python.exe.
Setup: apps/desktop/src-tauri/target/release/bundle/nsis/Color Studio Beta_0.3.0-beta.3_x64-setup.exe.
Caches/informes privados en .lumaforge-local. No publicar exe/datos originales.
Próximo trabajo: resolver actualización directa en Windows normal/limpio con
operador y ejecutar W01–W09/E01–E05. No ampliar producto ni fusionar la PR.

Integración final del colector: se detectó Unsupported review path por cuatro
inputs runtime añadidos al manifiesto. Corregido con allowlist exacta en
human_reviews.py (sin permisos nuevos),130 tests de seguimiento correctos,
incluyendo catálogo real y cambio de pin que invalida revisión. Colector con
GitHub real pasó en lectura:42 tareas, Windows enlaza PR89, aceptación MVP0/8,
beta/venta NO-GO. Pages todavía publica0.3.0-beta.2 desde05b4983 y ya muestra
PR89; beta3/recibos necesitan merge humano. Los cuatro archivos generados se
restauraron byte a byte. Evidencia RUNTIME_036_SYNC.json identifica la proyección
de rama y la lectura pública por separado; no se fingió publicar la rama.

Cierre de revisión: PR89 no-borrador y Issue57 status:review. Código b3f261f pasó
MVP41293860547, cliente41293860602 y validación/colector41293860581; ready-for-review
validó otra vez en41294067005. Aviso único41294069249 success; bot mencionó a
jea27 en67#issuecomment-6556221187. No hay confirmación nueva de recepción física.
No repetir el aviso. Los sync cancelados de la ráfaga no ejecutaron steps; su
reintento final/estado publicado se verifica en PR89/checks y comentario final57.
El checkpoint usa identidad no-reply por comando; la identidad anterior ya
estaba en el historial público. No se cambió config global ni reescribió historial.

## En curso · diagnóstico de actualización beta3 · 01-11-2026

PR89 integrada por jea27 en918cb638; nuevo worktree COL-036-actualizacion-segura,
rama codex/COL-036-actualizacion-segura desde main, Issue57 in-progress y67 canónica.
Se preserva worktree runtime-oficial y candidato0350f5b4 completo. Usuario autoriza
QA interna/VM oficial/Resolve gratuito, sin GO externo, merge o cambios del host.

Preflight real: virtualización firmware/hipervisor/VBS activos, Hyper-V de gestión
no disponible; consulta de features requiere elevación740.16GB nominales RAM y
aprox5GB libres; disco suficiente. No se habilitó nada ni se reinició. Guía y
script read-only preparados. Resolve no instalado; descarga oficial exige registro
personal del operador. Adobe registrado no acredita activación. Pruebas reales
de Windows limpio/desconexión/editores todavía no ejecutadas.

Diagnóstico: candidato instrumentado privado detiene con código90 antes de copiar
aplicación. Alcanzó Install; WebView2 presente156.0.4314.50 y sin desinstalador en
/S. El2 histórico sigue sin atribución confirmada. No confundir con error Win32 2.
Fixture de descarga NSISdl devuelve success pese al README antiguo. Otro fixture
loopback muestra HTTP plano para URL https (sin ClientHello TLS): defecto de
transporte comprobado, distinto de la causa histórica. No se ejecutó descarga.

Pendiente: reproducir beta2→beta3 directo con traza completa, fallo/recuperación y
datos/prefs; corregir casos medidos y sustituir descarga NSISdl por bootstrapper
Evergreen oficial fijado/firmado si procede. No se ha preparado candidato correctivo
ni se afirma que el2 esté resuelto. Logs/probes privados .lumaforge-local; nunca
publicar exe diagnóstico, rutas crudas o datos existentes. Reanudar aquí leyendo
este checkpoint, git status y las guías QA_WINDOWS11_VM/QA_RESOLVE_BETA3.
