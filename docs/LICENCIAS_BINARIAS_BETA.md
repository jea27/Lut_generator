# Distribución binaria0.3 · revisión específica

31-10-2026. Candidato inspeccionado: beta2, SHA256
3e3851ee4f3c67608d3802ad167572375b130eeafa57165d26379cd26797714f.
Esta es auditoría técnica/documental; no aceptación de contratos ni autorización
de entrega. Inventario de299 entradas es conservador e incluye build, no299
componentes probados como runtime.95 DLL/PYD del árbol extraído cotejados por
hash con entradas reales de Analysis-00.toc.176 entradas NSIS siguen inventariadas.

| Componente real | Condiciones y evidencia | Pendiente concreto |
|---|---|---|
| CPython3.12.14, stdlib/base_library.zip, python312/python3 y extensiones | PSF y licencias incluidas en LICENSE.txt; avisos ya capturados. Hashes vinculados a la instalación usada | La instalación procede del runtime de herramientas: documentar proveedor/build/fuente y autorización de redistribución; no llamarla binario PSF oficial sin prueba |
| NumPy2.5.4 y bibliotecas wheel | BSD y avisos internos, incluida la biblioteca numérica vendorizada; conservados en distribución | Contrastar avisos del wheel exacto; no deducir obligaciones solo de numpy/LICENSE |
| Pillow13, OpenCV-headless5, psutil7.2.2, pydantic_core2.50.2 | Textos declarados y avisos internos capturados; origen wheel cotejado por bytes | Conservar licencias de subcomponentes; FFmpeg excluido del payload y del alcance de vídeo |
| OpenSSL/libcrypto/libffi y extensiones CPython | Sujetos a sus avisos propios dentro del runtime CPython, no solo PSF | Vincular cadena de suministro del runtime que los aportó; no copiar versiones de otro Python |
| Paquetes Python puros / frontend Vue, Quasar, iconos | Textos en THIRD_PARTY_NOTICES y material-icons/LICENSE; build no se redistribuye como node_modules | Mantener inventario/lock y avisos exactos junto al instalador |
| Rust/Tauri/wry/tao y dependencias resueltas | MIT/Apache/BSD y excepciones según paquete; se conserva inventario incluidas proc-macros | selectors tiene MPL2: identificar código realmente incluido y ofrecer fuente exigible si procede; no declarar exclusión por inferencia |
| PyInstaller6.22.3 | GPL con excepción para aplicaciones empaquetadas; dependencias conservan obligaciones propias | No se modifica bootloader; mantener registro y textos. [Explicación oficial](https://www.pyinstaller.org/en/stable/license.html) |
| NSIS3.13 / plugins comunes | COPYING local de NSIS detalla componentes y excepciones, no una licencia única para todo plugin | Aviso acompañante incluido en ZIP; comprobar inclusión del siguiente setup |
| nsis_tauri_utils0.5.3 | Hash idéntico a release oficial; MIT/Apache2 con textos versionados en upstream/ | Añadidos después del build beta2: acompañantes del ZIP, no afirmar que ya estén dentro de ese setup |
| WebView2 Evergreen Standalone | Wrapper Microsoft firmado, hash62863f…249b; distribución offline documentada por Microsoft | Conservar términos exactos mostrados en descarga y revisión del titular. No se presume licencia Fixed Version ni se extrae/ejecuta su interior para afirmar SBOM completa |
| VCRUNTIME140/140_1 14.44.35211.0 | Archivos Microsoft firmados, bytes coincidentes con runtime local | Derecho depende de términos aplicables; lista REDIST no concede por sí sola derecho a cualquier copia |
| UCRT10.0.26100.4654/API-set:44 archivos | TOC demuestra caché nativa de una herramienta, ajena a instalación Python/SDK directa. ucrtbase firmado Microsoft; su hash no coincide con las dos copias x64 REDIST del SDK local | **Bloquea build/distribución** hasta procedencia/términos conciliados o reconstrucción aislada con origen permitido; no borrar/editar DLL del sistema |
| Demo, landing y evidencias visuales | Derivados CC0 Sergej Majboroda/Poly Haven y capturas de aplicación; créditos/hashes. Sin EXIF en6 JPEG de PR70 | No se amplía a fotografías privadas/personas ni permisos inexistentes |

Fuentes oficiales consultadas31-10-2026:

- [WebView2 distribución](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution): permite preparar el instalador standalone para equipos offline. Evergreen comparte runtime y recibe actualizaciones; no implica aplicación con cuenta o inferencia remota.
- [WebView2 datos y privacidad](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/data-privacy): Microsoft documenta diagnósticos y exige aviso de SmartScreen cuando se conserva habilitado. No se desactiva una protección para hacer una promesa de privacidad; texto fuente corregido y aviso Microsoft añadido. Ver [privacidad Microsoft](https://privacy.microsoft.com/privacystatement).
- [UCRT en Windows](https://learn.microsoft.com/en-us/cpp/porting/upgrade-your-code-to-the-universal-crt): integrado en Windows10+, con DLL retail en REDIST del SDK. Recomendar estudiar un build limpio que use el componente del SO; no retirar archivos de un candidato sin probar arranque en los cuatro escenarios limpios.
- [REDIST de VS2022](https://learn.microsoft.com/en-us/visualstudio/releases/2022/redistribution) remite a términos de la edición licenciada y archivos sin modificar. [Runtime](https://visualstudio.microsoft.com/license-terms/vs2022-cruntime/) y [Build Tools](https://visualstudio.microsoft.com/license-terms/vs2022-ga-diagnosticbuildtools/) tienen términos separados. Su lectura pública no acredita licencia/edición del titular.

El nuevo gate `audit_beta_binary_origins.py` falla antes de copiar staging/crear
NSIS si detecta entradas de caché nativa externa, no clasificadas o bytes
distintos. Informe real STAB_03_BUILD_ORIGINS:95 cotejados,44 bloqueados, FFmpeg
ausente de forma intencional. No se ejecutó un build nuevo ni se sustituyó beta2.
STAB_03_BINARY_ORIGINS concilia esos95 con la extracción del setup anterior.
La firma/pruebas funcionales y los27 hallazgos genéricos de rutas ya clasificados
son comprobaciones distintas: ninguna concede derechos de redistribución.
