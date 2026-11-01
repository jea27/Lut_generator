# Prueba guiada de Creator, Pro y Shot Planner

Para el responsable, sin programar. Seguimiento: #57, #67, #81–83.

## Abrir la entrega correcta

01-11-2026: existe el candidato **interno0.3.0-beta.3**, con Creator/Pro/Planner
y runtime Python incluido. Su SHA-256 es
`0350f5b44be2850f828a148debc4174b8f134953b080d895bbbca8620576b5cd`.
El archivo se facilita localmente por este chat; no hay release autorizada ni
descarga pública. El setup0.3.0-beta.2 no contiene estas experiencias.

1. Guarda antes recetas/presets/planes importantes y cierra Color Studio.
2. Comprueba versión/hash con `RUNTIME_036_ARTIFACT.json`. Si conservas beta2,
   haz una copia privada de `%LOCALAPPDATA%/ColorStudioBetaData`. No la subas a GitHub.
3. Para este ensayo interno utiliza la desinstalación explícita de beta2 y después
   instala beta3, conservando los datos. No marques «Eliminar datos de la app».
   La actualización directa automática **no está verificada**: devolvió2 en el
   contexto de Codex y el asistente se detuvo en el idioma del desinstalador previo.
   No ocultes ese fallo ni lo registres como PASS. Detalles en #67 y RUNTIME_036_QA.
4. Abre Color Studio desde su acceso directo. Confirma Ayuda0.3.0-beta.3 y los
   botones Creator/Pro. No necesitas Python, Node ni una consola para usarlo.

Si falta WebView2, el instalador usa Evergreen oficial y necesita Internet para
esa primera instalación; después hay que ejecutar la prueba offline por separado.
No desactives protecciones ni omitas un bloqueo de SmartScreen. Registra el error
y detente si Windows impide ejecutarlo. No se ha probado aún Windows limpio.

Las pruebas locales se ejecutaron desde Codex en un PC de desarrollo, con datos
de QA separados y redirección MSIX de archivos. No acreditan una instalación
normal de Windows limpio ni la ubicación de tus datos fuera de ese contexto.
Para W01–W09 sigue BETA_QA_EXTERNA; el titular debe aportar el entorno/operador.

## Recorrido de unos 15 minutos

Usa «Probar demo local» en la bienvenida o «Probar demo CC0». Las dos fotos
incluidas son CC0, acreditadas en `apps/demo/credits.json`. No hacen falta fotos
personales ni subir archivos a GitHub. Espera a «Listo para crear» antes de exportar.

| Caso | Qué hacer | Qué debes observar |
|---|---|---|
| C01 | En Creator, cargar la demo y mover el separador antes/después. | Dos imágenes importadas; la comparación muestra la misma fotografía de destino, no dos escenas diferentes. La guía avanza según tus acciones. |
| C02 | Bajar intensidad de color al 50%; activar acabado y probar glow, difusión y fade con valores suaves. | Se actualiza la vista previa. Son controles manuales; no se afirma que la referencia se haya reproducido fielmente. Esperar a que termine. |
| C03 | Exportar PNG y JPG y abrirlos. | Archivos a resolución del destino, sin sobrescribir originales. Valora altas luces, halos, detalle y color natural. La preview puede ser menor; para fidelidad compara a igual tamaño y con gestión sRGB. |
| P01 | Abrir Pro, modificar exposición un paso y guardar «Receta JSON». Volver a Creator y regresar a Pro. | Misma referencia, destino, intensidad, exposición y acabado. Creator avisa de ajustes Pro activos. Guardar otra receta permite comprobarla; no hay conversión de motor al cambiar modo. |
| P02 | Dar nombre al preset y guardarlo. Cambiar un ajuste y volver a aplicar ese preset. Probar deshacer/rehacer. | Se restaura la receta guardada. La aplicación no presenta el preset como aprobado por nadie. |
| P03 | En Pro guardar JSON y LUT .cube, leyendo el aviso. | JSON conserva glow/difusión/fade. La LUT solo transforma color y los omite. No esperar que una LUT reproduzca blur o bloom. Adobe/Resolve necesitan su propia prueba real. |
| P04 | Mientras exporta, intentar cambiar preset, importar receta, deshacer o eliminar imágenes temporales. | Esas acciones están deshabilitadas hasta terminar. No deben sustituir la receta a mitad de la operación. |
| S01 | Pro → Shot Planner → Preparar propuesta local. Mantener 25 FPS/180°. | Aparecen observaciones medidas, estimaciones sin confirmar, recomendaciones y cálculo con fuente. Obturación 1/50 s. Cámara, focal y luces originales no se afirman como detectadas. |
| S02 | Seleccionar Key, mover X, marcar una casilla y cambiar Creator → Pro → Shot Planner. | Diagrama y checklist conservados durante esta sesión. Guardar plan JSON y abrirlo en un editor de texto para revisar su contenido. |
| S03 | Pulsar Preparar otra vez. Cancelar el diálogo y después repetir aceptando. | Cancelar conserva las ediciones. Confirmar reinicia diagrama y checklist. Si cambias FPS/receta, aparece «desactualizado» y no permite guardar un plan antiguo como si fuera actual. |
| S04 | Abrir Fuentes y límites cuando tengas conexión. | Referencias de ARRI y ASC; no fotogramas de películas redistribuidos ni datos inventados de un rodaje. El enlace requiere Internet; generar/editar/exportar el plan no. |
| D01 | Pulsar Eliminar imágenes temporales y cancelar primero. | El aviso explica que se reinician ajustes y plan no guardados. Cancelar conserva todo. Antes de confirmar, guarda preset/receta/plan. Los originales y presets guardados se conservan. |

El plan JSON se **exporta, pero todavía no se reimporta**. Cambiar modo conserva
el plan en memoria; cerrar/reiniciar o sustituir la referencia no promete
recuperarlo editable. La sesión de imágenes/ajustes no se restaura sola al
reiniciar: vuelve a cargar imágenes y aplica un preset/receta guardado. Es un
límite actual a revisar, no una prueba superada de recuperación de proyectos.

## Enviar el resultado con privacidad

En la Issue de revisión o en #57, indicar: versión/PR revisada, Windows10/11,
caso (C01…D01), PASS/FAIL/NO EJECUTADO, esperado y observado. Para un fallo,
explicar pasos y adjuntar solo captura de la demo o datos sin información privada.
No adjuntar rutas de usuario, logs completos, EXIF, personas o fotos de clientes.
Si necesitas usar tus imágenes, hazlo localmente y comparte solo la descripción.

La aceptación es individual en Project OS → Mis revisiones. Revisa capacidad y
huella/versionado antes de publicar la decisión autenticada como `jea27`.
Aceptar Creator no acepta automáticamente Pro, Planner ni la distribución de
Windows. CI y merge tampoco sustituyen tu revisión.

## Windows limpio: instrucciones que faltan por ejecutar

Protocolo reproducible completo: `BETA_QA_EXTERNA.md`, casos W01–W09;
exportaciones en editores: `QA_EDITORES_03.md`.
No se ha ejecutado en Windows limpio en esta entrega. Para cada Windows10/11 x64
acordado, usar cuenta de prueba y fotografía CC0, sin datos reales:

1. Recibir **privadamente** el setup autorizado, versión, hash SHA-256 y manifiesto.
   Comprobar que es el candidato acordado; no aceptar el antiguo solo por el nombre.
2. Registrar Windows/build, RAM y presencia/ausencia de WebView2 y herramientas.
   Los alias de WindowsApps no demuestran Python instalado. El preflight de
   `scripts/qa_windows_clean.ps1` documenta el estado, no certifica limpieza.
3. Instalar por usuario y abrir desde Inicio. No debe pedir instalar Python/Node.
   No desactivar antivirus/SmartScreen para forzar el resultado; si bloquea,
   registrar y consultar. Probar WebView2 presente y ausente según W01–W09.
4. Sin conexión, completar C01–S03, preset, PNG/JPG/JSON/.cube y lote de dos fotos.
   Registrar errores, duración y dimensiones. Con WebView2 ausente, registrar
   si su instalación inicial necesita conexión; no prometer primer arranque offline.
5. Guardar preset y preferencia, cerrar, actualizar desde el candidato previo y
   reabrir. Comparar preset/receta/preferencias y archivos descargados; no asumir
   que las imágenes de sesión se cargan automáticamente. El protocolo de
   preservación usa conteos/hashes privados y no publica nombres personales.
6. Desinstalar; confirmar cierre del motor y que originales/exportaciones se
   conservan. Registrar si los datos de aplicación se retienen y verificarlo,
   sin borrar datos ajenos. Reinstalar solo si el protocolo autorizado lo requiere.

No instalar virtualización ni contactar probadores hasta la autorización de #67.
Venta y beta privada mantienen listas GO/NO-GO separadas en `GO_NO_GO_03.md`.
