"""Exercise the packaged sidecar with the licensed local pilot, never user files.

Produces a new private QA directory and a sanitized report; no downloads. This
is engineering evidence on rural photos, not market/portrait/clean-Windows QA.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
import httpx
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def main():
    executable=ROOT/'.lumaforge-local/beta-build/ColorEngine/ColorEngine.exe'
    output=ROOT/'.lumaforge-local'/('beta-qa-'+str(uuid.uuid4()))
    output.mkdir(parents=True)
    env={**os.environ,'LUMAFORGE_DATA_DIR':str(output/'data')}
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'apps/demo').glob('*.jpg')}
    child=subprocess.Popen([str(executable),'--parent',str(os.getpid())],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    try:
        ready=json.loads(child.stdout.readline());base='http://127.0.0.1:'+str(ready['port'])
        with httpx.Client(base_url=base,timeout=180) as client:
            for _ in range(100):
                try:
                    health=client.get('/api/health');health.raise_for_status();break
                except httpx.TransportError:time.sleep(.05)
            csrf=client.get('/api/session').json()['csrf']
            client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':csrf})
            def post(path,**kwargs):
                response=client.post(path,**kwargs);response.raise_for_status();return response
            demo=post('/api/demo/load',json={}).json()
            recipe=post('/api/fit',json={'source_id':demo['source']['id'],'reference_id':demo['reference']['id']}).json()['recipe']
            cube=post('/api/export/cube',json={'source_id':demo['source']['id'],'recipe':recipe})
            (output/'look.cube').write_bytes(cube.content)
            samples=[];ids=[]
            pilot=ROOT/'.research-media/polyhaven-rural'
            for path in sorted(pilot.glob('*.jpg')):
                raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
                uploaded=post('/api/images',files={'file':('pilot.jpg',raw,'image/jpeg')}).json();ids.append(uploaded['id'])
                response=post('/api/export/jpg',json={'source_id':uploaded['id'],'recipe':recipe})
                with Image.open(io.BytesIO(response.content)) as image:
                    assert image.size==(uploaded['width'],uploaded['height']) and image.info.get('icc_profile')
                samples.append({'input_sha256':digest,'dimensions':[uploaded['width'],uploaded['height']],
                                'export_ms':float(response.headers['X-Processing-Ms']),
                                'sampled_process_peak_rss_mb':float(response.headers['X-RSS-Peak-MB']),
                                'original_unchanged':hashlib.sha256(path.read_bytes()).hexdigest()==digest})
            assert samples,'No licensed pilot inputs found'
            record=post('/api/jobs',json={'source_ids':ids[:2],'recipe':recipe,'format':'jpg'}).json()
            for _ in range(600):
                record=client.get('/api/jobs/'+record['id']).json()
                if record['status'] not in ('running','queued','cancelling'):break
                time.sleep(.1)
            assert record['status']=='completed',record
            for item in record['items']:
                response=client.get(f"/api/jobs/{record['id']}/files/{item['index']}");response.raise_for_status()
                assert hashlib.sha256(response.content).hexdigest()==item['sha256']
            assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'apps/demo').glob('*.jpg')}
            report={'version':health.json()['version'],'environment':'Existing Windows developer machine; not clean VM',
                    'scope':'Real licensed rural photographs only; no portrait/skin/market validation',
                    'packaged_runtime':True,'runtime_required_from_user':False,'samples':samples,
                    'batch_status':record['status'],'batch_outputs_verified':len(record['items']),
                    'demo_originals_unchanged':True,'ffmpeg_binary_present':any(executable.parent.rglob('*ffmpeg*.dll')),
                    'cube_sha256':hashlib.sha256(cube.content).hexdigest()}
    finally:
        child.terminate();child.wait(timeout=10)
    # Test abnormal parent death: watchdog must terminate the packaged process.
    parent=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])
    watcher=subprocess.Popen([str(executable),'--parent',str(parent.pid)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    try:
        json.loads(watcher.stdout.readline());parent.terminate();parent.wait(timeout=5)
        watcher.wait(timeout=8);report['parent_death_watchdog']='passed'
    finally:
        if parent.poll() is None:parent.terminate();parent.wait(timeout=5)
        if watcher.poll() is None:watcher.terminate();watcher.wait(timeout=5)
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'private_report':str(output.relative_to(ROOT)/'report.json'),'result':report}))


if __name__=='__main__':main()
