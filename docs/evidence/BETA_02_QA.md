# Beta0.2 · evidencias de ingeniería · 30–31 octubre2026

## Resultados obtenidos

-23 unittest MVP OK, sin omisiones: identidad, LUT33³ trilineal, ICC/alfa/EXIF,
API, origen/cookie/token, presets CRUD/grupos, preferencias, escritura atómica,
cancelación real de job, reinicio interrupted, entradas corruptas y rutas inválidas.
-87 tests de seguimiento OK; tras incorporar main a7a8df8, **91 tests OK** sin
omisiones. Advertencia httpx/Starlette de deprecación, no fallo. TypeScript/Vite
build OK y npm audit de instalación0 vulnerabilidades; no prueba ausencia total
de vulnerabilidades. Workflows MVP/Studio ampliados a bases codex para PR apiladas.
-Rust1.99.1/MSVC, CLI Tauri2.12.4, NSIS3.13 y PyInstaller6.22.3: build real
completo. Herramientas instaladas con aprobación explícita, no permisos nuevos.
-Setup266193722 bytes (253.86MiB), sin firma. SHA256 y toolchain en
BETA_02_ARTIFACT.json. Se compiló antes del commit de fuentes: dirty=true
declarado, snapshot de inputs posterior en BETA_02_SOURCE_INPUTS.json. No afirmar
reproducibilidad bit a bit ni vinculación del binario a un commit limpio.
-Sidecar empaquetado ejecutado con cuatro JPEG rurales CC0 reales de unos16MP:
exports11.4–13.7s, RSS pico muestreado788.6–803.9MB. ICC y dimensiones originales
verificados; hashes de originales intactos. Lote real2 fotos completed, descargas
comparadas SHA256; demo sin modificaciones. No binario FFmpeg en árbol empaquetado.
BETA_02_SMOKE.json; outputs quedan privados en .lumaforge-local/beta-qa-*.
-Watchdog: muerte del padre de prueba termina sidecar dentro del límite8s.
Instancia única: segundo ejecutable sale y se conserva un solo proceso nativo.
Listener del sidecar observado exclusivamente en127.0.0.1, puerto dinámico.
-Instalación NSIS silenciosa por usuario exit0, frontend/backend incluidos,
atajo Inicio creado, avisos de terceros instalados. GUI WebView2 real: bienvenida,
demo, matching/comparador, guardar preset y biblioteca. Idioma ES→EN cambia
interfaz y persiste preferences.json. No se requieren Python/Node para ese arranque.
-Cierre nativo AltF4: desaparecen proceso y sidecar. Desinstalar exit0, ejecutable
retirado, ocho archivos privados conservados por hash; BETA_02_INSTALL.json.
Reinstalación del mismo candidato para handoff. El contexto Codex/MSIX redirige
LocalAppData a LocalCache del paquete: prueba en equipo de desarrollo, **no**
prueba limpia Windows10/11 ni comprobación exhaustiva fuera de esa virtualización.
-Captura auténtica del frontend empaquetado en navegador a1280x900, con demo CC0,
apps/landing/assets/studio.jpg. No es mockup ni captura generada. Cualquier otra
captura fallida del búfer nativo fue descartada; no se fabrica evidencia visual.

## Matriz GO / NO-GO

| Criterio | Estado y consecuencia |
|---|---|
| Candidato instalable local y demostración | Obtenido en este equipo; revisión humana pendiente |
| Unitarias/integración/color/LUT |23+91 locales OK; CI de la PR debe comprobarse por separado |
| Lotes/presets/persistencia/procesos | Implementados y pruebas anteriores OK; no recuperación automática de píxeles a mitad de lote |
| Windows limpio10/11, usuario estándar, con/sin WebView2 | Pendiente VM/máquina autorizada; NO-GO beta general |
| Retratos/piel/oscuras/claras/múltiples equipos | Solo paisaje real disponible. Fixtures numéricas no validan piel; NO-GO promesas universales |
| Photoshop/Premiere/Resolve | Photoshop2026 bloqueado por inicio de sesión; Premiere instalado sin importación verificada; Resolve ausente |
| Licencias/componentes incluidos | Inventario299 entradas y avisos incorporados; seis avisos fuente y conciliación binaria pendientes, NO-GO redistribución amplia |
| Firma/actualización/rollback | Sin firma ni updater automático. NO-GO distribución comercial hasta decidir canal/identidad/firma y QA |
| Privacidad | Local por defecto, sin telemetría/subidas; política de soporte/compra futura incompleta |
| Marca/titular/fiscalidad/EULA/precio/código público | Propuestas y borradores, sin aceptación legal/comercial. NO-GO venta |
| P0 comercial | Sin entrevistas nuevas, sin encuestas reales ni benchmark competitivo; COL001 pendiente |

## Intervención mínima necesaria

Revisar PR y probar candidato desde Explorador con el titular. Para siguiente QA:
equipo limpio o VM existente autorizada; iniciar personalmente sesión Adobe si
quiere verificar LUT; aportar2–3 retratos/fotos propias por ruta privada con
permisos documentados. No publicar medios/personas en Issues. Código público,
marca y contrato se deciden antes de vender, no bloquean otras pruebas locales.
No instalar virtualización, comprar certificados, cambiar visibilidad ni lanzar
comercialmente sin autorización específica. El envío de un aviso no aprueba nada.
