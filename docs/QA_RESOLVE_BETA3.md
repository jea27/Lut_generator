# DaVinci Resolve gratuito · prueba interna de LUT beta.3

01-11-2026 · COL-038/#59, coordinación con COL-036/#57 y solicitud canónica #67.
Guía preparada; **todavía no se ha instalado ni ejecutado Resolve ni importado una
LUT en él**. Beta externa y venta continúan **NO-GO**. Ningún resultado de esta
guía aprueba automáticamente una capacidad de Color Studio.

## Lo comprobado y lo que falta

En el inventario de este ciclo no aparece Resolve en el registro, procesos,
ejecutables habituales ni atajos. Photoshop2026 y Premiere2026 sí figuran
instalados; eso **no demuestra licencia activada, sesión operativa ni pruebas**.
No se han utilizado esos programas para esta validación.

El host observado tiene Windows11 Pro,16GB nominales de RAM y RTX3060Ti con
8192MiB de VRAM, confirmados mediante nvidia-smi. El driver informa617.14; no
se ha confirmado su canal Studio. En ese momento quedaban unos4,84GiB de RAM
libres: es una lectura temporal, no memoria garantizada para otra aplicación.

El [readme oficial21.1.2](https://www.blackmagicdesign.com/support/content/readme/be08842994c94d999da4ab052d0a2b2a)
indica16GB de RAM,32GB para Fusion,4GB de VRAM, OpenCL1.2 o CUDA12.8 y driver
NVIDIA Studio581.57 o posterior. El equipo cumple nominalmente RAM/VRAM y su
número de driver es posterior; **compatibilidad efectiva y arranque pendientes**.
No actualizar drivers por iniciativa de este procedimiento.

Se recomienda probar Resolve nativo en el host, con la VM de Color Studio
apagada y trabajo de otras aplicaciones guardado. No cerrar procesos ajenos
automáticamente. No asumir que la GPU virtual cumple los requisitos del editor
ni introducir passthrough o cambios del hipervisor para conseguirlo. La prueba
del editor en el host y la prueba de Color Studio en Windows limpio son evidencias
distintas; una no sustituye la otra.

## 1. Obtener la edición correcta

1. Abrir la [página oficial de Resolve](https://www.blackmagicdesign.com/products/davinciresolve)
   o el [centro de soporte Blackmagic](https://www.blackmagicdesign.com/support).
2. Elegir **DaVinci Resolve gratuito**, no **DaVinci Resolve Studio**. Para este
   PC Intel/AMD de64bit elegir Windows x86, no Windows ARM. Al preparar esta guía
   la versión estable ofrecida es21.1.2; registrar la versión realmente descargada.
3. El [formulario oficial](https://www.blackmagicdesign.com/event/davinciresolvedownload)
   solicita datos de identidad, contacto y dirección. **Lo completa jea27**, con
   datos reales que decida proporcionar y revisando su aviso de privacidad.
   Codex no inventa datos, no extrae los de otras aplicaciones ni envía el formulario.
   No hacen falta una compra, una cuenta Cloud para este ensayo local o una clave Studio.
4. Conservar la URL oficial de procedencia y el archivo descargado en la carpeta
   privada de herramientas/descargas acordada con Codex, fuera de Git. No subir
   el instalador, el formulario ni sus datos personales a Issues o al dashboard.

La [API pública oficial de descargas](https://www.blackmagicdesign.com/api/support/us/downloads.json)
identifica la edición gratuita como producto `davinci-resolve` y marca esta
descarga como `requiresRegistration: true`. No se ha enviado una solicitud de
registro ni descargado el paquete de varios GB durante esta preparación.

## 2. Verificar antes de instalar

Codex puede asistir en estas comprobaciones sobre el archivo proporcionado:

- Registrar nombre, versión, tamaño, URL de origen y SHA-256 del ZIP/instalador.
  Si Blackmagic publica un hash verificable para esa descarga, compararlo.
  Un hash calculado localmente identifica el archivo; por sí solo no prueba su origen.
- Si llega en ZIP, inspeccionar primero su índice y extraerlo en una carpeta
  privada nueva; no sobrescribir herramientas o archivos existentes.
- Comprobar la firma Authenticode del ejecutable y el editor correspondiente a
  Blackmagic Design. Registrar estado y resultado real. Una firma ausente,
  inválida o de otro editor requiere detener la instalación y revisar procedencia.
- Leer las condiciones que presente el instalador. El operador resuelve cualquier
  aceptación o elevación que requiera intervención. No introducir licencias,
  tarjetas, compras, certificados ni servicios de pago.

El readme advierte de utilidades acompañantes, Blackmagic RAW Player y Proxy
Generator. Revisar los componentes que realmente ofrezca el instalador; no dar
por instalados ni aceptar componentes innecesarios sin observar la pantalla.
Desktop Video corresponde al uso de hardware Blackmagic de monitorización, no
debe añadirse por suposición para este ensayo de imágenes/LUT.

No desactivar Defender, SmartScreen, firewall, firmas, privacidad o protecciones
para descargar, instalar o ejecutar. Ante un bloqueo, conservar el mensaje sin
datos personales y registrarlo como **BLOCKED**, no como PASS.

## 3. Preparar el proyecto de ensayo

1. Abrir Resolve gratuito y registrar versión y resultado de arranque. Si pide
   activación Studio, detenerse: comprobar la edición descargada. No comprarla.
2. Crear una biblioteca/proyecto **de QA nuevo**, por ejemplo `LumaForge-LUT-beta3`.
   No abrir, migrar ni modificar bibliotecas o proyectos personales existentes.
3. Usar únicamente el kit privado autorizado ya preparado en la raíz del proyecto:
   `.lumaforge-local/stab03-editors/`. No está publicado ni se descarga desde Pages.
   Si se trabaja desde un worktree, Codex localiza la carpeta compartida de la
   raíz sin copiar rutas personales al informe público.
4. El `manifest.json` del kit fija8 hashes, comprobados sin diferencias en este
   ciclo. Contiene `identity.cube`, `color-only.cube`, receta, foto/expected y
   chart/expected. No sustituirlos por fotografías personales o de clientes.
5. Seguir [QA_EDITORES_03.md](QA_EDITORES_03.md), casos **E01–E05**. Codex guiará
   los controles observados de la versión instalada; no se presentan los menús
   de una versión no ejecutada como verificados.

La fotografía del kit procede de la demo rural CC0 acreditada en
`apps/demo/credits.json`. El chart es **sintético** y solo prueba infraestructura,
orden de canales, gamma, niveles e interpolación. Ninguno representa entrevistas,
usuarios externos, retratos, calidad de mercado o aceptación humana.

## 4. Importar y comprobar las LUT

| Caso preparado | Operación | Qué registrar |
|---|---|---|
| E01 | Chart sintético + identity.cube | Orden RGB, extremos, gamma y niveles; export sin cambiar dimensiones. |
| E02 | Chart sintético + color-only.cube | Interpolación y errores sobre rampas/primarias frente al expected del kit. |
| E03 | Foto CC0 + color-only.cube | Comparación con photo-color-expected.png a igual resolución. |
| E04 | Foto/receta en Color Studio | Acabado en PNG/JPG/receta; .cube mantiene solo color. |
| E05 | Preview y export de la misma receta | Separar escala, radio espacial, ICC, cuantización e interpolación. |

Las LUT son33³ en **encoded-sRGB-D65 → encoded-sRGB-D65**. No son un Input LUT
de cámara ni una conversión Log/Rec.709. Registrar gestión de color, gamma, niveles
full/data, conversiones y ubicación del nodo LUT. Desactivar únicamente ajustes
creativos o conversiones del proyecto de QA que falseen el control; no tocar
protecciones del sistema. Comprobar trilineal para comparar con el motor;
tetrahedral es otro ensayo y debe identificarse como tal.

La LUT no puede transportar glow, difusión, fade o halation. No comparar su
resultado con `photo-finish-excluded-from-lut.png` para declarar fidelidad de color.
La receta propia y el render conservan los efectos manuales que correspondan.

## 5. Exportar evidencia medible y devolver el resultado

Exportar realmente desde Resolve una imagen lossless de cada caso, a las mismas
dimensiones, conservando su perfil/color management documentado. Guardar el
proyecto de QA para reproducirlo. Una captura de pantalla prueba que se ejecutó
la interfaz; no sirve para medir precisión de la LUT.

El comparador preparado en [QA_EDITORES_03.md](QA_EDITORES_03.md) exige PNG con
ICC, mismas dimensiones y sin alfa. Codex lo ejecuta sobre **exports reales** y
conserva hashes, error RGB y ΔE76. Si la salida de Resolve no lleva ICC, no añadir
la etiqueta sRGB por suposición para hacer pasar el comparador: registrar dominio
y conversión verificables, o **BLOCKED_DOMAIN**, antes de compararla.
Investigar una identidad que supere el redondeo esperado de1LSB; no cambiar las
tolerancias después para ocultar errores de gamma/niveles o diferencias estéticas.

Registrar por caso: versión de Color Studio/Resolve/Windows, hash de candidato
y kit, configuración cromática/interpolación, fecha, PASS/FAIL/BLOCKED/NO EJECUTADO,
esperado, observado y hashes de los exports. En GitHub solo entra un resumen sin
usuarios, seriales, rutas privadas, fotografías personales o logs completos.
Los archivos y cualquier material privado se devuelven por el canal acordado.

## Estado de esta entrega

| Comprobación real pendiente | Estado |
|---|---|
| Registro/descarga oficial por el operador | not_run |
| Hash/firma/licencia del instalador recibido | not_run |
| Instalación y arranque de Resolve gratuito | not_run |
| Importación y exports E01–E05 en Resolve | not_run |
| Comparación métrica de exports reales | not_run |
| Photoshop/Premiere con licencia y sesión operativa | not_run |
| Aceptación visual/humana de compatibilidad | pendiente, no concedida |

La comprobación de hashes del kit y el análisis escalar ya existente no cambian
esos estados. El siguiente paso dependiente del operador es completar el registro
oficial y proporcionar el archivo. La solicitud se coordina en
[Issue67](https://github.com/jea27/Lut_generator/issues/67), sin duplicar avisos.
