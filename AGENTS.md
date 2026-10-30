# LumaForge · instrucciones permanentes para Codex

## Contexto obligatorio y fuente de verdad
Antes de cualquier trabajo lee, en este orden:
1. `docs/TRASPASO_A_CODEX.md` (decisiones y contexto del proyecto)
2. `docs/ARQUITECTURA.md` y `docs/ESTUDIO_DE_MERCADO.md`
3. `docs/OPERATIVA_CON_IA.md` y `docs/NOTIFICACIONES_Y_APROBACIONES.md`
4. `site/data/roadmap.json` (42 IDs COL-###, fases y criterios de aceptación)
5. `docs/DIARIO_DESARROLLO.md` y el estado actual del repositorio (issues, PR y rama)

El sitio existente es un **dashboard de planificación**, NO el motor de color ya implementado. No declares funcionalidad no probada. Las tareas son intenciones, no pruebas de desarrollo.

## Objetivo del producto
Construir un motor de transferencia de look desde referencias para foto y vídeo: análisis determinista/local primero; IA local opcional para adaptar individualmente; IA externa solo mediante decisión humana; exportaciones abiertas (LUT .cube primero, XMP cuando sea viable). Arquitectura híbrida local/web, Windows primero; no acoplar el núcleo a Photoshop ni producir resultados engañosos de color.

## Ciclo por cada tarea
- Trabaja exclusivamente con una Issue `[COL-###]` de la hoja de ruta, con sus criterios de aceptación, dependencias y límites.
- Actualiza la Issue a `status:in-progress` solo al empezar. Registra decisiones materiales en `docs/DIARIO_DESARROLLO.md` y en la PR, no alteres manualmente `status` del JSON para simular progreso.
- Crea rama `codex/COL-XXX-resumen`, realiza cambios acotados, tests y documentación. Adjunta evidencia reproducible; anota comandos y resultados reales.
- Está **autorizado de forma condicionada** a crear commits y hacer `git push` **solo a su rama de trabajo** y abrir PR a `main` una vez que el usuario haya habilitado GitHub y autorizado este procedimiento en la sesión inicial. No hacer push ni modificar `main` directamente. No hacer merge, cerrar Issues, ni aplicar `approved`.
- Si la PR está lista, ponla no-borrador y deja la Issue/PR en revisión. El dashboard se sincroniza por GitHub Actions; no finjas que una actualización es instantánea si la acción no ha terminado.
- Si requiere decisión, credenciales, gasto, licencias, API externa, acceso a datos privados, publicación, cambios destructivos o discrepancias de requisitos: abre o actualiza la Issue con la decisión, opciones y recomendación; después añade `needs-human` y comprueba el workflow y la mención. Detén únicamente el trabajo que depende de esa autorización y continúa con tareas independientes ya autorizadas. No trates el silencio ni el envío o recepción del aviso como aprobación.
- Nunca ejecutas con permisos irrestrictos por comodidad ni haces cambios fuera del workspace. Guarda secretos solo en el almacén de secretos correspondiente, nunca en Git, PR, web o logs.

## Aprobación
`done` se obtiene exclusivamente de las reglas del sync GitHub: issue cerrada + etiqueta `approved` + PR fusionada si corresponde. La IA nunca se autoaprueba. Para una sola cuenta GitHub, los requisitos de revisión formal necesitan un revisor distinto o controles externos: el texto del prompt por sí solo no sustituye permisos reales.

## Autonomía P0 y recuperación (instrucción del usuario, 2026-10-30)

- Crear/actualizar rutinariamente Issues, ramas y PR de P0 y publicar sus ramas
  está autorizado. Tras una entrega, continuar con otra tarea independiente
  elegible; detener únicamente trabajo que dependa de una decisión pendiente.
- Ningún merge, escritura directa en main, cierre aprobado o etiqueta approved
  por el agente. P1 requiere criterios de salida de P0 y autorización explícita
  del usuario; un merge o una notificación no cumplen esa autorización.
- Cada solicitud nueva usa título `[LUMAFORGE] ACCIÓN REQUERIDA — ...` y campos
  Qué has terminado, Qué necesitas de mí, Por qué necesitas mi intervención,
  Opciones disponibles, Tu recomendación, Cómo responder y Enlace. Publicar la
  solicitud antes de needs-human y comprobar workflow/mención. Reutilizar una
  solicitud para el mismo bloqueo, sin retirar/reaplicar etiquetas para repetirlo.
- Mantener docs/ESTADO_AGENTE.md con tareas, ramas, pruebas, cambios pendientes,
  bloqueos, siguientes tareas e instrucciones de reanudación en cada checkpoint.
- Distinguir preparación de instrumentos, ejecución real y aprobación humana.
  No rellenar evidencia ausente con fixtures de pruebas o hipótesis.

## Verificaciones técnicas
- Dashboard: `python -m unittest discover -s tests -v`.
- Nuevas funciones: añadir pruebas apropiadas, comprobar espacios de color, gestión de gamma, gamut clipping y reproducción consistente entre plataformas.
- Nada de fotos personales de clientes en Git ni de recursos descargados sin licencia.
- Al finalizar responde: tarea e Issue; rama/PR y enlace; cambios; tests con evidencia; limitaciones; decisión humana solicitada; siguiente tarea propuesta (sin iniciarla sin permiso).
