# COL-003 · Protocolo comparable y revisión documental

Issue #17. Fecha de consulta: 2026-10-30. **Cero productos ejecutados y cero
resultados de matching medidos**. Esta entrega no satisface todavía «probar
cinco competidores con la misma muestra». No se implementa motor de color.

Continuación: `P0_CANONCGT.md` añade un sexto candidato documental sin cambiar
los cinco casos requeridos. `P0_METRICAS.md` y `scripts/benchmark_metrics.py`
preparan mediciones offline; los controles de infraestructura no son resultados
de productos ni validación de mercado.

## Candidatos y evidencia primaria

| Candidato | Declaración documental consultada | Qué falta comprobar ejecutándolo |
|---|---|---|
| Luttie | Su documentación describe Color Match de imagen/referencia y LUT en navegador | Acceso al nivel requerido, versión de navegador/build, resultado y exportación |
| fylm.ai | La documentación describe Matches como referencia para Colour Match y exige seleccionar transformaciones ACES | Acceso, transformaciones equivalentes y posibilidad de exportar bajo el plan disponible |
| DaVinci Resolve | La página Color describe Shot Match entre clips; no confundirlo con igualar una carta ColorChecker | Preparar los mismos stills, ajustes de gestión de color, versión/edición y resultado |
| G'MIC | Sitio oficial: framework y CLI/plug-in local en Windows; publicación de versión 4.0.7 el 28-10-2026 | Seleccionar y registrar el filtro/parámetros de transferencia realmente disponibles en la instalación autorizada; no asumir LUT export |
| Colourlab Ai | Página de producto v4: Apple silicon/macOS 14; Windows todavía anunciado como futuro | Hardware/acceso. No sustituir v4 por v3 silenciosamente; documentar y revisar una sustitución |

Fuentes consultadas, declaraciones de proveedor sin pruebas propias:

- [Luttie Color Match](https://luttie.app/docs/color-match).
- [fylm.ai Matches](https://fylm.ai/docs/what-are-matches-and-how-do-i-use-them/).
- [DaVinci Resolve Color](https://www.blackmagicdesign.com/products/davinciresolve/color).
- [G'MIC oficial](https://gmic.eu/).
- [Colourlab Ai 4 producto](https://colourlab.ai/products/colourlab-ai-4).
- [Colourlab v3 para flujos existentes](https://colourlab.ai/version-3).

**Discrepancia documental encontrada:** la landing antigua de
[Colourlab beta](https://4.colourlab.ai/) anuncia Windows en octubre, mientras
la página actual de producto y la página v3 siguen indicando v4 para Apple
silicon y Windows pendiente. Sus [FAQ](https://docs.colourlab.ai/faq) también
conservan texto de beta. No asumir disponibilidad Windows por una fecha de
marketing pasada ni equiparar versiones. Se prioriza el requisito de la página
de producto hasta verificar un binario autorizado. No se citan precios como
actuales ni se compran pruebas; una comparación de costes requerirá consulta
de planes y permiso cuando implique gasto.

## Dependencias y bloqueos

Se necesita el dataset COL-004: 20 pares reales, permisos y preparación de color
documentados. El manifiesto de slots no basta. No se instalan productos, crean
cuentas, aceptan contratos ni suben imágenes a terceros desde esta entrega.
La afirmación de procesamiento local de un proveedor no autoriza otras rutas
de IA/cloud ni el envío de material de clientes.

Propuesta de continuación: herramientas ya instaladas/autorizadas y datos
propios. Registrar qué producto es inaccesible y por qué. Si hace falta cambiar
un candidato (por ejemplo Colourlab v3 o un sexto producto en Windows), revisar
la selección antes de ejecutar, conservando el motivo y la versión del plan.
Un bloqueo de acceso no es un fallo de calidad y no cuenta como herramienta
probada. No iniciar el motor LumaForge para suplir la herramienta que falte.

## Congelar el experimento

1. Congelar el manifiesto de COL-004 por SHA256 y los hashes de cada fuente y
   referencia; usar los mismos bytes en todas las herramientas. No retocar
   entradas para favorecer una herramienta. Si se exige conversión de entrada,
   registrarla, guardar su hash y aplicar la misma condición o informar que la
   comparación no es directa.
2. Registrar equipo, sistema, GPU/CPU, pantalla y condición de visualización
   con ID de evidencia. No publicar identificadores personales del ordenador.
3. Registrar versión real/build y modalidad de cada herramienta, parámetros,
   perfiles/transformaciones de entrada/salida y qué funciones están incluidas.
   sRGB y Rec.709 no se asumen idénticos; documentar cada configuración, sin
   implementar conversiones nuevas en esta fase.
4. Ordenar ejecuciones antes de mirar resultados; conservar la asignación. Para
   la revisión ciega, usar códigos de salida sin nombres de producto y separar
   esa tabla de la evaluación humana. No pedir al evaluador «confirmar» una
   herramienta favorita.

## Dos pasadas que no se mezclan

- **Automática:** una salida de matching por cada producto y par, con ajustes
  predeterminados documentados y sin retoque manual posterior: 5 x 20 = 100
  comparaciones esperadas. Si una función no existe, registrar el bloqueo; no
  inventar una equivalencia manual como resultado automático.
- **Ajustada, opcional:** permitir hasta 5 minutos de ajustes manuales por
  caso para investigar recuperabilidad. Registrar como refined, separado de
  automatic. Nunca usar esa pasada para inflar los 100 casos automáticos.

Cronometrar por separado preparación/importación, matching y ajuste manual.
El registro de esta entrega guarda elapsed_seconds del matching, con método
stopwatch/application-log. Registrar si hubo red, primera ejecución o caché;
no comparar un tiempo warm con otro cold sin explicarlo. Una ejecución aislada
no demuestra latencia media ni rendimiento de LumaForge.

## Evidencia y evaluación

Por cada ejecución completada: hashes de entradas, salida y captura; versión;
fecha; tiempo observado y método; IDs SETTINGS-…, COLOR-… y REVIEW-…. Guardar
capturas/medios en almacenamiento autorizado y usar IDs en el resumen público.
Evaluar de manera separada estilo global, piel si existe, sombras/luces, clipping
visible, banding, artefactos y facilidad de corregir. Marcar no aplicable cuando
no haya piel; no convertirlo en puntuación perfecta. Anotar desacuerdos humanos
y casos fallidos. Las etiquetas subjetivas no son métricas colorimétricas.

Probar exportación LUT e imagen solo si están disponibles bajo el acceso
autorizado; registrar no soportado/bloqueado sin rellenar una exportación falsa.
Guardar capturas originales, ajustes y explicación del fallo. Ninguna imagen
de prueba privada se añade al repositorio público por esta tarea.

## Registro e informe técnico

`data/p0/benchmark.json` define cinco candidatos, 20 IDs y `runs: []`.
`scripts/validate_benchmark.py` audita recuentos y comparabilidad; no procesa
imágenes, calcula métricas de color ni inventa puntuaciones.

```powershell
python scripts/validate_benchmark.py
python scripts/validate_benchmark.py RUTA_PRIVADA_AL_REGISTRO --ready
python -m unittest discover -s tests -v
```

Exit 0 valida esquema (con --ready, completitud del registro); 2 indica
incompleto; 1 indica errores. Rechaza pares/productos duplicados, entradas
distintas entre productos, tiempos no finitos, versiones/fechas ausentes y
mediciones atribuidas a ejecuciones bloqueadas. Requiere 100 registros
automáticos, con cinco productos cubiertos y dataset fijado por hash.

**bookkeeping_ready no es investigación aceptada:** los IDs/hashes son
referencias declaradas, no verifican el contenido de capturas, permisos,
calidad o veracidad de una ejecución externa. research_validated siempre es
false en la herramienta; el usuario revisa las evidencias y decide. Los tests
con 100 fixtures no son 100 comparativas realizadas.

## Informe de resultados futuro (sin rellenar)

- Productos realmente accesibles y probados: pendiente.
- Pares con permiso y hashes: pendiente de COL-004.
- Ejecuciones/capturas verificadas: 0.
- Casos favorables y fallos por escena: sin datos.
- Preferencias humanas, limitaciones y alternativas: sin datos.
- Recomendación go/pivot/stop: pendiente de evidencia y COL-006.

La documentación primaria mejora la preparación, pero no sustituye pruebas ni
entrevistas. COL-001 sigue abierta y P1 requiere autorización explícita.
