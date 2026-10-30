# Arquitectura objetivo — evolución controlada

## Primer principio
El motor de color no depende de Photoshop, ni de Tauri, ni del frontend. La primera versión trabaja con imágenes SDR preparadas en sRGB y emite LUT en dominio documentado. Para vídeo, Rec.709 se tratará explícitamente y solo después se evaluarán Log/HDR.

```
Vue 3 / Quasar (web local)
    ↓ HTTP localhost
FastAPI (jobs, contratos, validación, caché)
    ↓
colour-core (NumPy/OpenCV/colour-science/OCIO)
    ├─ análisis global (histograma, curvas, color dominante)
    ├─ transferencia referencia ↔ destino
    ├─ motor determinista + límites de gamut y clipping
    ├─ módulos IA locales (opcionales; máscaras/contexto)
    ├─ evaluador (métricas y conjunto de pruebas)
    └─ exportadores: imagen, .cube, receta JSON
                 ↓ en P4
             FFmpeg por planos (SDR)
                 ↓ en P5
             Tauri Windows / conectores
```

## Especificación de artefactos
- **ReferenceProfile v1**: estadísticas perceptuales y metadatos de referencia, hash y ámbito cromático.
- **LookRecipe v1**: versión, perfil de entrada, intensidad, curvas, balance, restricciones y módulos locales usados.
- **TransferResult v1**: resultado de matching con evaluación básica, warnings y preview.
- **LUT .cube**: matriz 33³ como salida universal para transformación global; validación de coherencia preview/export. No confundir un LUT artístico con un Input LUT técnico.
- **Entrega renderizada**: JPEG/PNG o MP4 para tratamientos locales que el archivo .cube no puede transportar.

## Motor clásico (desarrollo P1)
1. Interpretar EXIF/orientación, ICC, alpha y tamaños máximos.
2. Convertir a espacio de trabajo bien definido; neutralizar discrepancias de perfil.
3. Estimar exposición, contraste y estadísticas Lab/Oklab; producir baseline Reinhard y baseline de histograma/curvas.
4. Ajustar con fuerza configurable, límites y regularización contra banding.
5. Aplicar la misma transformación a una rejilla RGB 3D; serializar `.cube`.
6. Verificar con pruebas de LUT identidad, pieles, gradientes, saturación y 20 pares.

## IA local (P3)
- Segmentación de personas/piel/cielo para ponderar regiones. Modelos ligeros y ejecución ONNX/PyTorch sobre CPU o GPU según benchmark; no presuponer que una 3060 Ti garantiza un FPS concreto.
- Mantener modelos descargables opcionales y no empaquetar pesos con licencia incompatible sin auditar.
- Corrección local solo en motor interno o render final; LUT como aproximación global si hay máscaras.
- Si se usa IA externa, exigir opt-in por proyecto, aviso de privacidad y presupuesto de tokens/imagenes.

## Vídeo (P4)
- Ingesta limitada inicialmente a SDR/Rec.709. Perfiles Log y HDR se añadirán tras diseñar conversiones seguras.
- Detector de cortes, selección de fotogramas representativos y receta de look por plano.
- Evitar aplicar un análisis IA nuevo por fotograma; combinar cambios de look y compensación temporal de manera estable.
- Audio sin recodificación cuando sea compatible; si no, indicar conversión. Probar 10 clips con luces y cortes.

## Calidad / observabilidad
- Tests deterministas sobre fixtures, métricas de color, tests de gamut y export de 33³.
- Conservar reporte de versiones y entradas resumidas sin almacenar imágenes privadas en logs.
- Métricas de tiempos, memoria y fallos del motor; telemetría siempre opt-in.
- CI y revisión humana antes de integrar código; control de cambios de modelos/licencias.

## Integraciones externas
- Photoshop/Premiere/Resolve con `.cube` y guías de instalación. Adobe Premiere soporta LUT personalizadas: https://helpx.adobe.com/premiere/desktop/correct-color/add-color-effects/install-custom-look-up-table-files.html
- Lightroom `.xmp` no es simplemente renombrar un `.cube`: estudiar un perfil compatible o representación de ajustes Camera Raw como proyecto separado, con pruebas de versiones.
- Tauri 2 con sidecar Python o ejecutable compilado solo cuando el motor y la UI estén estables.

## Seguridad y privacidad
- Ninguna API key en la web estática; no subir fotos por defecto.
- No ejecutar órdenes que lleguen de issues sin revisar como comandos shell.
- Sanitizar cualquier dato que salga del repositorio privado hacia el dashboard público.
- Mantener dependencias con licencias compatibles y registrar avisos legales de FFmpeg.
