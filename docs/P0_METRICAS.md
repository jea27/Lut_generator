# COL-003 · Entorno y métricas offline

No implementa transferencia de color. No instala herramientas. Runtime local
verificado: Python 3.12.14, NumPy 2.3.5 y Pillow 13.0.0 ya disponibles. Versiones
de referencia en `requirements-p0-metrics.txt`; no ejecutar pip sin autorización.
Los tests NumPy se omiten explícitamente en CI si no está disponible; las
pruebas numéricas locales son evidencia separada, no un pase numérico de CI.

## Contrato de medición

`python scripts/benchmark_metrics.py --output-image OUTPUT.jpg --target TARGET.jpg
--aligned-target --alignment-record ALIGN-001 --report NUEVO.json`

TARGET debe representar el **mismo contenido alineado**, con revisión registrada.
Una referencia de otra escena no es target para ΔE/PSNR/SSIM. No se registra,
deforma ni redimensiona para esconder diferencias de geometría. Se comprueba
tamaño tras orientación EXIF antes de reducir a lado máximo 512 para medir.
ICC incrustado se convierte en memoria a sRGB con LittleCMS, intento relativo;
sin ICC exige `--untagged-srgb-record` explícito. No escribir nuevas fotografías.
Solo still RGB opaco hasta 50 megapíxeles; RAW/Log/HDR/alfa/vídeo fuera de alcance.

| Dimensión | Medición preparada | Límite de interpretación |
|---|---|---|
| Fidelidad | ΔE76 CIELAB D65 media/p95; PSNR RGB codificado [0,1] | No es ΔE2000 ni equivalencia automática con el paper; exige target |
| Detalle | SSIM luma codificada, ventanas uniformes 7×7 válidas, covarianza muestral; correlación de gradientes | El contraste legítimo cambia estos diagnósticos; revisión visual obligatoria |
| Consistencia | Diferencia máxima entre repeticiones del mismo caso | Misma entrada, referencia y ajustes; no acredita coherencia temporal entre escenas |
| Rendimiento | Mediana/p95 nearest-rank de tiempos reales aportados | Separar arranque, inferencia, carga/exportación; no inventar muestras |
| Extremos | Fracción de canales exactamente 0/1 | No prueba clipping causado por la herramienta ni gamut de salida |

PSNR infinito se expresa `null` con indicador explícito; gradientes constantes
dan correlación `null`. Sin recorte silencioso de valores inválidos. Informe
incluye hashes originales, perfiles, tamaño, versiones y tiempo **de medición**;
`model_inference_seconds=null`. LPIPS no está instalado y queda sin medir.
`timing_summary` y `repeatability` están disponibles para el futuro runner;
todavía no ejecutan productos ni escriben en `data/p0/benchmark.json`.

Fuentes: [W3C, conversiones de color](https://www.w3.org/TR/css-color-4/#color-conversion-code)
para distinción sRGB lineal/codificado y Lab con blanco explícito;
[documentación primaria scikit-image](https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.structural_similarity)
para parámetros que hacen distintas las variantes SSIM. Implementación local
NumPy propia; no se declara reproducción exacta de sus resultados ni CanonCGT.

## Separación de evidencias

1. Fixtures sintéticas de unittest: solo prueban infraestructura.
2. Identidad sobre foto real: solo comprueba decodificación/perfiles/métricas.
3. Producto ejecutado: exige versión, ajustes, entrada/referencia/salida,
   tiempo observado y revisión según el protocolo existente.
4. Aprobación P0: sigue dependiendo de investigación real y revisión humana.

Ninguna de las dos primeras clases llena runs ni entrevistas. Los informes
de métricas llevan `research_validated=false`; escribirlos nunca aprueba P0.
