# Guía práctica · Windows + Codex + GitHub + móvil

## 1. Descomprimir
Extrae este ZIP en `C:\Proyectos\LumaForge`. Abre la carpeta raíz en IntelliJ IDEA, el terminal PowerShell o la app ChatGPT para Windows en modo Codex. No abras solo la carpeta `site`: el contexto de Codex está en el directorio raíz.

## 2. Instalar herramientas en PowerShell
Si faltan (reinicia el terminal después):
```powershell
winget install --id Git.Git
winget install --id OpenJS.NodeJS.LTS
winget install --id Python.Python.3.12
winget install --id GitHub.cli
npm install -g @openai/codex@latest
```
Alternativa: app ChatGPT para Windows (Codex integrado). Descarga oficial: https://chatgpt.com/download/

Comprueba:
```powershell
git --version
python --version
gh --version
codex --version
```

## 3. Abrir proyecto y probar
```powershell
cd C:\Proyectos\LumaForge
powershell -ExecutionPolicy Bypass -File scripts/check_setup.ps1   # Auditoría, sin escrituras remotas
python -m unittest discover -s tests -v
python scripts/import_issues.py
python -m http.server 8080 --directory site
```
Dashboard: http://localhost:8080 — detener servidor con Ctrl+C. La web usa `site/data/roadmap.json` cuando puede pedirlo; sin GitHub muestra un estado inicial, no real remoto.

## 4. Codex aprende el proyecto
```powershell
cd C:\Proyectos\LumaForge
codex
```
En Codex, pega el contenido de `PROMPT_INICIAL_CODEX.md`. No necesitas copiar todo el chat: los documentos hacen de memoria compartida durable. Mantén el sandbox y solicitudes de aprobación activados; evita permisos irrestrictos.

## 5. Crear GitHub remoto (solo tras tu confirmación)
```powershell
gh auth login
git init
git add .
git commit -m "chore: initialize LumaForge planning and Codex handoff"
git branch -M main
# Sustituye NOMBRE_REPO según prefieras, recomendado público solo si los metadatos no son sensibles:
gh repo create NOMBRE_REPO --public --source . --remote origin --push
```
> Si ya existe repo, no vuelvas a hacer `git init` ni sobrescribas `origin`: comprueba antes `git status`, `git remote -v`, `gh repo view`.

## 6. Activar web
GitHub → repositorio → Settings → Pages → Source: **GitHub Actions**. Ejecuta Actions → **Publicar roadmap** → Run workflow. Abre el enlace de Pages que muestre la acción. La URL típica es `https://USUARIO.github.io/NOMBRE_REPO/`, no la des por creada hasta verificarla.

## 7. Importar las 42 Issues (solo cuando quieras)
```powershell
python scripts/import_issues.py           # Simulación, sin cambios
python scripts/import_issues.py --apply   # Crea tickets reales, evita IDs duplicados
```
Para empezar, también puedes crear solo una Issue `[COL-...]` a mano y conectar lo demás más tarde.

## 8. Avisos al móvil
GitHub → repo → Settings → Secrets and variables → Actions → **Variables** → New repository variable:
- Name: `REVIEWER_GITHUB`
- Value: **tu usuario de GitHub** (sin @)

Instala GitHub Mobile, inicia sesión y habilita push de @menciones y asignaciones. El workflow `.github/workflows/alert-human.yml` comenta desde `github-actions[bot]` al etiquetar una issue como `needs-human` o al abrir una PR `[COL-XXX]` lista para revisión. Puedes probarlo creando una issue de prueba con `needs-human`. Ver `docs/NOTIFICACIONES_Y_APROBACIONES.md`.

## 9. Trabajar de verdad por tarea
1. Elige un COL-###, crea/selecciona su Issue.
2. Codex implementa en rama `codex/COL-###-tema`, corre tests y documenta.
3. Codex hace `git push` a su rama y abre PR **solo después** de la autorización inicial de este flujo; nunca hace merge.
4. GitHub Actions detecta Issues y PR y actualiza el dashboard remoto. El usuario recibe push móvil para revisión/ayuda.
5. El humano revisa y corrige, integra a main, coloca `approved` y cierra la Issue (si corresponde). El dashboard reflejará `done` tras sincronizar.

## 10. Que trabaje cuando te ausentes
Una sesión Codex interactiva no se transforma por sí sola en servicio 24/7. En modo local necesitas PC encendido y sesión/orquestador activo. Para autonomía real, desarrollar una cola de trabajo con `codex exec` o SDK, budgets, límites, reintentos, logging y puertas de aprobación. No lanzar una tarea ilimitada ni usar `--dangerously-bypass-approvals-and-sandbox`.

## Seguridad importante
- No publiques repositorio privado, secretos, contraseñas, fotografías privadas ni credenciales en GitHub Pages.
- Si quieres código privado y dashboard público, hay que separar un repo de publicación con JSON sanitizado; **no está implementado**.
- El objetivo inicial es transparencia y control, no que Codex decida por su cuenta qué es una entrega aprobada.
