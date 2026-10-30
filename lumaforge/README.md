# LumaForge · Entrega para Codex local en Windows

**EMPIEZA AQUÍ:** `GUIA_WINDOWS_CODEX.md` para instalar y conectar, después abre `PROMPT_INICIAL_CODEX.md` y pégalo en Codex. El contexto exhaustivo de la conversación anterior está en `docs/TRASPASO_A_CODEX.md`; las reglas permanentes para el agente están en `AGENTS.md`.

El sitio es una **hoja de ruta funcional**, no el producto de edición todavía. Ni GitHub ni notificaciones móviles están conectados hasta completar los pasos y autorizaciones iniciales.

---

# LumaForge · Centro de proyecto (starter funcional)

Sitio estático responsive y accesible desde navegador, con **42 tareas**, investigación, decisiones, arquitectura y sistema de sincronización automático de estado desde GitHub Issues/PRs cuando se despliega.

**Estado actual:** entrega de planificación, no motor de edición de color. El nombre es provisional. Las tareas inicialmente aparecen planificadas; no se ha conectado GitHub ni un agente de desarrollo real.

## 1. Probar en tu equipo

**Modo rápido:** abre `site/index.html` directamente. La web utiliza datos iniciales embebidos en `site/data/fallback.js`; el borrador de revisión se guarda en tu navegador si este permite localStorage.

**Modo servidor local (recomendado):** desde la raíz del proyecto:

```bash
python -m http.server 8080 --directory site
```

Abre http://localhost:8080. El dashboard reconsulta `data/roadmap.json` cada 60 segundos y muestra nuevas versiones publicadas. No requiere npm ni servicios de pago.

## 2. Publicar con URL accesible

1. Crea un repositorio GitHub nuevo, preferiblemente inicialmente **público** si vas a usar la plantilla de un repositorio. No subas secretos ni materiales de clientes.
2. Sube todos los archivos y carpetas, incluida `.github/workflows/publish-roadmap.yml`, en rama `main`.
3. En GitHub → **Settings → Pages**, selecciona **Build and deployment → Source: GitHub Actions**.
4. En **Actions**, ejecuta manualmente el workflow **Publicar roadmap** (o haz push a `main`).
5. GitHub Pages te dará la URL pública: normalmente `https://USUARIO.github.io/REPOSITORIO/`.
6. Prueba desde el móvil. Si no se despliega, revisa el registro de Actions/permisos del repositorio.

El workflow lee Issues y PR con `GITHUB_TOKEN`, ejecuta tests, genera un JSON **solo de metadatos no sensibles** y publica `site/` en Pages. La web vuelve a consultar ese JSON cada minuto; las actualizaciones de Issues/push se publican después de que termine la acción, y las PR abiertas sin otro evento se reflejan al siguiente cron (cada 30 minutos, sujeto a retrasos de GitHub).

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

El script no crea issues automáticamente para evitar 42 tickets no revisados. Si deseas automatizar el alta, crea un script de importación con confirmación humana y evita duplicados.

## 4. ¿Cómo revisar desde la web?

- Abre Roadmap → Detalles de la tarea.
- Consulta el criterio de aceptación y los enlaces GitHub si están asociados.
- Escribe un borrador, guárdalo localmente o copia el comentario.
- Pega la revisión en la Issue o PR; **la web pública es de solo lectura para GitHub**. Esto evita almacenar tokens de escritura en el navegador.

## 5. Seguridad del modelo público/privado

**Importante:** GitHub Pages normalmente expone el sitio y su JSON a quien tenga el enlace, aunque el repositorio de origen no sea público según el plan/configuración. No publicar un roadmap derivado de issues privadas con títulos o enlaces sensibles. Si prefieres código privado + dashboard público, crea un proyecto de publicación separado con campos sanitizados y credenciales del lado de Actions. Esa arquitectura de dos repositorios está documentada, pero no implementada en este starter.

El sitio no ejecuta IA; solo observa el progreso. No se ha desplegado ninguna URL real de tu cuenta.

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
