# Revisiones de capacidades · COL044 / Issue76

La sección **Mis revisiones** permite abrir una capacidad, leer criterio/pasos,
completar checklist y elegir Aprobar o Pedir cambios. El botón final copia el
comentario y abre su Issue: pegarlo y publicarlo autenticado como **jea27**.
La página no envía una aprobación por su cuenta ni guarda un token de GitHub.
Observaciones públicas: no introducir personas, fotos, rutas privadas o secretos.
Los borradores del modal viven solo en memoria de esa pestaña.

## Fuente de verdad y seguridad

1. Comentario original `LUMAFORGE_REVIEW_V1` con JSON estricto: feature, revision,
   commit, version, decision, checklist y notes. No se admite añadir actor/fecha
   inventados desde la web, claves duplicadas, contenido extra o JSON no finito.
2. Workflow `Validar revisión humana`, evento issue_comment, checkout **main**
   con historia completa y sin credenciales persistentes. Lee el evento desde
   GITHUB_EVENT_PATH, sin interpolar el comentario en shell ni ejecutar su texto.
   Solo contents:read e issues:write para el recibo/cola; sin commits automáticos.
3. Verifica login jea27, ID45896918 y tipo User, tanto emisor del evento como
   autor obtenido de la API. Issue canónica, comentario sin edición, hash igual
   al evento, versión/commit ancestro y huella actual. Aprobar exige todas las
   comprobaciones; correcciones exigen observaciones, sin forzar checklist pasado.
4. Recibo único de github-actions[bot] registra capacidad, huella, commit/versión,
   usuario/ID, fecha UTC de GitHub, checklist, ID/hash del comentario y presencia
   de observaciones. El original conserva observaciones; no se copian al JSON
   público. La proyección revalida autor, original, hash y recibo: no basta pegar
   un texto que parezca un recibo o llamar approved a una etiqueta.
5. Sync publica estado por **ID de capacidad**, no por Issue compartida. Glow,
   Difusión, Fade y su entrega manual se deciden individualmente. El denominador
   de8 entregables núcleo sigue independiente de sus componentes y la demo.

Huella SHA256 de blobs Git declarados en review_paths, versión y criterios/
checklist. Cambios de documentación ajena no invalidan; cualquier modificación
de archivo relacionado sí exige revisar de nuevo, de forma conservadora. No se
promete detección semántica de significancia. Historial permanece en recibos y
comentarios, con commit/huella anterior visible. No se ejecuta código del commit
revisado: solo se leen objetos Git con argumentos validados.

Editar/borrar el comentario invalida esa decisión; no reactiva una aprobación
antigua. Para corregir una decisión se publica un nuevo comentario completo.
Reintentos/eventos duplicados no generan otro recibo de la misma decisión;
concurrencia por Issue y orden por ID original evitan aplicar tarde una decisión
antigua sobre otra reciente. La aceptación se muestra aunque CI esté pendiente;
su eje técnico sigue independiente. Ningún merge o etiqueta aprueba capacidades.
Las42 tareas históricas conservan sus reglas y no se cierran/aprueban por este flujo.

## Correcciones y agente

El recibo de cambios registra observaciones en su comentario original y crea
automáticamente la señal `agent-action-required`. Se retira cuando ninguna
capacidad de esa Issue tiene correcciones vigentes; aprobar Glow no borra una
solicitud de Difusión. La cola por capacidad aparece en Mis revisiones. Es una
notificación persistente de trabajo en GitHub, no una promesa de despertar una
sesión Codex que no esté ejecutándose. El agente consulta esta cola al reanudar,
enlaza correcciones y entrega una nueva versión para que el responsable la pruebe.

Los comentarios del bot no encadenan otros workflows mediante el token por
defecto: el refresco usa workflow_run completado de Validar revisión humana.
También se cubren comentarios editados/eliminados y el cron existente. API fallida
conserva snapshot anterior; no concede una aprobación ni representa éxito nuevo.

## Demostración y activación

Issue77 y review-demo son sintéticos, separados de las15 capacidades y métricas.
El agente solo puede publicar aprobaciones de esta demo; nunca de producto real.
El evento issue_comment requiere el workflow en la rama por defecto: ver
[documentación GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#issue_comment).
Sin hacer merge, la prueba usa dispatch del workflow existente en esta rama:
solo actor autorizado, comentario numérico y demo/Issue77; job Pages omitido.
Ejecuta el mismo procesador, genera recibo real de Actions y guarda proyección
como artefacto, sin desplegar código de PR como main. Resultados y límites en
docs/evidence/HUMAN_REVIEW_DEMO.json al finalizar la prueba.

Después de integración humana: comprobar event issue_comment de la demo,
workflow de validación y sync completos, y JSON público actualizado. Esa última
prueba de activación en producción no se sustituye por la demostración de rama.
No se hace merge por el agente para conseguirla.

## Posible aprobación directa futura

Requeriría registrar una GitHub App con acceso mínimo a Issues del repositorio,
autenticar a jea27 y verificar su ID en un servicio de confianza. Un endpoint
serverless podría gestionar callback/token de usuario de corta duración, CSRF,
nonce y versión, y publicar el mismo comentario. Secreto de cliente/clave de app
quedan en almacén del servidor, nunca en Pages ni localStorage. Se necesita
autorización para registrar la app, sus permisos y el servicio; no se configura
ni compra nada en esta entrega. Referencia: [tokens de usuario de GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app).

La comprobación actual acredita la cuenta GitHub, no la presencia física del
propietario: quien utilice credenciales de esa cuenta puede actuar como ella.
Por eso los agentes tienen prohibido emitir aprobaciones reales y las pruebas
utilizan exclusivamente demo. No se presenta el prompt como separación técnica
de identidades ni como autenticación adicional inexistente.
