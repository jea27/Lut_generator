# Beta.3 → beta.5 · asistente para la VM existente

05-11-2026. Solo QA interna, con imágenes generadas. Beta externa y venta NO-GO.
VM indicada por el operador: `ColorStudio-QA-Win11`. No se crean ni restauran
checkpoints. Una entrada del gestor acredita su existencia, no la limpieza de su
contenido: el operador debe confirmar que el guest tiene actualmente el estado
limpio adecuado. La comprobación posterior exige que no haya App/Data de ensayo.

## Tres pasos del operador

1. Guarda tu trabajo, abre Hyper-V y comprueba que la VM indicada está arrancada
   con el estado limpio previsto. No arranques otra VM ni cambies sus recursos.
   Si necesitas restaurar un checkpoint, decide y realiza esa operación tú; el
   asistente nunca lo hace. No actives carpetas compartidas.
2. Abre **PowerShell como administrador en el host**, entra en el worktree de
   PR90 y ejecuta estos comandos. El recibo y ZIP se generan con esta entrega:

```powershell
$qa = Get-Content .lumaforge-local/closure-20261105/kit-receipt.json -Raw | ConvertFrom-Json
./scripts/qa_vm_assistant.ps1 -KitZip .lumaforge-local/vm-qa-beta5-cycle-20261106.zip -ExpectedSha256 $qa.kit_zip_sha256 -Run -ConfirmCleanCheckpoint
```

   Elige el ID del checkpoint limpio que muestra la lista. Introduce las
   credenciales **de la VM** únicamente en el diálogo local que aparece. No las
   envíes a Codex ni GitHub. `-ConfirmCleanCheckpoint` es tu declaración del estado
   actual; no aplica/restaura el checkpoint ni certifica su contenido por nombre.
3. Deja que termine y conserva los informes privados. Si falla, no borres datos,
   no reinstales para sustituir una actualización fallida y no repitas sobre el
   mismo estado sin revisar el informe. Si una política/SmartScreen lo bloquea,
   registra BLOCKED; no se modifica la política ni se eluden protecciones.

Puedes ejecutar el comando sin `-Run -ConfirmCleanCheckpoint` para consultar
únicamente la VM y sus checkpoints; no pide credenciales ni ejecuta código guest.
La sesión actual de Codex no puede consultar Get-VM y no tiene credenciales del
guest; por ello **todavía no se ha ejecutado el ciclo dentro de Hyper-V**.

## Qué automatiza

- SHA del ZIP, miembros declarados, hashes, rutas, VM exacta/ID y BIOS UUID del
  host frente al SMBIOS del guest. Windows11 cliente Hyper-V y contexto de pruebas.
- Copia únicamente el kit verificado mediante PowerShell Direct, sin carpetas
  compartidas, WinRM de red, cuentas nuevas o credenciales guardadas.
- Instala beta.3; verifica todo el runtime contra manifiestos fijados antes de
  ejecutarlo. Crea imágenes/presets/receta sintéticos por HTTP y guarda un baseline
  de hashes ligado al volumen y directorio NTFS.
- Provoca un fallo controlado de actualización manteniendo un handle de directorio
  sin permiso de compartir borrado. Exige código2, fase `directory_switch_failed`
  y error Win325/32 en los logs nuevos. Comprueba que siguen beta.3 y los datos.
- Libera el handle, actualiza directamente a beta.5 y verifica los mismos datos,
  sin desinstalar. Prueba API de Creator/Pro, reinicio, PNG/preview a igual tamaño,
  receta, presets, LUT color-only y Planner con fuentes/incertidumbre.
- Solicita cancelar un lote real. Si termina antes, registra NOT_EXERCISED y el
  ciclo no pasa. Los fixtures de interrupción son una evidencia distinta de una
  cancelación del NSIS o un corte de alimentación; ninguna omisión cuenta como PASS.
- Deshabilita los adaptadores **del guest verificado**, repite el flujo local y
  los vuelve a habilitar en finally. PowerShell Direct no depende de esa red.
  No cambia adaptadores del host, firewall, antivirus, VBS o SmartScreen.
- Verifica el desinstalador por hash; desinstala y comprueba conservación de datos.

## Qué queda fuera del resultado automático

El informe `technical_automation_passed` solo describe esos casos ejecutados.
La revisión visual de la UI, arranque desde Inicio, accesos directos, licencia de
Windows, Process Monitor y LUT en Resolve/Adobe quedan pendientes por separado.
No establece aceptación humana ni GO. Si el hash real del desinstalador difiere,
se detiene antes de ejecutarlo; su compatibilidad se comprobará en el guest.

Después de un ciclo completo correcto puedes probar la UI en la VM mediante
`Kit/qa_guest_checks.ps1 -Install -Launch`, siguiendo [la guía manual](PRUEBA_CREATOR_PRO_PLANNER.md).
Esta instalación posterior es exclusivamente para revisar la interfaz; no se usa
como evidencia de actualización. Copia los resultados por el canal privado acordado.
La captura [Procmon](QA_BETA5_INTERNA.md) y [Resolve](QA_RESOLVE_BETA3.md) siguen
sus protocolos. Nunca adjuntes PML/CSV, UUID, rutas o informes crudos a GitHub.

Los logs/resultados quedan en `C:\LF-QA\Reports` dentro del guest y el resumen
se copia a una carpeta nueva `.lumaforge-local/vm-assistant-*` del host. Se
conservan todos los datos sintéticos y logs; no hay limpieza al terminar. Si la
conexión se interrumpe, inspecciona primero el guest y sus procesos: no supongas
que la instalación se detuvo ni restaures un checkpoint por automatismo.

Mecanismo oficial: [PowerShell Direct de Microsoft](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/powershell-direct).
Requiere acceso administrativo Hyper-V y credenciales válidas del guest. La
identidad usa [UUID SMBIOS](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-computersystemproduct);
los identificadores se conservan exclusivamente en el informe privado.


## Contención adicional · 6 noviembre

Antes de copiar el kit y antes de instalar, el asistente y el ciclo rechazan un
perfil con almacén predeterminado existente, directorios de instalación conocidos
o registro de desinstalación de Color Studio Beta. Se comprueban HKCU/HKLM en
ambas vistas32/64 solo en lectura. Un error al leer registro también bloquea.
No se ejecuta el desinstalador previo para limpiar el perfil ni se restauran
checkpoints automáticamente. El operador debe elegir un estado realmente vacío.
Esto evita que el instalador legado encuentre otra instalación registrada fuera
de la carpeta sintética. Es una protección preventiva; no atribuye el incidente
histórico al instalador. Los kits del5 de noviembre se conservan como históricos;
utilizar el nuevo kit del6 de noviembre con ambas guardas.
