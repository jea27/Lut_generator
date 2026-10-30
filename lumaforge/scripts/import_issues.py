#!/usr/bin/env python3
"""Crea issues del roadmap sin duplicados; modo seguro por defecto (dry-run).

Requiere GitHub CLI ya autenticado y ejecución desde un repositorio con remoto.
Uso: python scripts/import_issues.py [--apply]
"""
import argparse
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / 'site' / 'data' / 'roadmap.json'
ID_IN_TITLE = re.compile(r'\[([A-Z]+-\d{3})\]')
LABELS = {
    'roadmap': ('0969DA', 'Issue relacionada con la hoja de ruta'),
    'needs-human': ('F9A825', 'Requiere decisión o ayuda humana y notificación móvil'),
    'blocked': ('D73A4A', 'No puede continuar'),
    'approved': ('0E8A16', 'Aceptación humana; nunca asignar por IA'),
    'status:in-progress': ('1D76DB', 'Implementación en curso'),
    'status:review': ('BFD4F2', 'Lista para revisión humana'),
}

def gh(*args):
    p = subprocess.run(['gh', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if p.returncode:
        raise RuntimeError(f"Error gh {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout.strip()

def issue_title(task):
    return f"[{task['id']}] {task['title']}"

def issue_body(task):
    return (f"## Objetivo\n{task['title']}\n\n"
            f"## Fase y prioridad\n{task['phase']} · {task['priority']} · Ejecutor: {task['executor']}\n\n"
            f"## Criterio de aceptación\n{task['acceptance']}\n\n"
            "## Condiciones\n- Respetar AGENTS.md y docs.\n"
            "- Adjuntar pruebas y evidencia reproducible.\n"
            "- La IA no puede cerrar, fusionar ni aplicar `approved`.\n")

def existing_ids(titles):
    return {m.group(1) for title in titles for m in ID_IN_TITLE.finditer(title or '')}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Confirma escrituras remotas en GitHub')
    args = parser.parse_args()
    tasks = json.loads(DATA.read_text(encoding='utf-8'))['tasks']
    if not args.apply:
        print(f"DRY RUN: {len(tasks)} tareas candidatas. No se escribirá nada en GitHub.\n")
        for task in tasks:
            print(f"  {issue_title(task)}")
        print("\nPara importar tras aprobarlo: python scripts/import_issues.py --apply")
        return
    # No crear labels ni issues sin autenticar y sin repo remoto.
    print('Repositorio:', gh('repo', 'view', '--json', 'nameWithOwner', '--jq', '.nameWithOwner'))
    existing = existing_ids([i['title'] for i in json.loads(gh('issue', 'list', '--state', 'all', '--limit', '1000', '--json', 'title'))])
    for name, (color, desc) in LABELS.items():
        gh('label', 'create', name, '--color', color, '--description', desc, '--force')
    created = skipped = 0
    for task in tasks:
        if task['id'] in existing:
            print('EXISTE:', task['id'])
            skipped += 1
            continue
        url = gh('issue', 'create', '--title', issue_title(task), '--body', issue_body(task), '--label', 'roadmap')
        print('CREADA:', task['id'], url)
        created += 1
    print(f'Finalizado: {created} creadas, {skipped} existentes. No se aprobó ninguna tarea.')

if __name__ == '__main__':
    main()
