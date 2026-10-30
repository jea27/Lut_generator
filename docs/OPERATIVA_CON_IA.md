# Manual de trabajo humano + IA + dashboard

## ¿Qué actualiza el dashboard realmente?

El **workflow incluido** consulta el estado de Issues y pull requests del **mismo repositorio** cada 30 minutos y en eventos de Issues/push a main. Publica `site/data/roadmap.json` en GitHub Pages; la web lo consulta al cargar y cada 60 segundos mientras está abierta. El workflow publica estado, **no implementa código**.

No hay agente de desarrollo conectado de forma predeterminada. Para automatizar programación debes activar por separado Codex en tu IDE o un agente GitHub que pueda recibir issues. No se ha conectado nada a tu cuenta.

## Convención de seguimiento

- Cada issue lleva ID estable en su título: `[COL-007] Definir pipeline...` y etiqueta **roadmap**.
- El agente trabaja sobre rama independiente y abre una PR con el mismo ID `[COL-007] ...` en su título.
- Etiqueta `status:in-progress`: en curso.
- PR abierta / fusionada o issue cerrada sin aprobación: **para revisar**.
- Etiqueta `blocked`: bloqueada (prioritaria sobre cualquier estado).
- **Aprobada:** issue cerrada con etiqueta `approved`, y **PR fusionada si ese entregable la requiere**. No permitir al agente aplicar `approved`.
- Las tareas humanas de investigación pueden aprobarse sin PR.
- Las notas creadas en el dashboard son *borradores locales*: copiar y pegar en la issue o PR. No hay escritura directa desde el sitio público.

## Qué debería hacer un agente (ejemplo de prompt para Codex)

```
Actúa como implementador de LumaForge. Lee docs/ARQUITECTURA.md,
docs/OPERATIVA_CON_IA.md y la tarea [COL-XXX] en site/data/roadmap.json.

Objetivo: implementar SOLO la tarea asignada y cubrir el criterio de aceptación.
Condiciones: no hagas merge; no apliques 'approved'; no cierres issues;
no modifiques Git o ramas de terceros sin autorización; no subas imágenes
privadas; no cambies ámbitos de color sin documentarlo; añade tests y
muestras reproducibles. Al terminar, describe decisiones, riesgos, pruebas
ejecutadas y cambios pendientes. Prepara una PR para revisión humana.
Si faltan requisitos esenciales o hay riesgo de pérdida de datos, detente
y explica la decisión necesaria.
```

## Checklist de revisión humana

1. ¿Se cumple el criterio de aceptación de la issue?
2. ¿Hay evidencia verificable (pruebas, capturas, dataset, comparativa)?
3. ¿Se respetan interfaces, privacidad, color space, licencias y alcance?
4. ¿Las pruebas de CI pasan y hay regresiones en los casos difíciles?
5. ¿Puedo probarlo en mi PC o en una previsualización antes de aprobar?
6. Si no: comentar y solicitar cambios. Si sí: integrar PR, añadir `approved` y cerrar issue.

> Una PR fusionada no equivale automáticamente a aceptación del usuario. Se publica como «para revisar» hasta que tenga aprobación explícita.

## Ruta para automatización real de desarrollo

**Nivel 1 (recomendado):** Codex en IntelliJ/terminal desarrolla issues seleccionadas manualmente; publica ramas/PR; GitHub Actions actualiza el dashboard.

**Nivel 2:** Agente remoto GitHub habilitado (según plan y disponibilidad), que acepta tareas/Issues y crea PR; los controles de branch protection mantienen el merge humano. GitHub documenta agentes que reciben issues: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/kick-off-a-task

**Nivel 3:** Orquestador de cola que inicia tareas priorizadas después de aprobación, registra uso de IA, presupuesto, artefactos de prueba y cambios. **No incluido** en este starter: requiere permisos, infraestructura y límites; no es seguro automatizarlo sin política y repo.

Codex también tiene funciones de revisión de PR que pueden complementar, no sustituir, a la revisión manual: https://help.openai.com/es-es/articles/20001552-review-pull-requests-with-codex

## Seguridad de repositorios privados

Si el motor/estrategia es privado, evita desplegar directamente una versión pública con títulos internos de Issues. Lo ideal es tener un repositorio privado de código y un repositorio público `roadmap-public` al que un workflow autorizado envíe solo `id`, `status`, `phase`, `updated_at` y enlaces públicos permitidos. El paquete actual de un repositorio no implementa esa separación; está diseñado para una prueba controlada con tareas no sensibles.
