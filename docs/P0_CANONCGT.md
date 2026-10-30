# COL-003 · CanonCGT, candidato de investigación

Fuentes primarias consultadas 2026-10-30. No se ejecutó el modelo.

## Arquitectura y resultados publicados

[Ko, Ko y Kim, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Ko_CanonCGT_Reference-Based_Color_Grading_via_Canonical_Pivot_Representation_CVPR_2026_paper.html),
[artículo v1](https://arxiv.org/html/2606.01638v1): un extractor de estilo
condiciona dos etapas que producen LUT 3D: canonicalización para retirar el
sesgo tonal del origen y grading hacia la referencia. DP-CGT combina aprendizaje
supervisado de presets y refinamiento autosupervisado con fotografías no emparejadas.

Tabla 1, cifras **de los autores**, no medidas por LumaForge: PSNR 28,99 dB,
SSIM 0,9608, ΔEab 5,46 y LPIPS 0,0665. El apéndice F.1 declara 8 ms/FHD y
0,26 GB con RTX 3090, promedio de 100 inferencias. No extrapolar a este Windows,
CPU o flujo de lectura/exportación. Tintes extremos y monocromo presentan
limitaciones descritas por los autores. El protocolo de reconstrucción del
paper no equivale a acertar la intención de cualquier referencia libre.

## Licencia, datos y reproducibilidad

[Repositorio oficial fijado](https://github.com/Jinwon-Ko/CanonCGT/tree/229a7d3ec24af19ea5d97bb136f0317762bb9261).
Su [README](https://github.com/Jinwon-Ko/CanonCGT/blob/229a7d3ec24af19ea5d97bb136f0317762bb9261/README.md)
incluye código **y pesos preentrenados** bajo
[Apache 2.0](https://github.com/Jinwon-Ko/CanonCGT/blob/229a7d3ec24af19ea5d97bb136f0317762bb9261/LICENSE).
No hay restricción no comercial declarada para estos dos componentes.
Si se redistribuyen: conservar licencia, avisos aplicables y marcar modificaciones;
comprobar NOTICE/dependencias de la versión efectivamente usada.

El README distingue FiveK Expert C y presets de Lightroom: no redistribuye
presets ni dataset emparejado por restricciones de licencia. Las colecciones
no supervisadas también conservan sus propias condiciones. Apache no otorga
derechos sobre esas fotografías. No se descargó ningún dataset de entrenamiento.

Entorno oficial: Python 3.9, PyTorch 1.12.1/CUDA 11.3, torchvision 0.13.1,
torchaudio 0.12.1, OpenCV headless 4.10.0.82 y LPIPS, entre otros. El runtime
local Python 3.12 no tiene Torch; no instalar ni asumir compatibilidad automática.
No se descargaron pesos ni ejecutó código externo. Antes de inferencia:
revisar código/carga de checkpoints, fijar hashes, entorno aislado y memoria/GPU;
solicitar autorización específica para instalaciones si se necesitan.

## Incorporación a la comparativa

Se añade como **sexto candidato documental**, separado de los cinco productos
ya fijados en `data/p0/benchmark.json`. No sustituye silenciosamente ninguno,
no cuenta como producto probado y no se altera el denominador 5×20.
Es una referencia relevante de LUT condicionadas; adoptarla como arquitectura
de LumaForge requeriría decisión humana. No se inicia P1.
