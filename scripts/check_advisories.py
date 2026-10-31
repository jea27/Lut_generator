"""Read-only OSV check of pinned public dependency names/versions; no installs.

Only lockfile package metadata is sent to https://api.osv.dev, never images,
paths, user data or credentials. This is not a redistribution/legal approval.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import tomllib
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
INPUTS=('requirements-mvp.txt','apps/web/package-lock.json','apps/desktop/src-tauri/Cargo.lock')


def packages(root=ROOT):
    values=set()
    for line in (root/INPUTS[0]).read_text().splitlines():
        if not line.strip() or line.startswith('#'):continue
        match=re.fullmatch(r'([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+-]+)',line.strip())
        if not match:raise ValueError('Dependency must be pinned before advisory check')
        values.add(('PyPI',*match.groups()))
    lock=json.loads((root/INPUTS[1]).read_bytes())
    for location,p in lock['packages'].items():
        if not location or p.get('link'):continue
        name=p.get('name') or location.rsplit('node_modules/',1)[-1]
        values.add(('npm',name,p['version']))
    cargo=tomllib.loads((root/INPUTS[2]).read_text())
    for p in cargo['package']:
        if p.get('source','').startswith('registry+'):
            values.add(('crates.io',p['name'],p['version']))
    return [{'package':{'ecosystem':e,'name':n},'version':v} for e,n,v in sorted(values)]


def request_batch(queries):
    request=urllib.request.Request('https://api.osv.dev/v1/querybatch',
        data=json.dumps({'queries':queries}).encode(),method='POST',
        headers={'Content-Type':'application/json','User-Agent':'LumaForge-Dependency-Audit/1'})
    with urllib.request.urlopen(request,timeout=30) as response:return json.load(response)


def check(queries,fetch=request_batch):
    findings=[]
    for offset in range(0,len(queries),200):
        original=queries[offset:offset+200]
        active=[(i,dict(q)) for i,q in enumerate(original)]
        ids=[set() for q in original]
        for _ in range(8):
            response=fetch([q for i,q in active])
            rows=response.get('results')
            if not isinstance(rows,list) or len(rows)!=len(active):raise ValueError('Incomplete OSV response')
            pending=[]
            for (i,q),row in zip(active,rows):
                if not isinstance(row,dict):raise ValueError('Invalid OSV result')
                for vuln in row.get('vulns',[]):
                    identifier=vuln.get('id','')
                    if not re.fullmatch('[A-Za-z0-9_.-]{1,100}',identifier):raise ValueError('Invalid advisory identifier')
                    ids[i].add(identifier)
                if row.get('next_page_token'):pending.append((i,{**q,'page_token':row['next_page_token']}))
            if not pending:break
            active=pending
        else:raise ValueError('OSV pagination limit reached; refuse incomplete audit')
        for q,advisories in zip(original,ids):
            if advisories:findings.append({**q,'advisories':sorted(advisories)})
    return findings


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('report',type=Path)
    args=parser.parse_args();queries=packages();findings=check(queries)
    report={'schema':'lumaforge-dependency-advisories-v1','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'service':'https://api.osv.dev/v1/querybatch','package_versions_queried':len(queries),
            'inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS},
            'findings':findings,'reported_advisories_absent':not findings,'redistribution_approved':False,
            'limits':'Database match only, including build dependencies; no guarantee of absence of vulnerabilities or unknown versions. No binaries, runtime, licenses or clean-Windows test attested.'}
    args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'package_versions_queried':len(queries),'packages_with_advisories':len(findings)}))
    return 2 if findings else 0


if __name__=='__main__':raise SystemExit(main())
