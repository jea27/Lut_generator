# LumaForge — Investigación de mercado y posicionamiento
**Fecha de corte:** 30 de octubre de 2026. **Estado:** desk research; no incluye entrevistas primarias ni pruebas propias de los productos. **Nombre:** provisional, sin comprobación de marca/dominio.

## Resumen ejecutivo

- **La categoría ya existe.** Color matching de referencia, 3D LUT automáticas y edición IA tienen competidores bien establecidos, productos web y proyectos open source. La ventaja no puede ser «convertir una foto en LUT» por sí sola.
- **Hipótesis de producto a validar:** solución local centrada en Windows que genera looks portables para foto y vídeo, permite inspeccionar el ajuste y aplica adaptación contextual opcional sin suscripción obligatoria.
- **Ruta comercial sensata:** elegir primero un caso de uso específico (p. ej., creador híbrido que usa Photoshop y Premiere/Resolve), probarlo frente a herramientas existentes y medir intención de pago antes de invertir en IA semántica avanzada.
- **No hay base para afirmar una cifra de mercado (TAM/SAM/SOM).** Falta definir cliente, geografía, precio realizado y conversión. Una encuesta sobre adopción de IA no es una estimación del mercado direccionable.

## Panorama de competidores (precios publicados, no auditados mediante compra)

| Producto | Solución | Precio observado | Implicación |
|---|---|---|---|
| Colourlab Ai 4 | Matching por referencia, auto balance, pipeline audiovisual | USD 49/mes; USD 399/año; USD 799 perpetuo | Competidor técnico de alto nivel. La versión 4 comienza en Apple Silicon; Windows planificado, no permanente. |
| Luttie | Color Match Pro en navegador, intensidad, LUT | Pro USD 21,99/mes; acceso semanal y perpetuo | Competidor muy directo de UX y exportación. Afirma ejecución sin subir las imágenes. |
| fylm.ai | Editor web, extracción, matching, looks, colaboración | Free; Lite USD 7/mes anual; Pro USD 15/mes anual | Demuestra que existe una alternativa económica. |
| ShotMatch | Foto/vídeo, referencia, presets y export LUT | Consultar precio vivo | Requiere benchmark en varias escenas y distintos vídeos. |
| Neurapix | SmartPresets y edición fotográfica para Lightroom | Desde 0,04 €/foto; ilimitado 49,95 €/mes facturado anual | Gran foco foto y consistencia. |
| Imagen AI | Edición a escala, perfiles y IA por fotografía | Desde 0,05 USD/foto + 7 USD/mes de base | Modelo de consumo frente a modelo local. |
| Aftershoot | Culling, edición y retoque local | Edición desde USD 30/mes anual | Local/offline ya es oferta existente; no es ventaja única. |
| DaVinci Resolve | Herramientas profesionales de matching/color | Versión gratuita disponible | Sustituto muy potente si el usuario ya sabe etalonar. |
| Kalora (Gumroad) | Imagen + destino → LUT para vídeo | Oferta de descarga, precio variable | Muestra barrera baja de herramientas económicas. |
| REFGRADE (open source) | Motor híbrido referencia + LUT + integración Resolve | Repositorio público | Muestra que parte de la arquitectura es replicable. Auditar licencias antes de reutilizar código. |

**Fuentes primarias:**
- Colourlab: https://colourlab.ai/products/colourlab-ai-4/ y https://colourlab.ai/pricing/
- Luttie: https://luttie.app/docs/color-match y https://luttie.app/pricing
- fylm.ai: https://fylm.ai/pricing/
- ShotMatch: https://shotmatch.io/
- Neurapix: https://neurapix.com/es/
- Imagen: https://imagen-ai.com/solution/time-saving-photo-editing-software-for-professionals/
- Aftershoot: https://aftershoot.com/
- Kalora: https://toolandkits.gumroad.com/l/shbqbn
- REFGRADE: https://github.com/Aasishmuchala/DavinciPlugin

## Señales de demanda y limitaciones

Adobe publicó en junio de 2026 una investigación con varias fuentes, incluida encuesta a 1.433 creativos de EE. UU. y Reino Unido; comunica un 45,1% de uso sustancial de IA generativa para retoque de color/tono entre profesionales estadounidenses de fotografía. Es un indicador de adopción de herramienta, no de deseo de pagar por nuestro producto. https://www.adobe.com/ai/research/202606/ai-is-redistributing-creative-work.html

Otra encuesta de Adobe Express a 384 creadores de vídeo de EE. UU. comunica que 71% había usado herramientas de generación/edición de vídeo con IA y que 56% declaraba ahorrar más de 30 minutos por vídeo. Las muestras, preguntas y segmentaciones no son equivalentes. No extrapolar a todo el sector audiovisual. https://www.adobe.com/express/learn/blog/ai-video-tools

## Segmentos y jobs-to-be-done

### A. Creador híbrido foto + vídeo (hipótesis prioritaria)
- Necesidad: identidad cromática consistente entre fotografías del mismo proyecto y vídeos de redes.
- Herramientas habituales: Photoshop/Lightroom + Premiere/Resolve/CapCut.
- Compra si: prueba rápida, compatible, calidad consistente y evita suscripción adicional.
- Barrera: se conforma con LUT gratuitas o con presets comprados.

### B. Fotógrafo de eventos / bodas
- Necesidad: aplicar estilo en cientos de fotografías tomadas bajo luces variables.
- Compra si: la adaptación local supera las LUT genéricas en personas y calidad.
- Barrera: imagenes RAW, integración Lightroom y modelos entrenados a su propio estilo (Imagen/Neurapix/Aftershoot).

### C. Videógrafo indie / editor
- Necesidad: homogeneizar cámaras y escenas, look reproducible entre planos.
- Compra si: no rompe pieles, gamut ni continuidad temporal.
- Barrera: flujo de color profesional y fuerte presencia de Resolve/Colourlab.

### D. Influencer y aficionado
- Necesidad: un resultado inmediato sin dominar herramientas pro.
- Compra si: onboarding muy simple y precio reducido.
- Barrera: disposición a pagar incierta; herramientas gratuitas.

## Mapa de posicionamiento propuesto (NO validado)

- **Qué vendemos:** del fotograma de inspiración a un estilo ajustable y reutilizable, en varios editores, con procesamiento local.
- **No vendemos:** copia exacta del preset original de un tercero, reconstrucción de máscaras de un LUT o colorimetría profesional completa desde la primera versión.
- **Diferenciador a probar:** receta portable + LUT + adaptación contextual y corrección humana en una sola UX.
- **No competir solo por precio**: fylm.ai y opciones gratuitas ponen techo a la utilidad de una herramienta superficial.

## Modelo de ingresos — pruebas, no precios definitivos

Probar tres esquemas en entrevistas con conceptos y demo comparables:
1. Gratis limitado, licencia local de pago único de **29–79 €** para uso individual.
2. App gratis + paquetes de estilos o herramientas avanzadas de pago único.
3. Suscripción **5–12 €/mes** solo si aporta funciones recurrentes valiosas (sin imponerla para procesamiento básico).

Estas bandas son **hipótesis de test**, no previsiones de ingresos ni precios acordados. Deben compararse contra disposición de pago real y costes de soporte. No prometer IA remota ilimitada sin coste variable.

### Estimación del coste inicial de infraestructura (no presupuesto cerrado)
- GitHub Pages / Cloudflare Pages: puede caber en planes gratuitos según uso, límites y políticas vigentes.
- Dominio: gasto anual variable; no necesario para probar el MVP.
- Motor CPU y modelos locales: sin coste por llamada API, pero con energía, equipo, soporte y mantenimiento.
- IA remota opcional: 0 € si no se activa; coste variable si se usa. Requerirá política de consentimiento y límite de consumo.
- Coste humano y tiempo del desarrollador: **principal coste**, no incluido en cuentas de hosting.

## Investigación primaria: guion y criterios go/no-go

**Entrevistar a 12 personas**: al menos 4 del grupo A, 4 del B y 4 del C o D; registrar software, número de imágenes/clips por semana, tiempo perdido, solución actual y ejemplos de resultados fallidos.

**Cinco productos para benchmark mínimo:** Luttie, fylm.ai, DaVinci Resolve, una opción local gratuita y Colourlab (si hay hardware/licencia disponible). Usar el mismo dataset de 20 pares fuente-referencia; retratos con diferentes pieles e iluminación, paisajes, interiores, mezclas de color, nocturnas, contraluces. Cuidar consentimiento y licencias.

**Métricas piloto propuestas:**
- 70% de preferencia ciega por la salida del MVP frente a baseline clásico *en conjunto de evaluación* (objetivo exploratorio; ajustar por dificultad y muestra).
- 5/5 usuarios completan importar → comparar → ajustar → exportar sin asistencia crítica.
- Al menos 4/12 entrevistados declaran haber pagado o estar dispuestos a un ensayo pagado real, mejor que una pregunta hipotética de disposición.
- 0 fallos graves de color manager en el conjunto piloto; no usar una métrica única para juzgar la estética.

**Go:** evidencia de una necesidad repetida, mejora percibida y prueba de pago. **Pivot:** calidad aceptable pero poco interés por pagar; enfocarse en integración/editor/mercado. **Stop:** resultados inferiores a alternativas fáciles y sin necesidad insatisfecha.

## Supuestos y amenazas

- Una sola referencia visual no identifica el preset original; distintos colores de escena y posprocesado pueden generar la misma apariencia final.
- Un LUT 3D transforma color global; no representa cambios espaciales, piel con máscara o retoques locales independientes.
- Las pantallas, perfiles ICC, gamma, Rec.709, Log y HDR alteran la percepción y el resultado exportado.
- Derechos de muestras, frames de películas y modelos de IA requieren revisión antes de distribuir datasets o vender producto.
- Distribuir FFmpeg puede implicar obligaciones LGPL/GPL según compilación: https://www.ffmpeg.org/legal.html

## Resultado del desk research

**Recomiendo avanzar únicamente al prototipo técnico y validación inicial, no comprometer aún 20 semanas de desarrollo ni un modelo comercial fijo.** La hoja de ruta incluye puertas de decisión al final de cada fase.
