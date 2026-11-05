"""Exercise an installed engine over real loopback HTTP using synthetic inputs only.

Standard-library client; runs with the installed isolated Python, not a dev venv.
The CLI is confined to the verified VM kit. API checks do not certify GUI UX.
"""
import argparse
import copy
import hashlib
import http.cookiejar
import io
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


def digest(raw):return hashlib.sha256(raw).hexdigest()


class Client:
    def __init__(self, port):
        if type(port) is not int or not 1 <= port <= 65535:raise ValueError('Invalid loopback port')
        self.base='http://127.0.0.1:'+str(port);self.headers={}
        self.opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def call(self, method, path, body=None, raw=None, content_type=None, expected=200):
        if not path.startswith('/') or path.startswith('//') or '..' in path or '://' in path:raise ValueError('Invalid API path')
        headers=dict(self.headers)
        if body is not None:raw=json.dumps(body).encode();content_type='application/json'
        if content_type:headers['Content-Type']=content_type
        request=urllib.request.Request(self.base+path,data=raw,headers=headers,method=method)
        try:
            with self.opener.open(request,timeout=180) as r:status,payload,response_headers=r.status,r.read(),dict(r.headers)
        except urllib.error.HTTPError as e:status,payload,response_headers=e.code,e.read(),dict(e.headers)
        if status!=expected:raise RuntimeError('Unexpected HTTP status '+str(status)+' for '+method+' '+path.split('/')[1])
        return payload,response_headers

    def json(self,method,path,body=None):return json.loads(self.call(method,path,body)[0])


def upload(client,raw):
    boundary='lfqa'+uuid.uuid4().hex
    payload=('--'+boundary+'\r\nContent-Disposition: form-data; name="file"; filename="synthetic.png"\r\nContent-Type: image/png\r\n\r\n').encode()+raw+('\r\n--'+boundary+'--\r\n').encode()
    result=json.loads(client.call('POST','/api/images',raw=payload,content_type='multipart/form-data; boundary='+boundary)[0])
    uuid.UUID(result['id']);return result


def exercise(client, inputs, output, seed=None, cancellation=True, web_required=True):
    """Real API contract checks; callers provide an owned synthetic output folder."""
    from PIL import Image
    health=client.json('GET','/api/health')
    if web_required:client.call('GET','/')
    token=client.json('GET','/api/session')['csrf']
    client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':token})
    if seed is None:
        source=upload(client,(inputs/'source.png').read_bytes());reference=upload(client,(inputs/'reference.png').read_bytes())
        recipe=client.json('POST','/api/fit',{'source_id':source['id'],'reference_id':reference['id']})['recipe']
        recipe['look'].update(enabled=True,glow=.2,diffusion=.1,fade=.1)
        presets=[client.json('POST','/api/presets',{'name':'Synthetic QA '+str(i),'recipe':recipe})['id'] for i in (1,2)]
        seed={'source':source,'reference':reference,'recipe':recipe,'presets':presets}
    recipe=seed['recipe'];edit={'source_id':seed['source']['id'],'recipe':recipe}
    existing={p['id']:p for p in client.json('GET','/api/presets')}
    assert all(existing[k]['recipe']==recipe for k in seed['presets']),'Preset did not survive'
    for role in ('source','reference'):client.call('GET','/api/images/'+seed[role]['id']+'/preview')
    rendered=[]
    for mode in ('creator','pro','creator'):
        prefs=client.json('GET','/api/preferences');prefs['workspace']=mode
        assert client.json('PUT','/api/preferences',prefs)['workspace']==mode
        rendered.append(client.call('POST','/api/export/png',edit)[0])
    assert rendered[0]==rendered[1]==rendered[2],'Mode changed recipe output'
    preview=client.call('POST','/api/preview',edit)[0]
    assert preview==rendered[0],'Small synthetic preview differs from full export'
    with Image.open(io.BytesIO(rendered[0])) as image:
        assert image.size==(seed['source']['width'],seed['source']['height']) and image.info.get('icc_profile')
    assert client.json('POST','/api/export/json',edit)==recipe
    cube=client.call('POST','/api/export/cube',edit)[0]
    color_only=copy.deepcopy(edit);color_only['recipe']['look']['enabled']=False
    assert cube==client.call('POST','/api/export/cube',color_only)[0],'LUT must exclude optical effects'
    plan=client.json('POST','/api/planner',{'reference_id':seed['reference']['id'],'recipe':recipe})['plan']
    assert plan['human_validated'] is False and plan['original_setup_recovered'] is False
    assert {x['kind'] for rows in plan['sections'].values() for x in rows}=={'observation','estimate','recommendation','source_confirmed'}
    assert all(urllib.parse.urlsplit(s['url']).hostname in ('www.arri.com','theasc.com') for s in plan['sources'])
    plan['diagram']['nodes'][0]['x']=.25
    assert json.loads(json.dumps(plan))['diagram']['nodes'][0]['x']==.25
    assert not re.search(r'(?i)(?<![a-z0-9])[a-z]:[\\/]|github_pat_|gh[pousr]_',json.dumps(plan))
    for name,payload in [('output.png',rendered[0]),('look.cube',cube),('recipe.json',json.dumps(recipe).encode()),('plan.json',json.dumps(plan).encode())]:
        with (output/name).open('xb') as stream:stream.write(payload)
    cancel='NOT_RUN'
    if cancellation:
        # Distinct IDs, under the actual batch/image limits. A completed race is
        # recorded as NOT_EXERCISED rather than called a successful cancellation.
        ids=[upload(client,(inputs/'source.png').read_bytes())['id'] for _ in range(8)]
        job=client.json('POST','/api/jobs',{'source_ids':ids,'recipe':recipe,'format':'png'})
        client.json('POST','/api/jobs/'+job['id']+'/cancel',{})
        for _ in range(600):
            job=client.json('GET','/api/jobs/'+job['id'])
            if job['status'] not in ('queued','running','cancelling'):break
            time.sleep(.05)
        cancel='PASS' if job['status']=='cancelled' else 'NOT_EXERCISED' if job['status']=='completed' else 'FAIL'
        assert cancel!='FAIL','Cancellation failed or timed out'
    return seed,{'version':health['version'],'web_bundle_served':web_required,'creator_pro_export_equal':True,'small_preview_export_equal':True,'presets_preserved':2,'recipe_roundtrip':True,'lut_excludes_optics':True,'planner_uncertainty_sources_and_json':True,'cancellation':cancel,'png_sha256':digest(rendered[0]),'cube_sha256':digest(cube),'scope':'Bundled API exercised; GUI interaction and aesthetic acceptance remain pending'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--seed',type=Path);parser.add_argument('--cancellation',action='store_true');args=parser.parse_args()
    kit=Path(__file__).resolve().parents[1];app=Path('C:/LF-QA/App');data=Path('C:/LF-QA/Data')
    if os.name!='nt' or kit!=Path('C:/LF-QA/Kit') or Path(sys_executable()).parent!=app/'runtime' or os.environ.get('LF_QA_VM_VERIFIED')!='1':raise RuntimeError('Only the verified guest orchestrator may run this CLI')
    for p in (kit,app,data,args.output):
        if p.resolve()!=p.absolute() or not p.absolute().is_relative_to(Path('C:/LF-QA')):raise RuntimeError('Unsafe QA location')
    if not (data/'.synthetic-qa-only').is_file():raise RuntimeError('Unclassified data store')
    args.output.mkdir(exist_ok=False,parents=True)
    env=dict(os.environ,LUMAFORGE_DATA_DIR=str(data));windows=Path(os.environ['SYSTEMROOT']);env['PATH']=os.pathsep.join(map(str,[windows/'System32',windows]))
    stderr=(args.output/'engine.log').open('xb');child=subprocess.Popen([sys_executable(),'-I','-S','-B','-u',str(app/'runtime/app/apps/desktop/engine_entry.py'),'--parent',str(os.getpid())],stdout=subprocess.PIPE,stderr=stderr,env=env,cwd=args.output)
    try:
        ready=queue.Queue();threading.Thread(target=lambda:ready.put(child.stdout.readline(4097)),daemon=True).start()
        metadata=json.loads(ready.get(timeout=45));client=Client(metadata['port'])
        for _ in range(200):
            try:client.json('GET','/api/health');break
            except (OSError,urllib.error.URLError):time.sleep(.05)
        seed=json.loads(args.seed.read_bytes()) if args.seed else None
        seed,result=exercise(client,kit/'inputs',args.output,seed,args.cancellation)
        (args.output/'state.json').write_text(json.dumps(seed,indent=2)+'\n',encoding='utf-8')
        (args.output/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    finally:
        if child.poll() is None:child.terminate();child.wait(timeout=10)
        stderr.close()


def sys_executable():
    import sys
    return sys.executable


if __name__=='__main__':main()
