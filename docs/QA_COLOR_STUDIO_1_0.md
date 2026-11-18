# Color Studio 1.0.0 · QA de publicación en Windows

El candidato incluye edición local de fotografías SDR, Creator y Pro, Color
Match, glow/difusión/fade manuales, presets, lotes, proyectos locales,
exportación PNG/JPEG/JSON y LUT .cube 33³. Shot Planner propone configuraciones
a partir de referencias y parámetros aportados. En esta versión, vídeo, RAW,
Log y HDR quedan fuera del flujo admitido.

El instalador x64 está identificado por SHA-256 en [el recibo de compilación](evidence/COLOR_STUDIO_1_0_ARTIFACT.json).
El nombre registrado de Windows sigue siendo `Color Studio Beta` para que el
instalador reconozca la instalación anterior. La aplicación muestra Color Studio
1.0. El instalador incluye CPython y las dependencias previstas. Si WebView2 no está
instalado, el bootstrapper oficial requiere red durante la instalación.

## Ejecutar la prueba

Usa la VM aislada `ColorStudio-QA-Win11` y la cuenta de administrador del invitado.
La [guía original de Hyper-V](QA_HYPER_V_BETA7.md) contiene el ciclo beta.3 → beta.5
pendiente y explica cómo conservar los resultados antes de aplicar un checkpoint.

En un estado limpio de la VM, abre **Windows PowerShell como administrador en
el anfitrión** y pega este bloque. Introduce las credenciales del invitado en
el diálogo local.

```powershell
$lfRepo = Join-Path $env:USERPROFILE 'Documents\ChatGPT\Lut generator'
Set-Location -LiteralPath (Join-Path $lfRepo '.codex-worktrees\COL-036-color-studio-1')
.\scripts\qa_vm_assistant.ps1 -KitZip '.lumaforge-local/vm-qa-color-studio-1.zip' -ExpectedSha256 '659f6bc327147cfd3084bdbe82814ba00625abe08d99c1e4f308827e736a8d84' -Run -ConfirmCleanCheckpoint -CleanCandidate
```

El informe debe decir `cycle = clean_candidate`, `kit_version = 1.0.0` y
`technical_automation_passed = true`. El asistente comprueba la instalación,
la reapertura de proyectos, las exportaciones, la red del invitado y la
desinstalación con datos sintéticos. Guarda el informe privado. Para comprobar
la actualización beta.3 → 1.0.0 con el mismo instalador, conserva lo anterior,
aplica el checkpoint manualmente si lo autorizas y ejecuta el mismo bloque
quitando `-CleanCandidate`. Conserva ambos informes.

El [recorrido manual](PRUEBA_CREATOR_PRO_PLANNER.md) comprueba el lanzamiento
nativo, el funcionamiento visual de Creator/Pro y el Planner. Los casos del
[editor externo](QA_EDITORES_03.md) verifican la importación y el dominio sRGB de
la LUT en Resolve. La evaluación estética y los requisitos de licencia y
soporte se revisan por separado.

## Estado de salida

- [#57](https://github.com/jea27/Lut_generator/issues/57) y
  [#67](https://github.com/jea27/Lut_generator/issues/67). Instalación limpia,
  actualización, recuperación y conservación pendientes de resultado real en VM.
  El fallo intermitente previo y las eliminaciones históricas siguen en el
  registro de riesgos.
- [#59](https://github.com/jea27/Lut_generator/issues/59). Compatibilidad externa
  de LUT pendiente hasta que se ejecuten los casos en un editor.
- [#60](https://github.com/jea27/Lut_generator/issues/60),
  [#61](https://github.com/jea27/Lut_generator/issues/61) y
  [#62](https://github.com/jea27/Lut_generator/issues/62). Aceptación de derechos,
  QA externa y decisión comercial pendientes. Project OS sigue en NO-GO.
