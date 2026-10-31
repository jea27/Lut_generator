# Auditoría de beta0.3 · distribución y licencias

Actualización de integración: jea27 fusionó69→COL042,65→main y66→COL037, en ese
orden. Los cambios66/69 no alcanzaron main. PR70 hacia main reúne lo pendiente;
CI correcta y decisión humana en67. COL026 sigue review; ningún merge equivale
a aprobación completa. El apartado siguiente registra la auditoría inicial.

31-10-2026. PR65/66 auditadas: abiertas, mergeable y checks MVP/Studio correctos
en sus HEAD d90da2d/32278e4. No fusionadas. Issue67 sigue con solicitud humana,
sin respuesta nueva al iniciar este ciclo. No se interpreta aviso como aceptación.

## Fallos encontrados y correcciones

1. Ejecutable nativo0.2:155 coincidencias ASCII de rutas C:\Users\... de
   compilación. Nuevo builder remapea perfil y raíz mediante flags de Rust;
   ejecutable0.3 recompilado:0 coincidencias ASCII. No se editan DLL firmadas.
2. Builder elegía el primer `*setup.exe`; al coexistir versiones podía asignar
   a una versión nueva el hash de0.2. Corregido: nombre exacto de productName,
   versión y arquitectura del config, Get-Item literal. Manifest registra commit,
   dirty, tamaño, firma, hash y estado de bloqueo; no inferir versión de un glob.
3. Controles de acabado alargaban la página y alejaban el comparador. Paneles
   laterales ahora desplazan por separado en escritorio, comparador y export
   permanecen accesibles. Móvil conserva flujo vertical. Bienvenida actualizada0.3.

## Payload: alcance real

`audit_beta_artifact.py` enumera/hasha árbol PyInstaller, descomprime archivo
Python/PYZ e inspecciona co_filename y constantes, además del ejecutable Tauri.
Busca patrones de perfiles locales ASCII/UTF16, tokens/claves y archivos de
desarrollo/privados. No guarda coincidencias sensibles ni rutas fuente en Git.
Informes LOOK_03_PAYLOAD y manifest final: revisar antes de distribuir.

No encontró patrón de secreto, perfil **local** ni archivo privado/desarrollo
en ese scope; persisten27 archivos/módulos con patrones de rutas de proveedor
o ejemplos de C:\Users\..., incluidos DLL/stdlib/Pydantic/NumPy/Click.
Las27 coincidencias se clasificaron con hashes: cuentas genéricas de build o
ejemplos de documentación,0 desconocidas. Se completó extracción NSIS; no se
afirma ausencia universal de PII ni se altera el scanner bruto conservador.
No modificar DLL de Microsoft/terceros para ocultar datos o invalidar firmas.

Con autorización posterior se preparó7-Zip26.05 portátil oficial y se extrajeron
las176 entradas del NSIS: plugins, uninstaller y WebView2 offline incluidos.
7zr/Extra/SFX se verificaron contra SHA256 del release oficial; el SFX se abrió
como archivo, sin ejecutar un instalador o usar MSI. Herramienta privada en
.lumaforge-local/tools/7zip/full/7z.exe, no se redistribuye con LumaForge.
La extracción completa mantiene27 findings solo de rutas proveedor/ejemplo;
0 local-profile/token/dev en ese scope. WebView2 offline firmado Microsoft
válidamente; conserva hash62863f...249b y copia en .lumaforge-local/vendor-pins.
El interior comprimido del instalador Microsoft no fue expandido/ejecutado.
No equivale a prueba limpia ni análisis antimalware o ausencia universal de PII.

El exe extraído difiere3 bytes del target/release: Tauri cambia el marcador
__TAURI_BUNDLE_TYPE_VAR_UNK a NSS durante empaquetado. Verificado contra fuente
local tauri-utils2.10.2/platform.rs y normalización exacta, sin descartar otras
diferencias. LOOK_03_NSIS.json enumera176 hashes y registra esa comprobación.
Plugin nsis_tauri_utils0.5.3 coincide SHA256 con release oficial; textos Apache2
/MIT y NSIS3.13 COPYING preparados como avisos acompañantes. Condiciones
Microsoft pendientes de revisión; las27 rutas son cuentas genéricas/ejemplos
ya clasificados, sin perfil local o datos de clientes detectados.
No se alteran DLL firmadas ni se autoaprueba la redistribución.

## Inventario y derechos

299 entradas conservadoras (Python runtime/build, npm runtime, Cargo incluidas
herramientas/proc-macros). Todas tienen licencia declarada y ahora texto de aviso;
0 avisos ausentes. Se recuperaron6 textos faltantes:4 MIT/BSD desde commits
declarados en cargo_vcs_info, plist por LICENCE del commit y MPL2 canónica para
selectors. URLs/hashes/notas en packaging/notices/upstream/sources.json; se
incorporan al NOTICE del instalador. No asumir que299 paquetes están todos en
el binario ni que tener texto equivale a revisión jurídica completada.

Setuptools incluye17 avisos, también de sus componentes vendorizados. Ruedas
NumPy/Pillow/OpenCV/CPython conservan avisos de dependencias internas. FFmpeg
externo no incorporado; DLL de vídeo OpenCV excluida, sin soporte de vídeo.
PyInstaller GPL/bootloader-exception conservados. selectors MPL llega por
tauri-utils/codegen/proc-macros; clasificar build/runtime y obligaciones sobre
código realmente redistribuido, no concluir solo por la licencia raíz de Tauri.

WebView2, loader/SDK, VC runtime y UCRT requieren conciliar los archivos y sus
condiciones Microsoft. Fuentes oficiales consultadas:
[WebView2 distribución](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution),
[lista de redistribución VS2022](https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution).
La lista remite a términos de la edición licenciada y distribución sin modificar;
no se afirma que instalar Build Tools resuelva por sí solo todos los derechos.
Pendiente validar titular/condiciones aplicables y añadir avisos exigibles de
la combinación concreta antes de entrega externa. No gastos ni aceptación de
contratos nuevos por el agente.

Demo:2 derivados CC0 Sergej Majboroda/Poly Haven y créditos/hashes incluidos,
sin medios privados. Investigación y consentimientos siguen fuera de Git.
Sin cuenta, telemetría, pagos o subida de imágenes. Feedback técnico generaJSON
local y no hace fetch/envíos; QA00 descargado y verificado synthetic=true,
counts_as_interview=false, separado en .research-private/beta/qa.

## GO / NO-GO

- Demostración técnica local: candidato utilizable con límites y efectos manuales.
- Beta privada externa: **NO-GO todavía**, hasta payload/NSIS conciliado, Windows
  limpio y actualización reales, términos/soporte mínimos y autorización del titular.
- Lanzamiento comercial: **NO-GO**, además entrevistas/P0, calidad/piel, marca,
  fiscalidad/licencia propia/firma/soporte/privacidad aún pendientes.

No se publican release general o cobros. Los cinco recorridos preparados son un
piloto futuro, no cinco pruebas realizadas ni cumplimiento de COL041 completo.


## Correcciones finales beta2

Candidato vigente0.3.0-beta.2, source a452a5f, dirty=false,266211731 bytes.
SHA256 3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f.
Conservado beta1 como evidencia histórica. Se corrigió el enlace de feedback que
no abría nueva ventana en Tauri: diálogo iframe local ahora visible en WebView2,
sin salir del editor; browser confirma misma imagen/URL. También se fuerza
migración UI de presets v1 a receta v2 antes de activar efectos: preset v1 real
de QA aplicado, glow activado y JSONv2 descargado/validado. No es respuesta real.
Upgrade a beta2 exit0, mismos8 archivos de datos preservados. No Windows limpio.
Premiere intentado: muestra selector de suscripción; no se contrató ni se
activó prueba. Photoshop no ofreció documento/editor verificable. Importación
real de LUT externa sigue pendiente en equipo con editor ya activado.


Actualización final de clasificación: las27 coincidencias de rutas se han
resuelto técnicamente como cuentas genéricas de compilación de proveedor o
placeholders/ejemplos de documentación (incluido ntpath.splitroot).0 perfiles de
origen sin clasificar. Hashes de cada archivo/contenedor cotejados con el NSIS
completo en LOOK_03_PATH_CLASSIFICATION.json. El scanner bruto conserva sus27
hallazgos y no se ocultan ni alteran DLL; no son rutas del perfil local, secretos
o datos de clientes. No constituye aprobación de COL040 ni prueba universal de
privacidad. Siguen las puertas de Windows limpio y derechos/condiciones Microsoft.
