# Runtime Windows embebido · COL-036 / #57 / #67

01-11-2026. Preparación autorizada para un **candidato interno**, sin permiso de
beta externa, venta, merge o aceptación de capacidades. PR88 fue integrada por
jea27 en05b4983; esta continuación conserva sus cambios.

## Qué se redistribuye y de dónde viene

`packaging/runtime.lock.json` fija CPython3.14.10 WindowsAMD64 embeddable,
su SHA-256 publicado por la PSF y19 wheels de PyPI con URL/versión/hash.
El cierre de dependencias se verifica también contra METADATA/RECORD de los
archivos descargados. No se instala pip en el embeddable ni se obtiene una
DLL de System32, Python personal o aplicaciones del equipo.

El bundle conserva los binarios originales de ZIP/wheels y sus avisos. El
builder rechaza archivos alterados, traversal, enlaces, colisiones Windows,
arquitecturas distintas y dependencias nativas no incluidas/no reconocidas
como componentes del SO. Solo entran las dos fotos CC0 declaradas por hash en
`apps/demo/credits.json`; un archivo adicional hace fallar el build.

| Componente | Evidencia/condiciones |
|---|---|
| CPython oficial | ZIP, hash, firmas PSF requeridas y LICENSE.txt completo, incluidos subcomponentes. No se cambia el binario. |
| NumPy/OpenBLAS y otras bibliotecas nativas de wheels | RECORD, hashes de cada archivo, arquitectura/importaciones y textos de terceros del wheel. Una licencia de paquete no sustituye las de sus componentes. |
| Visual C++ incluido por PSF/NumPy | Binarios Microsoft originales con firmas requeridas; sin recoger copias del equipo. Conservar restricciones/avisos y revisar condiciones de redistribución antes de entrega externa. |
| UCRT y API sets | Requisitos del Windows10/11 x64 de destino; no se copian ni empaquetan DLL del sistema. |
| Contenedor Rust/Tauri/Vue/Quasar | Cargo.lock/package-lock, compilación con rutas remapeadas e inventario conservador de289 entradas, incluidos compilación y otras plataformas. No se afirma que las289 estén enlazadas en el exe. |
| NSIS/plugins | Licencias originales acompañantes, hashes/arquitecturas reconciliados durante la inspección del setup. |
| WebView2 | Evergreen oficial mediante `downloadBootstrapper`. Si falta, la instalación inicial necesita Internet; Windows/WebView2 conservan sus propios diagnósticos y actualizaciones. No se distribuye un runtime FixedVersion. |

Fuentes: [PSF3.14.10](https://www.python.org/downloads/release/python-31410/),
[vendorización del embeddable](https://docs.python.org/3.14/using/windows.html#the-embeddable-package),
[Microsoft VC++](https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files),
[opciones oficiales Tauri/WebView2](https://v2.tauri.app/distribute/windows-installer/#webview2-installation-options).
Los textos/condiciones específicos se conservan en `packaging/notices/` y en
el runtime. La auditoría técnica no concede aceptación legal/comercial al titular.

## Aislamiento y datos

Tauri ejecuta su `runtime/python.exe` por ruta absoluta con `-I -S -B -u`.
`python314._pth` enumera únicamente ZIP, runtime, vendor y app; no importa site,
paquetes de usuario, directorio actual, PYTHONPATH o Python del registro. No se
instala un Python global ni se modifica PATH del sistema. El proceso hijo conserva
el watchdog del padre, loopback, sesión, CSRF, CSP y los límites de imágenes.

El entrypoint mantiene `%LOCALAPPDATA%/ColorStudioBetaData`, igual que beta2.
Las pruebas pueden elegir una carpeta privada mediante LUMAFORGE_DATA_DIR;
ni sesiones ni pycache deben aparecer en la instalación. Cambiar el contenedor
no migra ni borra automáticamente recetas/imágenes/presets. Los originales
siguen fuera de los archivos temporales de la app.

Los fuentes propios se copian con LF canónico para que autocrlf no cambie el
payload. Los archivos de upstream se conservan byte a byte. `.gitattributes`
preserva los avisos legales fijados: cambiar saltos de línea rompía sus hashes.
No se normalizan DLL o licencias para hacerlas pasar por otras copias.

## Construir y comprobar

Herramientas de build existentes, no incluidas en producto: Python3.12.x,
Node26.13.0/npm11.20.0, Rust/Cargo1.99.1, MSVC/SDK y Tauri2.12.4. Versiones en
`packaging/build-environment.json`; no hay instalación automática local de
herramientas si no coinciden. Preparar npm ci y cargo fetch --locked una vez.
Los dos módulos de auditoría adicionales tienen versiones/hashes en
`requirements-runtime-build.txt`. La venv existente se usa solo como herramienta.

Desde el worktree preparado, usando la ruta de su Python de build:

```powershell
./scripts/build_beta.ps1 -BuildPython ../../.venv-mvp/Scripts/python.exe -Offline
```

Por defecto exige fuentes comprometidos en Git y crea un runtime nuevo sin
sobrescribir prototipos. `-AllowDirtyInternal` existe para diagnóstico, declara
el estado y nunca debe presentarse como candidato limpio. El staging anterior
solo se sustituye si es propio, marcado, sin enlaces y coincide con su manifiesto.

Comprobaciones individuales reproducibles:

```powershell
python scripts/build_embedded_runtime.py .lumaforge-local/runtime-nuevo --offline
python scripts/test_embedded_runtime.py .lumaforge-local/runtime-nuevo .lumaforge-local/tests.json --offline
python scripts/qa_runtime_isolation.py .lumaforge-local/runtime-nuevo .lumaforge-local/isolation.json
python scripts/audit_embedded_payload.py .lumaforge-local/runtime-nuevo .lumaforge-local/payload.json
./scripts/audit_runtime_signatures.ps1 -Runtime .lumaforge-local/runtime-nuevo -Report .lumaforge-local/signatures.json
python scripts/smoke_beta.py --executable .lumaforge-local/runtime-nuevo/python.exe
```

Dos ensamblados se comparan por manifiesto y todos sus hashes. Eso prueba
reproducibilidad del payload bajo esos inputs/herramientas; no demuestra por
sí solo un NSIS idéntico bit a bit. El setup recibe versión, SHA-256 y origen
real en beta-artifact.json. El binario se conserva localmente; el workflow del
repositorio público solo permite subir informes saneados, nunca el instalador.

## Evidencias y límites de aceptación

Las pruebas de infraestructura incluyen tripwires de PYTHONHOME/PYTHONPATH/cwd,
origen real de módulos cargados, conservación al reiniciar y núcleo cargado
desde el bundle. Son pruebas efectivas sobre el equipo de desarrollo existente,
no una máquina Windows limpia. Los extras HTTP del runner de tests están en
`runtime-qa.lock.json`, separados y nunca en el producto.

El protocolo humano se mantiene en `BETA_QA_EXTERNA.md` W01–W09 y la guía
`PRUEBA_CREATOR_PRO_PLANNER.md`. Para WebView2 ausente, conectar durante la
instalación o preparar previamente su instalador Evergreen offline oficial;
no desactivar SmartScreen/antivirus ni copiar DLL para sortear un error.
Instalación limpia, primera ejecución offline y ausencia de herramientas requieren
el entorno real acordado. No hay VM nueva habilitada por esta entrega.

Las importaciones LUT en Photoshop, Premiere y Resolve continúan **pendientes**
hasta abrir esos programas realmente: `QA_EDITORES_03.md` E01–E05. No se anuncian
como compatibilidad certificada. Beta externa y venta permanecen **NO-GO** hasta
cerrar QA, derechos/condiciones, revisión y permiso de entrega. Los resultados
del candidato se registran en evidencias, Issue57/67 y el checkpoint.
