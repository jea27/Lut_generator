# COL036 · actualización verificable de Windows

Entrega correctiva interna, sin autorización de distribución. No modifica el motor.

## Evidencia y causa

El `2` histórico de beta.3 no tenía fases ni registros suficientes. NSIS define
ese resultado como aborto por script, no como un error Win32 concreto. La
repetición silenciosa beta.2→beta.3 en el host terminó con `0`, con un preset real
de QA recuperado por la API y los archivos privados conservados. Eso no reproduce
ni explica el incidente histórico. Desinstalar/reinstalar se usó exclusivamente
para preparar la línea base beta.2, nunca como solución de actualización.

Defectos independientes medidos: el overlay silencioso conserva `_internal` y
`ColorEngine.exe` heredados; NSISdl devolvió `success` en una prueba loopback con
URL HTTPS en la que el servidor recibió GET HTTP en claro, sin TLS ClientHello.
La descarga externa Microsoft también devolvió `success`; no se capturó su tráfico
y no se infiere de ello su transporte ni la causa del incidente anterior.

## Sustitución por etapas

1. El instalador por usuario toma el mismo mutex que la aplicación; pide cerrarla
   sin terminarla a la fuerza. Un segundo instalador tampoco puede actualizarla.
2. Comprueba Evergreen antes de tocar la instalación. Se elimina NSISdl: se embebe
   el bootstrapper oficial, sin modificar, con URL HTTPS inmutable, SHA256 fijado,
   firma Microsoft válida y arquitectura verificada durante la construcción.
3. Extrae todo a un directorio nuevo, hermano de la carpeta de destino. El antiguo
   desinstalador no se ejecuta. La aplicación anterior sigue completa.
4. El Python aislado incluido comprueba un manifiesto SHA256 completo, cuyo hash
   se compila en NSIS: launcher, runtime y avisos. El desinstalador generado se
   inspecciona por separado mediante extracción completa del NSIS.
5. Bajo lock del sistema operativo, valida propiedad del destino y rechaza enlaces,
   rutas protegidas, traversal, colisiones y archivos de paquete inesperados.
   Conserva extras personales fuera de componentes gestionados. Calcula el hash
   agregado del árbol anterior antes del cambio; no publica nombres personales.
6. Escribe y sincroniza un diario privado. Mueve la carpeta anterior a una copia
   hermana `.lf-previous-…` y el stage validado a su nombre definitivo. Si la segunda
   operación devuelve un error, intenta restaurar la anterior sin borrados.
7. Solo entonces actualiza registro y accesos directos. Persiste idioma también
   con `/S`. Registra fases y resultados del hijo sin rutas/fotografías/tokens.

El instalador cambia su CWD al padre antes de ejecutar Python: no mantiene abierto
el directorio que intenta renombrar. El helper puede moverse junto con su runtime;
debe verificarse también con el candidato nativo real, no solo con fixtures.

La revisión encontró una limpieza heredada que usaba `MainBinaryName` del registro
como nombre para `Delete`: se eliminó, pues el stage nuevo no necesita esa limpieza.
El desinstalador comprueba atributos de todos los directorios gestionados y sus
ancestros antes del primer borrado; si detecta reparse/junction o no puede
verificarlos, aborta. La función real se prueba con NSIS fijado y junctions locales
sin privilegios. No se garantiza resistencia frente a manipulación concurrente
hostil del sistema de archivos por la misma cuenta durante la desinstalación.

## Conservación y recuperación

`ColorStudioBetaData` está fuera de la carpeta de instalación y no se toca. Los
extras en la raíz se copian a la nueva instalación; los que estén dentro de
`runtime`, `notices`, `_internal` u otros componentes gestionados quedan en la
copia anterior completa, no se mezclan con el runtime aislado nuevo. La copia no
se borra automáticamente. Consume espacio adicional y es privada: no debe
adjuntarse a GitHub ni redistribuirse, especialmente si contiene el runtime beta.2.
No ejecutar `uninstall.exe` dentro de una copia anterior: ese desinstalador puede
retirar las claves de la instalación activa. La recuperación se hace verificando
y restaurando carpetas, con el operador; no encadenando desinstaladores de backups.

En el siguiente intento, un diario pendiente permite verificar la copia completa
y restaurarla si falta el destino, o verificar el nuevo paquete si el cambio ya
terminó. Si cambió la copia, el destino o el paquete nuevo está corrupto, se
detiene sin sobrescribir datos. Hace falta inspección del operador: guardar ambos
árboles y el diario privado, cerrar app/instaladores, identificar versión y hashes,
y restaurar solo una copia íntegra a un destino libre. No borrar ni ejecutar DLL
sueltas y no enviar el contenido privado a Issues. Un fallo posterior de registro
no equivale a ausencia del nuevo paquete; las fases distinguen ambos casos.

Los tests simulan interrupciones de proceso y errores de archivos; no acreditan
corte de corriente, VM limpia, antivirus, SmartScreen ni todos los bloqueos de
Windows. No se promete rollback universal frente a corrupción posterior o disco
defectuoso. Si se retiene el diario tras un commit correcto, se registra ese hecho
y el siguiente intento vuelve a validarlo.

## Construcción y pruebas

Desde esta rama, con herramientas ya autorizadas y Node/Rust fijados:

```powershell
./scripts/build_beta.ps1 -BuildPython ../../.venv-mvp/Scripts/python.exe -Offline
```

`-Offline` exige tener todos los inputs verificados en la caché privada del
worktree. Sin el flag, se obtienen solo los inputs fijados, nunca herramientas
adicionales. El script compila nativo sin bundle, genera ledger y hash NSIS, empaqueta
y extrae el resultado completo para cotejar bytes, arquitectura, avisos y privacidad.
El candidato nuevo usa beta.4; nunca sustituye silenciosamente el hash de beta.3.

Ejecutar los tests del helper, MVP, seguimiento y frontend. Después, con fotos CC0
o fixtures autorizados, actualizar beta.3→beta.4 y beta.2→beta.4 directamente,
recuperar presets/Creator/Pro, comparar hashes de preferencias y originales,
comprobar que el runtime legado ya no está activo y repetir tras un fallo controlado.
Guardar registros crudos privados; publicar solo recibos sanitizados.

Windows limpio y desconexión física requieren el operador del entorno. El
bootstrapper embebido no contiene todo Evergreen: si falta el runtime, necesita
Internet. Con Evergreen ya instalado, el procesamiento de Color Studio es local;
su funcionamiento realmente desconectado sigue pendiente hasta ejecutarlo.

## Fuentes primarias

- [Códigos de salida NSIS](https://nsis.sourceforge.io/Docs/AppendixD.html).
- [Modo silencioso NSIS](https://nsis.sourceforge.io/Docs/Chapter4.html#silent).
- [Plantilla Tauri fijada](https://github.com/tauri-apps/tauri/blob/tauri-cli-v2.12.4/crates/tauri-bundler/src/bundle/windows/nsis/installer.nsi).
- [Distribución Evergreen de Microsoft](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/distribution).
- [Descarga y condiciones WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/).

Las condiciones propietarias siguen como puerta separada de distribución; una
firma válida y la recomendación técnica de Microsoft no son aprobación comercial.
