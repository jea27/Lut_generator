Estado de estabilización: ver ESTABILIZACION_03.md y GO_NO_GO_03.md. Microsoft WebView2 tiene diagnósticos/actualizaciones propios; «sin telemetría» se limita al código de LumaForge. El setup beta2 existente todavía contiene el texto anterior. No hay candidato nuevo ni autorización externa.

> Vigente:0.3.0-beta.2 desde a452a5f (clean),266211731 bytes.
> SHA256 3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f.
> Corrige feedback nativo y migración UI de presets v1. NOTAS beta1 conservadas
> debajo como historial. Sin firma/release, NO-GO distribución externa/venta.
> Hashes y auditoría ampliada en LOOK_03_ARTIFACT_B2/NSIS/VENDOR_INPUTS.json.

# Candidato vigente0.3.0-beta.1 · 31-10-2026

Instalador exacto Color Studio Beta_0.3.0-beta.1_x64-setup.exe (266203035 bytes).
SHA256 ae47f44e6f9382810e20a7a98b0b46bf6d53411e7f1c8b0fb2e9c7acf595ac21.
Build desde396a508, dirty=false. No firmado, distribución bloqueada por QA y
payload pendiente. Conservado0.2 como referencia histórica, no recomendado
para distribuir por rutas de compilación. Ver BETA_03_AUDITORIA.md.

Primeros pasos: instalar→demo o dos fotos autorizadas→Color Match→ajustes→
activar Look Match y ajustar glow/difusión/fade→guardar preset/JSONv2→PNG/JPG.
El acabado es manual experimental y tiene bypass/intensidad independientes.
LUT .cube solo color, confirmación explícita al exportar; no conserva acabado.
Feedback incluido desde ayuda o /feedback/: JSON local por canal privado,
sin fotos/telemetría. Guardar presets antes de salir. No hay cuentas ni pagos.

Procedimiento limpio, cinco recorridos y paquete de LUT lossless:
BETA_QA_EXTERNA.md. Demo CC0 ya incorporada con créditos. Fotos privadas nunca
se adjuntan a Issues. Los detalles siguientes conservan la guía0.2; los límites
JPG/PNG8/24MP/32MiB y custodia de datos siguen vigentes.

---

# Color Studio 0.2.0-beta.1 · Windows

Nombre provisional. Candidato técnico sin firma, no licencia comercial ni
validación de P0. El dashboard de Pages se conserva y no aloja este editor.

## Usar el instalador candidato

Artefacto local: apps/desktop/src-tauri/target/release/bundle/nsis/
Color Studio Beta_0.2.0-beta.1_x64-setup.exe. Comparar SHA256 con el informe
evidence/BETA_02_ARTIFACT.json. No sustituir un instalador por el mismo nombre
sin revisar su hash. No hay enlace público ni Release creada en esta entrega.

1. Ejecutar el setup por usuario en Windows x64 con permiso del titular.
2. Abrir Color Studio Beta desde el menú Inicio. No se requiere Python/Node,
   terminal ni configurar puertos. NSIS incorpora WebView2 offline; si ya existe
   una versión válida, utiliza esa instalación. No desactivar SmartScreen.
3. Elegir ES/EN en bienvenida; probar demo local CC0 o importar referencia y
   fotografía propia autorizada (JPG/PNG8, máximo24MP y32MiB).
4. Analizar, comparar con el deslizador, afinar intensidad/exposición/contraste/
   saturación/temperatura. Guardar preset antes de cerrar. Intensidad0 desactiva
   todo el look sobre RGB normalizado, no promete los mismos bytes JPEG/EXIF.
5. Biblioteca: aplicar, editar nombre/grupo/receta actual, eliminar confirmado.
   Receta JSON permite portabilidad. El editor no restaura la selección de fotos
   ni el historial undo/redo después de cerrar; presets y preferencias sí.
6. Lotes: seleccionar hasta16 imágenes, usar receta global actual, elegir PNG/JPG,
   iniciar y descargar resultados. Cancelar conserva archivos ya terminados.
   Cierre inesperado marca interrupted al volver; iniciar nuevo lote, no se
   afirma reanudación automática. Eliminar copias temporales solo cuando no haya
   lote activo. Las fotos originales no se modifican.

Datos privados persistentes: %LOCALAPPDATA%/ColorStudioBetaData/{images,presets,
jobs}, preferences.json. Desinstalar quita binarios/atajos y conserva esos datos
para evitar pérdidas. No publicar esa carpeta. La eliminación manual completa
requiere respaldo y elección del usuario, no la ejecuta el agente.

## Seguridad y procesos

El ejecutable Tauri lanza ColorEngine con PID padre. El sidecar reserva su socket
127.0.0.1:puerto dinámico y sirve frontend+API en el mismo origen. Cierre normal:
kill/wait del hijo; padre desaparecido: watchdog con límite adicional3s. Una
instancia por sesión evita escritores simultáneos/cookies compartidas de host.
El puerto no se persiste; un reinicio establece sesión nueva.

Cookie HttpOnly/SameSiteStrict, token aleatorio en memoria para mutaciones,
comprobación Host/Origin/Sec-Fetch-Site, sin CORS permisivo. APIs privadas GET
también requieren sesión y origen. El bootstrap de sesión solo sirve el mismo
origen; la UI puede renovarla tras reinicio. No se envía el secreto por stdout,
URLs o archivos. Defensa frente a páginas web ajenas, **no** aislamiento contra
otros procesos del mismo usuario, malware o extensiones con acceso privilegiado.
El HTTP loopback no cifra entre procesos locales. No hay cuentas, telemetría propia,
actualizador automático, pagos ni APIs externas de imagen.

No hay actualización silenciosa/rollback transaccional: revisión e instalación
manual de versión conocida por ahora; datos separados de binarios. Antes de
automatizar, hacen falta artefactos/metadatos firmados, compatibilidad de esquema,
respaldo y recuperación comprobada. Reinstalar no aprueba calidad ni tarea.

## Compilar de nuevo

Fuentes oficiales: [Tauri requisitos Windows](https://v2.tauri.app/start/prerequisites/),
[NSIS/WebView2](https://v2.tauri.app/distribute/windows-installer/),
[sidecars](https://v2.tauri.app/develop/sidecar/) y
[PyInstaller](https://pyinstaller.org/en/stable/usage.html). Herramientas ya
instaladas con aprobación; no reinstalar por no estar en PATH.

```powershell
./.venv-mvp/Scripts/python.exe -m pip install -r requirements-mvp.txt -r requirements-build.txt
npm ci --prefix apps/web
./scripts/build_beta.ps1
```

El builder agrega Cargo al PATH solo para su proceso, verifica tests/build,
congela sidecar onedir, copia staging marcado y compila NSIS. No borrar un staging
ajeno sin marca. Usa bloqueos Cargo/npm y versiones pip, Rust1.99.1. VS/MSVC/SDK,
WebView2 y NSIS dependen de inputs del equipo; conservar versiones y hashes.
No garantiza reproducibilidad bit a bit. Licencias en packaging/notices se
generan de paquetes locales; revisar diferencias al cambiar cualquier dependencia.
FFmpeg se excluye: no hay procesamiento de vídeo. Workflow manual
beta-candidate compila un artefacto7d, no publica Releases ni vende el programa.

## QA reproducible y límites

```powershell
./.venv-mvp/Scripts/python.exe -m unittest discover -s tests_mvp -v
./.venv-mvp/Scripts/python.exe -m unittest discover -s tests -v
./.venv-mvp/Scripts/python.exe scripts/smoke_beta.py
```

El smoke requiere el piloto CC0 local y genera carpeta privada nueva; comprueba
el ejecutable empaquetado, exports, lotes, hashes de originales y watchdog.
No descarga imágenes ni prueba Photoshop, piel o un Windows limpio. Consultar
evidence/BETA_02_QA.md. No repetir mediciones sin cambios que lo justifiquen.

Plan pendiente limpio: máquina virtual nueva con Windows10/11 x64, sin Python,
Node, Rust ni VS; snapshots previos, usuario estándar, con/sin WebView2; instalar,
primera ejecución/demo/export/PRNG sesión, reiniciar, cerrar normal/forzado y
desinstalar. Comprobar menú Inicio, procesos/puertos, ICC, originales, presets y
datos conservados; guardar versiones/hash/resultados. No hay VM preparada ni
autorización para habilitar funciones Windows; no declarar esta prueba hecha.

## LUT y editores externos

.cube33³, dominio0..1 **sRGB codificado D65/SDR**, orden rojo más rápido; no
convierte Log/HDR ni describe gestión de color del editor. Receta global aplicada
por interpolación trilineal. PNG/JPG sRGB normalizado; alpha se conserva en PNG,
JPEG compone blanco. Conversiones ICC/EXIF y8bits documentadas en el MVP.

Photoshop: abrir copia autorizada como sRGB, Capa > Nueva capa de ajuste >
Consulta de colores, cargar archivo3DLUT .cube. Contrastar sin otros ajustes,
misma gestión de color y dithering documentado. [Procedimiento Adobe](https://www.adobe.com/learn/photoshop/web/edit-photo-color-lookup-adjustment).
Premiere: clip SDR correctamente interpretado, Lumetri Color > LUT creativa
con Browse, intensidad100, sin dobles conversiones/ajustes; registrar gestión
del proyecto y color de secuencia. Es un procedimiento por comprobar, no evidencia.
Resolve no está instalado; no se afirma compatibilidad. Photoshop2026 pide
inicio de sesión Adobe en este equipo: detener importación hasta sesión humana.
No se publican capturas de autenticación ni identificadores del equipo.
