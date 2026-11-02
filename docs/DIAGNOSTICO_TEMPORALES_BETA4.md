# COL036 · diagnóstico pendiente de cuatro temporales

No aceptar todavía la conservación global de datos. El operador ha indicado que
no realizó esa limpieza y pide investigar antes de aceptar. La PR90 permanece en
borrador; beta externa y venta continúan NO-GO.

## Hechos comprobados

- La captura inicial contiene9 archivos:6 imágenes temporales,2 presets y
  preferencias. La vista actual contiene5:2 imágenes, los mismos2 presets y las
  mismas preferencias. Los hashes de los5 presentes coinciden. No se publican
  nombres, hashes de esos datos ni rutas privadas.
- Las comparaciones inmediatamente antes/después de las instalaciones,
  actualizaciones, fallos controlados y desinstalaciones registradas fueron
  idénticas. Eso no certifica todo el intervalo entre sesiones.
- No se han encontrado los cuatro nombres en las carpetas de trabajo, copias de
  instalación y vistas de AppData examinadas. No se han restaurado archivos.
- La carpeta actual de imágenes conserva fecha de modificación anterior a la
  primera captura. Ese dato no identifica la causa ni prueba que no hubo borrado.
- Los servidores de desarrollo observados usan el módulo de API en otro worktree;
  su configuración por defecto es local a ese worktree. No se les atribuye el cambio.
- El historial de herramientas examinado no identifica una orden que borre esos
  cuatro archivos. La captura inicial no registró identidad de volumen/directorio;
  falta cerrar su trazabilidad física.
- Consultar metadatos del diario NTFS funciona; leer sus registros devuelve
  **Acceso denegado5**. No se han elevado permisos ni cambiado el diario.

## Una comprobación del operador

Usar una ventana PowerShell independiente de Codex en el worktree de PR90. Para
leer el diario se requiere una consola elevada por el operador; Codex no solicita
contraseña ni realiza esa elevación. La ruta privada exacta se facilita en el chat,
no en GitHub.

```powershell
.\scripts\diagnose_private_store.ps1 -ReadUsn
```

El script compara solo las entradas de la captura privada y lee el diario existente
con `fsutil usn readjournal`. Conserva únicamente las filas cuyos nombres coinciden
con los archivos ausentes (hasta2048, indicando si se trunca). Registra también la
identidad NTFS actual de los directorios para contrastar el contexto fuera de Codex;
no reconstruye la identidad de la captura antigua. No restaura, borra, instala, cambia permisos ni modifica
el diario. Si no tiene elevación, deja esa lectura pendiente. Puede pasarse
`-DataDir` para mantener explícitamente la carpeta original con otra cuenta/contexto.

El resultado se guarda con nombre nuevo bajo `.lumaforge-local/store-diagnosis-…json`;
la consola muestra su ubicación. Compartirlo solo mediante el chat privado. **No
adjuntarlo a una Issue/PR**: incluye metadatos privados y posibles filas del diario.

La ausencia de filas no prueba ausencia de borrado: el diario tiene retención
limitada. Tampoco identifica el proceso responsable. Las filas servirán para
delimitar fecha, motivo e identidad del objeto; después se decidirá el siguiente
paso, sin restauraciones automáticas sobre datos existentes.

## Validación del instrumento

Tests con archivos inertes verifican comparación sin escrituras en el almacén,
informe de ausentes y rechazo de salida externa o sobrescritura. Son pruebas del
instrumento, no resultados de investigación ni aceptación de producto. Windows5.1
ejecutó la comparación local:4 ausentes,0 hashes cambiados. La lectura USN quedó
pendiente de operador elevado.

[Referencia oficial de fsutil usn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-usn).
