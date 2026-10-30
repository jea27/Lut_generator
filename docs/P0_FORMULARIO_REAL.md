# COL-002 · Formulario y recibos de investigación real

Instrumento **preparado, sin participantes ni respuestas reales**. Issue #16.
Complementa el cuestionario COL-005; no sustituye las 12 entrevistas del gate.

## Uso local sin proveedor externo

Abrir `research/form.html` en un navegador moderno; si file:// restringe scripts,
usar `python -m http.server 8765 --bind 127.0.0.1 --directory research` desde
esta carpeta. Visitar http://127.0.0.1:8765/form.html. No exponer 0.0.0.0,
publicar en Pages, usar túneles ni activar un proveedor de formularios.
No hay envío, analítica ni persistencia del formulario. Exporta JSON local;
el participante decide compartirlo por un canal privado previamente acordado.

Tres etapas guardan respuestas antes de mostrar estímulos: Q1–Q8 trabajo real;
Q9–Q11 concepto e importe espontáneo; Q12–Q15 escenario 49 € y cierre. Preguntas
opcionales, omisión/negativa conservadas; no se imputan como compra ni como cero.
La versión y fechas de etapa quedan en el archivo. El código R001–R999 es
asignado por el responsable, sin nombre, email ni empresa. Los tiempos y códigos
son autodeclarados: no acreditan por sí solos persona real ni ausencia de fraude.

## Registro verificable, sin inventar verificación

1. Antes de distribuir: jea27 define canal privado, candidatos autorizados,
   responsable y plazo de conservación; entrega información de participación y
   retirada. No contactar personas por iniciativa del agente. La recepción local
   de un JSON no autoriza publicar su texto ni contactar de nuevo.
2. Participante revisa/elimina identificadores de sus respuestas y comparte
   voluntariamente el JSON por ese canal. No subirlo a Issue/PR ni al sitio.
3. Operador: `python scripts/register_form_response.py RUTA_PRIVADA.json`.
   El original y su recibo SHA-256/fecha de recepción quedan en
   `.research-private/responses/`, ignorado por Git. No sobrescribe ni duplica
   código, ID o hash. Correcciones/retiradas las gestiona el responsable:
   mantener control de versiones privado o eliminar según la petición.
4. Revisar identidad de sesión con el canal de reclutamiento, consentimiento,
   coherencia/omisiones, códigos únicos y anonimización. Registrar privadamente
   quién verificó, cuándo, método, limitaciones y referencia al recibo. Un hash
   demuestra integridad, **no** autenticidad ni consentimiento efectivo.
5. Solo una entrevista realmente celebrada y documentada puede incorporarse al
   registro `interviews.json` con acta/REDACT y criterios existentes. No convertir
   automáticamente un formulario en `interview_notes`. Síntesis pública solo
   agregada, revisada y sin texto identificativo ni contactos.

Fixtures sintéticas solo viven en tests temporales. El registro de entrevistas
permanece vacío; ninguna respuesta real se genera para demostrar la UI. No se
añade un formulario al dashboard publicado ni se contrata servicio externo.

## Petición mínima al responsable

Recomiendo que jea27 distribuya personalmente el instrumento a tres personas
conocidas (A, B y C/D), por su canal privado habitual, y indique responsable y
plazo de conservación. Alternativa: autorizar explícitamente al agente canal,
destinatarios y texto antes de cualquier contacto. No hace falta publicar una
base de datos ni facilitar al agente direcciones personales en GitHub.
