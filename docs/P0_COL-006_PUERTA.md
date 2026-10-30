# COL-006 · Puerta de salida de P0, sin autorización de P1

Issue #19. Documento de control preparado el 30-10-2026. No es un acta de
aprobación ni una decisión go. El agente no inicia el motor de color.

## Evidencia requerida y estado real de esta sesión

| Frente | Evidencia exigida | Estado verificable |
|---|---|---|
| COL-001 | Entrevistas y mapa trazable de situaciones repetidas | Guion preparado; sin actas reales recibidas |
| COL-002 | Al menos 12 actas anonimizadas, frecuencia, alternativas e intención de pago | Registro vacío, se prepara control de evidencia |
| COL-004 | 20 pares, diversidad y permisos claros | 20 slots previstos, 0 medios aportados o descargados |
| COL-003 | Cinco competidores sobre los mismos pares y evidencia de resultados | Investigación documental/protocolo; cero ejecuciones reales |
| COL-005 | Tres hipótesis falsables y cuestionario de pago | Documentos presentes en PR #14 integrada; Issue #13 abierta sin approved |
| COL-006 | Acta con evidencia, riesgos y autorización explícita para el motor | Pendiente de evidencia y decisión humana |

No confundir códigos de salida correctos sobre plantillas con datos disponibles.
Los fixtures de tests son ajenos al conjunto de validación y a las entrevistas.
Los recuentos reflejan entradas aportadas a esta sesión; no se presupone que
no existan medios o entrevistas fuera del proyecto. El usuario puede aportarlos.

## Regla de conciliación de COL-005

El sincronizador exige Issue cerrada + approved y PR integrada si procede.
COL-005 requiere documentación; las tres hipótesis y el cuestionario están
presentes, pero el agente no acepta su calidad en nombre del usuario. Por eso
PR #14 integrada + Issue #13 abierta sin approved da review, no done. No hay
que forzar JSON, cerrar la Issue o inferir aprobación de un merge.

La revisión puede aceptar el instrumento y mantener sus hipótesis sin contrastar.
Son hechos distintos. La notificación existente se reutiliza para esta decisión.

## Orden de continuación

1. Revisar los instrumentos sin rebajar criterios después de obtener resultados.
2. Incorporar actas reales con consentimiento para notas y contenido anonimizado.
3. Incorporar medios privados y evidencia de permisos/preparación sRGB acordada.
4. Ejecutar el benchmark con versiones, mismos archivos/hash, ajustes y capturas.
   Un producto no accesible se registra como bloqueado, no como fallo de calidad.
5. Sintetizar resultados favorables y contrarios por segmento/escena; documentar
   límites, coste y opciones. No calcular mercado o demanda desde una muestra
   pequeña como si fuera representativa.
6. Usuario revisa el acta y decide go, pivot o stop. Incluso con evidencia
   favorable, esperar autorización explícita antes de P1.

Preparar herramientas de registro y protocolos de estos pasos es trabajo P0.
Implementar transformaciones, LUT o modelos de imagen es P1/P3 y queda fuera.

## Plantilla del acta humana (sin cumplimentar)

- Fecha, revisor responsable y versión de evidencia:
- Enlaces a COL-001…COL-005 y a los informes reales:
- Recuento de entrevistas, pares con permiso y comparativas ejecutadas:
- Casos favorables, contrarios y ausencias:
- Riesgos de color, privacidad, compatibilidad y viabilidad:
- Decisión: pendiente / go / pivot / stop:
- Alcance de la autorización P1, si la hubiera:
- Correcciones requeridas y responsable:

Un documento vacío o una opción de esta plantilla no es autorización. Ni el
agente ni un script rellenan la decisión o aplican approved por el usuario.

## Auditoría de estado reproducible

```powershell
python scripts/p0_status.py --github
python scripts/p0_status.py --github --ready --as-of 2026-10-30
```

La herramienta solo lee los tres registros y las Issues canónicas con roadmap.
Ignora solicitudes de notificación, detecta IDs duplicados y exige cierre más
approved para reflejar aceptación de cada tarea. Una PR fusionada no la inventa.
La fecha explícita debe actualizarse al reanudar una sesión posterior.

Exit 2 con --ready es el resultado esperado mientras falten evidencia o
aceptación. Exit 1 indica un validador/registro inválido o no disponible. Sin
--ready puede devolverse 0 para una auditoría estructural de registros vacíos;
no significa P0 completado. Si GitHub no se consulta o falla, no inferir aprobación.

Opciones --interviews, --dataset y --benchmark permiten leer registros locales
privados explícitos sin copiarlos a Git. --media-root comprueba los medios de
COL-004. El informe contiene contadores, no respuestas o rutas privadas.
automatic_p1_authorization siempre es false: este programa no concede permisos
ni inicia P1, aunque los registros y las etiquetas estén completos.
