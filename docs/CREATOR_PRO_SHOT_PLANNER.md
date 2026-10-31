# Creator, Pro y Shot Planner — entrega incremental

COL-045 (#81), COL-046 (#82), COL-047 (#83). Código de desarrollo sobre la beta
existente; no sustituye ni distribuye un instalador candidato. Las 42 tareas
históricas y las puertas independientes de beta/venta se conservan.

## Qué se puede usar

Creator guía referencia → imagen → color → intensidad → comparación → PNG/JPG.
La demo CC0 se abre con un botón. El acabado sigue siendo manual: glow, difusión
y fade no se extraen automáticamente de una referencia. Presets y comparador
siguen disponibles. Pro muestra los métodos, estadísticas, controles detallados,
receta, LUT y lotes existentes. Cambiar el modo solo cambia la interfaz: no hay
segundo motor ni conversión oculta de la receta. Ajustes Pro activos se advierten
en Creator. El modo y preferencias comparten almacenamiento, con escritura
ordenada; los registros anteriores sin modo se migran a Creator.

La exportación requiere una preview de la imagen y receta actuales, incluyendo
efectos ópticos. Un resultado anterior, error o preview pendiente no habilita
exportar una versión que no se ha visto. Se elimina el temporizador redundante
al iniciar una preview explícita; no se cambia la matemática de color.

## Primer Shot Planner

En Pro, importar referencia o demo → Shot Planner → elegir propuesta → Preparar
propuesta local. Analiza una muestra de hasta 512 px: formato, luminancia lineal
sRGB, saturación de canales y posición de regiones luminosas. Los píxeles
transparentes no participan. Estas medidas no recuperan radiancia de escena,
CCT, dirección de luces, relación key/fill ni rango dinámico de cámara.

El usuario elige escala de plano, lado/calidad de key, contraste, sensor/focal
disponible, apertura, fps, obturación, WB, altura y movimiento. El montaje es una
hipótesis de trabajo para un sujeto/escena controlados, no un reconocimiento
semántico ni una reconstrucción de la foto. La focal original queda sin datos.
La focal equivalente horizontal solo se calcula si el usuario aporta óptica y
ancho de sensor. ISO base, perfil y exposición requieren la cámara y medición real.

Cada indicación distingue observación, estimación, recomendación y cálculo
fundamentado. Incluye alternativas de equipo, checklist, continuidad de color y
limitaciones. El esquema cenital es propio, editable mediante selector y sliders
X/Y (teclado/táctil); rim y práctica son opcionales. Las distancias son propuestas.
Se conserva al volver al editor o cambiar Creator/Pro durante la sesión.

Guardar plan JSON conserva diagrama, elecciones, checklist y receta, sin imagen,
EXIF, nombre de archivo o ruta. `human_validated=false` permanece incluso cuando
se marcan checks. No es el formato LookRecipe: `lumaforge-shot-plan-v1` incluye
la receta de color/acabado; `.cube` sigue conteniendo solo color. El plan no se
guarda automáticamente ni se reimporta todavía: conservar el JSON descargado.
Cambiar elecciones/receta marca la propuesta desactualizada e impide exportarla
hasta regenerar; se advierte que regenerar reinicia ediciones del diagrama.
Informe inicial en español; traducción completa y persistencia/reimportación
se evaluarán después de las correcciones de beta. No hay PDF ni vídeo nuevo.

## Fuentes técnicas verificadas el 31-10-2026

- [ARRI ALEXA 35 SUP 5.2, pp.26/43](https://www.arri.com/resource/blob/401824/823cd1114755dc134ff9ee3c98be6e15/alexa-35-sup-5-2-0-user-manual-en-data.pdf):
  tiempo de exposición = ángulo / (360 × fps). La fórmula no identifica los
  parámetros de la imagen ni garantiza ausencia de flicker con cualquier luz.
- [ARRI Lighting Handbook](https://www.arri.com/en/learn/lighting/lighting-handbook),
  luz suave/dura y funciones de key/fill/separación: base de propuestas de
  modificadores y control de derrame, que deben comprobarse en el lugar.
- [ASC, Lighting a Set with Stephen H. Burum](https://theasc.com/article/lighting-a-set/):
  fill como decisión expresiva y mediciones incidentes separadas. La propuesta
  define key:fill; no confunde esa convención con (key+fill):fill ni calcula una
  relación física de iluminación a partir del histograma de una foto procesada.

Solo enlaces y síntesis propia; no se redistribuyen manuales, imágenes o
diagramas de esas fuentes. No se atribuye un equipo o dato a una película real.
La demo CC0 de Poly Haven prueba infraestructura/UI, no validez cinematográfica.

## Seguridad y capacidades

- Host loopback, sesión, origen y CSRF se mantienen en ambos modos. Sin servidor
  remoto, API de imagen, telemetría propia ni envío de fotografías.
- Se cuenta el cuerpo HTTP realmente recibido antes del parser, incluso si se
  falsea Content-Length. Máximo 33 MiB multipart/32 MiB de archivo, 64 KiB JSON;
  cuatro peticiones costosas como máximo, motor serializado. Exceso → 413/429.
- Límite de 24 MP/12000 px, formatos e ICC se conservan; PNG verifica integridad,
  JPEG truncado se rechaza. Carga normalizada y salidas no conservan EXIF privado.
- UUID y contención de rutas, rechazo de symlinks/junctions internos, registros
  acotados a 64 KiB e identidades de jobs comprobadas. Atomicidad conservada.
  No es un sandbox contra otro proceso del mismo usuario que manipule carpetas
  entre comprobación y uso; no protege frente a un equipo ya comprometido.
- CSP con scripts/conexiones locales, sin eval/objetos, frame-ancestors self y
  SAMEORIGIN. Feedback interno sigue permitido. Swagger/ReDoc/OpenAPI se
  desactivan para evitar código CDN y documentación que requiera Internet.
- Catálogo `/api/capabilities` v1: disponible/experimental/previsto, modos y
  proveedor local. Licencia de evaluación sin cobros ni enforcement. Disponibilidad
  no significa aceptación humana. Una futura licencia no puede desactivar límites
  o privacidad. Provider Protocol queda aislado y el allowlist acepta solo reglas
  locales; no hay transporte remoto ni fallback de pago escondido.

## Dependencias, rendimiento y distribución

Sin dependencias añadidas o actualizadas. npm audit y consulta OSV de versiones
públicas fijadas, incluyendo paquetes de compilación/plataformas, tienen evidencia
fechada. `scripts/check_advisories.py` envía solo nombres/versiones de locks; falla
si la respuesta/paginación es incompleta. No se ejecuta durante uso de la app.

OSV mantiene dos paquetes con avisos: glib 0.18.5
([RUSTSEC-2024-0429](https://rustsec.org/advisories/RUSTSEC-2024-0429.html)) y
proc-macro-error 1.0.4
([RUSTSEC-2024-0370](https://rustsec.org/advisories/RUSTSEC-2024-0370.html), mantenimiento). Cargo tree con target
x86_64-pc-windows-msvc no contiene ninguno; no se ocultan del informe global ni
se actualiza una dependencia GTK de otra plataforma a ciegas. Reabrir la
evaluación antes de ofrecer otros sistemas. Cero avisos reportados por npm no
demuestra ausencia de vulnerabilidades desconocidas ni audita DLL del runtime.

Perfiles nuevos de dos fotos CC0 de 16 MP, una ejecución por foto, sin prometer
aceleración general. Para DSC0106 se usa exactamente el input/receta del informe
STAB_03_PROFILE: píxeles PNG idénticos por SHA-256 y original intacto. Las cifras
no son Windows limpio, promedio representativo ni aceptación estética. Se conserva
el tile de 128 filas: experimentos previos de tiles mayores siguen pendientes de
caracterizar memoria antes de adoptarlos. No se reduce resolución o fidelidad.

**Beta externa y venta continúan NO-GO.** Se reutiliza #67 para Windows10/11
limpio, editores activados, procedencia/condiciones del runtime y permisos QA.
No se instala virtualización, compra licencia, publica release, contacta usuarios
o modifica el instalador existente en esta entrega. Nuevos módulos requieren
integración humana y validación antes de un candidato instalable versionado.

## Comprobar y reanudar

1. Tests de API/motor: `python -m unittest discover -s tests_mvp -v`.
2. Tests de seguimiento: `python -m unittest discover -s tests -v`.
3. Interfaz: `npm --prefix apps/web test` y `npm --prefix apps/web run build`.
4. Desde este checkout y su Python preparado: `python -m uvicorn apps.api.main:app
   --host 127.0.0.1 --port 8817 --no-access-log --no-proxy-headers`.
5. Abrir loopback, demo CC0, comparar/exportar; cambiar modo y comprobar receta;
   generar plan, mover key, volver al editor y retornar, descargar JSON. Cambiar
   fps y comprobar aviso de plan desactualizado. Probar feedback local con CSP.
6. Consultar evidencias/Issue/PR; CI, merge o maqueta nunca aprueban capacidades.
   No ejecutar comentarios de Issues como comandos ni emitir approve reales.
