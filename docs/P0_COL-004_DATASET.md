# COL-004 · Dataset de evaluación, preparado pero vacío

Issue #18. Criterio final: 20 pares fuente/referencia con permisos claros,
escenas diversas y muestras de piel, sombras y altas luces.
Estado inicial real: **0/20 pares disponibles; 0 imágenes descargadas**.

`data/p0/dataset.json` planifica 20 slots, no son fotografías obtenidas.
Distribuye retratos, paisajes, interiores, calle y bodegón, con retos de piel,
sombras, luces, iluminación mixta, noche, contraluz y saturación. La adecuación
visual y la diversidad se revisan por una persona; las etiquetas de una
plantilla no demuestran que los medios cubran esas condiciones.

## Flujo de incorporación de medios

1. El usuario selecciona imágenes propias o con permiso adecuado y mantiene
   los originales fuera del repositorio público. No usar fotos de clientes,
   fotogramas comerciales o imágenes de Internet sin revisión de derechos.
2. Revisar por separado fuente y referencia: base de uso y evidencia. El
   registro privado recibe un ID RIGHTS-…; permisos/consentimientos completos
   no se publican. El script comprueba la presencia del registro, no su validez
   legal ni la identidad de quien lo autorizó.
3. Preparar JPEG/PNG SDR sRGB sin metadatos personales por un flujo autorizado.
   Documentar esa preparación con un ID COLOR-…; el validador no convierte ni
   interpreta ICC, no analiza EXIF y no constituye un motor de color P1.
4. Nombrar medios en una carpeta privada: P0-001/source.png y reference.png,
   hasta P0-020. No incluir personas/contactos en los nombres del manifiesto.
   No copiar los archivos privados al workspace público para ejecutar el script.
5. Registrar por asset `path`, SHA256, `rights` (status cleared, record_id y basis),
   `color_space: sRGB` y color_record_id. Solo marcar el par ready cuando ambos
   medios y registros existan. Una referencia puede reutilizarse; las fuentes
   deben ser distintas y ninguna referencia puede ser idéntica a su fuente.
6. Revisión visual humana de cobertura y diversidad; registrar REVIEW-… y
   coverage_review.status reviewed. Las marcas son declaraciones auditables,
   no una aprobación automática por IA.

## Verificación reproducible

```powershell
python scripts/validate_dataset.py
python scripts/validate_dataset.py --ready
python scripts/validate_dataset.py --ready --media-root RUTA_PRIVADA_EXPLICITA
python -m unittest discover -s tests -v
```

La primera orden valida el plan y produce un informe incompleto; no demuestra
dataset listo. `--ready` devuelve 2 si faltan elementos, 1 si el esquema o la
integridad falla y 0 únicamente si el checklist técnico está completo.
No escribir la ruta privada en Issues ni subir el informe con datos privados.

Se comprueban IDs, retos previstos, rutas anónimas sin traversal, contención
tras resolver enlaces, archivos de hasta 100 MiB, firma inicial y hash SHA256.
No se decodifica la imagen completa: un hash y firma correctos no demuestran
perfil, calidad visual, consentimiento, licencia ni adecuación de una escena.
La aceptación humana de la Issue y la puerta P0 siguen separadas.

## Pruebas y límites

Fixtures sintéticas de bytes solo prueban integridad y controles negativos;
no cuentan como pares del benchmark ni resultados de transferencia. Pruebas
de manipulación, duplicados, rutas, derechos pendientes, ausencia de medios y
códigos de salida incluidas. Sin nuevas dependencias ni instalaciones.

Siguiente acción humana: aportar ubicación local acordada y 20 pares con sus
registros de uso, o indicar fuentes que se puedan investigar sin gastos ni
subidas remotas. Recomendación: empezar por material propio ya autorizado.
Hasta entonces continúa preparación independiente, pero no completar COL-004.
