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

## Próxima evidencia: auditoría existente y, si procede, Process Monitor

El operador puede consultar únicamente los eventos Security ya existentes con
[collect_private_event_evidence.ps1](../../scripts/collect_private_event_evidence.ps1).
Necesita su consola elevada fuera de Codex; no cambia permisos ni activa auditoría.
Usa la hora local exacta comunicada por el chat. Filtra nombres de la instantánea
privada y candidatos a correlación por handle/PID dentro de seis minutos. Un evento
4660 sin ObjectName se conserva solo como candidato asociado; no atribuye por sí
solo la causa. Una ausencia de eventos no demuestra ausencia de borrado.

```powershell
.\scripts\collect_private_event_evidence.ps1 -IncidentLocalTime 'AAAA-MM-DDTHH:mm:ss'
```

El informe se comparte solo por chat privado; nunca en Issues, PR ni Pages.
No repetir ReadUsn ni restaurar archivos mientras se investiga. El código de
contención en la rama no protege automáticamente procesos/versiones ya abiertos.

No se ha localizado ni ejecutado Process Monitor en esta sesión. Si hace falta observar
el proceso y la pila nativos de una nueva reproducción:

1. El operador obtiene [Process Monitor oficial](https://learn.microsoft.com/sysinternals/downloads/procmon),
   verifica firma Microsoft, lee los términos y gestiona la elevación/controlador.
   Codex no instala ni carga el controlador, ni cambia protecciones.
2. Detener la captura, limpiar solo la vista de Procmon y configurar Include por
   ruta que comience por el workspace + `.lumaforge-local\data-incident-repro-`.
   Excluir actividad ajena al fixture de la captura guardada. Guardar el PML solo
   dentro de la carpeta privada. No filtrar únicamente por nombre del proceso:
   se busca también un posible proceso externo que toque el fixture.
3. Iniciar captura y ejecutar desde este worktree, con el Python de QA existente:

   ```powershell
   & ../../.venv-mvp/Scripts/python.exe -B scripts/reproduce_private_deletion.py --mode legacy --probe images
   & ../../.venv-mvp/Scripts/python.exe -B scripts/reproduce_private_deletion.py --mode contained --probe images
   & ../../.venv-mvp/Scripts/python.exe -B scripts/reproduce_private_deletion.py --mode legacy --probe batch-part
   & ../../.venv-mvp/Scripts/python.exe -B scripts/reproduce_private_deletion.py --mode contained --probe batch-part
   ```

4. Detener captura. Correlacionar ruta sintética, PID, imagen/command line del proceso,
   tiempo y operaciones CreateFile/SetDispositionInformationFile/CloseFile, resultado
   y stack disponible. Conservar PML y CSV privados; publicar solo un resumen saneado.
5. Esto verifica una reproducción nueva; no convierte una operación similar en
   atribución de los eventos históricos. No probar instaladores/desinstaladores
   nativos del producto en el host: hacerlo después en VM aislada autorizada.

## Hipótesis pendientes y decisión

Una llamada al DELETE antiguo, otra herramienta/proceso o una limpieza exterior
podrían explicar los cuatro PNG. No existe prueba de cuál ocurrió. Para los otros
cuatro ausentes de la vista externa, la existencia de copias en otro contexto es
evidencia separada; no se afirma un borrado adicional ni una migración demostrada.
La revisión de código y las reproducciones reducen riesgos futuros, no cierran
el incidente ni autorizan distribución. PR90 sigue en borrador y no se aprueba nada.

Fuentes primarias: [estructura y límites del USN](https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ns-winioctl-usn_record_v2),
[semántica del diario](https://learn.microsoft.com/en-us/windows/win32/fileio/change-journal-records),
[Process Monitor](https://learn.microsoft.com/sysinternals/downloads/procmon).
