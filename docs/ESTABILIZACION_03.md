# Revisión técnica de Color Studio0.3 · 31-10-2026

Entrega COL013#45, con evidencias para COL038#59, COL040#60 y COL026#68.
No se cambia el motor ni los efectos del candidato0.3.0-beta.2. No hay nuevo
instalador en este ciclo: las correcciones de texto y del builder son fuente
para el siguiente candidato, pendiente de procedencia de dependencias y QA.

## Integración y revisión de PR70

GitHub registra merge por jea27 a las08:27:11 UTC, main cfb6d11. El árbol de main
es idéntico al HEAD4920cf0 de PR70; los commits fuente de65/66/69 son ancestros.
69 archivos cambiados frente a main anterior0539b9f. Escáner de blobs modificados:
0 patrones de token/clave privada/perfil local y0 rutas privadas/generadas.
Seis JPEG revisados: derivados rurales CC0 y capturas de QA ya documentados,
0 campos EXIF. No se añaden fotos privadas o respuestas. Alcance y hashes en
STAB_03_PR70_REVIEW.json; no es detección universal de secretos ni elimina
identidades de autores ya presentes en el historial público de Git.

CI final de70 fue correcta: MVP41184186135, Studio41184186164, validate41184186206.
Regresión local de partida:30 MVP+91 seguimiento, sin omisiones; TypeScript/Vite
compilan. Las nuevas herramientas incorporan pruebas específicas adicionales.
No hubo merge, approved, cambio de permisos o escritura directa a main del agente.

## Riesgos y resultado

| Prioridad | Hallazgo real | Tratamiento |
|---|---|---|
| Bloquea distribución |44 DLL UCRT/API-set recogidas de caché nativa de herramientas; derechos de esa copia sin conciliar | Nuevo gate falla antes de empaquetar otro instalador; ver LICENCIAS_BINARIAS_BETA |
| Bloquea aceptación | Sin Windows10/11 limpio accesible ni importación real en editores activados | Protocolo y fixtures preparados; resultados siguen not_run |
| Antes de distribución | «Sin telemetría» era demasiado amplio para WebView2 | Texto fuente corregido a telemetría propia y aviso Microsoft; beta2 existente aún conserva texto anterior |
| Antes de distribución |3 avisos NSIS/plugin acompañan el ZIP de revisión pero no el NSIS beta2 | Incluirlos en próximo candidato con nueva versión/hash; no presentar el ZIP como corrección retroactiva del exe |
| Pendiente humano | Titular/licencia del proyecto y cadena de suministro CPython/Microsoft | No se aceptan contratos ni se presume licencia de redistribución |
| Límite de calidad | Paisaje CC0 no demuestra piel, fidelidad completa de referencia ni vídeo | Mantener muestras autorizadas y aceptación pendientes |

## Perfil real, sin optimización del motor

Reproducir con .venv-mvp:

```powershell
./.venv-mvp/Scripts/python.exe scripts/profile_export.py .research-media/polyhaven-rural/DSC_0106-jpg_plain.jpg .lumaforge-local/look03-qa/recipe.json .lumaforge-local/profile.json --repeats 3 --experiment-tiles 256 512
```

4928x3264, misma receta de glow/difusión/fade del checkpoint. Tres ejecuciones,
cache LUT precalentada; primera con cProfile. Medianas medidas en este equipo:

| Etapa | Segundos |
|---|---:|
| Decodificación/ICC |0,548|
| LUT trilineal |9,005|
| Acabado |6,267|
| Render completo (incluye las dos anteriores) |15,331|
| Cuantización/PNG |1,445|
| Pipeline completo |17,376|

No sumar render con sus subetapas ni tratar medianas independientes como suma
exacta. Píxeles PNG idénticos en tres pasadas; original inalterado. Fuente en
STAB_03_PROFILE.json. El valor histórico32,392s fue del binario congelado en otra
ejecución; esta diferencia NO prueba una mejora entregada. No se midió RAM nueva.

El mayor coste es transform(): indexación trilineal y temporales de NumPy.
GaussianBlur y conversiones repetidas en halos contribuyen al acabado.
Ensayos aislados de128→256/512 filas de acabado: pipeline16,001/14,774s y
acabado4,657/3,779s. Píxeles PNG iguales al baseline de esta foto; una medición
por variante, sin nueva medición de memoria/cancelación. No se incorporan.

Propuestas medibles, en orden para después de QA:
1. Tiles256: exigir repetición en las cuatro CC0, alfa/radios extremos,
   equivalencia píxel a píxel, memoria8GB y latencia de cancelación antes de cambiar.
2. Reducir temporales del interpolador sin alterar precisión: comparar contra
   oráculo escalar, fronteras y export cuantizado; no cambiar a float16 ni tetrahedral.
3. Evitar blur de máscara unitaria cuando no hay alfa y blur suave si difusión0:
   demostrar equivalencia numérica/PNG antes de aceptar; no limitar resolución.
4. Compresión PNG alternativa solo si preserva exactamente píxeles/ICC y se mide
   tamaño/tiempo. Ningún ajuste aplicado para producir una cifra atractiva.

Precisión LUT serializada: error máximo1,091e-7 frente al render de color en262
puntos con oráculo escalar independiente, primarias y extremos. Es prueba de
infraestructura, no compatibilidad Photoshop/Premiere/Resolve. El estudio previo
real preview/full (MAE0,004760/P950,014547) permanece en LOOK_03_BENCHMARK.json:
resizing y radio espacial impiden exigir igualdad entre resoluciones distintas.
