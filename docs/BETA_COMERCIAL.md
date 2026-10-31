# Preparación comercial · borrador para revisión

30-10-2026. **NO-GO venta / NO-GO beta pública general.** El instalador es un
candidato técnico, sin firma, pendiente de Windows limpio, calidad diversa,
compatibilidad externa y autorización de distribución. Este documento no
formaliza contratos, precios ni asesoramiento jurídico/fiscal.

Continuación31-10-2026: conservar la investigación comercial integrada en
P0_COMERCIAL_ESPANA_UE.md y LOOK_MATCH_REQUIREMENTS.md. No se cambia el estímulo
49€ de COL005, el cuestionario publicado ni se implementa Look Match espacial.
Bloom/halation/difusión siguen como propuesta posterior; la beta solo transfiere
color global. Las propuestas de prueba/licencia aquí no son decisiones aceptadas.

## Código y publicación

Consulta real de GitHub: jea27/Lut_generator PUBLIC, licenseInfo=null. La ausencia
de LICENSE no equivale a dominio público ni concede una licencia comercial al
usuario del programa. No se añade una licencia propia automáticamente.
[GitHub explica los derechos por defecto y las posibilidades de ver/fork](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
No se puede retirar lo que terceros ya hayan copiado de un repositorio público.

| Alternativa | Consecuencias y costes |
|---|---|
| Núcleo futuro privado + dashboard público | Recomendada antes de vender: separación deliberada, repositorio y permisos por autorizar; coste de mantenimiento de dos superficies. No oculta el código ya publicado |
| Open core | Publicar una licencia elegida tras revisar titularidad/contribuciones; módulos comerciales separados. Mayor mantenimiento y límites claros de soporte |
| Todo abierto | Ingresos por soporte/paquetes/distribución; menor exclusividad, exige modelo comercial y licencia compatibles |

PyInstaller no cifra ni protege jurídicamente Python; la ingeniería inversa y
la extracción son posibles. No basar el negocio en ofuscación. Sin cambios de
visibilidad, permisos, historial ni traslado del código durante esta entrega.

## Auditoría de redistribución

`scripts/audit_beta_licenses.py` genera inventory.json y THIRD_PARTY_NOTICES.txt
en packaging/notices; el instalador los incluye. Inventario conservador de299
entradas: ruedas Python, frontend runtime y grafo Cargo del target Windows con
build-dependencies. Las versiones se fijan en lockfiles/requirements. No es un
SBOM binario completo ni un dictamen legal. Seis crates carecen de archivo de
aviso en la raíz del paquete: alloc-stdlib, plist, selectors, webview2-com,
webview2-com-macros y webview2-com-sys. Verificar licencia completa/origen antes
de redistribución amplia, incluso si sus metadatos son permisivos.

Python/NumPy/Pillow/OpenCV incluyen componentes de terceros; se conservan sus
textos, no se sustituye su auditoría por la licencia principal. selectors declara
MPL2.0; separar build/runtime y verificar obligaciones de fuente si se distribuye
su código. PyInstaller declara GPL con una excepción para el bootloader: revisar
la [excepción oficial](https://pyinstaller.org/en/stable/license.html), también
capturada del paquete, junto con las licencias del programa empaquetado.

El binario FFmpeg de OpenCV se excluye del bundle al no usar vídeo. No se incorpora
FFmpeg externo ni se ofrece procesamiento de vídeo; futura integración debe
fijar build/licencia/opciones y obligaciones de LGPL/GPL/patentes antes de elegir
binarios. WebView2 offline y VC runtime tienen condiciones Microsoft separadas:
conciliar los archivos realmente distribuidos y conservar sus avisos antes de GO.

Demo: dos derivados1024px de fotografías CC0 Poly Haven/Sergej Majboroda;
apps/demo/credits.json documenta URLs y hashes de originales/derivados, sRGB y
eliminación EXIF. Solo esas fotografías autorizadas van en Git. No hay fotos
privadas, respuestas de investigación, telemetría ni identificadores de hardware.

## Marca provisional

LumaForge y Color Studio son nombres de trabajo, no marcas despejadas. El usuario
ha advertido una empresa audiovisual LumaForge. Alternativas para estudiar:
Tonaloom, LutHarbor y Chromalune; **ninguna tiene disponibilidad verificada**.
El [localizador OEPM](https://consultas2.oepm.es/LocalizadorWeb/index.jsp) distingue
marcas nacionales/internacionales y remite a las de UE; una búsqueda idéntica no
descarta semejanzas. Encargar revisión España/UE (clases9/42 como hipótesis a
confirmar, denominativa/fonética/gráfica), dominios y conflictos antes de elegir.
No comprar dominios, solicitar registro ni cambiar marca definitiva sin decisión.

## Licencia y precio propuestos

Recomendación: beta técnica gratuita, por invitación, sin renovación ni tarjetas;
no añadir un reloj artificial o sistema de cuentas antes de validar valor. Para
producto: prueba local de14 días como propuesta, después licencia por versión
mayor con actualizaciones correctivas de plazo definido; alternativa suscripción
anual con actualizaciones. El plazo, dispositivos, soporte y precio requieren
aceptación humana; contrastar COL005 con respuestas reales, no fijar precio con
hipótesis o tests sintéticos. Cero coste de API por imagen en el diseño local;
persisten costes de soporte, firma, fiscalidad, distribución y mantenimiento.

Sin proveedor ni cobros activados. Pago futuro en checkout alojado reconocido,
separado del editor offline: backend de licencias recibe webhook firmado,
valida importe/moneda/producto, deduplica event_id, registra revocaciones y emite
licencia firmada; el escritorio verifica firma pública offline. Nunca almacenar
tarjetas, secretos de proveedor ni abrir webhook en el loopback del usuario.
Una indisponibilidad de red no debe corromper presets/fotos ni resultados.
Decidir período offline/revocación y privacidad antes de implementar.

Comparar merchant-of-record (p.ej. Paddle) con PSP (p.ej. Stripe): el primero puede
asumir partes fiscales contractualmente, el segundo no sustituye obligaciones
del vendedor. Las comisiones dependen de país, método, moneda y contrato; pedir
cotización vigente. Fórmula de margen: precio sin IVA − comisión porcentual −
comisión fija − soporte − firma/distribución imputados. Sin precio definitivo.
[Paddle](https://www.paddle.com/pricing) y [Stripe España](https://stripe.com/es/pricing)
son fuentes para presupuesto, no acuerdos ni altas realizadas.

## Firma, versiones y distribución

Versionado0.2.0-beta.1, changelog y SHA256 del artefacto. NSIS por usuario no pide
Python/Node/Rust. WebView2 evergreen offline se empaqueta; no implica que las
actualizaciones del runtime/Windows/Adobe sean offline. Sin firma Authenticode:
SmartScreen puede mostrar avisos; no pedir desactivar protecciones ni prometer
que un certificado elimine cualquier aviso.

| Opción | Implicación |
|---|---|
| Candidato local sin firma | Sin coste de certificado; solo QA controlada, identidad del editor no validada |
| Certificado de firma de CA con soporte Tauri | Verificación de identidad, custodia hardware/HSM y renovaciones; presupuesto humano |
| Microsoft Artifact Signing | Servicio gestionado Basic/Premium, validación de identidad y cuenta Azure; elegibilidad/región/coste por confirmar |

Recomendación: completar QA y luego cotizar servicio gestionado frente a CA.
La [documentación Tauri](https://v2.tauri.app/distribute/sign/windows/) describe
firma Windows y [Microsoft](https://learn.microsoft.com/en-us/azure/artifact-signing/overview)
el modelo gestionado. La [tarifa Azure](https://azure.microsoft.com/en-us/pricing/details/artifact-signing/)
consultada no devolvió importes numéricos fiables; no se inventan precios.
No se contrata, crea cuenta/certificado o guarda credencial. Release preparada
en BETA_RELEASE_NOTES.md; no se publica sin autorización específica.

## Borrador de términos de uso y soporte

**No publicable hasta completar [TITULAR LEGAL], [NIF], [DOMICILIO], [EMAIL DE
SOPORTE], ámbito territorial y revisión profesional.**

El titular facilita una beta técnica de escritorio para aplicar transformaciones
globales de color a imágenes cuyos derechos debe poseer o gestionar el usuario.
No ofrece resultados de color garantizados ni aprobación profesional del look.
El usuario conserva sus derechos sobre entradas y exportaciones. El titular no
recibe una licencia sobre las fotos por el mero procesamiento local.
Debe conservar copias de seguridad y revisar el resultado antes de uso crítico.
No excluir derechos irrenunciables de consumidores ni responsabilidad legal
mediante una cláusula genérica de «sin garantías».

Soporte propuesto: incidencias técnicas por canal privado definido por titular;
no adjuntar fotos, rutas personales o recibos a Issues públicas. GitHub puede
usarse solo para errores sin datos personales. Definir horarios, plazo de
respuesta, actualizaciones de seguridad y fin de soporte antes de vender.
No se prometen SLA, reembolsos ni atención24h aún no acordados.

## Borrador de licencia de usuario final

Pendiente licencia del código propio y derechos de terceros. Propuesta: licencia
personal no exclusiva de uso del binario para dispositivo(s) acordados, permite
uso comercial de exportaciones en la medida de los derechos de entrada. Presets
creados por el usuario siguen siendo suyos. Especificar transferencia de licencia,
actualizaciones, plazo, compatibilidad, soporte y terminación proporcional.
Las licencias de terceros conservan sus permisos/obligaciones; no prohibir
derechos de ingeniería inversa/interoperabilidad legalmente irrenunciables.
No activar aceptación electrónica hasta revisar texto y registrar su versión.

## Borrador de privacidad

Editor: JPG/PNG y presets procesados localmente; copias sRGB y resultados en
%LOCALAPPDATA%/ColorStudioBetaData. Sin cuenta, anuncios, telemetría, subida de
fotos o API externa. El proceso loopback atiende solo el equipo local. Borrar
temporales desde la aplicación requiere confirmación y no borra originales;
desinstalar conserva datos privados para evitar pérdida. Informar cómo localizar
y retirar presets/jobs/caché tras respaldo, sin borrar imágenes ajenas.

Distribución/soporte/compra futura: identificar responsable, finalidades, base
jurídica, destinatarios/encargados, transferencias, plazos y canal de derechos;
minimizar datos de licencia y no recoger identificadores de hardware sin diseño
y revisión. La web preparada no contiene analytics/formularios; un hosting real
podría generar registros IP del proveedor, que habrá que informar. Capturas o
fotos con personas identificables requieren evaluación de base legítima y
permisos; el consentimiento no se presume por poseer el archivo.
[AEPD: responsabilidad sobre datos identificables](https://www.aepd.es/preguntas-frecuentes/2-tus-obligaciones-como-responsable-del-tratamiento/8-responsable-y-encargado-del-tratamiento/FAQ-0251-como-se-si-soy-responsable-o-encargado).

## España y UE · revisión humana antes de venta

Asesoría debe confirmar alta/actividad, facturación/IVA y posible OSS según tipo
de cliente/país; no basta integrar pagos. [AEAT sobre OSS](https://sede.agenciatributaria.gob.es/Sede/iva/iva-comercio-electronico/cuestiones-generales.html).
Preparar identificación del prestador y contratación electrónica conforme a
[LSSI](https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758), información de precio
total, compatibilidad, soporte y condiciones. Revisar conformidad/actualizaciones,
desistimiento y requisitos específicos de contenido digital, incluidas las
condiciones que permitan una excepción válida; no usar un checkbox genérico
para suprimir derechos. [Texto consolidado consumidores](https://www.boe.es/buscar/act.php?id=BOE-A-2007-20555).
Revisar RGPD/LOPDGDD, encargados y seguridad para cualquier tratamiento posterior.
La IA prepara software/borradores y evidencias; titular/asesores aceptan las
decisiones legales, fiscales, de marca y comerciales. Sin ventas hasta resolverlas.
