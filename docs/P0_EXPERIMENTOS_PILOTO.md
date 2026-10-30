# COL-003 · Experimentos posibles con las cuatro fotos CC0

Issue #17. Cuatro archivos reales representan **dos capturas rurales**, no cuatro
escenas independientes. No cubren piel, interiores ni 20 pares diversos.
No se implementa matching ni se ejecutan productos para producir esta entrega.

| Experimento | Puede hacerse ahora | Interpretación |
|---|---|---|
| Hashes, decodificación/ICC y orientación | Sí, cuatro originales locales | Integridad y preparación de entradas reales |
| Identidad foto consigo misma | Sí, cuatro controles | Diagnóstico de métricas; cero calidad de producto demostrada |
| Repetir decodificación/preproceso tres veces | Sí | Reproducibilidad local y tiempo observado de infraestructura |
| Error plain-pretty de DSC_0106 | No, dimensiones diferentes | Rechazar antes de resize, sin inventar alineación |
| Error plain-pretty de DSC_0181 | Pendiente aunque coincida tamaño | Revisar registro/alineación e intención del target; no asumir ground truth |
| Matching con referencia de otra captura | Preparar casos; ejecución pendiente de acceso | Evaluación de estilo/revisión humana; no ΔE pixel a pixel contra otra escena |
| Consistencia temporal/vídeo/piel | No hay muestra adecuada | No medir ni asignar puntuación perfecta |

## Ejecución reproducible de controles

`python scripts/run_pilot_controls.py --manifest data/p0/pilot.json
--media-root .research-media/polyhaven-rural --report NUEVO_REPORTE.json --repeats 3`

Verifica los cuatro nombres y SHA-256 antes de procesar, y nuevamente el hash
al decodificar. No sigue enlaces fuera de la raíz ni sobrescribe evidencia.
Lee originales sin modificarlos; orientación/ICC sRGB y thumbnail Lanczos con
lado máximo 512 solo en memoria para medir. No descarga, publica ni renderiza
nuevas fotos. No actualiza `benchmark.json`, dataset.json ni entrevistas.

El informe distingue primera observación y dos posteriores por foto; no se
garantiza caché fría ni se comparan GPU/productos. Los tiempos incluyen lectura,
ICC/orientación y preparación, separados del tiempo de cálculo de identidad.
Repetibilidad de decodificación no equivale a consistencia de un motor.

## Casos de herramienta preparados, todavía sin ejecutar

Congelar cuatro casos antes de recibir resultados: 0106 plain→0181 pretty,
0181 plain→0106 pretty, 0106 pretty→0181 plain y 0181 pretty→0106 plain.
La flecha significa origen y referencia de estilo de **otra captura**, no target
alineado. Usar siempre hashes originales del manifiesto. Estas variantes están
correlacionadas; no tratarlas como cuatro personas o cuatro escenas independientes.

Para cada producto autorizado: versión, ajustes, gestión de color, salida,
captura y tiempos observados según el protocolo COL003. Revisar conservación
del contenido y estilo por separado; píxeles contra referencia de otra escena
no miden fidelidad. No subir material a una herramienta cloud sin permiso.
No reemplazar 5×20 por este piloto ni contar controles como runs automáticos.
