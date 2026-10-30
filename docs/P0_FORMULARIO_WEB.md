# COL-005 · Enlace web y primer lote de investigación

Reutiliza Issues #13 y #16. Esta entrega amplía el formulario preparado en PR33;
no ejecuta entrevistas ni cambia el consentimiento o el esquema JSON v1.

## Enlace y publicación

Ruta prevista en el alojamiento existente:
https://jea27.github.io/Lut_generator/investigacion/

Solo se considera publicada tras merge humano y Actions correctas, seguido de
comprobación HTTP y de navegador. La rama no publica Pages ni el agente fusiona.
No se crean proveedores, bases de datos ni permisos nuevos. Dos workflows de
Pages empaquetan los mismos tres archivos permitidos desde research/; así una
sincronización posterior no elimina el formulario. Los datos permanecen fuera
del artefacto: solo HTML, CSS y JavaScript. Fuente única en research/.

## Tres códigos preparados, aún sin asignar

| Código | Enlace previsto | Estado |
|---|---|---|
| R101 | https://jea27.github.io/Lut_generator/investigacion/#R101 | Reservado, no distribuido |
| R102 | https://jea27.github.io/Lut_generator/investigacion/#R102 | Reservado, no distribuido |
| R103 | https://jea27.github.io/Lut_generator/investigacion/#R103 | Reservado, no distribuido |

El fragmento precarga únicamente el código: no contiene nombre/email ni se envía
como parte de la petición HTTP. No es contraseña ni prueba de identidad.
No asignar códigos automáticamente a participantes inexistentes. La tabla
privada código-persona la custodia jea27, fuera de Git; nunca se publica.
R999 sigue reservado para QA sintética, sin contar como respuesta real.

## Consentimiento y privacidad conservados

La casilla voluntaria mantiene su texto: notas anonimizadas para investigación,
posibilidad de retirada, sin autorizar contacto ni publicación de respuestas.
Ninguna casilla se premarca desde el enlace. Las respuestas solo viven en memoria
de la pestaña; descargar/compartir requiere acción del participante. Sin fetch,
analítica, cookies propias ni almacenamiento persistente. Referrer no-referrer y
CSP connect-src/form-action none. Solo se permite script/estilo del propio sitio.

El alojamiento sí recibe peticiones de archivos públicos. GitHub documenta que
[Pages registra IP para seguridad](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).
No se promete anonimato de navegación ni que GitHub deje de procesar datos
técnicos. Abrir el formulario no transmite respuestas al alojamiento.

Antes de distribuir, jea27 comunica por el canal privado responsable/contacto,
finalidad, conservación y forma de retirada. Responsable/plazo recomendados en
#29 siguen siendo propuestas, no acuerdos inventados. El agente no contacta
participantes ni publica datos privados. No compartir el enlace como invitación
definitiva sin esa información; sí se puede usar para prueba técnica R999.

## Recoger e importar JSON por canal privado

1. Responsable acuerda un canal privado ya utilizado con la persona (por ejemplo,
   conversación individual o carpeta con acceso restringido); sin publicar aquí
   direcciones, nombres, credenciales ni enlaces de acceso privado.
2. Entrega un código de la tabla a una sola persona y registra privadamente la
   asignación/fecha/versión de información y consentimiento. No presupone segmento.
3. Participante completa las etapas y prepara JSON. Puede revisar el archivo,
   descargarlo a Archivos/Descargas o abrir el menú nativo de compartir cuando
   esté disponible. Elige el destinatario privado acordado. Cancelar no confirma
   envío; la aplicación tampoco confirma recepción porque se abrió ese menú.
4. Recibir el archivo original como documento, sin pegar respuestas en Issues,
   renombrar extensiones, comprimir con pérdida ni editarlo para alterar respuestas.
   Confirmar el código por el mismo canal. Si hay identificadores, no publicarlos:
   gestionar corrección/retirada con el responsable y conservar solo lo autorizado.
5. Desde la raíz, PowerShell:

```powershell
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/register_form_response.py "RUTA_PRIVADA\R101-respuesta.json"
```

Original y recibo quedan en `.research-private/responses/`, ignorados. SHA-256
fija bytes recibidos; fecha de recepción no sustituye fecha de sesión. No se
sobrescriben ni duplican código/UUID/hash. No corregir el registro a mano para
saltar duplicados: gestionar la revisión privada conforme a P0_FORMULARIO_REAL.
Estado `submitted_unverified`, `counts_as_interview=false`; una respuesta solo
puede convertirse en evidencia de entrevista si esta se celebró realmente y
se documenta por separado. Nunca importar R999 en el registro de participantes.

## Verificación móvil

Probar 320/390/430 píxeles, retrato y paisaje, desplazamiento/zoom, consentimiento
sin premarcar, fragmento, tres etapas, Q11 antes del precio, vista previa JSON,
descarga y cancelación/fallback de compartir. [Web Share](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share)
requiere soporte/contexto seguro y elección del usuario; no se asume disponible.
Las pruebas de viewport en Chromium no son una prueba física de Safari/iPhone.
Antes de invitar personas: prueba real R999 en el iPhone, guardar a Archivos y
devolver el JSON sintético por el canal privado elegido. Esa prueba no es encuesta.
