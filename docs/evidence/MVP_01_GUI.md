# Comprobación GUI local · 2026-10-30

Datos reales de dos fotografías públicas CC0 Poly Haven, no entrevistas ni
validación comercial. Captura aportada por el usuario no utilizada como imagen.

- Abrir build Vue/Quasar servido por FastAPI en 127.0.0.1:8790: correcto.
- Importar referencia DSC_0181 pretty y destino DSC_0106 plain por selectores
  reales del navegador; ambos 4928x3264, análisis/histogramas visibles.
- Analizar y transferir: comparación antes/después visible, preview ~1040–1125ms
  en la ejecución observada, lado máximo1280. No incluye descarga cloud.
- Intensidad Home→0% y End→100% observadas. Deslizador de comparación50→51.
- Exposición0→0,10; guardar preset local Rural CC0 demo; Deshacer→0,05;
  aplicar preset→0,10. Importar receta tras subir exposición a0,15→restaura0,10.
- Descargar PNG desde GUI: 4928x3264 con ICC sRGB verificados; ~10,8s y
  ~793MB de RSS muestreado de proceso en ese instante. No pico exacto ni GPU.
- Descargar .cube y JSON desde GUI, comprobados contenido33³ y receta versionada.
  JPG también probado en smoke real por API a resolución original.
- Viewports390x844 y1280x900: scrollWidth375 y1265, sin desbordamiento horizontal.
  No se declara prueba física en Safari/iPhone ni evaluación por usuarios reales.

Los archivos exportados de GUI están en Descargas del equipo; otros artefactos
de smoke en .lumaforge-local/demo, ignorados. La captura de interfaz se guarda
localmente; no se suben fotografías ni datos privados a GitHub.
