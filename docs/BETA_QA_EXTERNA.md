# Beta privada · procedimiento reproducible y cinco pruebas

Estado vigente: PR70 integrada por jea27; main verificado cfb6d11. Nuevo bloqueo
de procedencia44 DLL en LICENCIAS_BINARIAS_BETA.md. No hay nuevo instalador ni
prueba limpia. Los apartados fechados siguientes conservan contexto histórico.

31-10-2026. Preparado, no ejecutado en Windows limpio. PR65/66 abiertas y
checks correctos al auditarlas; no merge del agente. COL026#68 añade acabado
manual experimental. No es una inferencia fiel de efectos de referencia.

## Puertas separadas

**Beta privada: NO-GO de entrega externa todavía.** Exige candidato fijado a
commit limpio/hash, inventario de payload conciliado y rutas clasificadas,
Windows limpio/actualización probados, guía/feedback offline y decisión del
titular sobre participantes/canal/datos. Después puede aprobarse un piloto
limitado de cinco usuarios, sin convertirlo en validación de10–20 equipos COL041.

**Venta/lanzamiento comercial: NO-GO.** Además faltan P0 comercial, calidad
diversa/piel, compatibilidad real de editores, revisión legal/fiscal/titular,
licencia propia, marca, firma y estrategia de distribución/soporte. No se activa
checkout, release general, actualizador, telemetría o servicio externo.

## Preparar máquina limpia

El titular aporta VM/equipo Windows10 y11 x64 ya autorizado; no habilitar
Hyper-V/Sandbox ni comprar licencias por iniciativa del agente. Guardar snapshot
limpio, usar cuenta estándar, sin Python/Node/Rust/VS instalados. Dos variantes:
WebView2 ausente y ya presente; no desinstalar runtime compartido del equipo real.
Registrar build Windows, RAM y variante, sin nombre de equipo/usuario/seriales.

1. Copiar setup0.2 y candidato nuevo, SHA256SUMS y guía por canal acordado.
   Comparar hash publicado en PR con Get-FileHash. Ejecutar preflight:
   `./scripts/qa_windows_clean.ps1 -Installer RUTA -ExpectedSha256 HASH -Output preflight.json`.
   No ejecuta instalador ni prueba funciones. Alias WindowsApps no acredita Python.
2. Desconectar red en la VM mediante el operador. La aplicación debe completar
   demo, análisis, efectos, preset, lotes y exports offline. Si el instalador
   necesita WebView2, debe utilizar el runtime offline incluido. No sortear
   SmartScreen ni desactivar Defender; cualquier bloqueo es evidencia y requiere
   intervención del titular, no aprobación automática.
3. Instalar por usuario desde Explorador, comprobar atajo Inicio, versión y ruta
   privada. Abrir desde Inicio, bienvenida ES/EN y demo; sin terminal/servidor
   manual. Revisar procesos y listener: solo loopback, un sidecar, cierre completo.
4. Guardar preset v1 y copias CC0/sentinela antes de actualizar; anotar hashes
   en registro privado. Cerrar aplicación, instalar versión nueva, abrir desde
   Inicio y comprobar versión, presets antiguos, preferencias y nuevos efectos.
   Receta v1 debe mantener resultado de color; convertir a v2 al añadir acabado.
5. Forzar cierre solo del proceso de prueba durante lote; al reabrir, estado
   interrupted y archivos ya terminados disponibles. No afirmar reanudación.
6. Actualización manual fallida: conservar instalador anterior conocido y copia
   privada de datos. Snapshot revierte todo el entorno de ensayo. No prometer
   rollback de aplicación automático. No bajar de v2 a v1 sin copia: el anterior
   no entiende efectos, aunque el anterior instalador0.2 se conserve.
7. Desinstalar con aplicación cerrada. Deben retirarse binarios/atajos/procesos;
   originales/sentinela/presets siguen con los mismos hashes. Reiniciar Windows,
   comprobar ausencia de arranque automático inesperado y reinstalar. Registrar
   resultados reales PASS/FAIL/BLOCKED, versión, hash y evidencia privada.

## Cinco usuarios piloto (sin contactos ni respuestas inventadas)

| Código sin asignar | Perfil propuesto | Recorrido y foco |
|---|---|---|
| B01 | Windows11, sin herramientas de desarrollo | Instalar offline/demo/PNG/preset/reinicio/desinstalar |
| B02 | Windows10 x64 | Misma matriz, con WebView2 ya presente, actualización0.2→0.3 |
| B03 | Fotógrafo autorizado | Fotos claras/oscuras y retratos propios con permisos, corrección manual y comparación al100% |
| B04 | Editor con Adobe activado | LUT color-only en Photoshop y Premiere disponibles; documentar color/dithering/ausencia de efectos |
| B05 | Portátil8GB o hardware diferente | Lote16, cancelación, disco/rutas con espacios, memoria/rendimiento y error recuperable |

Son perfiles a conseguir, no participantes reclutados. Una persona puede
rechazar/abandonar sin enviar feedback. El titular acuerda responsable, canal
privado, plazo y permisos antes de invitaciones. No asignar identidades en Git.
El agente no contacta participantes sin autorización concreta de destinatario/canal.

## Checklist funcional de cada prueba

- Abrir JPG/PNG y demo autorizada; entrada corrupta/RAW/16bit rechazada de forma
  comprensible; los originales no cambian. No usar fotos privadas en capturas públicas.
- Color Match y Look Match por separado: bypass, intensidad0, glow/difusión/fade,
  undo/redo, preset guardar/cargar/editar/grupo, JSON exportar/importar y reinicio.
- Exportar PNG/JPG con dimensiones/ICC/alfa documentados; verificar apariencia
  al100% con misma gestión de color. Registrar halos/bordes/ruido/piel/clipping.
- LUT genera aviso y contiene **solo color**. La recetaJSONv2 y el render llevan
  acabado. Halation, microcontraste dedicado e inferencia de filtros siguen pendientes.
- Lote con misma receta, progreso/cancelación, exportación y recuperación; no
  sobrescribir inputs. Comparar hash/dimensiones y anotar tiempo/RAM aproximados.
- Ayuda→feedback abre formulario incluido `/feedback/`, funciona offline y no
  envía red. Descargar JSON y revisar antes de devolver por canal privado acordado.

## Feedback y custodia

Formulario técnico incluido, sin analytics, cuentas, email o fotos. Códigos B01–05
sin identidad; QA00 reservado a infraestructura sintética. Archivo JSON lleva
verification=unverified y counts_as_interview=false; no prueba identidad,
consentimiento o entrevista COL001. El titular recibe por canal privado elegido,
guarda fuera de Git en .research-private/beta/, verifica código/versión/alcance,
fecha de recepción y hash SHA256; registra duplicados y conserva original.
Solo un resumen sin datos personales entra en Issue. No adjuntar archivos crudos
a GitHub/Pages. Plazo y eliminación los decide el responsable, todavía pendiente.

## LUT: prueba real de editores preparada

Paquete local .lumaforge-local/look03-qa: before.png, color.png, finish.png,
color-only.cube y recipe.json; fotografías CC0, no target humano aprobado.
Photoshop2026 pide inicio de sesión y Premiere está instalado sin prueba real;
Resolve ausente al último inventario. El titular debe activar sesión/licencia.

En Photoshop abrir before.png en sRGB, añadir Consulta de colores/Color Lookup,
cargar color-only.cube al100%, sin otros ajustes; guardar copiaPNG con ICC.
Comparar con color.png (no con finish.png); cuantizar/dithering/interpolación
pueden diferir, documentar antes de aceptar tolerancia. El acabado solo se
reproduce importando receta en LumaForge y exportando imagen. No anunciar que
la LUT conserva difusión/glow/fade. En Premiere usar clip SDR interpretado
correctamente, LUT creativa al100% sin doble conversión, exportar frame sRGB
documentado y comparar. Registrar versión y configuración, no solo que abre.
No instalar otro editor ni comprar licencia para esquivar el bloqueo.

## Matriz operable de Windows limpio

Cuatro snapshots independientes: W10-SIN-WV, W10-CON-WV, W11-SIN-WV y W11-CON-WV,
x64, cuenta estándar,8GB mínimo a evaluar, sin herramientas de desarrollo. No
desinstalar WebView2 del host compartido. Registrar edición/build, RAM, versión
WebView2 y hash del candidato, sin usuario/host/serial. El inventario actual no
encontró Get-VM/vmms, VBoxManage, vmrun, procesos de VM ni Windows Sandbox;
no hay sesión de VM accesible/autorizada. No se habilitó virtualización.

| Caso | Acción exacta | Evidencia/aceptación requerida | Estado actual |
|---|---|---|---|
| W01 | Snapshot, preflight y hash antes de instalar | Hash exacto, herramientas ausentes y snapshot identificado por código privado | not_run |
| W02 | Red de VM desconectada; instalar por usuario | Exit/diálogo real, sin descargar dependencias; no bypass SmartScreen/Defender | not_run |
| W03 | Inicio→Color Studio, repetir apertura | Bienvenida, versión, una instancia, motor supervisado; nada en interfaces públicas | not_run |
| W04 | Demo CC0→analizar→ajustar→PNG/JPG/JSON/LUT | Dimensiones/ICC/hash del original; LUT aviso solo color, receta conserva acabado | not_run |
| W05 | Guardar preset/preferencias; cerrar y reabrir | Datos persistentes, sin Internet, sin depender de Python/Node del host | not_run |
| W06 | Instalar0.2, guardar presetv1 y foto sentinela; actualizar a candidato | Snapshot/Verify de archivos y migración funcional v1→v2; registrar cambios esperados separadamente | not_run |
| W07 | Lote2, cancelación y cierre forzado de la app de ensayo | No corromper originales, estado interrupted honesto, ningún sidecar huérfano | not_run |
| W08 | Desinstalar cerrado, reiniciar; reinstalar | Binarios/atajos retirados, hashes privados conservados, no autostart inesperado | not_run |
| W09 | Feedback offline y error con entrada corrupta/16bit | JSON local sin envío; error claro; sin respuesta real inventada | not_run |

Para conservar datos, ejecutar en la máquina de ensayo con app cerrada. En
PowerShell5.1 nativo (sin perfil) no hace falta Python ni alterar políticas:

```powershell
./qa_windows_preservation.ps1 -Mode Snapshot -DataDirectory "$env:LOCALAPPDATA/ColorStudioBetaData" -Baseline ./datos-antes-privado.json
# Actualizar o desinstalar, siguiendo W06/W08; cerrar de nuevo la app.
./qa_windows_preservation.ps1 -Mode Verify -DataDirectory "$env:LOCALAPPDATA/ColorStudioBetaData" -Baseline ./datos-antes-privado.json -Report ./preservacion-resumen.json
```

Copiar los dos scripts desde scripts/ junto a setup y hash por canal privado.
Snapshot no sobrescribe baseline ni acepta directorio vacío/reparse points.
Verify permite archivos nuevos y falla con exit2 si falta/cambia un hash previo;
no borra/restaura nada. Baseline contiene nombres relativos: **privado, nunca Git**.
Solo el resumen sin nombres puede publicarse tras revisión. Una preferencia o
registro de job modificado legítimamente sigue siendo cambio: documentarlo y
conservar baseline; no regenerarlo para ocultar diferencias.

Guardar registro por caso PASS/FAIL/BLOCKED con fecha real, hash, versión,
configuración y evidencia privada. not_run nunca se convierte a PASS por script,
ausencia de errores, fixture o ejecución en el equipo de desarrollo. Si un
caso crítico falla, bloquear entrega y registrar Issue67 con resumen saneado.
