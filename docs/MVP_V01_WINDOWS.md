# LumaForge MVP v0.1 · abrir y probar en Windows

La aplicación está separada de site/. Requiere Python 3.12 y Node 24+ para
prepararla una vez con Internet; después el build y el procesamiento son locales,
sin tokens, cuenta ni APIs de imagen. Se autorizaron estas dependencias para el MVP.

## Arranque inmediato en este equipo

1. Abrir la raíz del proyecto y ejecutar **Iniciar-LumaForge.cmd**.
2. Visitar **http://127.0.0.1:8790** en Edge/Chrome. Si ya está ejecutándose,
   abrir la dirección sin lanzar un segundo servidor. Mantener la consola abierta.
3. Para detener, Ctrl+C en esa consola. No cambia permisos, PATH ni main.

Si faltan dependencias, en PowerShell desde la raíz:

```powershell
./scripts/setup_mvp.ps1
```

El script busca primero el Python 3.12 del runtime de este equipo. En otro equipo,
`./scripts/setup_mvp.ps1 -PythonPath "RUTA_A_PYTHON_312.exe"`. Instala versiones
fijadas en .venv-mvp y npm ci desde package-lock, compila TypeScript/Vue/Quasar.
Si la política del equipo impide scripts, no modificarla: ejecutar manualmente
`python -m venv .venv-mvp`, `.venv-mvp/Scripts/python.exe -m pip install -r
requirements-mvp.txt`, `npm --prefix apps/web ci`, `npm --prefix apps/web run build`.

## Recorrido de edición

1. Importar referencia y destino con los paneles de la izquierda (JPG/PNG8 SDR).
2. Revisar histograma RGB, paleta aproximada, luminancia y contraste de referencia.
3. Elegir Estadísticas Lab o Solo media Lab, pulsar **Analizar y transferir**.
4. Deslizar el comparador; el lado izquierdo es después y el derecho antes.
   Zoom centrado sincronizado mediante −/+, botón 100% para volver al encuadre.
5. Intensidad cero quita **todo** el look, incluidos controles manuales. Ajustar
   exposición creativa, contraste, saturación y temperatura. Deshacer/Rehacer
   recupera hasta 30 estados de edición de la sesión, no es un historial en disco.
6. Nombre del preset y botón + guardan receta en la biblioteca local. Pulsar un
   preset la recupera. Receta JSON descarga una copia que puede reimportarse.
7. Exportar PNG o JPG procesa el tamaño original. La LUT .cube 33³ es un mapa
   global sRGB: no contiene máscaras, alfa, un modelo adaptativo o la fotografía.

No se requieren fotografías específicas para probar. Para reproducir la demo
interna con los CC0 ya descargados: referencia DSC_0181-jpg_pretty.jpg y destino
DSC_0106-jpg_plain.jpg, en `.research-media/polyhaven-rural/`. No redistribuir
fotografías privadas ni emplear la captura de referencia aportada como dataset.

## Datos locales y privacidad

Las copias normalizadas están en `.lumaforge-local/images/`, los presets en
`.lumaforge-local/presets/`, ambos ignorados por Git. No se modifican originales
ni se conservan EXIF/GPS en exportaciones; se incrusta un ICC sRGB nuevo. No hay
subidas cloud, analítica, CDN, claves o llamadas de pago durante la edición.
**Eliminar imágenes temporales** pide confirmación y borra solo copias de imagen
de esta aplicación; mantiene presets y los originales externos. Máximo ocho
copias temporales y 100 presets; limpiar imágenes antes de importar más.
No exponer el puerto a LAN ni Internet: es un MVP para una sola sesión local.

## Verificación y limitaciones

```powershell
./.venv-mvp/Scripts/python.exe -m unittest discover -s tests_mvp -v
npm --prefix apps/web run build
```

Los límites, curvas, ICC, alfa y dominio de LUT están en MVP_COLOR_CONTRACT.md.
Máximo24MP/32MiB/12000px por lado; no RAW/Log/HDR/16bit/vídeo. La LUT corresponde
al renderer trilineal propio, no se ha probado todavía dentro de editores externos.
La vista previa usa como máximo1280px; la exportación procesa el original. Es una
aproximación creativa, no recuperación exacta del preset o iluminación de referencia.
La prueba real CC0 produjo PNG/JPG de4928×3264 en unos9–11s y ~785MB de RSS
muestreado de proceso; cifras de este equipo y una ejecución, no garantía de
latencia ni pico exacto. P0 comercial y revisión humana de calidad siguen pendientes.

## Preparación posterior, sin implementar ahora

- IA local: adaptador opcional separado, con hash/licencia de pesos y comparación
  contra baselines; sin llamadas externas ni segmentación silenciosa.
- Piel/sujetos: futuras máscaras separadas de la LUT, evaluadas con permisos.
- Vídeo/FFmpeg: gestión explícita Rec.709/Log, muestreo por planos y coherencia.
- Tauri: empaquetar UI compilada y sidecar loopback con ciclo de vida controlado.
- Editores: validar .cube en versiones concretas y definir XMP como otro formato.

Son propuestas de extensión en la arquitectura acordada, no funcionalidades de v0.1.
