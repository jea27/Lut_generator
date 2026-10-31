# Casos de LUT y gestión de color · preparados, no ejecutados en editores

31-10-2026. Photoshop/Premiere instalados pero sin sesión de edición validada
en este ciclo; bloqueos previos de acceso/licencia persisten. Resolve no disponible
en el inventario anterior. No se abrió un documento ni se importó LUT real nueva.

Preparación reproducible, solo con imagen opaca autorizada:

```powershell
./.venv-mvp/Scripts/python.exe scripts/qa_editor_exports.py prepare apps/demo/source.jpg .lumaforge-local/look03-qa/recipe.json .lumaforge-local/editor-qa-nuevo
```

Directorio nuevo obligatorio. Contiene foto rural CC0 redimensionada1024, expected
color y finish separados, chart **sintético**, identidad/color .cube33³, receta y
manifest de hashes. La reducción es solo para el ensayo de editores, nunca una
optimización silenciosa de exportación original. Créditos en apps/demo/credits.json.
El chart no acredita calidad fotográfica ni participante alguno. Todas las
ejecuciones de editor del manifest empiezan not_run. La comprobación escalar de
serialización se ejecutó realmente (error máximo1,091e-7), no abre ningún editor.

| Caso | Entrada y operación | Control requerido |
|---|---|---|
| E01 | chart-source + identity.cube | Orden RGB, extremos, gamma y niveles completos; export sin redimensionar |
| E02 | chart-source + color-only.cube | Interpolación trilineal comparable y rampas/primarias sin conversiones ocultas |
| E03 | photo-source + color-only.cube | Comparar con photo-color-expected.png, nunca con finish |
| E04 | Misma foto y receta en LumaForge | finish contiene glow/difusión/fade; la LUT no los transporta |
| E05 | Preview y export de la misma configuración | Separar diferencias de escala/radio, interpolación, ICC y cuantización |

## Photoshop

Abrir PNG conservando ICC sRGB, documento RGB8. Añadir capa Color Lookup al100%
normal con la LUT indicada, sin otras capas/ajustes; registrar dithering si la
versión lo ofrece. Exportar PNG a dimensiones originales con ICC, sin EXIF de
terceros, y conservar PSD privado para reproducir. Ejecutar primero identidad y
después color, en chart y foto. Photoshop documenta [Color Lookup](https://www.adobe.com/us/learn/photoshop/web/edit-photo-color-lookup-adjustment)
y [conversión de perfiles](https://helpx.adobe.com/photoshop/desktop/adjust-color/color-profiles/change-color-profile-for-documents.html).

## Premiere

Registrar versión, modo de color, espacio interpretado de la imagen, working/
output space, auto tone/gamut mapping y posición de Lumetri. La LUT es
**encoded sRGB→sRGB D65**, no un Input LUT de cámara ni una transformación
técnica Rec.709. Compartir primarias no iguala funciones de transferencia.

Primero demostrar E01 en un flujo que preserve los valores RGB del dominio de
la LUT, sin asignar etiquetas falsas ni doble conversión. Después E02/E03.
Si esa versión no permite aislar el dominio sRGB, registrar **BLOCKED_DOMAIN**;
no aplicar sin más en Rec.709 y llamarlo fidelidad verificada. Para un flujo
gestionado futuro, documentar explícitamente transformación antes y después de
LUT y generar expected en ese mismo dominio antes de aceptarlo. Exportar frame
lossless etiquetado: si no lleva ICC, documentar sus primarias/transferencia y
proceso verificable de conversión, no añadir sRGB por suposición para pasar el
comparador. Referencia [gestión de color de Premiere](https://helpx.adobe.com/premiere/desktop/correct-color/set-up-color-management/how-color-management-works.html).

## DaVinci Resolve

Proyecto de ensayo independiente, imagen full/data range y resolución exacta.
Usar dominio sRGB comprobado alrededor del nodo LUT; sin input LUT de cámara,
ACES/RCM/tone mapping inadvertidos ni LUT de salida. Registrar interpolación
trilineal para comparar con motor; tetrahedral se ensaya aparte y no se oculta
como redondeo. E01 debe superar gamma/niveles antes de E02/E03. Documentar
color management y gamma/output del PNG. La [guía oficial de Resolve20](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Colorist-Guide.pdf)
explica interpolación; registrar la versión real disponible, sin asumir20/Studio.

## Medir una devolución real

```powershell
./.venv-mvp/Scripts/python.exe scripts/qa_editor_exports.py compare .lumaforge-local/editor-qa-nuevo/photo-color-expected.png .research-private/beta/photoshop-export.png .research-private/beta/photoshop-medicion.json
```

Exige PNG con ICC, mismas dimensiones y sin alfa; convierte perfiles con el
contrato de image_io. Reporta error RGB en unidades de8bit y ΔE76 D65, hashes,
sin aprobar compatibilidad. Añadir por separado versión/configuración/fecha y
prueba de ejecución real. No medir screenshots ni JPEG como precisión LUT.
Identidad y LUT trilineal de control deben investigarse si exceden redondeo
esperable de1LSB; no establecer tolerancia estética retrospectiva para ocultar
gamma/niveles. Tetrahedral, dithering,8bit y gestión ICC se diagnostican por
separado. Aprobación humana tras métricas y revisión visual, no por abrir .cube.
