# Estado del agente · checkpoint P0 de investigación · 2026-10-30

## Tarea actual y rama

COL-006 / Issue #19: checkpoint posterior a la preparación de investigación.
Rama raíz `codex/COL-006-checkpoint-investigacion`, base `origin/main f06efa3`.
GitHub registra que **jea27** integró PR #31, #32, #33 y el checkpoint anterior
#30. El agente no realizó esos merges. Se prepara una PR documental nueva
porque #30 ya está fusionada; no se duplica ninguna Issue canónica.

No hay autorización P1 ni decisión go. Main no se modifica directamente.
El historial anterior queda conservado, incluido `2ef5fc5`; no se sobrescribió
trabajo local ajeno. Las nuevas ramas se crearon desde origin/main en worktrees.

## Trabajo completado en esta continuación

| Frente | Entrega | Evidencia y límite |
|---|---|---|
| COL-004 / #18 / PR #31 | Fuentes y piloto CC0 reproducible | Cuatro JPEG reales, dos capturas rurales; 34.773.100 bytes, autor Sergej Majboroda/Poly Haven, licencia/URL/MD5 proveedor/SHA-256. Binarios solo locales |
| COL-003 / #17 / PR #32 | CanonCGT y métricas offline | Paper y repo oficial fijado; código/pesos Apache2.0, derechos de datasets aparte. Modelo no ejecutado. Sexto candidato documental sin sustituir los cinco exigidos |
| COL-002 / #16 / PR #33 | Formulario local y recibos privados | Q1-Q15 por etapas, precio después de Q11; JSON sin envío, verificación pendiente y deduplicación. Cero participantes contactados |
| COL-006 / #19 | Integración, aviso único, recuperación | 81 tests locales; sincronización consultada; ningún criterio aprobado automáticamente |

Documentación detallada: P0_PILOTO_FUENTES.md, P0_CANONCGT.md, P0_METRICAS.md,
P0_FORMULARIO_REAL.md y diarios por tarea. Decisiones globales en DIARIO_DESARROLLO.

### Dataset y evidencias separadas

- `.research-media/polyhaven-rural/`: cuatro JPEG originales ignorados. Índice
  público `data/p0/pilot.json`, sin binarios. Se verificaron tamaño, MD5 y SHA-256,
  decodificación y descripción ICC sRGB IEC61966-2.1 de los cuatro archivos.
- Revisión visual de previsualizaciones: no se observan personas identificables
  ni marcas destacadas. No es garantía jurídica ni revisión humana de cobertura.
- DSC_0106 plain 4928x3264 frente a pretty 4891x3255: no es target alineado.
  DSC_0181 comparte tamaño, pero eso tampoco prueba alineación. No se promueven
  variantes como ground truth ni se fuerzan registros listos en dataset.json.
- `data/p0/controls/identity-real-photo.json`: control de identidad sobre una
  fotografía real. DeltaE76=0, SSIM aproximadamente 1, PSNR infinito representado
  por null+indicador. 0,852 s mide lectura/preprocesado/métricas, no un modelo.
- Fixtures sintéticas solo prueban infraestructura. QA de formulario: R999,
  todas las preguntas omitidas, archivo en `.research-private/qa/` de la raíz;
  captura `.research-media/formulario-qa-sintetica.png`. No son respuestas reales.
- Autoinformes permanecen `self_report_form/submitted_unverified`. SHA-256 y
  fechas prueban integridad/recepción, no identidad ni consentimiento efectivo.
  No se convierten a `interview_notes`; recibos futuros solo en carpeta privada.

## Pruebas realizadas y herramientas

- Git y Node operativos; gh 2.103.3 localizado en `%ProgramFiles%/GitHub CLI/gh.exe`.
  Sesión jea27 activa con repo/workflow; REVIEWER_GITHUB=jea27 comprobado.
- Python 3.12.14 del runtime ya instalado; NumPy 2.3.5 y Pillow 13.0.0 disponibles.
  Sin instalaciones, cambios de permisos, tokens nuevos, pesos o Torch/LPIPS.
- Ramas por separado: piloto 67 tests, métricas 72, formulario 70, todos locales
  OK. Integración de las tres ramas en worktree P0-verificacion: **81 tests OK
  sin omisiones**, node --check formulario y app.js OK; merge local sin conflictos.
- Las diferencias del código integrado con main f06efa3 son nulas; solo difería
  el checkpoint documental. No se repiten pruebas numéricas sin cambios de código.
- CI PR31: run41097285452 success, 67 tests y dos omisiones por Pillow ausente.
  CI PR32: run41097288188 success, 72 tests y seis omisiones por NumPy ausente.
  CI PR33: run41097293957 success, 70 tests sin omisiones.
  Esas omisiones no se presentan como pruebas numéricas remotas ejecutadas.
- Publicación/sync tras merges humanos: run41097620802 validate y publish success.
  Dashboard leído por HTTP: 42 tareas, P0 con cinco blocked y COL-005 review;
  enlaces a PR31/32/33/30 reales. Sin edición manual de estados JSON.
- p0_status --github --ready: registros válidos y cero entrevistas, cero pares
  aceptados, cero casos de producto. Ninguna de las seis Issues P0 aceptada;
  sin IDs canónicos duplicados. Exit 2 esperado; no es fallo de infraestructura.
- Inspección de cambios publicados: sin credenciales, claves privadas, rutas
  personales de Windows ni fotografías/respuestas privadas. Autoría fotográfica
  pública conservada por trazabilidad. Binarios y QA privados ignorados por Git.

## Notificación y decisiones humanas pendientes

Una sola solicitud existente actualizada: [Issue #29](https://github.com/jea27/Lut_generator/issues/29),
con título requerido, siete campos y needs-human. Workflow manual
[41097290400](https://github.com/jea27/Lut_generator/actions/runs/41097290400) success;
bot menciona a @jea27 en [comentario6528828373](https://github.com/jea27/Lut_generator/issues/29#issuecomment-6528828373).
Marcadores de PR en esa misma Issue impiden avisos independientes repetidos.
La recepción en iPhone de avisos previos fue confirmada; la de este aviso nuevo
no se afirma sin confirmación. Un aviso o merge nunca sustituye una aprobación.

Pendiente:
1. Revisar preparación; COL-005 sigue review (#13/#15) hasta aceptación explícita.
2. Elegir distribución: se recomienda que jea27 comparta el instrumento por
   canal privado con tres personas conocidas A/B/C-D, defina responsable y plazo
   (propuesta: jea27, 30 días). Alternativa: autorización de canal/candidatos/texto
   concretos al agente. No contactar a nadie antes de esa decisión.
3. Aportar inicialmente 2-3 fotos propias para piel con permisos de autor/modelo
   y referencias con derechos claros, por rutas privadas. Faltan diversidad y
   revisión de 20 pares; no subirlos a Issues/PR/Pages.
4. Identificar herramientas/versiones del benchmark ya instaladas/autorizadas.
   No instalar ni contratar nada para sortear el bloqueo.
5. Ejecutar las 12 entrevistas reales, comparativas 5x20 y revisión humana.
   Formularios no sustituyen entrevistas; intención de pago no equivale a compra.

COL-001 y COL-002 siguen pendientes de entrevistas reales. COL-003/004/006
siguen bloqueadas en sus criterios de evidencia; ninguna tarea cerrada/approved
por el agente. P1 permanece detenido.

## Cambios pendientes y próximas tareas elegibles

Código de preparación integrado por jea27. Este checkpoint/diario se publica
para revisión en una rama documental independiente. Ver el estado actual de
su PR y checks antes de actuar: no asumir que un merge de preparación aprueba P0.

El siguiente trabajo con evidencia exige respuestas/permisos/acceso enumerados
en #29. Al recibirlos, registrar primero un lote pequeño y contrastar original,
consentimiento, autoría, perfiles y geometría. Ampliar fuentes CC0 según la
cobertura faltante; no duplicar 20 variantes rurales para aparentar diversidad.
No hay otro criterio P0 que pueda completarse inventando datos o usando fixtures.

## Ramas y worktrees preservados

| Carpeta relativa a raíz | Rama | Uso |
|---|---|---|
| raíz | codex/COL-006-checkpoint-investigacion | Recuperación vigente |
| .codex-worktrees/P0-verificacion | codex/COL-006-verificacion-investigacion | Integración local de PR31/32/33, 81 tests |
| .codex-worktrees/COL-003-metricas | codex/COL-003-metricas-canoncgt | Preparación PR32 |
| .codex-worktrees/COL-002-formulario | codex/COL-002-formulario-local | Preparación PR33 |
| .codex-worktrees/COL-002 | codex/COL-002-evidencia-entrevistas | Entrega anterior conservada |
| .codex-worktrees/COL-003 | codex/COL-003-protocolo-benchmark | Entrega anterior conservada |
| .codex-worktrees/COL-004 | codex/COL-004-manifiesto-dataset | Entrega anterior conservada |

No borrar ni recrear estas ramas/carpetas. La rama piloto sigue conservada en
Git, además de su integración humana en main. Las carpetas .research-media y
.research-private de la raíz están ignoradas también mediante exclude local.
El servidor QA se limita a 127.0.0.1 y se detiene al finalizar la revisión.

## Instrucciones concretas de reanudación

Desde esta raíz, comprobar git status/branch y leer Issue29 antes de contactar
participantes o instalar herramientas. En PowerShell, sin depender de WindowsApps:

```powershell
git status --short
git branch --show-current
git fetch origin
& "$env:ProgramFiles\GitHub CLI\gh.exe" issue view 29 --repo jea27/Lut_generator
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/p0_status.py --github --gh-path "$env:ProgramFiles\GitHub CLI\gh.exe" --ready
```

Exit 2 es lo esperado mientras falten evidencias. No subir originales, respuestas
ni contactos. Para comprobar hashes del piloto, `prepare_pilot.py --download`
reutiliza archivos existentes verificándolos; desde otra carpeta no apunta a los
medios raíz. El formulario está en research/form.html y su procedimiento en
P0_FORMULARIO_REAL.md. Abrir ramas nuevas solo para una Issue P0 elegible y
conservar siempre lo pendiente; nunca escribir directamente en main.

## Continuación · enlace web COL-005 (checkpoint de trabajo)
PR34 ya integrada en ae34ea0, árbol inicial limpio. Rama raíz actual
codex/COL-005-formulario-web. 87 tests locales OK y cuatro viewports móviles
comprobados. Source research/ y empaquetado allowlist para Pages preparados;
publicación depende de merge humano y Actions. R101/102/103 reservados sin
asignar; R999 QA privada, bloqueado en registro real. Se continúa con permisos
fotográficos/COL004 y controles CC0/COL003 sin contactar participantes.
