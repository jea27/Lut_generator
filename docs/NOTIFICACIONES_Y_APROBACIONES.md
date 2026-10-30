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
- **Revisión de código:** cuando se abre o se marca como lista para revisión una PR no-borrador `[COL-###]`, el bot menciona al revisor para revisar diff, tests y evidencias.
- **Autorización:** gastos, proveedores, secretos, publicar a producción, permisos, arquitectura no aprobada y operaciones destructivas quedan detenidas hasta respuesta explícita; no basta con notificar.

## Prueba mínima (cuando el repo esté conectado)
```powershell
gh label create needs-human --color F9A825 --force
gh issue create --title "[COL-000] PRUEBA aviso móvil" --body "Prueba: confirmar recepción y cerrar manualmente." --label needs-human
```
Esta prueba genera una Issue fuera de los 42 IDs válidos y podría permanecer fuera del dashboard; ciérrala/bórrala una vez comprobada. Asegúrate de que el workflow fue habilitado en Actions y revisa su ejecución si no llega push.

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
`publish-roadmap.yml` valida las PR hacia `main` y publica Pages únicamente tras un push a `main`, después de superar la validación. Sincroniza metadatos en cada publicación; no se publica por cambios de Issues, cron ni ejecución manual. La web consulta JSON periódicamente, pero esos cambios de estado se reflejan tras el siguiente push a `main`. Si Pages no está desplegado, la sincronización visual remota no funciona aunque el repo sí tenga Issues.

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
críticos o el disparador manual: el manual del workflow actual se omite por su
condición de job. Para repetir la prueba, usar una Issue acordada y añadir
needs-human después de publicar la pregunta. Los cambios más amplios de
seguimiento siguen separados en la rama local de preparación P0.
