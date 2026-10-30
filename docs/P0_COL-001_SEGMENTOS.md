# COL-001 · Segmentos y trabajos por resolver

Estado: preparación local para revisión. Sin entrevistas realizadas ni evidencia
primaria registrada. Esta entrega no cumple todavía el criterio completo de
COL-001 ni autoriza el motor. Fuente: hipótesis del estudio de mercado heredado.

## Selección y dependencias

COL-001 es la primera tarea P0 planificada y no tiene prerrequisitos técnicos.
El JSON no contiene un grafo de dependencias; el siguiente orden es operativo,
no una modificación de la hoja de ruta:

| Tarea | Se puede preparar ahora | Evidencia necesaria para aceptar |
|---|---|---|
| COL-001 | Segmentos, guion y mapa inicial | Entrevistas y situaciones repetidas trazables |
| COL-002 | Plantilla y selección de participantes | 12 actas anonimizadas reales |
| COL-004 | Matriz de escenas y registro de permisos | 20 pares con permisos documentados |
| COL-003 | Plantilla de comparación | Dataset COL-004 y pruebas de 5 competidores |
| COL-005 | Hipótesis y cuestionario | Revisión humana de las tres hipótesis falsables |
| COL-006 | Plantilla de decisión | Evidencia P0, riesgos y go/no-go humano |

Issue canónica creada tras autorización el 30-10-2026:
https://github.com/jea27/Lut_generator/issues/6, abierta, roadmap y
status:in-progress. Sin entrevistas ni aceptación humana todavía.

## Segmentos candidatos

| Segmento | Situación a investigar | Trabajo esperado | Solución actual a preguntar | Señal que lo refutaría |
|---|---|---|---|---|
| A · Creador híbrido foto/vídeo | Entrega una misma campaña en fotos y clips | Conseguir un estilo coherente entre editores sin rehacer todo | LUT, presets, correcciones manuales, servicios | No mezcla foto/vídeo o la coherencia no es un problema recurrente |
| B · Fotógrafo de eventos | Edita lotes con distintas luces y personas | Reducir correcciones repetidas conservando piel y exposición | Presets propios, Lightroom, edición por lotes | El preset actual resuelve el trabajo con pocas correcciones |
| C · Videógrafo/editor | Igualar planos y referencias con distintas condiciones | Mantener intención estética y continuidad entre planos | Herramientas del editor, LUT, corrección manual | La herramienta actual es suficiente y el cambio de flujo no compensa |
| D · Creador ocasional | Busca aproximar una referencia sin dominar color | Obtener un resultado comprensible y ajustable | Apps móviles, filtros, LUT gratuitas | Poca frecuencia o ninguna acción para resolverlo |

Estas filas son hipótesis, no hallazgos. No se declara elegido el segmento ganador.
La propuesta previa prioriza A; debe contrastarse con B y C/D.

## Plan de entrevistas

Objetivo heredado: 12 participantes, al menos 4 de A, 4 de B y 4 de C o D.
Entrevistas de 25–35 minutos realizadas por el usuario o con su autorización
expresa para contactar participantes. No se han enviado mensajes ni reclutado.

1. Pedir permiso para tomar notas; grabar solo con consentimiento específico.
2. Preguntar por el último proyecto real, antes de presentar LumaForge.
3. Recorrer herramientas, volumen, pasos y correcciones; buscar un ejemplo
   concreto reciente, no opiniones generales sobre IA.
4. Preguntar frecuencia, minutos invertidos y consecuencias del fallo.
5. Registrar qué pagó o probó realmente y quién decide la compra. No sugerir
   precios durante el descubrimiento ni prometer resultados de un motor inexistente.
6. Al final presentar la hipótesis local/portable y preguntar qué cambiaría
   en su flujo y qué le impediría probarla. Separar esas opiniones de conducta real.

Preguntas base:

- Cuéntame la última vez que quisiste reproducir un estilo de otra imagen o plano.
- ¿Qué entregabas, con qué herramientas y cuántas imágenes o clips había?
- ¿Cómo resolviste exposición, piel y diferencias entre escenas?
- ¿Qué parte tuviste que repetir? ¿Puedes describir un fallo concreto?
- ¿Con qué frecuencia sucede y cuánto tiempo estimas que consume?
- ¿Qué has intentado cambiar? ¿Qué herramienta has comprado o descartado y por qué?
- ¿Necesitas trabajar sin conexión o mover el look entre distintos editores?
- ¿Qué tendría que demostrar una prueba para que decidieras usarla de nuevo?

## Registro de evidencia

Usar códigos E01…E12. No publicar nombres, contactos, grabaciones ni medios de
clientes. Las actas compartidas se anonimizan; cualquier material privado se
mantiene fuera del repositorio y del dashboard. No crear ni subir muestras sin
permisos específicos.

| Código | Fecha | Segmento | Trabajo reciente | Frecuencia | Tiempo declarado | Solución actual | Fallo observado/declarado | Evidencia anonimizada |
|---|---|---|---|---|---|---|---|---|
| Pendiente | — | — | — | — | — | — | — | Sin entrevistas |

Cada acta debe separar hechos observados, declaraciones del participante,
estimaciones e interpretación del investigador. Registrar también desacuerdos
y ejemplos donde la solución actual funciona bien.

## Mapa de situaciones repetidas

Completar después de las entrevistas. No convertir las hipótesis en evidencia.

| Situación repetida | Códigos de entrevistas | Nº participantes/total | Impacto | Alternativa actual | Necesidad sin resolver |
|---|---|---|---|---|---|
| Pendiente de investigación | — | 0/0 | Sin medir | Sin contrastar | Sin validar |

Una situación se propondrá como repetida si aparece en al menos dos actas
independientes, siempre mostrando el denominador y el segmento. Es una regla
de síntesis exploratoria, no evidencia de representatividad estadística.

## Revisión humana y siguiente paso

El usuario revisa este guion y comienza entrevistas; se incorporan actas
anonimizadas y se completa el mapa antes de aceptar COL-001. La preparación
documental puede revisarse mediante PR, pero no cerrar ni aprobar la Issue.
COL-006 exige además 12 entrevistas, 20 pares y benchmark de 5 productos.
P1 permanece detenido hasta esa decisión o autorización explícita del usuario.
