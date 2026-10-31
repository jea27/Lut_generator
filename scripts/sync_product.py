"""Public, allowlisted product telemetry. Read trusted checkout only, never PR artifacts.

On API errors no output is replaced: Pages keeps its last complete snapshot.
No issue/PR/release bodies, emails, local paths, logs or binary downloads.
"""
import datetime
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SECRET = re.compile(r'(?i)(?:(?<![a-z0-9])[a-z]:[\\/]|file://|github_pat_|gh[pousr]_|-----BEGIN|[\w.+-]+@[\w.-]+\.[a-z]{2,})')
VERSION = re.compile(r'^\d+\.\d+\.\d+(?:-(?:alpha|beta|rc)\.\d+)?$')


def text(value, limit=160):
    value = str(value or '')
    return 'Metadatos omitidos por privacidad' if SECRET.search(value) else value[:limit]


def timestamp(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)',value): return None
    try: datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError: return None
    return value


def sha(value): return value if isinstance(value,str) and re.fullmatch('[a-f0-9]{40}',value) else None


def link(value, repo):
    base = 'https://github.com/'+repo+'/'
    if isinstance(value, str) and value.startswith(base) and not SECRET.search(value):
        u = urllib.parse.urlsplit(value)
        route=urllib.parse.unquote(u.path).removeprefix('/'+repo+'/')
        if u.hostname == 'github.com' and not u.username and not u.password and not u.query and not u.fragment and re.fullmatch(
                r'(?:issues/[1-9]\d*|pull/[1-9]\d*|actions/runs/\d+|releases/tag/[A-Za-z0-9._/-]+|commit/[a-f0-9]{40})',route): return value
    return None


def path(root, value):
    if not isinstance(value, str) or not value.startswith(('apps/','packages/','tests_mvp/','docs/evidence/')):
        raise ValueError('Unsupported public evidence path')
    candidate = (root/value).resolve()
    if not candidate.is_relative_to(root.resolve()) or any(part.startswith('.') for part in Path(value).parts):
        raise ValueError('Evidence path escapes trusted checkout')
    return candidate


class GitHub:
    def __init__(self, repo, token): self.repo, self.token, self.public = repo, token, False

    def get(self, endpoint, params=None):
        query = urllib.parse.urlencode(params or {})
        url = f'https://api.github.com/repos/{self.repo}{endpoint}'+('?' + query if query else '')
        headers = {'Accept':'application/vnd.github+json','User-Agent':'LumaForge-Product/1'}
        if self.token: headers['Authorization'] = 'Bearer '+self.token
        for attempt in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=25) as response:
                    return json.load(response)
            except urllib.error.HTTPError as error:
                if error.code==403 and self.public and 'Authorization' in headers and attempt<2:
                    # Public GET fallback, never permission escalation. A private
                    # repository is refused before enabling this path.
                    headers.pop('Authorization')
                    continue
                if error.code not in (429,500,502,503,504) or attempt == 2: raise
                # Bounded retry; do not echo API error bodies or credentials.
                time.sleep(attempt+1)
            except urllib.error.URLError:
                if attempt == 2: raise
                time.sleep(attempt+1)

    def pages(self, endpoint):
        items = {}
        for page in range(1,11):
            batch = self.get(endpoint, {'state':'all','per_page':100,'page':page})
            if not isinstance(batch,list): raise ValueError('Expected list from GitHub')
            for item in batch:
                if not isinstance(item,dict) or not isinstance(item.get('id'),int): raise ValueError('Invalid GitHub record')
                items[item['id']] = item
            if len(batch)<100: return sorted(items.values(),key=lambda x:x['id'])
        raise ValueError('Pagination exceeded safe limit; refuse incomplete snapshot')


def labels(issue): return {x.get('name','').lower() for x in (issue or {}).get('labels',[])}
def blocked(issue): return bool(labels(issue) & {'blocked','needs-human'})
def approved(issue): return bool(issue and issue.get('state')=='closed' and 'approved' in labels(issue) and not blocked(issue))


def evidence(root, item):
    p = path(root,item['path'])
    if not p.is_file(): return None
    value = json.loads(p.read_bytes()).get(item['field'])
    return None if value is None else type(value) is type(item['equals']) and value == item['equals']


def metric(values):
    values = list(values)
    if not values or all(v is None for v in values): return {'passed':None,'total':len(values),'unknown':len(values),'percent':None}
    unknown = sum(v is None for v in values)
    count = sum(v is True for v in values)
    return {'passed':count,'total':len(values),'unknown':unknown,'percent':None if unknown else round(100*count/len(values))}


def validate(manifest, root):
    if manifest.get('schema_version')!=1: raise ValueError('Unknown product schema')
    ids = set()
    for f in manifest['features']:
        if not re.fullmatch('[a-z][a-z0-9-]{1,40}',f['id']) or f['id'] in ids: raise ValueError('Duplicate/invalid feature')
        ids.add(f['id'])
        if not f.get('acceptance') or text(f['title'])!=f['title'] or text(f['acceptance'],1000)!=f['acceptance']:
            raise ValueError('Invalid public criterion')
        for value in f['code_paths']+f['tests']+[e['path'] for e in f['evidence']]: path(root,value)
    for members in manifest['metrics'].values():
        if len(members)!=len(set(members)) or not set(members)<=ids: raise ValueError('Invalid metric denominator')
    legacy={t['id'] for t in json.loads((root/'site/data/roadmap.json').read_bytes())['tasks']}
    operations=manifest.get('operations',[])
    if len({op['id'] for op in operations})!=len(operations) or any(op['id'] in legacy for op in operations):
        raise ValueError('Project operations must not duplicate historical tasks')
    path(root,manifest['version_source'])


def derive(manifest, root, repo, issues, pulls, runs, main_sha, releases, artifacts, observed_at):
    validate(manifest, root)
    if any(type(x.get('number')) is not int or x['number']<=0 for x in issues+pulls): raise ValueError('Invalid issue/PR number')
    issue_by = {x['number']:x for x in issues if 'pull_request' not in x}
    pr_by = {x['number']:x for x in pulls}
    required = manifest['required_ci']
    ci_main = {}
    for name in required:
        candidates = [r for r in runs if r.get('name')==name and r.get('head_sha')==main_sha and r.get('head_branch')=='main']
        ci_main[name] = max(candidates,key=lambda r:(r.get('run_number',0),r.get('run_attempt',0)),default=None)
    ci_pass = None if any(not r for r in ci_main.values()) else all(r.get('conclusion')=='success' and r.get('status')=='completed' for r in ci_main.values())
    features = []
    for f in manifest['features']:
        issue = issue_by.get(f['issue'])
        baseline = [pr_by[n] for n in f['delivery_prs'] if n in pr_by]
        related = [p for p in pulls if re.search(r'\['+re.escape(f['task'])+r'\]',p.get('title',''))]
        latest = max(related,key=lambda p:p.get('updated_at',''),default=None)
        merged = any(p.get('merged_at') and p.get('base',{}).get('ref')=='main' for p in baseline)
        implemented = bool(f['code_paths'] and merged and all(path(root,p).is_file() for p in f['code_paths']))
        proofs = [evidence(root,e) for e in f['evidence']]
        verified = (None if any(v is None for v in proofs) else ci_pass and all(v is True for v in proofs) and bool(f['tests']) and all(path(root,p).is_file() for p in f['tests'])) if implemented else False
        accepted = None if issue is None else approved(issue) and merged and f['group'] not in ('Futuro','Integración')
        state = 'planned'
        if implemented: state = 'implemented'
        if verified: state = 'verified'
        if implemented and not accepted: state = 'review'
        if implemented and not accepted and (latest and latest.get('state')=='open' and latest.get('draft') or 'status:in-progress' in labels(issue)):
            state = 'progress'
        if not implemented and 'status:in-progress' in labels(issue) and f['group']!='Futuro': state = 'progress'
        if accepted: state = 'approved'
        if blocked(issue) and f['group']!='Futuro': state = 'blocked'
        links = [{'label':'Prueba','url':f'https://github.com/{repo}/blob/main/{p}'} for p in f['tests']]
        links += [{'label':'Evidencia','url':f'https://github.com/{repo}/blob/main/{e["path"]}'} for e in f['evidence']]
        features.append({'id':f['id'],'title':f['title'],'group':f['group'],'task':f['task'],'acceptance':f['acceptance'],
                         'status':state,'implemented':implemented,'technically_verified':verified,'human_approved':accepted,
                         'blocked':blocked(issue) and f['group']!='Futuro','issue_url':link((issue or {}).get('html_url'),repo),
                         'pr_url':link((latest or (baseline[-1] if baseline else {})).get('html_url'),repo),
                         'evidence':links,'verification_scope':'Tests de main y evidencia versionada; no aceptación estética ni Windows limpio'})
    # Versioned artifact allowlist. Never copy filenames/local paths or arbitrary fields.
    builds = []
    for p in sorted((root/'docs/evidence').glob('*ARTIFACT*.json')):
        d = json.loads(p.read_bytes())
        if not VERSION.fullmatch(str(d.get('version',''))) or not re.fullmatch('[a-f0-9]{64}',str(d.get('sha256',''))): continue
        if not re.fullmatch('[a-f0-9]{40}',str(d.get('source',''))) or type(d.get('bytes')) is not int or d['bytes']<=0: continue
        builds.append({'version':d['version'],'sha256':d['sha256'],'source':d['source'],'bytes':d['bytes'],
                       'dirty':d.get('dirty'),'signature':text(d.get('signature')),'clean_windows':d.get('windows_clean_install')=='passed',
                       'evidence_url':f'https://github.com/{repo}/blob/main/{p.relative_to(root).as_posix()}'})
    def version_rank(b):
        parts = re.findall(r'\d+',b['version'])
        return tuple(map(int,parts[:3]))+(1 if '-' not in b['version'] else 0,int(parts[3]) if len(parts)>3 else 0)
    builds.sort(key=version_rank,reverse=True)
    version = json.loads(path(root,manifest['version_source']).read_bytes())['version']
    if not VERSION.fullmatch(version): raise ValueError('Invalid source version')
    candidate = next((b for b in builds if b['version']==version and b['dirty'] is False),None)
    published = [r for r in releases if not r.get('draft') and r.get('published_at')]
    published.sort(key=lambda r:r.get('published_at',''),reverse=True)
    release = None
    if published:
        r = published[0]; tag = text(r.get('tag_name'))
        authorized = ('release-approved:'+tag.lower()) in labels(issue_by.get(manifest['approval_issue']))
        release_build = next((b for b in builds if b['version']==tag.removeprefix('v') and b['dirty'] is False),None)
        asset_verified = bool(release_build and any(a.get('state')=='uploaded' and str(a.get('name','')).endswith('.exe') and
                                      a.get('digest')=='sha256:'+release_build['sha256'] for a in r.get('assets',[])))
        release = {'tag':tag,'url':link(r.get('html_url'),repo),'published_at':timestamp(r['published_at']),'authorized':authorized,
                   'asset_matches_manifest':asset_verified,'download_url':link(r.get('html_url'),repo) if authorized and asset_verified else None}
    by_id = {f['id']:f for f in features}
    metrics = {key:metric(by_id[f]['technically_verified' if key=='technical' else 'human_approved'] for f in members) for key,members in manifest['metrics'].items()}
    gates = {}
    for category, rules in manifest['readiness'].items():
        rows = []
        for rule in rules:
            kind = rule['kind']
            value = (candidate is not None) if kind=='candidate' else bool(release and release['authorized'] and release['asset_matches_manifest']) if kind=='release' else (approved(issue_by[rule['issue']]) if rule['issue'] in issue_by else None) if kind=='approval' else evidence(root,rule)
            rows.append({'id':rule['id'],'title':rule['title'],'passed':value,'issue_url':f'https://github.com/{repo}/issues/{rule["issue"]}' if 'issue' in rule else None})
        gates[category] = {'checks':rows,'metric':metric(r['passed'] for r in rows),'go':all(r['passed'] is True for r in rows)}
    recent_prs = sorted(pulls,key=lambda p:p.get('updated_at',''),reverse=True)[:12]
    workflows = {}
    for r in sorted(runs,key=lambda r:(r.get('run_number',0),r.get('run_attempt',0)),reverse=True):
        if r.get('name') not in required+['Compilar candidato beta Windows','Publicar roadmap','Sincronizar roadmap']: continue
        key = (r['name'],r.get('head_branch'))
        if key not in workflows:
            workflows[key] = {'name':r['name'],'branch':text(r.get('head_branch')),'sha':sha(r.get('head_sha')),
                              'status':text(r.get('status')),'conclusion':text(r.get('conclusion')) or None,'url':link(r.get('html_url'),repo),'updated_at':timestamp(r.get('updated_at'))}
    public_artifacts = [{'id':a['id'],'name':text(a.get('name')),'expired':bool(a.get('expired')),'created_at':timestamp(a.get('created_at'))}
                        for a in artifacts if a.get('name')=='color-studio-windows-candidate' and type(a.get('id')) is int]
    build_runs=[r for r in runs if r.get('name')=='Compilar candidato beta Windows']
    build_run=max(build_runs,key=lambda r:(r.get('run_number',0),r.get('run_attempt',0)),default=None)
    installer_build=({'status':text(build_run.get('status')),'conclusion':text(build_run.get('conclusion')) or None,
                      'url':link(build_run.get('html_url'),repo),'sha':sha(build_run.get('head_sha')),
                      'updated_at':timestamp(build_run.get('updated_at'))} if build_run else None)
    human = [{'number':i['number'],'title':text(i.get('title')),'url':link(i.get('html_url'),repo),'updated_at':timestamp(i.get('updated_at'))}
             for i in issue_by.values() if i.get('state')=='open' and 'needs-human' in labels(i)]
    human.sort(key=lambda i:i.get('updated_at') or '',reverse=True)
    operations=[]
    for op in manifest.get('operations',[]):
        issue=issue_by.get(op['issue']);pull=pr_by.get(op['pr'])
        accepted=approved(issue) and bool(pull and pull.get('merged_at') and pull.get('base',{}).get('ref')=='main')
        state='blocked' if blocked(issue) else 'approved' if accepted else 'review' if pull and not pull.get('draft') else 'progress' if pull or 'status:in-progress' in labels(issue) else 'planned'
        operations.append({'id':op['id'],'title':text(op['title']),'status':state,'excluded_from_product_metrics':True,
                           'issue_url':link((issue or {}).get('html_url'),repo),'pr_url':link((pull or {}).get('html_url'),repo)})
    return {'schema_version':1,'product':manifest['product'],'sync':{'status':'complete','observed_at':observed_at,'main_sha':main_sha},
            'source_version':version,'candidate':candidate,'latest_release':release,'versions':builds,'features':features,'metrics':metrics,'readiness':gates,
            'pull_requests':[{'number':p['number'],'title':text(p.get('title')),'state':'merged' if p.get('merged_at') else 'draft' if p.get('draft') else p.get('state'),
                             'url':link(p.get('html_url'),repo),'base':text(p.get('base',{}).get('ref')),'updated_at':timestamp(p.get('updated_at'))} for p in recent_prs],
            'ci':list(workflows.values())[:12],'installer_build':installer_build,'installer_artifacts':public_artifacts,'human_requests':human,'operations':operations,
            'privacy':'Solo metadatos públicos permitidos; no cuerpos, logs, fotos, datos de participantes o rutas locales.'}


def main():
    repo = os.environ.get('GITHUB_REPOSITORY','')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo): raise ValueError('Invalid repository')
    api = GitHub(repo,os.environ.get('GITHUB_TOKEN',''))
    meta = api.get('')
    if meta.get('private') is not False: raise ValueError('Refuse private repository metadata publication')
    api.public = True
    issues, pulls = api.pages('/issues'), api.pages('/pulls')
    runs = api.get('/actions/runs',{'per_page':100})['workflow_runs']
    main_runs = api.get('/actions/runs',{'branch':'main','per_page':100})['workflow_runs']
    candidate_runs = api.get('/actions/workflows/beta-candidate.yml/runs',{'per_page':1})['workflow_runs']
    releases = api.pages('/releases')
    artifacts = api.get('/actions/artifacts',{'per_page':100})['artifacts']
    sha = api.get('/commits/main')['sha']
    if not re.fullmatch('[a-f0-9]{40}',sha): raise ValueError('Invalid main revision')
    result = derive(json.loads((ROOT/'site/data/product-manifest.json').read_bytes()),ROOT,repo,issues,pulls,runs+main_runs+candidate_runs,sha,releases,artifacts,
                    datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'))
    encoded = json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    out = ROOT/'site/data/product.json'
    temp = out.with_suffix('.json.tmp'); temp.write_text(encoded,encoding='utf-8'); temp.replace(out)
    js = 'window.INITIAL_PRODUCT = '+encoded.rstrip().replace('<','\\u003c').replace('>','\\u003e')+';\n'
    out.with_name('product-fallback.js').write_text(js,encoding='utf-8')
    print(json.dumps({'features':len(result['features']),'source_version':result['source_version'],'technical':result['metrics']['technical'],'human':result['metrics']['human']}))


if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,OSError,urllib.error.URLError):
        raise SystemExit('Product sync failed; last complete published state is retained. Inspect API availability/schema privately.')
