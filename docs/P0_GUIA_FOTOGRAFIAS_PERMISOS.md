# COL-004 · Incorporar fotografías con permisos documentados

Issue #18. Procedimiento para fuente y referencia, antes de promover un par al
dataset P0. No constituye permiso otorgado por el agente. Los originales,
firmas, contactos y autorizaciones cumplimentadas se conservan **privadamente**.

## Qué puede aportar el responsable

Primero 2–3 muestras propias para piel, más referencias cuyo uso esté autorizado.
Preferir adultos participantes voluntarios y escenas sin datos sensibles.
No hace falta publicar fotos ni remitir documentos de identidad. Una ruta local
privada y registros de alcance verificables permiten comenzar la revisión.
El conjunto final sigue necesitando 20 pares y diversidad de escenas/luces.

## Admisión por etapas

1. **Procedencia y autor:** quién hizo cada foto, fuente original/URL cuando
   exista, fecha de obtención, original y SHA-256. Ser dueño del archivo no
   acredita autoría ni permite reutilizar automáticamente el trabajo de un cliente.
2. **Derecho de uso:** licencia identificada con versión, URL/fecha y evidencia
   privada, o permiso del titular con alcance explícito. Confirmar copia local,
   análisis y transformaciones necesarias para comparación interna P0. Si una
   licencia impide ese uso o falta claridad, mantener en cuarentena, sin procesar.
3. **Personas identificables:** revisar rostros y otros elementos identificadores.
   Para este piloto exigir autorización documentada de las personas para el uso
   interno descrito; no inferirla de haber posado, de una red social pública o
   de que el fotógrafo permita usar la obra. No usar casos de menores o capacidad
   de consentimiento dudosa en el lote inicial sin revisión humana específica.
4. **Información y alcance:** antes de recibir, acordar responsable/contacto,
   finalidad, almacenamiento, acceso y plazo de conservación; cómo corregir o
   retirar. Investigación interna no incluye publicar, redistribuir, entrenar IA,
   marketing o subir a servicios externos. Cualquier ampliación exige su decisión
   y permiso específico, no una casilla que el agente marque por la persona.
5. **Custodia:** original inalterado y permisos en almacenamiento privado con
   acceso limitado. Separar correspondencia/contactos del índice técnico.
   Revisar EXIF (GPS/autor/contacto), nombres de archivos, pantallas y reflejos
   antes de compartir siquiera un informe. No copiar esos datos a GitHub.
6. **Preparación técnica:** decodificar, revisar ICC/orientación, dimensiones,
   representatividad y relación fuente-referencia. Si se prepara una copia sRGB,
   conservar ambos hashes, receta/herramienta y registro COLOR; no modificar el
   original ni confundir referencia estilística con target alineado.
7. **Admisión:** responsable revisa registros RIGHTS/COLOR y cobertura, dejando
   IDs públicos y estado real. El validador comprueba estructura/integridad,
   no autenticidad de permisos. No poner cleared/reviewed por haber rellenado una
   plantilla. Hasta revisión, el archivo no se promociona como par listo.
8. **Retirada/cambio:** localizar por código/hashes originales y derivados,
   bloquear uso nuevo y retirar del conjunto activo mientras se resuelve con el
   responsable. Registrar privadamente qué se corrigió/retiró y cuándo. La gestión
   de copias, retención y borrado se acuerda con él; no publicar razones sensibles.

## Registros separados

| Registro | Contenido | Ubicación |
|---|---|---|
| RIGHTS-ID | Titular, licencia/permiso, alcance, comprobación, fecha | Evidencia privada; en Git solo ID y base no identificativa |
| PERSON-ID | Consentimiento de cada persona identificable, información y retirada | Privado, nunca firmas/nombres en roadmap |
| COLOR-ID | ICC/espacio, orientación, copia preparada y hashes | Metadatos técnicos revisados sin EXIF privado |
| REVIEW-ID | Revisión de cobertura y aptitud del par | Resumen no identificativo; evidencia privada enlazada por ID |

Usar `docs/plantillas/PERMISO_FOTOGRAFIA.md` como lista de alcance para acordar,
no como consentimiento ya obtenido. Guardar la copia cumplimentada fuera de Git.
No almacenar imágenes nuevas ni permisos reales en docs/plantillas o data/p0.

## Fuentes de referencia comprobadas 2026-10-30

La [LO 1/1982, arts. 2 y 7](https://www.boe.es/buscar/act.php?id=BOE-A-1982-11196)
trata consentimiento y uso de imagen. La licencia del fotógrafo y los derechos
de una persona representada son comprobaciones distintas. El alcance concreto
lo revisa el responsable antes de incorporar material; esta guía no presume
una excepción legal para LumaForge.

Los [assets Poly Haven son CC0](https://polyhaven.com/license); el
[instrumento CC0](https://creativecommons.org/publicdomain/zero/1.0/) mantiene
la distinción respecto de privacidad, imagen y marcas. Las cuatro fotos rurales
existentes ya tienen trazabilidad separada; no se les exige inventar una firma
de fotógrafo para sustituir su licencia. Tampoco cubren el requisito de piel.
