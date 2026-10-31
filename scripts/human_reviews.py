"""Authenticated, version-bound Issue decisions. No eval, labels as approval or secrets in Pages."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
REPO='jea27/Lut_generator'
REVIEWER={'login':'jea27','id':45896918,'type':'User'}
BOT={'login':'github-actions[bot]','id':41898282,'type':'Bot'}
PREFIX='LUMAFORGE_REVIEW_V1\n```json\n'
RECEIPT='<!-- lumaforge-review-receipt-v1 -->\n```json\n'


def canonical(value): return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(value): return hashlib.sha256(value.encode()).hexdigest()
def identity(user,expected): return all(user.get(k)==v for k,v in expected.items())
def policy(root=ROOT): return json.loads((root/'site/data/product-manifest.json').read_bytes())
def catalog(manifest): return manifest['features']+[manifest['review_demo']]


def git(root,*args):
    return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.DEVNULL)


def context(root,feature,manifest,commit='HEAD'):
    commit=git(root,'rev-parse',commit).decode().strip()
    if not re.fullmatch('[a-f0-9]{40}',commit): raise ValueError('Invalid commit')
    paths=sorted(set(feature.get('review_paths',feature['code_paths'])))
    if not paths: return None
    blobs={}
    for path in paths:
        if not re.fullmatch(r'(?:apps|packages|site|tests_mvp)/[A-Za-z0-9_./-]+',path) or '..' in Path(path).parts:
            raise ValueError('Unsupported review path')
        blobs[path]=git(root,'rev-parse',commit+':'+path).decode().strip()
    version=json.loads(git(root,'show',commit+':'+manifest['version_source']))['version']
    criteria={'id':feature['id'],'acceptance':feature['acceptance'],'checklist':feature['review']['checklist'],
              'version':version,'blobs':blobs}
    return {'commit':commit,'version':version,'revision':digest(canonical(criteria))}


def unpack(body,prefix):
    if isinstance(body,str):body=body.replace('\r\n','\n')
    if not isinstance(body,str) or len(body)>10000 or not body.startswith(prefix) or not body.endswith('\n```'): raise ValueError('Invalid review envelope')
    def pairs(items):
        result={}
        for k,v in items:
            if k in result: raise ValueError('Duplicate JSON key')
            result[k]=v
        return result
    value=json.loads(body[len(prefix):-4],object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))
    if not isinstance(value,dict): raise ValueError('Expected object')
    return value


def decision(comment,issue,feature,manifest,root=ROOT,current=True):
    if not identity(comment.get('user',{}),REVIEWER): raise ValueError('Reviewer not authorized')
    if comment.get('created_at')!=comment.get('updated_at'): raise ValueError('Edited comment; post a new decision')
    if type(comment.get('id')) is not int or comment['id']<=0: raise ValueError('Invalid comment id')
    if comment.get('issue_url')!=f'https://api.github.com/repos/{REPO}/issues/{issue}' or issue!=feature['issue']:
        raise ValueError('Wrong canonical issue')
    d=unpack(comment['body'],PREFIX)
    if set(d)!={'feature','revision','commit','version','decision','checklist','notes'}: raise ValueError('Unexpected review fields')
    if d['feature']!=feature['id'] or d['decision'] not in ('approve','changes'): raise ValueError('Unknown decision/feature')
    if not re.fullmatch('[a-f0-9]{64}',str(d['revision'])) or not re.fullmatch('[a-f0-9]{40}',str(d['commit'])): raise ValueError('Invalid revision')
    if not isinstance(d['notes'],str) or len(d['notes'])>2000 or (d['decision']=='changes' and not d['notes'].strip()): raise ValueError('Changes require observations')
    required=[c['id'] for c in feature['review']['checklist']]
    if not isinstance(d['checklist'],list) or any(not isinstance(x,str) for x in d['checklist']) or len(set(d['checklist']))!=len(d['checklist']): raise ValueError('Invalid checklist')
    if not set(d['checklist'])<=set(required) or (d['decision']=='approve' and set(d['checklist'])!=set(required)):
        raise ValueError('Approval requires every check')
    if current:
        # Read Git objects, never checkout or execute the reviewed commit.
        subprocess.run(['git','merge-base','--is-ancestor',d['commit'],'HEAD'],cwd=root,check=True,capture_output=True)
        original=context(root,feature,manifest,d['commit']);now=context(root,feature,manifest)
        if original is None or now is None: raise ValueError('Capability is not reviewable yet')
        if d['revision']!=original['revision'] or d['revision']!=now['revision'] or d['version']!=original['version']:
            raise ValueError('Review version is stale')
    return d


def receipt(comment,issue,feature,manifest,root=ROOT):
    d=decision(comment,issue,feature,manifest,root)
    return {'schema':1,'feature':d['feature'],'revision':d['revision'],'commit':d['commit'],'version':d['version'],
            'decision':d['decision'],'checklist':d['checklist'],'reviewer':REVIEWER['login'],'reviewer_id':REVIEWER['id'],
            'at':comment['created_at'],'comment_id':comment['id'],'body_sha256':digest(comment['body']),
            'notes_present':bool(d['notes'].strip()),'demo':feature.get('demo',False)}


def projection(comments,issue,feature,manifest,root=ROOT):
    by_id={c['id']:c for c in comments}
    records={}
    for c in comments:
        if not identity(c.get('user',{}),BOT): continue
        try:
            r=unpack(c.get('body'),RECEIPT)
            expected={'schema','feature','revision','commit','version','decision','checklist','reviewer','reviewer_id','at','comment_id','body_sha256','notes_present','demo'}
            if set(r)!=expected or r['schema']!=1 or r['feature']!=feature['id'] or type(r['comment_id']) is not int or r['comment_id']<=0: continue
            if r['reviewer']!='jea27' or r['reviewer_id']!=REVIEWER['id'] or r['decision'] not in ('approve','changes'): continue
            if not re.fullmatch('[a-f0-9]{64}',str(r['revision'])) or not re.fullmatch('[a-f0-9]{64}',str(r['body_sha256'])) or not re.fullmatch('[a-f0-9]{40}',str(r['commit'])): continue
            if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-z]+\.\d+)?',str(r['version'])) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',str(r['at'])): continue
            if not isinstance(r['checklist'],list) or any(not isinstance(x,str) or not re.fullmatch('[a-z][a-z0-9-]{0,40}',x) for x in r['checklist']): continue
            if type(r['notes_present']) is not bool or r['demo'] is not feature.get('demo',False): continue
        except (ValueError,KeyError,TypeError): continue
        source=by_id.get(r['comment_id']);valid=False
        try:
            if source:
                d=decision(source,issue,feature,manifest,root,current=False)
                valid=(digest(source['body'])==r['body_sha256'] and all(d[k]==r[k] for k in ('feature','revision','commit','version','decision','checklist')) and r['at']==source['created_at'])
        except (ValueError,KeyError,TypeError): pass
        records[r['comment_id']]={k:r[k] for k in ('feature','revision','commit','version','decision','checklist','reviewer','at','comment_id','notes_present','demo')}
        records[r['comment_id']]['source_valid']=valid
    history=sorted(records.values(),key=lambda r:r['comment_id'])
    state='pending';latest=history[-1] if history else None
    if latest:
        state='needs_review'
        if latest['source_valid']:
            try:
                decision(by_id[latest['comment_id']],issue,feature,manifest,root)
                state='approved' if latest['decision']=='approve' else 'changes_requested'
            except (ValueError,KeyError,subprocess.CalledProcessError): pass
    for r in history:
        r['url']=f'https://github.com/{REPO}/issues/{issue}#issuecomment-{r["comment_id"]}'
    return {'state':state,'context':context(root,feature,manifest),'history':history,'latest':latest}


def post(api,endpoint,payload=None,method='POST'):
    req=urllib.request.Request(f'https://api.github.com/repos/{REPO}'+endpoint,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'Accept':'application/vnd.github+json','Authorization':'Bearer '+api.token,'Content-Type':'application/json'},method=method)
    with urllib.request.urlopen(req,timeout=25) as response:return json.load(response) if response.status!=204 else None


def process(api,issue,comment_id,manifest,root=ROOT,demo_only=False,expected_body=None):
    comments=api.pages(f'/issues/{issue}/comments')
    source=next(c for c in comments if c['id']==comment_id)
    if expected_body is not None and digest(source['body'])!=expected_body:raise ValueError('Comment changed after event')
    d=unpack(source['body'],PREFIX)
    f=next(f for f in catalog(manifest) if f['id']==d.get('feature') and f['issue']==issue)
    if demo_only and (not f.get('demo') or f['id']!='review-demo' or issue!=manifest['review_demo']['issue']):
        raise ValueError('Dispatch demo cannot approve real product')
    r=receipt(source,issue,f,manifest,root)
    for c in comments:
        if identity(c.get('user',{}),BOT):
            try:
                old=unpack(c.get('body'),RECEIPT)
                if old.get('comment_id')==comment_id and old.get('body_sha256')==r['body_sha256']:return False
            except ValueError:pass
    body=RECEIPT+json.dumps(r,ensure_ascii=False,indent=2)+'\n```'
    post(api,f'/issues/{issue}/comments',{'body':body})
    # Durable notification/queue for the agent, distinct from human approval.
    if r['decision']=='changes':
        post(api,f'/issues/{issue}/labels',{'labels':['agent-action-required']})
    return True


def reconcile_queue(api,issue,manifest,root=ROOT):
    features=[f for f in catalog(manifest) if f['issue']==issue]
    if not features:return
    comments=api.pages(f'/issues/{issue}/comments')
    pending=any(projection(comments,issue,f,manifest,root)['state']=='changes_requested' for f in features)
    current=api.get(f'/issues/{issue}')
    labeled=any(l.get('name')=='agent-action-required' for l in current.get('labels',[]))
    if pending and not labeled:post(api,f'/issues/{issue}/labels',{'labels':['agent-action-required']})
    if not pending and labeled:post(api,f'/issues/{issue}/labels/agent-action-required',method='DELETE')


def main():
    from sync_product import GitHub
    parser=argparse.ArgumentParser();parser.add_argument('--demo-comment',type=int);args=parser.parse_args()
    api=GitHub(REPO,os.environ.get('GITHUB_TOKEN',''));manifest=policy()
    if args.demo_comment:
        # Only owner-dispatched QA and one explicitly synthetic capability.
        if os.environ.get('GITHUB_ACTOR')!='jea27' or os.environ.get('GITHUB_ACTOR_ID')!=str(REVIEWER['id']):raise ValueError('Demo actor not authorized')
        process(api,manifest['review_demo']['issue'],args.demo_comment,manifest,demo_only=True)
        reconcile_queue(api,manifest['review_demo']['issue'],manifest)
        return
    event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_bytes())
    if event.get('repository',{}).get('full_name')!=REPO or event.get('issue',{}).get('pull_request'):return
    if event.get('action') in ('edited','deleted'):
        reconcile_queue(api,event['issue']['number'],manifest)
        return # edited/deleted trigger sync, never grant acceptance
    if not identity(event.get('sender',{}),REVIEWER):return
    if not event.get('comment',{}).get('body','').startswith(PREFIX):return
    try:
        process(api,event['issue']['number'],event['comment']['id'],manifest,expected_body=digest(event['comment']['body']))
        reconcile_queue(api,event['issue']['number'],manifest)
    except (ValueError,KeyError,StopIteration,subprocess.CalledProcessError):
        print('Decision rejected: unauthorized, incomplete, edited or obsolete. No approval recorded.')


if __name__=='__main__':main()
