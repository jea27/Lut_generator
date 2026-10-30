Preparación parcial de COL-006 (Issue #19), sin decisión go/no-go ni inicio de P1.

Incluye punto de recuperación, mapa de evidencia P0, conciliación de COL-005 y
protocolo de autonomía/avisos pedido por el usuario. COL-005 permanece en review
porque la Issue no está cerrada/aprobada; integrar su PR no supone aceptación.

El aviso de PR conserva los permisos originales y el mecanismo Issue+mención,
pero usa título [LUMAFORGE] ACCIÓN REQUERIDA y los siete campos obligatorios.
Deduplica PR y peticiones de Issue por contenido. Una petición incompleta se
rechaza en vez de generar un aviso ambiguo. El modo manual recibe el número de una Issue existente, valida su formato
y utiliza la misma deduplicación. No se instalan herramientas ni se modifican permisos de repositorio.

27 unittest locales OK, incluidas pruebas del script inline de Actions, formato
completo, petición incompleta y deduplicación. No se han inventado entrevistas,
medios, métricas ni aceptación. Las entregas de COL-002/003/004 se hacen en ramas
y PR independientes; ESTADO_AGENTE registra su estado real al cerrar la sesión.

Revisión: aceptar el mecanismo y control documental o pedir correcciones. No
cerrar automáticamente Issues de producto y no confundir este documento con
la autorización para P1. Evidencias remotas se registran en la Issue.
