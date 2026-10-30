# Contrato de color MVP v0.1

COL007–012. Entradas: still JPEG y PNG SDR de ocho bits, máximo 32 MiB,
24 megapíxeles y 12000 píxeles por lado. Se rechazan animación, CMYK, PNG con
otra profundidad y formatos RAW. La transferencia Log/PQ/HLG no se deduce de
un JPEG: no introducirlos como si fueran sRGB. Vídeo Rec.709 tiene una curva
distinta de sRGB aunque comparta primarias; está fuera de esta versión.

Pillow/LittleCMS aplica EXIF y convierte ICC RGB incrustado a sRGB, intento
colorimétrico relativo. Perfil inválido/incompatible provoca error explícito.
Sin ICC se asume sRGB y se informa en pantalla. No hay control de pantalla ni
garantía de apariencia entre monitores. Grises se expanden a RGB; RGBA conserva
alfa en PNG y lo compone sobre blanco al exportar JPEG. Solo se analizan píxeles
con alfa >0,05; no se implementan máscaras semánticas ni protección de piel.

## Receta global fija

La referencia se analiza a lado máximo 512: histograma RGB de 64 bins,
luminancia lineal, percentiles P05/P95 y contraste de su diferencia, media y
desviación CIELAB D65. Colores dominantes aproximados por cuantización RGB
16³, no agrupamiento semántico. Estadísticas de referencia y destino producen:
- Lab statistics: escala de desviaciones limitada 0,8–1,2 y offset ±12.
- Mean only: escala unidad y offset de medias ±12.

L adapta su desplazamiento cerca de blanco/negro y lo limita a ±15 antes de
esa atenuación. Se comprime cromaticidad hacia luminancia neutral para encajar
RGB lineal en gamut. Corrección de transferencia limitada a 0,25 por canal sRGB.
Saturación actúa sobre a/b; temperatura es un control creativo ±1 de ganancias
R/B, no temperatura Kelvin física. Exposición ±2 es una curva racional con
ganancia 2^EV y extremos preservados, no una simulación RAW de exposición.
Contraste 0,6–1,4 usa curva logística monotónica. Intensidad mezcla **todo** el
look (incluidos controles manuales); cero conserva exactamente el RGB de entrada.

La transformación se hornea en una LUT 33³ y el renderer aplica interpolación
trilineal de esa tabla. Así preview/export/LUT representan la misma receta
global, sin una normalización adaptativa escondida al exportar. Preview reduce
a lado máximo 1280 antes de aplicar; no es una prueba píxel a píxel de la foto
exportada reducida, debido al orden del resampling y la transformación no lineal.
Exportar siempre procesa dimensiones originales en bloques de 64 filas.

El formato .cube usa RGB flotante [0,1], rojo de variación más rápida y dominio
encoded-sRGB-D65, **no Input LUT ni Log/Rec.709/HDR**. Identidad y lector trilineal
independiente están probados; no se ha validado en Photoshop/Premiere/Resolve.
Cada editor requiere sRGB de entrada y gestión posterior correcta; otras
interpolaciones, como tetraédrica, pueden diferir. No prometer estilo exacto.

## Límites prácticos y medición

Transformación global aproximada, sin recuperar el preset original, iluminación
por escena ni detalle perdido. Las salvaguardas reducen cambios extremos, no
garantizan ausencia de artefactos o saturación no deseada en todos los casos.
Negativos de alfa, perfiles, finitud y rango se comprueban antes de render.

Tiempos wall-clock y RSS de proceso muestreado cada 10 ms se muestran para cada
preview/export: no son pico exacto de asignaciones ni memoria GPU. El smoke de
una foto real CC0 4928×3264 queda en docs/evidence/MVP_01_SMOKE.json; originales
y resultados solo en almacenamiento ignorado. No es validación comercial P0.
