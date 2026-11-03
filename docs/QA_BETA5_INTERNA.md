# Beta.5 · prueba privada en Windows11 limpio

**Solo QA interna. No release, beta externa ni venta autorizadas.** Causa histórica
no atribuida. El kit solo contiene instaladores propios verificados, herramientas
de QA, fuentes antiguas fijadas y dos PNG/receta sintéticos. No contiene las copias
privadas, diagnósticos del incidente, secretos ni fotografías personales.

## Preparar el entorno

Usar una VM Windows11 x64 nueva, ISO Microsoft y licencia/evaluación válida;
ver [preparación de VM](QA_WINDOWS11_VM.md). No cambiar el Windows principal.
Preflight03-11: gestor ausente y3,41GiB libres; no hay prueba limpia ejecutada.
El operador prepara el guest y libera recursos; no desactivar VBS/SmartScreen.
Transferir el ZIP privado, cotejar su SHA con el recibo facilitado y extraerlo
dentro del guest en `C:\LF-QA\Kit`. No mapear carpetas personales del host.

Abrir PowerShell **dentro del guest** y entrar en `C:\LF-QA\Kit`. Los scripts
rechazan el host físico, rutas enlazadas y hashes distintos. Si una política o
protección bloquea scripts/instalador, registrar BLOCKED y conservar el error;
no usar ExecutionPolicy Bypass ni ignorar SmartScreen para hacer pasar la prueba.

```powershell
./qa_guest_checks.ps1
./qa_guest_checks.ps1 -Install -RunFixtures -Launch
```

El segundo comando instala únicamente en `C:\LF-QA\App`, verifica bytes instalados,
ejecuta fixtures en carpetas nuevas y abre la app con datos en `C:\LF-QA\Data`.
Para ejecutar los3 symlinks se necesita una consola con el privilegio disponible
en el guest; las omisiones son BLOCKED, no PASS. No habilitar Developer Mode del host.
No hace falta instalar Python, Node, Git ni C++: se usa el intérprete aislado del
programa. Preflight y logs quedan en `Kit\private`; no prueban por sí solos Windows
limpio, aceptación humana ni entrega de notificaciones.

## Flujo de producto y conservación

1. Importar `Kit\inputs\source.png` y `reference.png`. Son gradientes sintéticos,
   no fotografías reales ni evidencia de calidad visual/comercial.
2. Analizar Color Match. Crear dos presets de ensayo, editar uno y guardar receta.
   Cambiar Creator → Pro → Creator: conservar imagen, receta y ajustes.
3. Aplicar glow/difusión/fade manuales; exportar PNG/JPG, receta JSON y LUT33³.
   Guardar las exportaciones en `C:\LF-QA\Exports`, fuera de la instalación.
   La LUT solo contiene color; no comparar su acabado espacial como si lo incluyera.
4. En Pro, generar Shot Planner: distinguir observaciones/estimaciones/recomendaciones,
   mover el diagrama y exportar JSON. No aceptar sus propuestas como rodaje reconstruido.
5. Cerrar la app. Snapshot antes de cada actualización/desinstalación:

```powershell
./qa_windows_preservation.ps1 -Mode Snapshot -DataDirectory C:\LF-QA\Data -Baseline .\private\before-update.json
./qa_guest_checks.ps1 -Install
./qa_windows_preservation.ps1 -Mode Verify -DataDirectory C:\LF-QA\Data -Baseline .\private\before-update.json -Report .\private\after-update.json
```

El mismo candidato comprueba reinstalación, **no** sustituye actualizar desde una
versión anterior. Para beta3→beta5 volver al checkpoint limpio; si el kit incluye
`previous.exe`, ejecutar `-InstallPrevious`, abrir la versión anterior con
`$env:LUMAFORGE_DATA_DIR='C:\LF-QA\Data'` y su exe en `App`, crear datos y cerrar.
Después Snapshot → `-Install` → Verify. Conservar la identidad NTFS y todos los hashes.
No desinstalar/reinstalar para declarar que pasó una actualización fallida.
Hacer también Snapshot/Verify separados de `Exports` para las recetas descargadas.

El fixture de bloqueo Win32 y el de destino sustituto ejercitan recuperación con
datos inertes. Para un fallo del instalador completo, conservar exit code y logs
de `ColorStudioInstallerLogs` del guest: no equiparar el fixture al NSIS completo.
Si aparece un destino ajeno, conservarlo junto a backup/diario; no borrarlo por script.

## Captura nativa privada

Usar [Process Monitor oficial](https://learn.microsoft.com/sysinternals/downloads/procmon)
en el guest. El operador acepta su EULA y elevación; no usar /AcceptEula.
ZIP4.12 fijado en `INCIDENT_036_TOOL_PREP.json`; si cambia el hash, detenerse.
Antes de grabar: filtro **Path begins with `C:\LF-QA\` → Include**, sin otras
Include, y Filter → Drop Filtered Events. Capturar solo estos fixtures/instalaciones.

```powershell
./qa_guest_checks.ps1 -RunProbes
```

Los4 probes comparan fuentes antiguas fijadas con el código instalado:6PNG borrados
antes/ninguno después; .part preexistente borrado antes/conservado después.
El modo directo no valida transporte HTTP ni autenticación; las pruebas API cubren
esa parte por separado. Grabar además instalación/actualización y acciones GUI con
las entradas sintéticas. Detener y guardar PML y CSV privados. Correlacionar PID,
imagen del proceso, hora, ruta sintética, resultado y operación de borrado. No subir
trazas/capturas completas a GitHub. No atribuye los4 eventos históricos.

## Sin conexión, desinstalación y Resolve

Tras instalar WebView2 cuando proceda, desconectar **solo el adaptador virtual**;
registrar su estado y repetir el flujo completo. No marcar offline por un flag
del programa. WebView2 Evergreen puede necesitar Internet si falta al instalar;
el procesamiento local no debe necesitarlo. No tocar las protecciones del host.

Cerrar la app, guardar un baseline nuevo y desinstalar desde Aplicaciones del guest.
Verificar que Data/Exports conservan identidad y hashes; registrar residuos y estado
de accesos directos. No limpiar datos para ocultar un fallo de desinstalación.

Para Resolve gratuito oficial usar [E01–E05](QA_RESOLVE_BETA3.md); registrar versión,
gestión de color, interpolación y exports reales. No declarar compatibilidad por
crear un .cube o por probar un comparador sintético. Photoshop/Premiere pendientes.

Resultado por caso: PASS / FAIL / BLOCKED / NOT_RUN, esperado, observado, hash de
candidato, Windows y fecha. Enviar los informes por canal privado; en GitHub solo
resumen saneado. Las validaciones de Windows/Procmon/editores siguen NOT_RUN hasta
ejecutarse. Aceptación y autorización de distribución se solicitan por separado.
