# Notificaciones móviles, GitHub y límites de autonomía

## Resumen
El sistema no envía push desde Codex de forma intrínseca: lo hace **GitHub Actions + GitHub Mobile** tras crear una solicitud visible en GitHub. Esto puede retrasarse por colas y opciones de notificaciones. Requiere conexión a Internet, Actions habilitado y GitHub configurado. No notifica si Codex se queda bloqueado sin publicar el evento; si el agente está totalmente desconectado, avisa solo en su consola local.

## Configuración inicial (GitHub)
1. Crea repositorio y publica el código con `gh auth login`, `git push`.
2. En Settings → Secrets and variables → Actions → **Variables** crea `REVIEWER_GITHUB` con tu nombre de usuario GitHub (no correo, sin @).
3. Activa GitHub Actions; la acción `.github/workflows/alert-human.yml` no utiliza secretos externos.
4. Instala **GitHub Mobile** en tu teléfono, inicia sesión y habilita notificaciones push de **menciones, tareas asignadas y revisiones**.
5. Comprueba la app: en Settings → Notifications del móvil da permiso a las notificaciones; en el repositorio selecciona Watch (participaciones/menciones o personalizado).

## ¿Cuándo salta el aviso?
- **Necesita ayuda:** Codex debe añadir la etiqueta `needs-human` a una Issue existente del roadmap y publicar antes una pregunta específica, opciones y riesgos. El workflow, activado al etiquetar, deja un comentario como `github-actions[bot]` que menciona al revisor.
- **Revisión de código:** cuando se abre, actualiza o marca lista una PR no-borrador `[COL-###]`, el bot crea una Issue de revisión vinculada a la PR, explica la decisión, añade needs-human y menciona al revisor allí. Las actualizaciones no duplican la solicitud existente. Se evita comentar en la PR porque el token actual devolvió 403; no se amplían permisos.
- **Autorización:** gastos, proveedores, secretos, publicar a producción, permisos, arquitectura no aprobada y operaciones destructivas quedan detenidas hasta respuesta explícita; no basta con notificar.

## Prueba mínima y solicitudes actuales

La recepción en el móvil ya fue confirmada. No repetir la prueba si el mismo
bloqueo ya tiene solicitud. Para una decisión nueva, crear o actualizar una
Issue con el título y los siete campos del protocolo, y después needs-human.
Una Issue COL-000 de ejemplo con cuerpo genérico ya no cumple el formato.

Para repetir expresamente una acción de prueba autorizada, usar una Issue de
acción existente, completa y etiquetada. El modo manual recibe su número:

```powershell
gh workflow run alert-human.yml --repo jea27/Lut_generator --ref main -f issue_number=NUMERO_REAL
```

Una petición ya mencionada se omite por su marcador; no retirar/aplicar la
etiqueta para reenviar el mismo bloqueo. Verificar run, comentario bot y, solo
si se está validando una recepción nueva, confirmación del usuario. Mantener
el registro histórico de las pruebas anteriores sin repetir notificaciones.

## Protocolo para el agente
El agente debe publicar un comentario de decisión en una Issue antes de marcar `needs-human`:
- Qué está haciendo y a qué criterio afecta.
- Qué acción necesita: contraseña/autorización/elección/corrección.
- 2 opciones, riesgos y recomendación (sin ejecutar la opción recomendada).
- Cómo se reanuda.
Tras etiquetar, detener únicamente el trabajo dependiente de esa autorización y continuar con tareas independientes ya autorizadas. Comprobar el workflow y la mención; envío y recepción no equivalen a aprobación. Antes de reanudar la decisión pendiente, leer comentarios nuevos y confirmar autorización explícita.

## Autorización y revisión real
El código puede publicarse en **rama `codex/...` y PR**, solo con el permiso inicial del usuario y credenciales adecuadas. `main` permanece bajo control humano. No confundir un comentario `aprobado` en una conversación con la posibilidad técnica de prevenir un merge si el agente comparte credenciales con el propietario. Una protección robusta requiere permisos separados (GitHub App/bot de agente, branch protection y/o revisor distinto).

Con una única cuenta GitHub, la aprobación formal de la propia PR puede no contar como revisión independiente. Se puede validar manualmente y hacer el merge personalmente, pero no inventar una barrera de seguridad que GitHub no aplica.

## Dashboard
`publish-roadmap.yml` valida PR y publica desde main. El workflow integrado `sync-roadmap.yml` sincroniza Issues/PR mediante eventos, cron y ejecución manual; no es necesario hacer commits de estados. Los cambios requieren que Actions termine y Pages sirva el nuevo JSON.

## Diferencia frente a ejecución 24/7
Ni el dashboard ni la acción de GitHub programan a Codex para desarrollar en tu PC: para procesamiento local continuo debes mantener PC encendido y una sesión/proceso Codex en marcha, o construir más adelante un runner/orquestador. No hay autonomía en segundo plano hasta configurar explícitamente ese componente.

## Prueba real verificada · 2026-10-30

- Repositorio: `jea27/Lut_generator`; CLI autenticada como `jea27`.
- Variable Actions consultada: `REVIEWER_GITHUB=jea27`. Ya existía; no se cambió.
- El workflow publicado utiliza `vars.REVIEWER_GITHUB`, la pasa al entorno y
  construye una mención al responsable. La etiqueta `needs-human` ya existía.
- Creada [Issue de prueba #3](https://github.com/jea27/Lut_generator/issues/3)
  con decisión solicitada, opciones y recomendación; después se añadió la etiqueta.
- [Ejecución 41079364488](https://github.com/jea27/Lut_generator/actions/runs/41079364488):
  evento issues, job notify y paso de mención finalizados con success.
- [Comentario del bot](https://github.com/jea27/Lut_generator/issues/3#issuecomment-6526303053)
  verificado: menciona a `@jea27`.
- Confirmación expresa del usuario en este chat: **«Sí, recibida en el móvil»**.
  Queda validado el recorrido real por etiqueta hasta GitHub Mobile para esta prueba.

No se modificaron permisos, tokens, protecciones ni ajustes del móvil. No se
fusionaron PR ni se aprobaron tareas. El cierre de la prueba queda al usuario.
Esta comprobación no garantiza entregas futuras ni valida los avisos por fallos
críticos o el disparador manual en aquella versión. La versión posterior incorpora
un target explícito y deduplicación, con pruebas locales documentadas. Para repetir la prueba, usar una Issue acordada y añadir
needs-human después de publicar la pregunta. Los cambios más amplios de
seguimiento siguen separados en la rama local de preparación P0.

### Revisión de PR sin ampliar permisos

El primer aviso de PR #4 falló con 403 al comentar en la propia PR:
https://github.com/jea27/Lut_generator/actions/runs/41079917645.
La corrección conserva todos los permisos y publica la solicitud en una Issue.
Run real correcto: https://github.com/jea27/Lut_generator/actions/runs/41080088759.
Solicitud creada por el bot: https://github.com/jea27/Lut_generator/issues/5,
con needs-human y comentario de mención verificables. La recepción móvil
confirmada por el usuario corresponde a la prueba #3; no se presupone una
confirmación adicional para cada aviso posterior.

## Formato obligatorio de acciones humanas

Título: `[LUMAFORGE] ACCIÓN REQUERIDA — Descripción concreta`.

El cuerpo contiene secciones Markdown `## Qué has terminado`,
`## Qué necesitas de mí`, `## Por qué necesitas mi intervención`,
`## Opciones disponibles`, `## Tu recomendación`, `## Cómo responder`
y `## Enlace`, con contenido concreto. Crear primero el cuerpo, después
needs-human. No usar títulos genéricos ni un aviso para cada actualización.

La propuesta de este cambio valida ese formato antes de mencionar al revisor
y deduplica una misma petición por contenido; las PR por su número estable.
El cambio no convierte un comentario o merge en aceptación de producto.
Las Issues históricas conservan su historia; para el mismo bloqueo se reutilizan
y se actualiza su formato sin reenviar una notificación ya entregada.
