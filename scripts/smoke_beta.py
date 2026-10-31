"""Exercise the packaged sidecar with the licensed local pilot, never user files.

Produces a new private QA directory and a sanitized report; no downloads. This
is engineering evidence on rural photos, not market/portrait/clean-Windows QA.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import queue
import shutil
import sys
import threading
import time
import uuid
import httpx
import psutil
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


def isolated_environment(data_dir):
    """Child-only environment, without modifying the computer or its PATH."""
    keep=('SYSTEMROOT','WINDIR','TEMP','TMP','LOCALAPPDATA','APPDATA','USERPROFILE',
          'COMSPEC','NUMBER_OF_PROCESSORS','PROCESSOR_ARCHITECTURE')
    env={key:value for key,value in os.environ.items() if key.upper() in keep}
    windows=Path(os.environ['SYSTEMROOT'])
    env.update(PATH=os.pathsep.join(map(str,(windows/'System32',windows))),
               PYTHONNOUSERSITE='1',LUMAFORGE_DATA_DIR=str(data_dir))
    return env


def read_ready(child,timeout=45):
    """Do not hang forever when a broken frozen program never prints a port."""
    lines=queue.Queue()
    threading.Thread(target=lambda:lines.put(child.stdout.readline(4097)),daemon=True).start()
    try:line=lines.get(timeout=timeout)
    except queue.Empty:raise RuntimeError('Packaged engine startup timed out') from None
    try:
        ready=json.loads(line)
        if not isinstance(ready,dict) or type(ready.get('port')) is not int or not 1<=ready['port']<=65535:raise ValueError()
    except (ValueError,TypeError):raise RuntimeError('Invalid packaged startup metadata') from None
    return ready


def loaded_modules(child,executable):
    allowed=(executable.parent.resolve(),Path(os.environ['SYSTEMROOT']).resolve())
    unexpected=[];python_bundled=False;count=0
    for mapping in psutil.Process(child.pid).memory_maps():
        path=Path(mapping.path)
        if path.suffix.lower() not in ('.dll','.pyd','.exe'):continue
        count+=1;resolved=path.resolve()
        if not any(resolved.is_relative_to(base) for base in allowed):unexpected.append(path.name)
        if path.name.lower().startswith('python') and path.suffix.lower()=='.dll':
            python_bundled=resolved.is_relative_to(executable.parent.resolve())
    assert python_bundled,'Python DLL was not loaded from the frozen bundle'
    assert not unexpected,{'unexpected_module_names':sorted(set(unexpected))}
    return {'observed_pe_modules':count,'unexpected_module_names':[],
            'python_dll_loaded_from_bundle':True,'scope':'Snapshot after all API operations, not a clean OS certification'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executable',type=Path,default=ROOT/'.lumaforge-local/beta-build/ColorEngine/ColorEngine.exe')
    parser.add_argument('--pilot',type=Path,help='Optional directory of already licensed local JPGs; never downloaded')
    args=parser.parse_args()
    executable=args.executable.resolve(strict=True)
    output=ROOT/'.lumaforge-local'/('beta-qa-'+str(uuid.uuid4()))
    cwd=output/'empty-cwd';cwd.mkdir(parents=True)
    env=isolated_environment(output/'data')
    tools={tool:shutil.which(tool,path=env['PATH']) is not None for tool in ('python','node','cargo','git')}
    assert not any(tools.values()),'Developer tool found in restricted child PATH'
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'apps/demo').glob('*.jpg')}
    stderr=(output/'engine-stderr.log').open('wb')
    child=subprocess.Popen([str(executable),'--parent',str(os.getpid())],stdout=subprocess.PIPE,stderr=stderr,env=env,cwd=cwd)
    try:
        ready=read_ready(child);base='http://127.0.0.1:'+str(ready['port'])
        with httpx.Client(base_url=base,timeout=180,trust_env=False) as client:
            health=None
            for _ in range(100):
                try:
                    health=client.get('/api/health');health.raise_for_status();break
                except httpx.TransportError:time.sleep(.05)
            assert health is not None,'Packaged health endpoint did not start'
            health.raise_for_status()
            assert client.get('/').status_code==200,'Packaged interface is missing'
            assert client.post('/api/demo/load',json={}).status_code==403,'Session guard missing'
            csrf=client.get('/api/session').json()['csrf']
            client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':csrf})
            assert client.get('/api/capabilities').json()['providers'][0]['requires_network'] is False
            def post(path,**kwargs):
                response=client.post(path,**kwargs);response.raise_for_status();return response
            demo=post('/api/demo/load',json={}).json()
            recipe=post('/api/fit',json={'source_id':demo['source']['id'],'reference_id':demo['reference']['id']}).json()['recipe']
            recipe['look']={**recipe['look'],'enabled':True,'glow':.2,'diffusion':.1,'fade':.1}
            exports=[]
            for mode in ('creator','pro','creator'):
                prefs=client.get('/api/preferences').json();prefs['workspace']=mode
                response=client.put('/api/preferences',json=prefs);response.raise_for_status()
                exports.append(post('/api/export/png',json={'source_id':demo['source']['id'],'recipe':recipe}).content)
            assert exports[0]==exports[1]==exports[2],'Modes changed rendered recipe'
            post('/api/presets',json={'name':'QA mode preservation','recipe':recipe})
            assert client.get('/api/presets').json()[0]['recipe']==recipe
            exported_recipe=post('/api/export/json',json={'source_id':demo['source']['id'],'recipe':recipe}).json()
            assert exported_recipe==recipe
            plan=post('/api/planner',json={'reference_id':demo['reference']['id'],'recipe':recipe}).json()['plan']
            assert not plan['human_validated'] and not plan['original_setup_recovered']
            assert plan['recipe']==recipe
            assert {item['kind'] for rows in plan['sections'].values() for item in rows}=={'observation','estimate','recommendation','source_confirmed'}
            for value in (str(ROOT),str(output),demo['reference']['id']):assert value not in json.dumps(plan)
            assert client.post('/api/planner',json={'reference_id':'../private'}).status_code==404
            cube=post('/api/export/cube',json={'source_id':demo['source']['id'],'recipe':recipe})
            (output/'look.cube').write_bytes(cube.content)
            samples=[];ids=[]
            pilot=args.pilot.resolve(strict=True) if args.pilot else ROOT/'apps/demo'
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
            modules=loaded_modules(child,executable)
            report={'version':health.json()['version'],'environment':'Existing Windows developer machine; not clean VM',
                    'scope':'Real licensed rural photographs only; no portrait/skin/market validation',
                    'packaged_runtime':True,'executable_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),
                    'developer_tools_found_in_child_path':tools,'cwd_empty_directory':True,
                    'module_audit':modules,'modes_preserve_export_bytes':True,'plan_privacy_and_claim_types':'passed',
                    'recipe_preset_optics_roundtrip':'passed','session_guard':'passed',
                    'clean_windows_verified':False,'redistribution_approved':False,'samples':samples,
                    'batch_status':record['status'],'batch_outputs_verified':len(record['items']),
                    'demo_originals_unchanged':True,'ffmpeg_binary_present':any(executable.parent.rglob('*ffmpeg*.dll')),
                    'cube_sha256':hashlib.sha256(cube.content).hexdigest()}
    finally:
        if child.poll() is None:child.terminate();child.wait(timeout=10)
        stderr.close()
    # Test abnormal parent death: watchdog must terminate the packaged process.
    parent=subprocess.Popen([sys.executable,'-c','import time;time.sleep(60)'])
    watcher=subprocess.Popen([str(executable),'--parent',str(parent.pid)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,env=env,cwd=cwd)
    try:
        read_ready(watcher);parent.terminate();parent.wait(timeout=5)
        assert watcher.wait(timeout=8)==0,'Watchdog did not exit cleanly'
        report['parent_death_watchdog']='passed'
    finally:
        if parent.poll() is None:parent.terminate();parent.wait(timeout=5)
        if watcher.poll() is None:watcher.terminate();watcher.wait(timeout=5)
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'private_report':str(output.relative_to(ROOT)/'report.json'),'result':report}))


if __name__=='__main__':main()
