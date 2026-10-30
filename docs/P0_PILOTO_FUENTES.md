# COL-004 · Piloto de fotografías trazables

Consulta: 2026-10-30. Issue #18. Dos capturas, cuatro JPEG originales de
[rural_landscape](https://polyhaven.com/a/rural_landscape), autor Sergej Majboroda.
Las variantes `jpg_plain` y `jpg_pretty` son archivos del proveedor, no resultados
de LumaForge. No se presupone que constituyan ground truth ni estén alineadas.

## Derechos y acceso

[Poly Haven](https://polyhaven.com/license) identifica sus assets como CC0 y
permite uso comercial, modificación y redistribución. Conservamos autor,
procedencia, variante, fecha, tamaño, MD5 publicado y SHA-256 calculado.
Los [términos de API](https://github.com/Poly-Haven/Public-API/blob/master/ToS.md)
permiten consultar assets con agente identificable; el script usa
`LumaForge-P0-research/1.0`. Una consulta inicial sin identificador obtuvo 403;
la petición identificada al endpoint del asset respondió correctamente.
No se rastrea masivamente el sitio ni se descargan renders de usuarios.

[CC0](https://creativecommons.org/publicdomain/zero/1.0/) no elimina derechos
de imagen, privacidad o marcas. El piloto rural evita deliberadamente retratos;
la revisión visual y de color sigue pendiente. No se publican las fotos en Git,
Pages ni una PR. La licencia de los assets no se atribuye al texto del sitio.

Alternativas: fotografías propias con permiso documentado son preferibles para
piel e interiores. Wikimedia Commons requiere revisar la licencia de **cada
archivo**, autor y restricciones; el pie CC0 de metadatos no licencia la foto.
No se incorpora material de colecciones académicas por su sola disponibilidad.

## Reproducción

Usar Python con Pillow disponible y ejecutar `python scripts/prepare_pilot.py
--download`. Descarga acotada a cuatro archivos (34.773.100 bytes), dominios y
rutas oficiales fijos. Archivos existentes se verifican, nunca se sobrescriben.
Un fallo de tamaño, MD5 o decodificación interrumpe el proceso. MD5 contrasta
el transporte con el proveedor; SHA-256 fija la identidad local, no prueba autoría.

Fotos locales ignoradas: `.research-media/polyhaven-rural/`; índice público:
`data/p0/pilot.json`. No sustituye `data/p0/dataset.json`: faltan diversidad,
20 pares, revisión sRGB/ICC, derechos adicionales y aceptación humana.
Los controles de infraestructura no cuentan como prueba de cinco competidores.
