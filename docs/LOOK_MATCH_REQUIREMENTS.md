> Actualización31-10-2026: COL026#68 implementa manualmente glow/difusión/fade
> y receta v2, con bypass independiente y LUT solo color. Ver LOOK_MATCH_V1.md.
> La tabla siguiente conserva el corte documental anterior: no describe el
> estado actual de esa implementación. Halation/extracción automática siguen
> pendientes, sin validación de fidelidad ni aprobación comercial.

# COL-005 · Look Match: requisito comercial y mapa competitivo

**Corte:** 30 de octubre de 2026. **Tipo de evidencia:** investigación de
documentación pública de proveedores y contraste con los contratos/evidencias
MVP existentes. Ningún competidor se ejecutó en esta tarea; no hay respuestas
de usuarios ni validación del posicionamiento.

## Dos operaciones distintas

| Operación | Qué transfiere | Componentes del producto |
|---|---|---|
| **Color Match** | Relaciones globales de color y tono entre una referencia y una imagen destino. | Colorimetría, curvas, exposición, contraste y saturación. |
| **Look Match** | El acabado visual además del tratamiento global de color. | Color Match más bloom/glow, halation, difusión, blur suave, fade, microcontraste, suavizado de textura y atmósfera. |

En la interfaz ambas deben estar separadas, activarse por separado y admitir
intensidad y comparación independientes. Look Match no debe implicar copia exacta
del preset que creó la referencia, su composición, iluminación, lente ni detalle
perdido. «Suavizado» significa tratamiento de textura global; no es retoque facial
ni eliminación de rasgos.

### Estado real del producto

| Estado | Evidencia / alcance |
|---|---|
| **Implementado en MVP v0.1** | Importación de still JPG/PNG8 SDR; análisis básico; transferencia global basada en estadísticas Lab (dos métodos); intensidad, exposición, contraste, saturación y temperatura; render de imagen y LUT .cube 33³ sRGB global. Véanse [contrato v0.1](MVP_COLOR_CONTRACT.md), [guía Windows](MVP_V01_WINDOWS.md) y [evidencia GUI](evidence/MVP_01_GUI.md). |
| **No implementado** | Curvas editables; cualquiera de los módulos ópticos/espaciales de Look Match; análisis o transferencia de bloom, glow, halation, difusión, blur, microcontraste, suavizado o atmósfera; exportación de receta con dichos módulos. |
| **Experimental** | Ningún efecto de Look Match tiene prototipo o medición experimental en el repositorio. La definición de este documento es una hipótesis de producto basada en desk research, no una prueba de viabilidad o calidad. |
| **Pendiente para objetivo comercial v1.0** | Separar Color Match y Look Match; representar una receta por capas con controles independientes; previsualizar y renderizar la composición completa; exportar la parte global de color como .cube y advertir que el .cube no transporta los efectos espaciales; exportar una receta de efectos verificable. |

El objetivo v1.0 es una **propuesta de producto**, no un cambio a la versión v0.1
ya implementada. La primera entrega comercial de Look Match se plantea para
fotografía fija. La aplicación temporal de esos efectos a vídeo queda pendiente de
una tarea posterior con estabilización temporal, manejo por plano y evaluación
en clips.

## Competidores: dos ejes que no conviene confundir

Las páginas siguientes describen las capacidades que los propios proveedores
publican. La columna «match de referencia» se refiere a transferencia a partir de
una imagen; «acabado óptico» se refiere a si el producto también ofrece efectos
que van más allá del color global. «No documentado» no demuestra que una
capacidad no exista.

| Producto | Match de referencia documentado | Acabado/efectos documentados | Lectura para la propuesta |
|---|---|---|---|
| **ShotMatch** | Sí: motores de matching de color por referencia y presets/texto para generar looks. | Sí: módulo/API aparte para ajustes, perfiles de película y efectos como grano, bloom, halation, aberración cromática y viñeta; permite intensidades/overrides. Su propia página dice que el `.cube` incluye solo el grade de color y deja textura/efectos en el preview. | Competidor directo con combinación de color + efectos. La documentación consultada no prueba que extraiga automáticamente los parámetros ópticos de una referencia arbitraria; parece combinar match de color y stack/preset de efectos. [Producto](https://shotmatch.io/) · [API de match, look y efectos](https://shotmatch.io/docs/api). |
| **Luttie** | Sí: Color Match para igualar una foto/frame a una referencia; AI Grade puede proponer grades editables. | Sí: efectos separados de grain, halation y bloom. Sus docs dicen que el LUT `.cube` exporta el grade, no esos efectos espaciales. | Fuerte solapamiento de UX con una vía clara para extender el acabado en la app/render; transferencia automática de los parámetros de efectos desde la referencia no aparece documentada. [Features](https://luttie.app/features) · [Film Effects](https://luttie.app/features/film-effects). |
| **Colourlab Ai 4 / Astra Film** | Sí: el proveedor define Match como transferir el look de una referencia; también ofrece balance automático, look-building y estilos reutilizables. | Sí: Astra integra color de película, grano, halation, simulación de lente y efectos espaciales; FilmLab ofrece módulos especializados. | La combinación más completa de match y finishing integrado entre los consultados. La documentación publica los controles de matching por separado de film emulation; no demuestra que esos efectos se infieran uno a uno de cualquier referencia. [Match y look-building](https://docs.colourlab.ai/getting-started/key-concepts) · [Astra Film](https://colourlab.ai/products/astra-film) · [FilmLab](https://colourlab.ai/products/filmlab-ai/). |
| **DaVinci Resolve** | Sí: Shot Match iguala principalmente color, contraste y brillo entre planos. | Sí: Film Look Creator y Resolve FX incluyen film grain, halation, bloom, defocus y otros efectos, ajustados por separado. | Permite construir un acabado completo dentro del editor, con intervención del usuario. La función Shot Match no equivale a inferir una receta óptica de una referencia. Algunas herramientas requieren Studio. [Color/matching](https://www.blackmagicdesign.com/products/davinciresolve/color) · [guía Film Look Creator](https://documents.blackmagicdesign.com/UserManuals/DaVinci-Resolve-20-Colorist-Guide.pdf). |
| **Dehancer** | No encontramos en la documentación consultada una transferencia automática de efectos desde una referencia arbitraria. | Sí: emulación de stock de película, grain, halation, bloom, difusión y otros módulos creativos configurables. | Acabado fotoquímico amplio por perfiles y controles; no es evidencia de reference-to-effects matching automático. [Features](https://www.dehancer.com/features) · [guía de efectos](https://www.dehancer.com/learn/article/faq-tools). |
| **fylm.ai** | Sí: AI Colour Match y herramientas contextuales; NeuralFilmAI adapta la emulación de color de película a cada imagen. | Su documentación pública consultada se centra en color, emulación tonal y exportación LUT/XMP/Capture One; no verificamos un stack propio de halation/bloom/difusión comparable a los anteriores. | Competidor fuerte en color y film color; no clasificar como estrictamente «solo LUT», pero los efectos espaciales no quedaron demostrados en las fuentes consultadas. [NeuralFilmAI](https://fylm.ai/neuralfilmai/) · [Matches](https://fylm.ai/docs/what-are-matches-and-how-do-i-use-them/). |

### Qué puede afirmarse y qué no

- **Existe transferencia de acabado cinematográfico amplio** en sentido de
  composición de módulos (Colourlab/Astra, Luttie, ShotMatch, Resolve y
  Dehancer). Competir alegando que LumaForge es la única herramienta con bloom o
  halation sería falso.
- En varias ofertas, **el match de referencia y los efectos espaciales son
  módulos distintos**. ShotMatch y Luttie explican expresamente que su `.cube`
  contiene solo la transformación de color; los efectos requieren preview,
  render o aplicación por separado. Resolve también separa Shot Match de sus FX.
- La oportunidad comercial que queda como **hipótesis verificable** es transferir
  de una referencia el acabado de forma más directa y transparente: separar la
  receta de color de la receta de efectos, dejar que el usuario inspeccione/varíe
  cada parte y mantener el flujo local y portable. La evidencia pública no basta
  para afirmar que ningún competidor ya lo resuelve; hace falta ejecutar el
  benchmark P0 con las mismas parejas y versiones.

## Propuesta comercial para v1.0

**Promesa a probar:** «Lleva a tus fotos el acabado visual de una referencia:
igualamos el color y reconstruimos por separado la respuesta de luz y textura,
para que puedas ajustar, comparar y exportar cada parte».

La diferenciación sería la combinación, no un efecto aislado:

1. **La referencia manda.** Arrancar desde la imagen elegida para proponer tanto
   una base Color Match como una receta Look Match, mostrando qué cambios son
   color y cuáles son textura/luz.
2. **Control y reversibilidad.** Intensidad y bypass por componente, comparador
   antes/después y advertencias de incertidumbre; el usuario decide sobre piel,
   luces intensas y escena.
3. **Salidas honestas.** Render de imagen con el acabado completo; `.cube` solo
   para la parte global colorimétrica; receta JSON versionada para ajustes
   adicionales. No prometer que LUT conserva blur, glow o halation.
4. **Local-first.** Mantener medios en el equipo por defecto; un análisis remoto
   seguiría siendo opt-in y sujeto a consentimiento/presupuesto.

La frase comercial anterior es una **hipótesis**, no copy aprobado ni promesa
medida. La ventaja debe validarse frente a ShotMatch, Luttie, Colourlab y el
stack manual Resolve/Dehancer. El criterio de éxito debe medir preferencia de
acabado, facilidad para corregirlo y fidelidad del render, no solo ΔE o matching
de paleta.

## Preguntas para reanudar P0 sin inventar datos

Cuando regresen participantes y medios con permisos, pedir que separen:

- ¿Qué elementos de una referencia intentas reproducir: paleta/contraste,
  blooming/halation, suavidad, grano, fade u otra cosa?
- ¿Qué reproduces ya con curvas/LUT y qué requiere filtros, nodos o plugins?
- ¿Preferirías ajustar el color y el acabado de forma independiente? ¿Qué efecto
  quitarías primero y por qué?
- ¿Te sirve un render final si el `.cube` solo lleva el color? ¿Necesitas además
  una receta editable en un editor concreto?
- ¿En qué imágenes el suavizado, glow o halation estropearía piel, bordes o
  detalle? Pide un ejemplo real, con autorización de uso antes de copiarlo.

No añadir estas preguntas al formulario web publicado ni tratar respuestas de
prueba como entrevistas: la revisión del guion COL-005 sigue pendiente en #15.

## Coordinación de roadmap

No se cambia `site/data/roadmap.json` en esta entrega mientras el agente principal
prepara la rama de beta/producto. Propuesta para revisar por GitHub antes de tocar
los criterios del dashboard: COL-005 cubre la hipótesis comercial; COL-019 debería
describir render con efectos y `.cube` de color; COL-026 es el destino técnico
existente para composición de look base y corrección local. No se crea un ID nuevo
ni se alteran estados. Se deja la propuesta en la Issue #13 y el PR de documentos
para que el responsable del roadmap pueda coordinarla con el trabajo activo.

Se conserva la investigación vigente de [precios, licencias y España/UE](P0_COMERCIAL_ESPANA_UE.md);
este documento no la reevalúa ni la duplica.
