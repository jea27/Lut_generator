# Look Match v1 · primera entrega manual · COL026 / #68

31-10-2026. Autorización explícita del usuario para implementación acotada,
independiente de IA local/P3 completa. No se afirma copiar fielmente el acabado
de una referencia; los parámetros se ajustan manualmente.

| Componente | Estado real |
|---|---|
| Color Match Lab/global | Existente, LUT33³ sRGB y controles separados |
| Glow/bloom de altas luces | Implementación inicial: extracción luminancia lineal sobre umbral, Gaussian blur y composición screen limitada |
| Difusión/blur suave | Implementación inicial: mezcla de blur lineal de radio relativo a lado corto, con alfa normalizado |
| Fade/atmósfera | Implementación inicial: elevación de negros y compresión de rango acotadas |
| Reducción de microcontraste | Efecto indirecto de difusión; sin módulo específico/frecuencias/controles dedicados |
| Halation | Pendiente: no simular que glow equivale a halation |
| Extracción del acabado desde referencia | Pendiente; ni modelo, estimador automático ni promesa de reconstrucción |
| Piel/óptica/consistencia temporal vídeo | Pendientes de imágenes autorizadas y experimentos |

## Contrato de receta y exportación

Recipe v2 incorpora look.enabled, strength, glow, diffusion, fade, radius y
threshold. Se aceptan recetas v1 sin acabado; UI las normaliza antes de editar.
No se aceptan efectos activados bajo version1 ni valores no finitos/fuera de
rango. Presets/JSON persistentes y lotes usan la misma receta. Efectos desactivados
o fuerza0 son bypass exacto del color. Intensidad de color0 no apaga acabado;
el acabado tiene su propio interruptor/intensidad. Cargar referencia vuelve a
calcular el color y conserva el acabado manual actual.

Orden: Color Match por la LUT33³ existente → difusión/glow en luz lineal → fade
acotado en sRGB codificado → intensidad del acabado. PNG/JPG incluyen todos los
efectos; alfa conservado y JPEG sobre blanco. El original no se escribe. La LUT
**solo lleva Color Match**, incluso fade se conserva deliberadamente en la
receta de acabado. Header y confirmación UI avisan al exportar .cube.

Radio normalizado respecto al lado corto (default0.008), sigma mínimo0.5px;
kernel finito3σ y halos de tile evitan discontinuidades. Cancelación cooperativa
entre bloques. RGB de píxeles invisibles no sangra a los visibles. No eliminar
ruido ni detalle perdido mediante afirmaciones sobre «reconstrucción».

## Pruebas y evidencia real

30 tests MVP pasan: identidad/compatibilidadv1, extremos finitos, halos entre
tiles <2e-6, transparencia, cancelación, reducción de borde por difusión,
propagación desde highlights, monotonicidad de fade, LUT independiente y
roundtrip de receta/preset/PNG a través de API.91 tests de seguimiento OK.
Fixtures prueban infraestructura matemática, no calidad de piel ni preferencia.

Benchmark real sobre CC0 rural4928×3264, receta en LOOK_03_BENCHMARK.json:
preview1024 ~0.729s; render completo+PNG32.392s, RSS muestreado815.4MB, original
intacto por SHA256 y dimensiones/ICC correctos. Proceso Python en este equipo,
no hardware externo ni promesa de rendimiento. Preview vs export reducido:
MAE RGB normalizado0.00476, P95 absoluto0.01455; resampling y radio mínimo producen
diferencias. No son un test de fidelidad al estilo de referencia ni garantía.

Revisión visual de LOOK_03_COLOR.jpg/FINISH.jpg: difusión y elevación de negros
visibles en paisaje; cielo ya recortado en entrada no recupera detalle. Textura
más suave, sin halos de tile aparentes en esa vista1024. No prueba al100% en
retratos ni aceptación humana. Autor Sergej Majboroda/Poly Haven, CC0 y hashes
en apps/demo/credits.json. Parámetros elegidos manualmente para QA, no inferidos.

Primera revisión externa: comparar al100%, escenas luminosas/oscuras, piel,
bordes de alto contraste y ruido; registrar aceptabilidad, halos/bleeding,
clipping y tiempos. Desactivar cualquier efecto perjudicial, mantener NO-GO
promesas de transferencia fiel. Ver BETA_QA_EXTERNA.md para cinco pruebas.


QA GUI adicional: preset v1 de fixture aplicado a foto CC0, acabado activado y
JSONv2 descargado, comprobados version2/enabled/glow1; no había migración de
versión suficiente en UI inicialmente y se corrigió. Advertencia .cube visible.
Feedback corregido con diálogo incrustado (conserva imagen/URL) y visible en la
app nativa beta2. QA00 únicamente sintética, B01–B05 sin asignar. Formulario de
feedback en español; interfaz principal ES/EN, sin afirmar feedback multilingüe.
