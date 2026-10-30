# Decisión explícita · iniciar MVP técnico P1/P2

Fecha: 2026-10-30. Fuente: petición del usuario adjunta en esta sesión,
«Comenzar el desarrollo real de la aplicación». Autoriza expresamente iniciar
P1 y P2 aunque la validación comercial P0 siga incompleta, preparar dependencias,
implementar/probar y publicar ramas/PR técnicas. No es una aprobación de P0.

Se conserva íntegra la investigación. COL001/002 siguen pendientes de entrevistas,
COL003 de comparativas y COL004 de cobertura/permisos revisados. El agente no
fusiona, cierra Issues ni aplica approved. El paso técnico autorizado no inventa
un go comercial ni altera automáticamente estados de site/data/roadmap.json.
P3/P4/P5 permanecen en diseño, sin IA, vídeo o empaquetado de escritorio ahora.

## Secuencia y flujo de usuario

1. Abrir servidor propio en loopback desde Windows, sin cuenta ni servicios cloud.
2. Importar referencia y destino JPG/PNG. Revisar perfiles y análisis de referencia.
3. Elegir uno de dos baselines Lab acotados y pulsar Analizar y transferir.
4. Comparar sobre la misma fotografía, ajustar intensidad y controles reversibles.
5. Guardar receta/preset y exportar PNG/JPG original o LUT global de 33³.

La captura aportada guía los paneles y el ambiente oscuro; no se usa como dato,
foto de benchmark, copia de interfaz ni recurso redistribuido.

Arquitectura: packages/colour_core independiente, apps/api FastAPI, apps/web
Vue3/TypeScript/Quasar con build Vite. El backend sirve la interfaz compilada y
API del mismo origen. Se conserva site/ y sus workflows de publicación. No se
publica el editor en GitHub Pages ni se abre el servidor a la red local.

## Condiciones de revisión

Pruebas técnicas y muestras CC0 comprueban ejecución, no calidad de mercado.
El usuario evalúa el look y los criterios completos de cada tarea. El MVP no
cumple por sí solo evaluación ciega, cinco usuarios, 20 pares ni aceptación final.
