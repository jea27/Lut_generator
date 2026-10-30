# LumaForge · Entrega para Codex local en Windows

**EMPIEZA AQUÍ:** `GUIA_WINDOWS_CODEX.md` para instalar y conectar, después abre `PROMPT_INICIAL_CODEX.md` y pégalo en Codex. El contexto exhaustivo de la conversación anterior está en `docs/TRASPASO_A_CODEX.md`; las reglas permanentes para el agente están en `AGENTS.md`.

El sitio es una **hoja de ruta funcional**, no el producto de edición todavía. GitHub y el despliegue actual de Pages se verificaron el 30-10-2026. Las notificaciones móviles siguen sin validar.

---

# LumaForge · Centro de proyecto (starter funcional)

Sitio estático responsive y accesible desde navegador, con **42 tareas**, investigación, decisiones, arquitectura y sistema de sincronización automático de estado desde GitHub Issues/PRs cuando se despliega.

**Estado actual:** entrega de planificación, no motor de edición de color. El nombre es provisional. Las 42 tareas aparecen planificadas. No hay Issues COL creadas en la consulta inicial; el motor no está iniciado.

## 1. Probar en tu equipo

**Modo rápido:** abre `site/index.html` directamente. La web utiliza datos iniciales embebidos en `site/data/fallback.js`; el borrador de revisión se guarda en tu navegador si este permite localStorage.

**Modo servidor local (recomendado):** desde la raíz del proyecto:

```bash
python -m http.server 8080 --directory site
```

Abre http://localhost:8080. El dashboard reconsulta `data/roadmap.json` cada 60 segundos y muestra nuevas versiones publicadas. No requiere npm ni servicios de pago.

## 2. Publicar con URL accesible

1. Usa el repositorio existente **[jea27/Lut_generator](https://github.com/jea27/Lut_generator)**. **LumaForge** sigue siendo el nombre provisional del producto.
2. Conserva `.github/workflows/`, `docs/`, `scripts/`, `site/`, `tests/`, `AGENTS.md` y este README directamente en la raíz Git, sin una carpeta contenedora `lumaforge/`. Integra la corrección en `main` mediante revisión humana.
3. Mantén GitHub → **Settings → Pages → Build and deployment → Source: GitHub Actions** (verificado por API como `build_type: workflow` el 30-10-2026).
4. El workflow **Publicar roadmap** valida las PR hacia `main`, incluidas sus actualizaciones. Solo publica Pages tras un push a `main` y si las validaciones pasan; no despliega desde el ref de una PR. La propuesta local `sync-roadmap.yml` añade eventos de Issues, finalización de CI de PR, cron y ejecución manual desde main, pendiente de revisión e integración.
5. La URL configurada es `https://jea27.github.io/Lut_generator/`; el despliegue existente fue comprobado; los cambios locales nuevos siguen sin publicar.
6. Prueba desde el móvil. Si no se despliega, revisa el registro de Actions/permisos del repositorio.

En las PR se ejecutan pruebas Python y validaciones de JavaScript y JSON con permisos de lectura, sin usar el entorno `github-pages`. Tras un push a `main`, el job de publicación lee Issues y PR con `GITHUB_TOKEN`, genera un JSON **solo de metadatos no sensibles** y publica `site/` en Pages. La web vuelve a consultar ese JSON cada minuto, pero los cambios de Issues/PR solo se publican con el siguiente push a `main`. Los recursos usan rutas relativas y conservan la base `/Lut_generator/`. El refresco por eventos preparado en esta rama se documenta en `docs/PREPARACION_DESARROLLO.md`; todavía no está activo en main.

**Alternativa:** Cloudflare Pages puede desplegar la web cuando hay pushes al repo, pero para sincronizar Issues/PR sin commits hay que mantener la acción de generación y añadir una publicación/trigger. La plantilla lista funciona con GitHub Pages, no tiene configuración de Cloudflare ya conectada.

## 3. Crear tareas enlazadas

Ejemplo de Issue:

```
Título: [COL-009] Implementar análisis de estadísticas perceptuales
Etiqueta: roadmap
Descripción: Criterio de aceptación en site/data/roadmap.json
```

- Pon `status:in-progress` cuando la tarea realmente empiece.
- La PR del agente debe tener `[COL-009]` en el título para enlazarse.
- Cuando esté lista para revisar, la PR aparecerá como «Para revisar».
- Para marcar la tarea **Aprobada**, necesitas la issue cerrada + `approved` y una PR fusionada para tareas técnicas que la requieren.
- Si la tarea está bloqueada, pon `blocked`.

`python scripts/import_issues.py` simula 42 altas sin escribir. `--apply` crea etiquetas e Issues evitando IDs existentes y exige autorización humana previa.

## 4. ¿Cómo revisar desde la web?

- Abre Roadmap → Detalles de la tarea.
- Consulta el criterio de aceptación y los enlaces GitHub si están asociados.
- Escribe un borrador, guárdalo localmente o copia el comentario.
- Pega la revisión en la Issue o PR; **la web pública es de solo lectura para GitHub**. Esto evita almacenar tokens de escritura en el navegador.

## 5. Seguridad del modelo público/privado

**Importante:** GitHub Pages normalmente expone el sitio y su JSON a quien tenga el enlace, aunque el repositorio de origen no sea público según el plan/configuración. No publicar un roadmap derivado de issues privadas con títulos o enlaces sensibles. Si prefieres código privado + dashboard público, crea un proyecto de publicación separado con campos sanitizados y credenciales del lado de Actions. Esa arquitectura de dos repositorios está documentada, pero no implementada en este starter.

El sitio no ejecuta IA; solo observa el progreso. La URL de Pages existente se ha verificado; una publicación posterior requiere revisión y autorización.

## 6. Documentación

- `docs/ESTUDIO_DE_MERCADO.md`: competencia, nichos, precios publicados, evidencia y validación de negocio.
- `docs/ARQUITECTURA.md`: contratos de color, motor, IA, vídeo, exportación y riesgos.
- `docs/OPERATIVA_CON_IA.md`: trabajo Codex/agentes, Issues, revisiones, seguridad y estados.
- `site/data/roadmap.json`: fuente de fases, tareas, decisiones y riesgos.
- `scripts/sync_github.py`: reconciliación de metadatos con Issues/PRs.
- `tests/test_sync.py`: pruebas de reglas de aprobación.

## 7. Criterios de aceptación del starter

- Abrir localmente sin npm ni servicios externos.
- Navegar por seis apartados responsive.
- Filtrar 42 tareas y ver sus criterios de aceptación.
- Mantener borradores de revisión localmente (si el navegador lo permite).
- Datos iniciales con progreso **0%**, sin inventar actividad.
- Actualización automática tras despliegue y autenticación de GitHub Actions.
- No contar tareas técnicas como completas sin PR fusionada y aceptación explícita.

### Ejecutar tests

```bash
python -m unittest discover -s tests -v
```

La reestructuración, las comprobaciones de conservación y las limitaciones de la validación están registradas en `docs/REESTRUCTURACION_RAIZ.md`.

Preparación del desarrollo y evidencias: `docs/PREPARACION_DESARROLLO.md`. Primera tarea P0: `docs/P0_COL-001_SEGMENTOS.md`.

COL-005: [hipótesis de negocio](docs/P0_COL-005_HIPOTESIS_NEGOCIO.md) y
[cuestionario de disposición a pagar](docs/P0_COL-005_CUESTIONARIO.md).
Instrumentos preparados para revisión; no contienen resultados de entrevistas.

Auditoría P0: `python scripts/p0_status.py --github --ready`. Un exit 2 informa
de evidencia o aceptación pendiente; no lo solventes inventando registros.
Recuperación de sesión: [docs/ESTADO_AGENTE.md](docs/ESTADO_AGENTE.md).
