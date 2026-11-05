# Project OS · autenticación y decisiones directas (COL-048)

## Estado y alcance

Esta implementación añade Cloudflare Pages Functions bajo `/api/*` para que
Project OS pueda autenticar a `jea27` y publicar el comentario estructurado que
ya valida el workflow `issue_comment`. La GitHub App actúa en nombre del usuario;
GitHub sigue siendo la auditoría y fuente de verdad. Cada decisión identifica una
capacidad y su revisión. El backend vuelve a comprobar la huella, versión,
checklist y Issue del snapshot público antes de enviar.

La ruta `GET /api/product` obtiene el snapshot publicado actual de GitHub Pages.
Así el host aislado de Cloudflare ve los cambios que Actions y el sincronizador
publican, sin copiar `product.json` ni fingir una actualización local.

El plan local no crea una App, base D1 ni proyecto Cloudflare. Tampoco demuestra
un login real, la atribución de un comentario real, el disparo de `issue_comment`
ni la visualización en iPhone. Esos criterios requieren configuración y E2E
humana en el entorno de staging.

## Rutas

| Ruta | Acción |
| --- | --- |
| `GET /api/auth/github/start` | Crea state de un solo uso y PKCE S256; inicia OAuth con `offline_access` y cuenta sugerida `jea27`. |
| `GET /api/auth/github/callback` | Consume state una vez, intercambia el código, valida login/ID y acceso de lectura a Issue 77. |
| `GET /api/auth/session` | Informa si hay sesión; devuelve CSRF temporal solo al navegador autenticado. |
| `POST /api/auth/logout` | Valida origen y CSRF, revoca sesión local y solicita revocación del grant. |
| `POST /api/reviews/{featureId}/decision` | Valida sesión, CSRF, rate limit, versión, checklist e idempotencia; publica el comentario compatible con el workflow existente. |
| `GET /api/product` | Sirve el snapshot público actual para mantener la vista de staging sincronizada. |

Las funciones no devuelven tokens al navegador. Los tokens de acceso y refresh
se guardan cifrados con AES-GCM en D1; la cookie de sesión es opaca, `Secure`,
`HttpOnly`, `SameSite=Lax`, `Path=/` y `__Host-`. La clave maestra se usa para
derivar claves separadas de cifrado y CSRF. Los errores y respuestas no incluyen
credenciales ni cuerpos sin filtrar de GitHub.

La idempotencia se reserva en D1 antes de llamar a GitHub. Si la conexión falla
tras crear el comentario, un reintento busca el mismo cuerpo exacto atribuido a
`jea27` antes de publicar otro. Una respuesta `202` indica que la misma petición
sigue procesándose; se reintenta con la misma clave. El comentario es público y
el estado solo cambia después de que GitHub Actions lo valide y sincronice.

La demo `review-demo`/Issue 77 solo se acepta cuando `ENABLE_REVIEW_DEMO=true`.
Las capacidades reales se rechazan si ya están aprobadas o si cambió commit,
versión, revisión o checklist. Si el snapshot público supera 60 minutos de edad,
el endpoint falla cerrado.

## Esquema D1

Aplicar `migrations/0001_project_os_auth.sql` a la base enlazada como
`REVIEW_DB`. Incluye state OAuth de un uso, sesiones revocables, envíos
idempotentes y contadores de rate limit con identificadores HMAC. No almacena
direcciones IP en claro.

## Configuración prevista, pendiente de pasos humanos

1. En Cloudflare, usar exclusivamente Workers Free y crear un proyecto Pages de
   staging desde `jea27/Lut_generator`. Limitar la integración de GitHub a este
   repositorio y desplegar solo `codex/COL-048-project-os-auth`; output
   `site`, comando de build vacío, Functions desde `/functions`. No activar
   deploy de `main` ni otras ramas.
2. Crear una base D1 para staging, aplicar la migración y enlazarla con el nombre
   `REVIEW_DB`. No crear Durable Objects, Worker adicional ni dominio.
3. Crear una GitHub App propiedad de `jea27`, disponible solo para esta cuenta,
   con callback exacto
   `https://lumaforge-project-os-jea27.pages.dev/api/auth/github/callback`.
   Dar solo `Metadata: read` e `Issues: read/write`; instalarla únicamente en
   `jea27/Lut_generator`. Habilitar expiración de tokens y usar `offline_access`.
   No generar clave privada ni PAT.
4. Configurar variables públicas de entorno: `GITHUB_APP_CLIENT_ID`,
   `ALLOWED_ORIGIN=https://lumaforge-project-os-jea27.pages.dev` y
   `ENABLE_REVIEW_DEMO=true` solo en staging.
5. Guardar en Cloudflare Secrets `GITHUB_APP_CLIENT_SECRET` y
   `SESSION_ENCRYPTION_KEY` (32 bytes, codificados en Base64). No copiar secretos
   al chat, Issue, repositorio, Pages ni logs.

El nombre de proyecto y callback son propuestas exactas; si el hostname está
ocupado o la pantalla solicita permisos adicionales, detener el alta y revisar
el alcance antes de aceptar. No se debe desplegar públicamente hasta validar las
pantallas y confirmar que el plan Free y el acceso al repo son los acordados.

## Pruebas locales

`node --test tests/project_os_auth.test.mjs`
usa `node:sqlite` para ejecutar la migración y dobles locales de la API de
GitHub. Comprueba cifrado/CSRF, validación estricta,
versiones obsoletas, publicación atribuida simulada e idempotencia. Estas pruebas
no son autenticación real ni E2E de GitHub. No enviar comentarios reales durante
ellas.

La E2E pendiente debe recorrer login real → Issue 77 → aprobación y solicitud de
cambios → evento `issue_comment` → workflow/sincronización → estado actualizado,
y repetirse en iPhone y escritorio. No aprobar capacidades reales en pruebas.
