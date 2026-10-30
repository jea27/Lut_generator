# COL-002 · Operativa de entrevistas y control de actas

Issue #16. **0 entrevistas recibidas o realizadas por el agente**. Criterio
final: al menos 12 actas anonimizadas con frecuencia, soluciones actuales e
intención de pago. El registro vacío no cumple ese criterio.

Se reutilizan los instrumentos COL-001 y COL-005 ya preparados; no se repiten
preguntas ni se crea una cohorte adicional. Objetivo: 4 A, 4 B y 4 C/D. Asignar
un código único E01…E99 por persona, un segmento principal y contarla una sola vez.
Los códigos no prueban identidades distintas: lo controla quien entrevista.

## Preparación y ejecución humana

1. El usuario aporta participantes o autoriza expresamente contactar candidatos.
   No se envían mensajes de reclutamiento desde esta entrega. No se recopilan
   nombres/contactos en el repositorio ni se pide al usuario publicarlos en Issues.
2. Revisar guion y consentimiento para notas; grabación requiere autorización
   específica aparte. Si no hay permiso, no guardar notas atribuibles ni una
   ficha completa para contarla como evidencia disponible.
3. Entrevistar con el orden de COL-005, sin revelar precio antes de tiempo ni
   ofrecer funciones inexistentes. Registrar desconocimiento o negativa tal cual.
4. Mantener las actas completas en almacenamiento privado controlado por el
   usuario. Revisar redacción de cualquier extracto y eliminar identificadores.
5. Registrar solo el resumen anonimizado y la referencia REDACT-E… de revisión.
   Antes de compartirlo en público, el usuario revisa también posibles
   identificadores indirectos (proyectos, marcas, citas o fechas muy precisas).
6. Sintetizar situaciones repetidas en COL-001 y respuestas comerciales en
   COL-005. No convertir la validación de formato en validación de hipótesis.

## Registro y validador

`data/p0/interviews.json` contiene una lista vacía intencional. Un registro real
complete utiliza: id, segmento A/B/C/D, fecha ISO, notes_consent true,
anonymized true, redaction_record_id REDACT-E01 (según código), frequency_30d
entero no negativo o null, current_solution, problem_summary, pay_intent y
evidence_type interview_notes. No usar comentarios de ejemplo como respuestas.

pay_intent: buy_if_conditions, consider, not_buy, unknown o declined. No se
cuenta ninguno como compra. Las respuestas ausentes se conservan (null o
categoría explícita); no se imputan ceros o sí. Las actas pueden estar completas
como sesiones aunque haya negativas/desconocimiento; se informa missing_answers.
El análisis de H1/H2/H3 sigue reglas propias y no sale de ese contador.

Los campos de contacto o cualquier otro campo fuera del esquema se rechazan;
los campos de texto requieren revisión humana porque un validador no puede
garantizar anonimización semántica. El informe solo publica contadores y códigos
de error por índice, no respuestas, rutas privadas o valores rechazados.

```powershell
python scripts/validate_interviews.py
python scripts/validate_interviews.py RUTA_PRIVADA_AL_REGISTRO --ready --as-of 2026-10-30
python -m unittest discover -s tests -v
```

Exit 0: esquema correcto; con --ready, checklist de 12 actas y cuotas completo.
Exit 2: todavía faltan actas/cuotas. Exit 1: formato/datos rechazados.
Revisar la fecha de --as-of al reanudar; no aceptar sesiones futuras. El script
no verifica que una conversación ocurrió ni aprueba una tarea: audita datos
aportados y declaraciones de consentimiento/redacción, no su veracidad externa.

## Bloqueo real y siguiente paso

Se puede preparar y probar el registro ahora; no es posible obtener entrevistas
reales inventando respuestas. Se necesita que el usuario realice las primeras
entrevistas o autorice un canal y candidatos concretos. Recomendación: comenzar
con una persona por segmento, revisar el guion y continuar hasta cubrir 12.
No se paga, recluta ni publica datos privados sin autorización específica.

Las pruebas usan entradas sintéticas solo en memoria. No se escriben al
registro real ni se cuentan como investigación. COL-001 permanece pendiente.
