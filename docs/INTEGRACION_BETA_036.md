# Integración y preparación de beta · COL036

31-10-2026. Issue #57; bloqueo de distribución #67; capacidades #81–83.
PR86 fue integrada por **jea27**, a las15:30:46Z, en
`5799531731c41057ae15ed159c25c89725709b55`. No es aceptación de capacidades.
La continuación usa `codex/COL-036-qa-integracion`, en un worktree independiente;
la raíz y el worktree de Creator quedan conservados. No hay merge del agente.

## Auditoría y correcciones acotadas

Revisados los38 archivos de PR86, el motor compartido, protección de entradas/
almacenamiento, flujos de preview/export, preferencias, Planner, workflows y
locks. Sin cambios de dependencias ni de matemática de color en esta entrega.
Los checks finales de PR86 son correctos: MVP41211808381, studio41211808388,
validate41212112840 y sync41215201465. El sync anterior cancelado se recuperó
en41212113424; no se oculta como fallo de código. Revisión humana sigue separada.

| Riesgo encontrado | Corrección/evidencia |
|---|---|
| Un cambio de modo antes del primer GET podía perderse y guardar preferencias por defecto. | Hidratar antes de cambiar, PUTs ordenados y pruebas del módulo real con GET/PUT retrasados y fallidos. |
| Preset, deshacer, importación o borrado podían competir con fit/export. | Guardas de operación y controles deshabilitados, también en biblioteca; comprobación real durante exportación. |
| Regenerar el Planner descartaba diagrama/checklist editados sin preguntar. | Confirmación; cancelar conserva, aceptar reinicia. JSON antes/después de cambiar modos idéntico. |
| El borrado de imágenes no explicaba pérdida de ajustes/plan no guardados. | Aviso explícito y bloqueo mientras hay operación; originales y presets guardados se conservan. |
| El smoke antiguo heredaba PATH/cwd y podía esperar stdout sin límite. | Entorno del hijo limitado a Windows, cwd vacío propio, inicio acotado, validación estricta del puerto y auditoría de módulos cargados. No cambia el entorno del equipo. |

El borrado espera la aceptación del servidor antes de cancelar la preview y
reiniciar el estado local, para conservar la sesión si se rechaza por un lote
activo. El guard del servidor tiene test automatizado; la secuencia concreta
de error concurrente en UI queda pendiente de prueba dedicada. El launcher
de desarrollo desactiva también proxy headers, como el sidecar.
No se añade almacenamiento de proyectos, importación del plan, inferencia de
acabados, vídeo, licencias de pago ni servicios externos.

## Pruebas ejecutadas y límites

- 61 unittest motor/API/harness,128 de seguimiento y6 Node correctos; build Vue/TS
  correcto. Los tests sintéticos son infraestructura, nunca entrevistas ni QA externa.
- Motor congelado construido con las herramientas existentes para **QA interna**,
  usando UI de esta entrega. No se ejecutó el builder NSIS ni se creó release.
- Demo y cuatro fotografías CC0 rurales, hash/original/resolución conservados.
  PNG idéntico entre modos, JSON/preset con óptica, LUT de color, lotes con hashes,
  Planner privado y watchdog correctos. No Python/Node/Cargo/Git encontrados en
  PATH del hijo;71 módulos PE observados proceden del bundle o Windows.
- Cuatro exportaciones JPG con glow0.2/difusión0.1/fade0.1:15.601–16.181s y
  RSS pico muestreado794.1–846.8MB. Una ejecución por foto, no percentil, mejora
  general ni comparación directa con otros perfiles/recetas. No baja resolución.
- Navegador real contra ese mismo congelado: receta descargada byte a byte igual,
  imágenes conservadas, Pro0.05 exposición y acabado0.01; Planner preservado al
  cambiar modos y confirmado al regenerar. PNG descargado;0 warnings/errores.
  Creator/Planner a390×844 sin desbordamiento horizontal; no iPhone físico,
  Safari ni nueva prueba nativa de WebView2.

Evidencia saneada: `evidence/INTEGRACION_036_QA.json` y cuatro capturas reales.
El ejecutable interno conserva la etiqueta0.3.0-beta.2 del código base; el informe
registra hash y archivos fuente exactos de la integración, **no otro candidato
con el mismo número**. No confundirlo con el setup beta2 antiguo. El próximo
setup necesitará versión nueva, manifiesto/hash, avisos y QA de distribución.

## Seguridad, privacidad y fuentes

Se conservan sesión/CSRF, host/origin loopback, CSP local, límites reales de
subida,24MP, decodificación, contención de rutas y rechazo de enlaces/junctions.
Los tests ejercitan entradas inválidas y traversal, lectura/escritura privada,
sesión y preservación; no constituyen sandbox contra otro proceso del mismo
usuario ni una auditoría externa. Importaciones no ejecutan código del JSON.
Fuentes propias/CC0 únicamente; plan sin imagen, EXIF, nombre, ruta o ID del
asset. Los avisos Microsoft/WebView2 siguen siendo específicos del tercero.

Las tres fuentes del Planner vuelven a comprobarse en origen: [manual ARRI SUP5.2,
pp26/43](https://www.arri.com/resource/blob/401824/823cd1114755dc134ff9ee3c98be6e15/alexa-35-sup-5-2-0-user-manual-en-data.pdf),
[ARRI Lighting Handbook](https://www.arri.com/en/learn/lighting/lighting-handbook),
[ASC/Burum](https://theasc.com/article/lighting-a-set/). Sustentan fórmula,
tamaño/calidad de luz y mediciones key/fill. Los contrastes/posiciones elegidos
son recomendaciones propias, no recetas de una película ni parámetros
recuperados. No se redistribuyen manuales, fotogramas ni diagramas ajenos.

## Distribución: NO-GO confirmado, no un fallo oculto

Auditoría nueva de95 PE:44 DLL siguen bloqueadas por procedencia de caché
nativa de herramientas. El gate se conserva. Escaneo de158 archivos y archivos
Python:27 con patrones de rutas de usuario de upstream/ejemplos;0 hallazgos del
perfil local actual,0 patrones de secretos y0 archivos de desarrollo/privados.
Esto no demuestra ausencia de todos los secretos ni aprueba esas rutas o derechos.
No se altera ningún binario para ocultar un resultado; NSIS/plugins/WebView2 no
se han vuelto a empaquetar o certificar. Windows limpio10/11 y editores reales
siguen **NO EJECUTADOS**. Ver `GO_NO_GO_03.md` y la solicitud canónica #67.

### Propuesta concreta para resolver el origen del runtime

La [PSF confirma que3.12.10 fue la última3.12 con instaladores](https://www.python.org/downloads/release/python-31214/).
No se propone volver a3.12.10 para construir con un runtime antiguo. Candidato
de build a evaluar: [CPython3.14.10 oficial Windows64](https://www.python.org/downloads/release/python-31410/),
SHA-256 publicado `92480239264744fe0386a1bd8275786fefa126e3129e56a68e22b52c73329965`.
La consulta a PyPI de los22 pins actuales y PyInstaller6.22.3 encuentra wheels
compatibles con CPython3.14/WindowsAMD64 para los23. Es **solo metadatos**: no
resolución completa, instalación, test, licencia aceptada ni build validado.
URLs, nombres y hashes en `evidence/RUNTIME_036_WHEEL_PLAN.json`.

Autorización pendiente: descargar/verificar ese instalador desde python.org,
comprobar firma PSF y preparar instalación aislada por usuario, en directorio
ignorado del workspace, sin añadir PATH, launcher, asociaciones ni accesos
directos, sin administrador, sin sustituir Python existente. La operación
propuesta, **no ejecutada**, es:

```powershell
.\python-3.14.10-amd64.exe /quiet InstallAllUsers=0 TargetDir="<workspace>\.lumaforge-local\python-3.14.10" PrependPath=0 AppendPath=0 Include_launcher=0 InstallLauncherAllUsers=0 AssociateFiles=0 Shortcuts=0 Include_test=0 Include_doc=0 Include_tcltk=0
```

El instalador puede registrar una instalación por usuario; no se promete cero
registro. Crear después un worktree de build separado con venv propio, fijar
dependencias/avisos y revisar runtime/UCRT/SDK REDIST antes del NSIS. No reutilizar
ni reemplazar la venv compartida. Si no hay wheels/resolución/tests compatibles,
parar y documentar; no actualizar pins automáticamente para forzar el build.
El [embeddable no admite gestionar pip como una instalación normal](https://docs.python.org/3/using/windows.html#the-embeddable-package),
por eso no se usa como atajo. La nueva versión tampoco concede derechos o GO.

## Reproducir y decidir

Comandos desde la rama, con entorno existente preparado:

```powershell
./.venv-mvp/Scripts/python.exe -m unittest discover -s tests_mvp -v
./.venv-mvp/Scripts/python.exe -m unittest discover -s tests -v
npm --prefix apps/web test
npm --prefix apps/web run build
./.venv-mvp/Scripts/python.exe -m PyInstaller --noconfirm --distpath .lumaforge-local/integration-build --workpath .lumaforge-local/integration-work packaging/ColorEngine.spec
./.venv-mvp/Scripts/python.exe scripts/smoke_beta.py --executable .lumaforge-local/integration-build/ColorEngine/ColorEngine.exe
./.venv-mvp/Scripts/python.exe scripts/audit_beta_binary_origins.py .lumaforge-local/integration-work/ColorEngine/Analysis-00.toc .lumaforge-local/integration-build/ColorEngine .lumaforge-local/integration-origins.json
./.venv-mvp/Scripts/python.exe scripts/audit_beta_artifact.py .lumaforge-local/integration-build/ColorEngine .lumaforge-local/integration-payload.json
```

Los dos audits dan salida2 mientras existan los hallazgos; eso es el resultado
esperado del gate, no un éxito de distribución. `--pilot` permite indicar la
carpeta privada de las cuatro fotos autorizadas ya disponibles, sin descargarlas.
Las salidas/datos/logs quedan en `.lumaforge-local/`, nunca como feedback público.

El responsable puede probar ya el código preparado siguiendo
`PRUEBA_CREATOR_PRO_PLANNER.md`. Para distribución debe responder en #67 al
runtime propuesto y aportar operador/entorno Windows10/11 limpio y editor
activado, sin nuevas compras o virtualización implícitas. Cada capacidad mantiene
su aceptación individual; #67 no se cierra por un check ni por integrar una PR.
