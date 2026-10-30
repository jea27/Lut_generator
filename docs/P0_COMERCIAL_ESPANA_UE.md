# COL-005 · Investigación comercial y comercialización en España/UE

**Corte documental:** 30 de octubre de 2026. **Estado:** investigación de fuentes
primarias públicas; no son entrevistas, compras, dictamen jurídico ni decisión
de precio. Las páginas de precios pueden cambiar y algunas páginas de un mismo
proveedor muestran tarifas incompatibles.

## Comparativa comercial observada

Precios transcritos tal como aparecen en las páginas oficiales consultadas; no
se han convertido divisas ni normalizado impuestos, región, promoción, versión
o límites de uso. No equivalen a una comparación de producto ejecutada.

| Oferta | Modelo y precio publicado | Lectura para LumaForge | Fuente / salvedad |
|---|---|---|---|
| Luttie Pro | Gratis para edición básica; pase de 7 días $12; mensual $21.99; acceso de por vida $109 (la página anuncia próximos tramos $149/$199) | Caso claro de uso episódico: acceso temporal y lifetime compiten con suscripción. Exportación LUT y matching están en Pro. | [Precios](https://luttie.app/pricing); página consultada el 30-10-2026. El precio de por vida es promocional y limitado según el proveedor. |
| fylm.ai | Gratis; Lite $7/mes y Pro $15/mes facturados anual; Team $30/mes facturado anual, desde 3 usuarios | Freemium y segmentación por proyecto individual, colaboración y almacenamiento. Sus costes recurrentes se justifican también por funciones cloud/equipo. | [Precios](https://fylm.ai/pricing/); página consultada el 30-10-2026. No atribuir esos importes a facturación mensual. |
| Colourlab Ai 4 | Producto: $49/mes, $399/año o $799 perpetuo. Otra página de precios repite ese cuadro; documentación de licencias/condiciones muestra $49/mes, $490/año o $980 perpetuo. | Escalera entre suscripción y perpetua; análisis detallado consume créditos en documentación de licencias. Windows aparece como próximo/pendiente, no como disponibilidad comprobada. | [Producto](https://colourlab.ai/products/colourlab-ai-4/), [precios](https://colourlab.ai/pricing/), [licencia y activación](https://docs.colourlab.ai/installation/licensing-and-activation). **Discrepancia pública de tarifa**: confirmar moneda, edición, región y plan antes de cotizar. Página de producto consultada 30-10-2026. |
| Neurapix | Página global muestra $0.04 por foto sin suscripción, o Unlimited $49.95/mes (facturación anual $599.40, excl. IVA); complementos de consistencia/recorte suman $0.01/foto | Pago por volumen ofrece entrada sin cuota fija; el ilimitado sirve a usuarios con alto volumen. Foto/LR, no el mismo alcance que una herramienta foto-vídeo local. | [Precios](https://neurapix.com/); consultado 30-10-2026. La página global mostró USD; no se verificó precio localizado para España. |
| Imagen AI | El estudio previo registró desde $0.05/foto más $7/mes; no se revalidó esta cifra en esta consulta | Referencia de consumo y cuota base, no se debe presentar como tarifa vigente sin nueva comprobación. | [Página de producto/precios](https://imagen-ai.com/solution/time-saving-photo-editing-software-for-professionals/); dato heredado pendiente de verificar. |

### Opciones de monetización que merece la pena contrastar

1. **Gratis limitado + licencia individual de pago único.** Se ajusta a procesamiento
   local y uso episódico; hay referentes públicos con lifetime, pero el soporte,
   compatibilidad futura y coste de mantenimiento no desaparecen al cobrar una vez.
2. **Pase temporal o licencia por proyecto.** Tiene precedentes explícitos en
   Luttie y puede reducir fricción para trabajos puntuales; requiere validar si
   la gente compra solo cuando tiene un encargo.
3. **Suscripción anual/mensual.** Es defendible si hay valor recurrente concreto
   (biblioteca, sincronización, soporte, colaboración o actualizaciones continuas).
   Cobrar suscripción por un motor local sin servicio continuo necesita evidencia.
4. **Pago por foto/créditos.** Tiene precedentes en edición fotográfica. No es
   preferible para una función determinista local sin coste marginal por uso;
   puede servir solo para una capacidad remota opcional con coste variable visible.
5. **Paquetes de looks/actualizaciones.** Puede complementar producto base, con
   derechos y alcance de licencia de cada paquete claramente separados.

**Recomendación de investigación, no de precio final:** mantener el experimento
COL-005 de 49 € como estímulo fijo de entrevista ya documentado y contrastarlo
frente a opciones explícitas de uso (licencia local única, pase/por proyecto,
suscripción solo con servicios recurrentes). No cambiar el cuestionario ni
publicar una oferta hasta que el propietario revise la solicitud vigente #15.
No extrapolar preferencias declaradas a conversión, ingresos o TAM.

## Esquema de licencias a decidir antes de vender

- **Titularidad del software propio:** llevar inventario de autores/contribuciones,
  avisos de copyright y dependencias. En España los programas de ordenador están
  sujetos a derechos de explotación, entre ellos reproducción, adaptación y
  distribución; una licencia de uso debe especificar concesión, duración,
  dispositivos/activaciones, uso comercial, actualizaciones y soporte. Véase
  [TRLPI consolidado, arts. 95–100](https://www.boe.es/eli/es/rdlg/1996/04/12/1/con/20200708).
- **Licencia de terceros:** no basta con que una librería sea gratuita. Auditar
  código, assets, fuentes, modelos y pesos por separado; registrar versión,
  licencia, obligaciones de atribución/avisos, redistribución y modificaciones.
  La auditoría existente de CanonCGT distingue código/pesos de derechos de sus
  conjuntos de entrenamiento; aplicar la misma separación a cualquier modelo.
- **Elección de producto:** licencia propietaria local o núcleo abierto con
  componentes comerciales son opciones distintas. Mantener un SBOM/NOTICE y
  revisar compatibilidad antes de empaquetar. No reutilizar LUTs, presets, fotos
  o modelos solo porque sean visibles en la web.
- **Uso profesional del resultado:** separar licencia del programa y permisos
  sobre el contenido de origen. Indicar que el cliente conserva responsabilidad
  por derechos de sus imágenes/referencias y que el programa no transfiere
  derechos de autor de una referencia ajena.
- **Dependencias con copyleft o codecs:** evaluar distribución enlazada,
  modificaciones, ofertas de código fuente y avisos para la compilación concreta.
  La presencia de FFmpeg no permite inferir la obligación sin revisar su build y
  configuración; mantener el análisis específico registrado en
  [FFmpeg legal](https://www.ffmpeg.org/legal.html).

## Lista de comprobación para una venta B2C desde España

Esto identifica temas a resolver con asesoría fiscal/jurídica antes de cobrar;
no determina la forma societaria, alta, tratamiento de cada SKU ni textos finales.

| Área | Implicación inicial para LumaForge | Evidencia oficial |
|---|---|---|
| Información del vendedor y e-commerce | Publicar identidad y datos de contacto exigibles, características/compatibilidad, precio total e impuestos/cargos, duración/renovación/cancelación y proceso contractual; confirmar el contrato en soporte duradero. Revisar LSSI-CE y normativa española de consumo. | [LSSI-CE consolidada](https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758); [BOE TRLGDCU](https://www.boe.es/buscar/act.php?id=BOE-A-2007-20555). |
| Botón y pedido | El paso final debe dejar inequívoco que el pedido obliga a pagar; no esconder la cuota o renovación. | [Your Europe: venta B2C a distancia](https://europa.eu/youreurope/business/selling-in-eu/selling-goods-services/ecommerce-distance-selling/index_en.htm). |
| Desistimiento y descarga | Regla general de venta a distancia: 14 días. La excepción para contenido digital sin soporte físico requiere consentimiento expreso previo para iniciar la ejecución durante ese período, reconocimiento expreso de pérdida del desistimiento al empezar y confirmación contractual. No usar casilla premarcada ni asumir que cualquier licencia/servicio cae automáticamente en esta excepción. | [Directiva 2011/83/UE, arts. 9 y 16(m)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32011L0083); [guía UE](https://europa.eu/youreurope/business/selling-in-eu/selling-goods-services/ecommerce-distance-selling/index_en.htm). |
| Conformidad de contenido digital | Software vendido a consumidores puede estar sujeto a reglas de conformidad, actualizaciones y remedios; redactar soporte/compatibilidad y ciclo de actualizaciones de forma coherente. | [Directiva (UE) 2019/770](https://eur-lex.europa.eu/eli/dir/2019/770/oj). |
| IVA transfronterizo | Un servicio electrónico B2C puede tributar donde reside el cliente. La UE publica un umbral conjunto de 10.000 € para ciertas operaciones B2C transfronterizas de servicios TBE y ventas intracomunitarias, sujeto a condiciones y cálculo del año actual/anterior; OSS puede centralizar declaraciones. Confirmar si cada venta de licencia descargable se clasifica como servicio electrónico y régimen aplicable con asesoría/AEAT. | [Comisión Europea: OSS y umbral](https://vat-one-stop-shop.ec.europa.eu/one-stop-shop_en); [lugar de tributación](https://taxation-customs.ec.europa.eu/taxation/vat/vat-directive/place-taxation_en); [AEAT, IVA](https://sede.agenciatributaria.gob.es/Sede/iva.html). |
| RGPD y medios | Una foto/vídeo donde una persona sea identificable puede ser dato personal. Procesamiento local reduce transferencias, pero no elimina obligaciones de la web, compras, soporte, telemetría o copias en nube del usuario. Definir finalidades/base jurídica, minimización, plazos, medidas y contratos con procesadores; DPIA si el tratamiento probablemente entrañe alto riesgo. | [EDPB para pequeñas empresas](https://www.edpb.europa.eu/sme/learn-the-basics/data-protection-basics_en); [EDPB: seguridad](https://www.edpb.europa.eu/sme/be-compliant/secure-personal-data_en). |
| Cookies/analítica | Inventariar cookies y almacenamiento/acceso no esencial de la web de venta; habilitar consentimiento previo cuando corresponda y ofrecer rechazo/configuración real. El caso de app local y una web promocional tiene superficies distintas. | [LSSI-CE, art. 22.2](https://www.boe.es/buscar/act.php?id=BOE-A-2002-13758); [guía de cookies AEPD](https://www.aepd.es/guias/guia-cookies.pdf). |
| Accesibilidad | Evaluar la aplicación de la European Accessibility Act a los servicios de comercio electrónico. La Directiva contempla exención para microempresas que prestan servicios; verificar definición/alcance y obligaciones nacionales antes de depender de ella. Mantener una UI accesible como requisito de producto aunque se aplique exención. | [Directiva (UE) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj); [Comisión: Accessibility Act](https://ec.europa.eu/social/main.jsp?catId=1202). |

## Decisiones comerciales pendientes

1. Segmento y canal: sigue sin evidencia primaria; revisar COL-001/002 y solicitud
   de revisión de hipótesis #15 antes de congelar un concepto comercial.
2. Precio y periodicidad: no elegir hasta contrastar el estímulo 49 € con conducta
   observada y con un producto demostrable; impuestos/cambio de divisa alteran
   precio final al consumidor.
3. Distribución: instalador directo, tienda/plataforma y procesador de pagos
   cambian obligaciones, comisiones, IVA, reembolsos y gestión de renovaciones.
4. Mercado inicial: España únicamente reduce localización inicial; vender en UE
   exige resolver precio/IVA por país, consumo, privacidad, soporte e idioma.
5. Asesoría antes de cobro: validar forma empresarial/fiscal, texto contractual,
   desistimiento y VAT/OSS con profesionales antes de poner checkout en marcha.

## Estado de evidencia

- Desk research actualizado; sin entrevistas nuevas, venta, test de precio,
  compras, benchmark de herramientas o asesoramiento legal individual.
- No se modifican las hipótesis ni se presenta la preparación como aceptación de
  COL-005. La Issue #13 permanece en revisión y la solicitud humana existente #15
  se reutiliza; no se genera otra notificación.
- Fuentes consultadas el 30-10-2026 salvo donde se indique. Revalidar páginas,
  tasas y derecho vigente antes de comercializar.
