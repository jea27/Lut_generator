# Corrección de la raíz del repositorio · 2026-10-30

## Alcance y estado inicial

Solicitud de mantenimiento de estructura, independiente de las 42 tareas de producto: no se crea ni se da por aprobada ninguna COL. La autorización de esta sesión permite preparar cambios locales; cualquier push o cambio de configuración remota requiere aprobación previa.

- `git status`: limpio, rama `main`, sincronizada con `origin/main`.
- `git rev-parse --show-toplevel`: `C:/Users/jeast/Documents/ChatGPT/Lut generator`.
- `git remote -v`: fetch y push en `https://github.com/jea27/Lut_generator.git`.
- Los 24 archivos versionados estaban bajo `lumaforge/`, incluidos los dos workflows que GitHub no podía descubrir desde la raíz.
- Rama de la corrección: `codex/fix-repository-root`.

## Modificaciones

1. Tras comprobar que no existía ningún destino, se movió todo el contenido de `lumaforge/` a la raíz: `.github/`, `.gitignore`, `docs/`, `scripts/`, `site/`, `tests/`, `AGENTS.md`, `README.md`, `GUIA_WINDOWS_CODEX.md` y `PROMPT_INICIAL_CODEX.md`. Se retiró únicamente el contenedor vacío. El directorio `.git` no se movió ni se reinicializó; no se reescribió el historial.
2. Se revisaron filtros `paths`, comandos, checkout y artefacto del workflow de publicación: ya usaban `site/**`, `tests/**`, `scripts/sync_github.py` y `.github/workflows/publish-roadmap.yml` desde la raíz. Ahora corresponden a los destinos reales. Los workflows no necesitan cambios de contenido.
3. Los scripts Python y tests usan `Path(__file__).resolve().parents[1]`; el comprobador PowerShell usa el padre de `$PSScriptRoot`. Se conservan porque ahora resuelven directamente a la raíz Git. Los enlaces de recursos web son relativos al sitio y funcionan bajo `/Lut_generator/`.
4. README y guía Windows identifican el remoto existente, la estructura correcta, el origen GitHub Actions y la URL configurada; se sustituyeron las instrucciones activas para crear otro repositorio. El prompt inicial también remite al repositorio existente. LumaForge sigue siendo el nombre provisional del producto.
5. Se añadió este informe y una entrada al diario. La auditoría y el traspaso anteriores se conservan como registros históricos; sus referencias al estado anterior no son instrucciones actuales.

## Validación ejecutada

Python utilizado: `C:\Users\jeast\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` (3.12.14). No hay comando `python` funcional en PATH; los comandos siguientes se ejecutaron con ese binario explícito.

- `python -m unittest discover -s tests -v`: **11 pruebas OK**, 8 del sincronizador y 3 del importador.
- `python scripts/import_issues.py`: **DRY RUN, 42 candidatas**, sin escrituras remotas.
- `node --check site/app.js` y `node --check site/data/fallback.js`: OK.
- Validación local con PyYAML 6.0.3, instalado únicamente en una carpeta temporal: los dos workflows se analizan correctamente, no contienen claves duplicadas y tienen la estructura básica de Actions. Se usó `BaseLoader` para preservar `on` como clave, evitando la interpretación booleana de YAML 1.1.
- Comprobación de contrato Pages: checkout `main`, entorno `github-pages`, permisos `pages: write` e `id-token: write`, acciones configure/upload/deploy y artefacto `path: site`: OK.
- Comparación de los 24 archivos originales con `git show HEAD:lumaforge/<ruta>`: contenido conservado salvo las tres guías editadas. Se normalizaron CRLF/LF en esa comparación porque `core.autocrlf=true`. Las 42 tareas COL-001…COL-042, sus estados, criterios y documentación de producto no se alteraron. JSON y fallback siguen coincidiendo.
- Servidor HTTP temporal en loopback, montado bajo `/Lut_generator/`: respuestas **200** para índice, CSS, ambos JavaScript y `data/roadmap.json`. Servidor detenido tras la comprobación. No equivale a una prueba visual del navegador.
- Revisión de referencias a `lumaforge/`: solo quedan explicaciones de la estructura corregida y registros históricos.
- `git diff --check` y `git diff --cached --check`: sin errores al preparar la entrega.

Las comprobaciones adicionales se ejecutaron con un script temporal local, sin añadir dependencias ni herramientas al proyecto. No se ejecutó actionlint: la validación YAML y del contrato básico no sustituye la evaluación completa de expresiones y eventos por GitHub Actions.

## Pages y límites de la comprobación remota

Consulta de solo lectura ejecutada:

```powershell
gh api repos/jea27/Lut_generator/pages --jq '{build_type: .build_type, status: .status, html_url: .html_url}'
```

Resultado: `build_type: workflow`, `html_url: https://jea27.github.io/Lut_generator/`, `status: null`. Se mantiene GitHub Actions como origen; no se cambiaron permisos, variables, entorno ni configuración remota. Este resultado confirma la configuración, no un despliegue correcto de los cambios locales.

Referencias oficiales consultadas:
- [Ubicación de workflows en la raíz](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).
- [Publicación de Pages mediante workflows y artefactos](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Preparación y autorización de publicación de la rama

Cambios preparados en el índice para revisión; mensaje propuesto:

```text
fix: move LumaForge project to repository root
```

En la entrega inicial no se había creado el commit ni realizado push, merge, PR o escritura remota. No se añadieron funciones de producto. Los demás hallazgos de la auditoría inicial quedan fuera de esta corrección.

El usuario autorizó después crear el commit, publicar exclusivamente la rama `codex/fix-repository-root` y abrir una PR hacia `main`. La integración en `main` permanece bajo revisión humana y no se autoriza el merge. Después de integrar, comprobar el workflow **Publicar roadmap**, su artefacto y la URL de Pages. No hace falta modificar el origen de Pages, que ya es GitHub Actions.
