# Windows11 limpio · preparar la VM y ejecutar QA interna

COL-036/#57, solicitud canónica#67. Operador propuesto: jea27, asistido por
Codex. Autorización de pruebas internas beta.3; beta externa y venta continúan
**NO-GO**. Esta guía no acredita una VM creada ni pruebas ejecutadas.

## Comprobación real del host · 01-11-2026

Windows11 Pro x64 build26200, Ryzen7 5800X/16 procesadores lógicos,15,92GiB RAM
total. En la lectura inicial había4,86GiB disponibles. Espacio libre observado:
C:411,3GiB y E:573,5GiB. Son valores de ese instante, no reservas de recursos.

Firmware de virtualización activado e hipervisor detectado; VBS activo. **No
equivale a disponer de un administrador de VM.** No se encontraron Get-VM,
New-VM, vmms/vmconnect/Hyper-V Manager ni VirtualBox/VMware/Sandbox en PATH y
rutas estándar. WMI muestra Hyper-V, gestión, VirtualMachinePlatform,
HypervisorPlatform y Sandbox desactivados (InstallState2). Una ubicación portátil
no estándar no queda descartada por esa búsqueda.

La consulta DISM de lectura Get-WindowsOptionalFeature devolvió
**0x800702E4/Win32740: ERROR_ELEVATION_REQUIRED**. WMI sí permitió consultar el
estado sin elevar. Los flags WMI SLAT/VMMonitorMode=False observados bajo el
hipervisor activo no se usan como prueba concluyente de incompatibilidad de CPU.
Microsoft explica esta limitación en sus
[requisitos Hyper-V](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/host-hardware-requirements).
[InstallState2 significa Disabled](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-optionalfeature);
[740 requiere elevación](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--500-999-).

Codex no ha instalado un hipervisor, habilitado features, reiniciado, descargado
una ISO ni creado una VM. No es seguro dar por disponible una VM todavía.

## 1. Guardar trabajo y repetir el preflight

Cierra tú las aplicaciones que no necesites; Codex no debe terminar procesos
ajenos ni descartar trabajo. Con4,86GiB libres no se recomienda arrancar el guest
propuesto de6–8GiB. No reducir calidad de imágenes para ocultar presión de RAM.

Desde la carpeta de este worktree:

```powershell
./scripts/qa_vm_preflight.ps1
```

El script solo consulta el host y guarda un recibo nuevo en `.lumaforge-local/`.
No recoge nombre de equipo/usuario, seriales, clave de producto, rutas personales,
procesos ni archivos privados. Diferencia hipervisor, gestor VM y error de
elevación. No instala, habilita, reinicia ni arranca nada. Si una política impide
ejecutarlo, detenerse y registrar el bloqueo; no desactivar protecciones.

Propuesta conservadora:6GiB guest después de disponer de al menos8GiB libres;
8GiB solo si el host conserva margen real. Es un gate de ingeniería, no el mínimo
oficial ni una garantía de rendimiento. Para un VHDX96GiB, una checkpoint de
hasta96GiB,12GiB de ISO y64GiB de margen del host, presupuestar268GiB libres en el
volumen del workspace. No se reservan ni escriben esos tamaños en el preflight.

## 2. Preparación administrativa: intervención del operador

Preferir Hyper-V nativo de la edición Pro. El operador debe confirmar que puede
habilitar **plataforma y herramientas de administración Hyper-V** y acordar el
reinicio si Windows lo requiere. Codex prepara y comprueba pasos; no ejecuta una
elevación/reinicio por sorpresa ni solicita contraseñas en GitHub.

La operación debe seguir la
[guía oficial de instalación de Hyper-V](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/install-hyper-v?pivots=windows).
Después del reinicio, volver a comprobar Get-VM, vmms y el acceso al gestor. Un
componente instalado no acredita por sí solo que la VM arranque correctamente.

No desactivar VBS, integridad de memoria, Defender, firewall, SmartScreen, Secure
Boot ni TPM para permitir un hipervisor alternativo. No cambiar BIOS, particiones,
discos físicos o instalación principal. Si no es posible preparar Hyper-V con
esas condiciones, el operador aporta una VM/equipo limpio ya autorizado.

## 3. Obtener la ISO y confirmar derechos del guest

Dos rutas oficiales; elegir una antes de descargar:

- [ISO Windows11 x64 de Microsoft](https://www.microsoft.com/en-us/software-download/windows11):
  usar la sección **Disk Image (ISO)** y una licencia válida para el guest. La
  descarga de una ISO no concede una licencia adicional por sí sola.
- [Evaluación Enterprise oficial](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise):
  actualmente26H2 y90 días; leer condiciones, registrarse y activar conforme a
  la página. Microsoft indica que no necesita clave de producto para esta
  evaluación, y describe los requisitos de cuenta. El operador introduce sus
  datos reales y realiza autenticación; Codex no inventa empresa ni credenciales.

Conservar edición, versión, idioma, fecha, URL oficial y SHA-256, contrastado con
la verificación proporcionada por Microsoft. No registrar email, cuenta, clave,
serial o enlaces personales temporales en Git. No afirmar autenticidad/hash de
una ISO que aún no se ha descargado. Una evaluación caducada no vale para QA.

**No usar Installation Assistant, USB de arranque ni setup.exe sobre el host.**
La ISO se adjunta exclusivamente al lector DVD virtual de la VM.

## 4. Crear una VM aislada cuando el entorno esté preparado

En Hyper-V Manager, el operador crea una VM nueva para Color Studio:

| Parámetro | Propuesta de prueba |
|---|---|
| Generación |2, sin convertir una VM anterior de Gen1 |
| CPU |4 vCPU |
| Memoria |6GiB tras liberar RAM;8GiB si hay margen |
| Disco | VHDX dinámico96GiB, como archivo nuevo dentro de `.lumaforge-local/vm/` |
| Seguridad | Secure Boot y vTPM activados |
| ISO | Microsoft x64 verificada, montada solo en DVD virtual |
| Red inicial | NAT/Default Switch solo cuando instalación/prerrequisitos lo necesiten |

[Mínimos oficiales de guest Windows11](https://learn.microsoft.com/en-us/windows/whats-new/windows-11-requirements#virtual-machine-support):
Gen2, al menos4GB RAM,64GB de disco,2vCPU y Secure Boot/vTPM. La propuesta superior
es un presupuesto de ensayo, no una certificación ni benchmark.

Crear únicamente el archivo VHDX: nunca elegir un disco físico/passthrough ni
modificar particiones. No compartir carpetas personales, unidades completas ni
credenciales del host. Transferir solo el paquete QA autorizado con instaladores,
hashes y demo CC0; no subir el instalador a una release pública para transferirlo.

Instalar Windows en el disco virtual nuevo y completar personalmente activación/
cuenta cuando proceda. No instalar Python, Node, Git, Rust, VS ni herramientas de
desarrollo en el guest. Tomar checkpoint limpio antes del primer candidato y
anotar edición/build/RAM sin identificadores personales.

## 5. Ejecutar y registrar, sin dar resultados por supuestos

Seguir W01–W09 de `BETA_QA_EXTERNA.md` y `PRUEBA_CREATOR_PRO_PLANNER.md`:
instalación, arranque, Creator/Pro/Planner, Color/Look Match manual, PNG/JPG,
receta, LUT, actualización directa, recuperación de fallo, desinstalación y datos.
Usar solo demo CC0/fixtures autorizados y sentinelas de QA. No usar fotos privadas.

Probar dos estados de WebView2 en snapshots separados. Cuando falte, instalar
Evergreen por mecanismo oficial con conexión; después no se necesita Internet
para procesar imágenes. Comprobarlo desconectando **la NIC virtual del guest**,
no la del host. Registrar que no hay conectividad real y ejecutar todos los
recorridos offline. PATH restringido o localhost por sí solos no prueban esto.

No considerar suficiente desinstalar/reinstalar para aprobar actualización:
repetir la actualización directa y los casos de fallo/recuperación definidos
por la PR correctiva, comprobando preferencias, presets, originales y hashes.
Conservar checkpoint anterior y copia privada antes de ese ensayo.

DaVinci Resolve puede probarse por separado en el host con GPU/RAM adecuadas;
no presuponer que una VM básica lo soporte. Photoshop/Premiere y otras licencias
solo se acreditan tras ejecución real. Cada caso empieza **NO EJECUTADO** y pasa
a PASS/FAIL/BLOCKED únicamente con evidencia de versión, hash y pasos observados.

Para asistencia, responder en#67 con entorno/operador, recursos disponibles,
estado Hyper-V y caso bloqueado. No publicar cuentas, claves, fotografías,
carpetas personales ni logs completos. El resultado de este procedimiento no
autoriza beta externa, venta, merge o aceptación humana de capacidades.
