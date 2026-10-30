#!/usr/bin/env python3
"""Sincroniza el estado publicado de la hoja de ruta con Issues y PRs.

Solo usa el plan versionado y metadatos de GitHub, nunca secretos ni cuerpos
completos de issues en la web. Una tarea no puede pasar a 'done' por la IA:
requiere issue cerrada + label 'approved' + PR fusionado si procede.
"""
import datetime
import json
import os
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / 'site' / 'data' / 'roadmap.json'
TASK_ID = re.compile(r'\[([A-Z]+-\d{3})\]')


def get_json_pages(repo, endpoint, token):
    items=[]
    for page in range(1, 11):
        params=urllib.parse.urlencode({'state':'all','per_page':100,'page':page})
        request=urllib.request.Request(
            f'https://api.github.com/repos/{repo}/{endpoint}?{params}',
            headers={
                'Accept':'application/vnd.github+json',
                'User-Agent':'LumaForge-Roadmap/0.1',
                'Authorization':f'Bearer {token}',
            },
        )
        with urllib.request.urlopen(request,timeout=25) as response:
            batch=json.load(response)
        if not isinstance(batch,list):
            raise ValueError(f'Respuesta inesperada en {endpoint}')
        items.extend(batch)
        if len(batch)<100:
            return items
    raise ValueError('Más de 1000 resultados. Añade paginación exhaustiva antes de continuar.')


def ids_from_title(title):
    return set(TASK_ID.findall(title or ''))


def derive_status(task, issue, pull):
    if not issue:
        return 'planned'
    labels={x.get('name','').lower() for x in issue.get('labels',[])}
    if labels & {'blocked', 'needs-human'}:
        return 'blocked'
    merged=bool(pull and pull.get('merged_at'))
    accepted=issue.get('state')=='closed' and 'approved' in labels
    if accepted and (not task.get('requires_pr') or merged):
        return 'done'
    if issue.get('state')=='closed' or merged or pull and pull.get('state')=='open' and not pull.get('draft') or 'status:review' in labels:
        return 'review'
    if 'status:in-progress' in labels:
        return 'progress'
    return 'planned'


def main():
    repo=os.environ.get('GITHUB_REPOSITORY','').strip()
    token=os.environ.get('GITHUB_TOKEN','').strip()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo):
        raise SystemExit('GITHUB_REPOSITORY debe ser owner/repo.')
    if not token:
        raise SystemExit('Falta GITHUB_TOKEN. No se publica un estado de sincronización ficticio.')
    data=json.loads(PATH.read_text('utf-8'))
    issues=get_json_pages(repo,'issues',token)
    prs=get_json_pages(repo,'pulls',token)
    # GitHub Issues API incluye PRs: excluirlos explícitamente.
    issue_by_id={}
    for issue in issues:
        if 'pull_request' in issue:
            continue
        labels={x.get('name','').lower() for x in issue.get('labels',[])}
        if 'roadmap' not in labels:
            continue
        for tid in ids_from_title(issue.get('title')):
            old=issue_by_id.get(tid)
            if old is None or issue.get('updated_at','')>old.get('updated_at',''):
                issue_by_id[tid]=issue
    pr_by_id={}
    for pr in prs:
        if pr.get('base', {}).get('ref') != 'main':
            continue
        for tid in ids_from_title(pr.get('title')):
            old=pr_by_id.get(tid)
            if old is None or pr_rank(pr)>pr_rank(old):
                pr_by_id[tid]=pr
    summary={}
    for task in data['tasks']:
        task_id=task['id']
        issue=issue_by_id.get(task_id)
        pull=pr_by_id.get(task_id)
        task['status']=derive_status(task,issue,pull)
        # Metadatos públicos: solo URLs y números; no incluir cuerpos privados.
        task['issue_url']=issue.get('html_url') if issue else None
        task['issue_number']=issue.get('number') if issue else None
        task['pr_url']=pull.get('html_url') if pull else None
        task['updated_at']=max((x.get('updated_at','') for x in (issue,pull) if x), default=None)
        summary[task['status']]=summary.get(task['status'],0)+1
    now=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
    data['project'].update({'mode':'github','repository_url':f'https://github.com/{repo}','updated_at':now})
    PATH.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    PATH.with_name('fallback.js').write_text(
        'window.INITIAL_ROADMAP = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    print(f"Sincronizadas {len(issues)} issues, {len(prs)} PR. Estado: {summary}. {now}")

def pr_rank(pull):
    # Keep a new active delivery visible; discarded PRs cannot hide a merge.
    return (2 if pull.get('state') == 'open' else 1 if pull.get('merged_at') else 0,
            pull.get('updated_at', ''))


if __name__=='__main__':
    main()
