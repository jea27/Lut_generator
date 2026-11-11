# Color Studio · QA final en Hyper-V

**Ejecuta primero beta.3 → beta.5. Después, con tu consentimiento para aplicar
el checkpoint limpio, instala beta.7 directamente desde ese estado.**
Utiliza la VM `ColorStudio-QA-Win11` y la cuenta de administrador del invitado.
El asistente comprueba la identidad del invitado antes de copiar el kit mediante
PowerShell Direct. La transferencia es puntual y los instaladores se ejecutan
dentro de la VM. [Requisitos de PowerShell Direct](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/powershell-direct)

## 1. Actualización de beta.3 a beta.5

En el **Windows anfitrión**, arranca la VM desde el estado limpio acordado.
Identifica el checkpoint anterior a Color Studio. Abre **Windows PowerShell
como administrador** en el anfitrión y pega el bloque completo.

```powershell
$lfRepo = Join-Path $env:USERPROFILE 'Documents\ChatGPT\Lut generator'
$lfQA5 = Join-Path $lfRepo '.codex-worktrees\COL-036-actualizacion-segura'
$lfQA7 = Join-Path $lfRepo '.codex-worktrees\COL-036-verificacion-integrada'

Set-Location -LiteralPath $lfQA5
.\scripts\qa_vm_assistant.ps1 -KitZip '.lumaforge-local/vm-qa-beta5-cycle-20261106.zip' -ExpectedSha256 '798dd0603f97d716d19424d6102ddcf242dcb4c732a1a4ab7dccddad3deca6ac' -Run -ConfirmCleanCheckpoint
```

Pega el ID del checkpoint limpio que muestra la lista. En el diálogo local,
escribe las credenciales del **invitado**. El ID vincula el informe al punto
de control y la opción `-ConfirmCleanCheckpoint` expresa que ya comprobaste el
estado de partida. El asistente no aplica checkpoints.

**Resultado esperado.** Instala beta.3, guarda imágenes sintéticas, presets
y preferencias, y toma un inventario con SHA-256 y la identidad del directorio
NTFS. Con un handle de directorio abierto, la actualización debe devolver
código 2 con la fase `directory_switch_failed` y preservar beta.3 y los datos.
Tras liberar el handle, la actualización directa debe terminar en beta.5 con
los mismos hashes. Luego se prueban la API, cancelación, recuperación con
fixtures, desconexión de adaptadores del invitado y desinstalación conservando
datos.

## 2. Instalación limpia de beta.7

Espera a que termine el primer ciclo. Conserva el informe y los logs **antes**
de volver al checkpoint. Si el ciclo falla o la copia falla, detente aquí para
revisar el resultado. Cuando quieras autorizar el segundo ciclo, aplica tú el
checkpoint limpio de esa VM en el Administrador de Hyper-V. Confirma que
corresponde a la VM indicada y que quieres sustituir el estado de prueba actual.
Arranca de nuevo la VM. En la misma ventana elevada del anfitrión, pega esto.

```powershell
Set-Location -LiteralPath $lfQA7
.\scripts\qa_vm_assistant.ps1 -KitZip '.lumaforge-local/vm-qa-beta7-clean-r2.zip' -ExpectedSha256 'ba6a86baa2607ed68cab3b18d274e5dcc6eed5a7c4850ede17494515e9d5b89b' -Run -ConfirmCleanCheckpoint -CleanCandidate
```

**Resultado esperado.** El informe indica `cycle = clean_candidate` y
`clean_candidate_install = PASS`. El asistente instala beta.7 sin beta.3
previa, verifica el runtime y ejecuta las pruebas sin un Python, Node, Git o
Cargo instalado en el invitado. Comprueba exportaciones PNG y LUT, Shot
Planner, presets, receta, proyecto Pro y comparador. Reabre el mismo
proyecto en otro proceso, compara los píxeles y verifica los hashes del
almacén antes y después. Luego prueba cancelación, recuperación, desconexión
real y desinstalación con los datos sintéticos intactos.

El kit también permite medir la actualización directa beta.3 → beta.7 en un
**tercer ciclo opcional**. Requiere conservar antes los informes, decidir de
nuevo si aplicar el checkpoint y repetir el segundo comando sin
`-CleanCandidate`. Es evidencia independiente de la instalación limpia.

## 3. Revisar los resultados

- El asistente intenta copiar la carpeta de resultados sintéticos a
  `.lumaforge-local/vm-assistant-…` en el anfitrión. Confirma que contiene
  `report.json` y los logs del ciclo. Si la copia falla, los originales están
  en `C:\LF-QA\Reports` **dentro de la VM**. Consérvalos antes de aplicar un
  checkpoint. Los informes completos quedan privados.
- Comunica `beta.5 PASS` o `beta.7 limpia PASS` solo si el informe de ese
  ciclo dice `technical_automation_passed: true`. Si no, comunica
  `FAIL` o `BLOCKED` y el nombre del paso. Los pasos de actualización que
  quedan `NOT_RUN` en el ciclo limpio son esperados.
- Si hay un fallo inesperado de actualización, conserva `report.json`,
  `failure-private.txt` y `native-installer-*.log`. El código 2 provocado es
  una prueba de contención. La causa del fallo intermitente anterior y el
  proceso de las eliminaciones históricas siguen pendientes de atribución.
- El ensayo de desconexión necesita un adaptador del invitado inicialmente
  activo. PowerShell Direct conserva el canal de control. Si el informe
  indica `network_restore_failed`, comprueba la red del invitado antes de
  repetir. Si el instalador o SmartScreen bloquean la prueba, anota el mensaje
  y deja las protecciones activas.

## 4. Interfaz y LUT en DaVinci Resolve

Después del ciclo limpio, puedes reinstalar beta.7 **dentro del invitado** para
revisar la interfaz. Es una prueba separada. Abre PowerShell dentro de la VM
y ejecuta `C:\LF-QA\Kit\qa_guest_checks.ps1 -Install -Launch`. Sigue el
[recorrido de Creator, Pro y Shot Planner](PRUEBA_CREATOR_PRO_PLANNER.md) con
las imágenes de `C:\LF-QA\Kit\inputs`. Guarda un proyecto, alterna los modos,
cierra la aplicación y reabre el proyecto. Comprueba receta, comparador y
exportación antes de registrar tu aceptación de cada función.

La carpeta `candidate` del informe beta.7 contiene `source.png`,
`identity.cube`, `look.cube` y `output-color-only.png`. Usa esos cuatro
archivos en un proyecto **nuevo** de DaVinci Resolve. Registra versión, dominio
sRGB y niveles completos. Aplica primero identidad y compara con `source.png`.
Luego aplica `look.cube` con interpolación trilineal y compara con
`output-color-only.png`, a la misma resolución y sin otras transformaciones.
Si Resolve no está instalado o no inicia en el invitado, registra
`BLOCKED`. La compatibilidad del editor se puede probar por separado en un
equipo con Resolve operativo. [Casos de precisión LUT](QA_EDITORES_03.md)

## Integración y aceptación

GitHub registra #92–95 integradas en la rama de #90. Verifica cada entrega
antes de decidir si #90 puede entrar en `main`.

| Orden | Entrega | Evidencia requerida |
|---|---|---|
| 1 | [#90](https://github.com/jea27/Lut_generator/pull/90) · Contención | Actualización y fallo controlado preservan hashes. Instalación limpia, desconexión y desinstalación ejecutadas en el invitado. Revisar riesgo residual. |
| 2 | [#95](https://github.com/jea27/Lut_generator/pull/95) · Creator | Dos aperturas separadas reutilizan los recursos de la demo. Importación normal y exportación funcionan en la interfaz. |
| 3 | [#92](https://github.com/jea27/Lut_generator/pull/92) · Pro | Un proyecto reabierto conserva imágenes, receta, controles, comparador y píxeles exportados. |
| 4 | [#93](https://github.com/jea27/Lut_generator/pull/93) · LUT | Píxeles equivalentes en el benchmark, tiempo y memoria revisados. Importación real en Resolve pendiente hasta ejecutar los casos. |
| 5 | [#94](https://github.com/jea27/Lut_generator/pull/94) · Planner | Valores reproducibles con parámetros conocidos y supuestos visibles. Exportación JSON separa medidas de estimaciones. |

Los SHA-256 de los instaladores comprobados son los siguientes.

| Instalador | SHA-256 |
|---|---|
| beta.3 | `0350f5b44be2850f828a148debc4174b8f134953b080d895bbbca8620576b5cd` |
| beta.5 | `789983ea5c8e71b92271b91e2fc7a76ad6d6fef3272ac5ac24d96ac4c308bb69` |
| beta.7 | `bea167cb7135866b3d96402457a6898a4b6427b0ab7fae3b28d54cb449d196e1` |

**Beta externa y venta siguen en NO-GO.** El ciclo automático registra pruebas
técnicas. El responsable revisa por separado la interfaz, los resultados
visuales, el riesgo residual y cualquier distribución.
