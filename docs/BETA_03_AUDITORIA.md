# Auditoría de beta0.3 · distribución y licencias

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
No se declaran limpios ni datos personales ausentes universalmente: hay que
clasificar esas rutas con hashes, cerrar consentimiento/obligaciones si procede
y completar inspección NSIS. El escáner deliberadamente no los autoacepta.
No modificar DLL de Microsoft/terceros para ocultar datos o invalidar firmas.

El NSIS integra WebView2 offline y plugins/launcher propios de NSIS. El informe
del staging no extrae por sí solo todo el NSIS ni demuestra qué instalará en un
Windows sin runtime. No hay7zip disponible; no se instala otra herramienta sin
explicar/aprobar. Inspección del script NSIS generado y hashes de sus inputs son
evidencia complementaria, no sustituto del ensayo limpio ni análisis antimalware.

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
